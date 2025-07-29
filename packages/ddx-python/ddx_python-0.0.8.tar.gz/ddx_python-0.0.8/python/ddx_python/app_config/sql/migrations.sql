/* Distributed state schema

   The app layer business logic guarantees **eventual consistency** of all tables in this schema.
   We do not store operator-specific records such as local timestamps and signature.

   Formatting guidelines: https://www.sqlstyle.guide/

   Note that the refential integrity constraints are deferrable for speedier batch inserts, see: https://emmer.dev/blog/deferrable-constraints-in-postgresql/
*/
CREATE SCHEMA state
    /* Epoch reference table.

       This helper table allows us to partition time series table simply by epoch id
       while supporting date range queries without spanning across partitions.

       Example usage:
       SELECT * FROM fill
         WHERE created_at > '2022-01-01'
         AND epoch_id >= (SELECT epoch_id FROM epoch WHERE start_time > '2022-01-01')`

       This query simply ensure epoch_id is given to the time series table fill to avoid
       scanning unnessary partitions, since the partition key isn't aware of dates.
       It should be simple to apply this pattern to date queries on all time series tables
       at the app layer since they all share the same characteristics.
    */
    CREATE TABLE epoch
    (
        epoch_id   BIGINT PRIMARY KEY,
        start_time TIMESTAMPTZ NOT NULL,
        end_time   TIMESTAMPTZ UNIQUE
    )

    CREATE TABLE schema_updates
    (
        epoch_id   BIGINT PRIMARY KEY,
        version    VARCHAR NOT NULL
    )

    /* Store the current time per the monotonic clock */
    CREATE TABLE time
    (
        is_set      bool PRIMARY KEY DEFAULT TRUE,
        value       BIGINT NOT NULL,
        timestamp   BIGINT NOT NULL,
        CONSTRAINT is_set CHECK (is_set) -- See: https://stackoverflow.com/questions/25307244/how-to-allow-only-one-row-for-a-table
    )

    /* ## CORE TABLES - BEGIN

       These tables store the minimum transactional data that the operator or an auditor client needs to replay the state.

       In addition, the tx_log metadata (epoch_id, tx_ordinal, event_kind) serves as a notification pub/sub
       to inform subscribers (e.g. the frontend) of data updates. However, the tx_log records are effectively
       compressed, meant to be processed by specialized clients to populate the verified store they ultimately query.
       Data-centric clients like the frontend should handle these notifications by looking up records efficiently
       from the user tables, thereby avoid all the overhead that comes with a verified state.
    */

    /* Sequential log of all state transitions. Can be used to replay the state.

       This is originates all time series tables and share their partitioning scheme.
    */
    CREATE TABLE tx_log
    (
        epoch_id        BIGINT CHECK (epoch_id >= 0),
        tx_ordinal      BIGINT CHECK (tx_ordinal >= 0),
        request_index   BIGINT   NOT NULL CHECK (request_index >= 0),
        batch_id        BIGINT   NOT NULL CHECK (batch_id >= 0),
        -- A relative measure of time, starting at zero on genesis and approximating one second.
        time_value      BIGINT   NOT NULL,
        -- The wall clock UNIX timestamp of the sequencer node at the time of incrementing the `time_value`.

        -- We add this metadata because `time_value` intervals are not guaranteed to stay constant especially
        -- during re-elections. Conversely, this second precision timestamp may be interpreted as
        -- a UTC date/time, a reference point for date range queries on time series tables.

        -- The tradeoff is that `time_stamp` could go backwards or gap after re-elections if nodes don't
        -- synchronize their clocks. On the other hand, `time_value` is guaranteed to always increase by one,
        -- approximating one second. Therefore, verified business logic should always use `time_value` as a
        -- measure of relative time. Only use `time_stamp` as a convenience to query by date without expecting
        -- absolute precision.
        time_stamp      BIGINT   NOT NULL,
        state_root_hash BYTEA    NOT NULL,
        event_kind      SMALLINT NOT NULL,
        event           JSONB    NOT NULL,
        PRIMARY KEY (epoch_id, tx_ordinal)
    )
        PARTITION BY RANGE (epoch_id)

    CREATE TABLE tx_log_default PARTITION OF tx_log default

    CREATE INDEX tx_log_request_index ON tx_log (request_index)

    CREATE INDEX tx_log_event_kind ON tx_log (event_kind)

    -- ## CORE TABLES - END

    -- TODO: Split into a seperate schema to allow state-only modes in the future.
    /* ## USER TABLES - BEGIN

       User tables share the folling key characteristics:

       1. Mission critical user interface for the frontend - An exchange is a data-centric
          and reactive application. It accumulate large amounts of data at high speeds. The constant
          orderflow must be processed at high-speed to display the order book in real-time.
          Trade, liquidations, mark price, deposit and withdrawals (all critical financial information)
          must accumulate in a ledger that traders rely on for financial decisions. A highly optimized
          dbms like Postgres is an ideal repository to store and access such transactional data.
          These tables must be highly optimize for the most common data access use cases, any overhead
          has the potential to create visible lag for traders.
       2. Unverified - There ables must be optimized for speed of frequent queries including aggregates
          and paging through trader-centric historical records. In contrast with the operator and auditors,
          the frontend queries on unverified data which simplifies data access dramatically. Using the verified
          data access (building a state tree by appling business logic to the tx_log) would not scale.
       3. Full history - These tables include all trading records, which traders need to make financial
          decisions. The operator, on the other hand, needs only the current state maching so the
          operator does NOT query these tables.
    */

    /* Specifications */
    CREATE TABLE specs
    (
        kind       SMALLINT    NOT NULL,
        name       VARCHAR     NOT NULL,
        expr       VARCHAR     NOT NULL,
        value      JSONB       NOT NULL,
        PRIMARY KEY (kind, name)
    )

    /* Tradable products (listing) */
    CREATE TABLE tradable_products
    (
        symbol     VARCHAR     NOT NULL,
        kind       SMALLINT    NOT NULL,
        name       VARCHAR     NOT NULL,
        params     JSONB               ,
        is_active  BOOLEAN     NOT NULL,
        epoch_id   BIGINT      NOT NULL,
        tx_ordinal BIGINT      NOT NULL,
        created_at TIMESTAMPTZ NOT NULL,
        -- Event though symbol is unique, the primary key must include the partitioning column.
        PRIMARY KEY (epoch_id, tx_ordinal, symbol),
        -- Ensure tx_log integrity.
        FOREIGN KEY (epoch_id, tx_ordinal) REFERENCES tx_log (epoch_id, tx_ordinal)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED
    )
        PARTITION BY RANGE (epoch_id)

    CREATE TABLE tradable_products_default PARTITION OF tradable_products default

    /* Real-time order book data

       For new maker orders posted to the book, store records in this table an `order_intent`.
       However, store taker orders and self-canceling orders in `order_itent` only.
       Store updates resulting from fills in this table only.
       Delete records when `remaining_amount == 0`.
    */
    CREATE TABLE order_book
    (
        order_hash       BYTEA      PRIMARY KEY,
        symbol           VARCHAR    NOT NULL, -- TODO: Consider creating on table per symbol (e.g. order_book_ETHP, order_book_BTCP)
        side             SMALLINT   NOT NULL,
        original_amount  NUMERIC    NOT NULL,
        amount           NUMERIC    NOT NULL,
        price            NUMERIC    NOT NULL,
        trader_address   BYTEA      NOT NULL,
        strategy_id_hash BYTEA      NOT NULL,
        book_ordinal     BIGINT     NOT NULL
        -- TODO 3591: Why do we keep the time value in BookOrder for business logic but not here? Do we not need it or lookup order_intent?
    )

    /* Fields we're querying on to construct the order book */
    CREATE INDEX order_book_symbol ON order_book (symbol)

    CREATE INDEX order_book_side ON order_book (side)

    CREATE INDEX order_book_amount ON order_book (amount)

    CREATE UNIQUE INDEX order_book_symbol_book_ordinal ON order_book (symbol, book_ordinal)

    /* ### TIME SERIES TABLES

       All time series table share these key characteristics:

       1. Include the `epoch_id` and `tx_ordinal` columns to link back to `tx_log`.
       2. Foreign key into `tx_log` with cascading deletes.
       3. Include a `created_at` UTC timestamp column derived from `tx_log.time_stamp` on insert.
       4. Append-only, no updates expected unless it's the admin pruning records.
       5. Foreign key into `epoch` for good measure. This can be dropped since the tx_log FK already ensure epoch_id integrity.

       #### Primary Keys and Ordinals

       We choose the primary key of time series table based on the **natural key** candidates already
       available in the table. The key caveat is that the primary key must always include `epoch_id`
       because of a partitioning key constraint. Therefore, all primaries keys are composite keys:
       `epoch_id` + shortest natural key available.

       In some cases, the natural key would be too large or not sufficient to guarantee uniqueness, we solve
       this by adding an `ordinal` column at the end of our natural key scheme. This ordinal is not
       to be confused with auto-generated surrogate key schemes. It applies only to natural keys
       that begin with `epoch_id` + `tx_ordinal`, meaning it covers a single atomic state transition. It simply
       counts the instances of the natural key in the corresponding `tx_log` record. The tx_log record already
       includes this ordinal in the form of the array or matrix storing our natural key data.
       A tx_log record **never** include unordered lists (or it wouldn't be replayable), so it is always
       possible to compute this ordinal statelessly (proving that this scheme remains a natural key).
       For this reason, we don't need to worry about concurrency or resuming the sequence. We let
       the app layer populate it simply by counting during its insert loop. We do not, nor should we, use
       `nextval` nor any of the Postgres SEQUENCE apparatus designed for surrogate key schemes.
    */

    /* Order intent history */
    CREATE TABLE order_intent
    (
        epoch_id       BIGINT      NOT NULL,
        order_hash     BYTEA       NOT NULL,
        tx_ordinal     BIGINT      NOT NULL,
        symbol         VARCHAR     NOT NULL,
        side           INT         NOT NULL,
        amount         NUMERIC     NOT NULL,
        price          NUMERIC     NOT NULL,
        trader_address BYTEA       NOT NULL,
        strategy_id    VARCHAR     NOT NULL,
        order_type     INT         NOT NULL,
        stop_price     NUMERIC     NOT NULL,
        nonce          BYTEA       NOT NULL,
        modify         BYTEA,
        signature      BYTEA       NOT NULL,
        created_at     TIMESTAMPTZ NOT NULL, -- UTC value derived from `tx_log.time_stamp`
        -- Event though order_hash is unique, the primary key must include the partitioning column.
        PRIMARY KEY (epoch_id, tx_ordinal),
        -- Ensure tx_log integrity.
        FOREIGN KEY (epoch_id, tx_ordinal) REFERENCES tx_log (epoch_id, tx_ordinal)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED
    )
        PARTITION BY RANGE (epoch_id)

    -- Note that a simple UNIQUE constraint on `order_hash` does not work because of declarative partitioning limitations.
    -- psql:/tmp/migrations.sql:449: ERROR:  unique constraint on partitioned table must include all partitioning columns
    -- DETAIL:  UNIQUE constraint on table "order_intent" lacks column "epoch_id" which is part of the partition key.
    CREATE INDEX order_intent_order_hash ON order_intent (order_hash)

    CREATE TABLE order_intent_default PARTITION OF order_intent default

    /* Liquidation history */
    CREATE TABLE liquidation
    (
        epoch_id                       BIGINT      NOT NULL,
        tx_ordinal                     BIGINT      NOT NULL,
        ordinal                        BIGINT      NOT NULL,
        symbol                         VARCHAR     NOT NULL,
        trader                         BYTEA       NOT NULL,
        strategy_id_hash               BYTEA       NOT NULL,
        -- The price reading that triggered the strategy liquidation NULL in the case of funding payment triggered liquidations.
        trigger_price_hash             BYTEA,
        mark_price                     NUMERIC     NOT NULL,
        insurance_fund_capitalization  NUMERIC     NOT NULL,
        created_at                     TIMESTAMPTZ NOT NULL,
        -- Augmenting the txid with strategy and symbol because one tx can have multiple liquidations.
        PRIMARY KEY (epoch_id, tx_ordinal, symbol, trader, strategy_id_hash),
        FOREIGN KEY (epoch_id, tx_ordinal) REFERENCES tx_log (epoch_id, tx_ordinal)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED
    )
        PARTITION BY RANGE (epoch_id)

    CREATE TABLE liquidation_default PARTITION OF liquidation default

    /* ADL (auto-deleveraging) history

       This table reflects specificities of ADLs assossiated with their origin. Since all ADLs originate
       in liquidations, this table links back to the liquidation table in order to include ADL data in
       liquidation reports.
     */
    CREATE TABLE adl
    (
        epoch_id                    BIGINT      NOT NULL,
        tx_ordinal                  BIGINT      NOT NULL,
        -- See note above about the use of ordinal in primary keys
        ordinal                     BIGINT      NOT NULL DEFAULT 0,
        amount                      NUMERIC     NOT NULL,
        realized_pnl                NUMERIC,
        collateral_address          BYTEA       NOT NULL,
        symbol                      VARCHAR     NOT NULL,
        side                        INT         NOT NULL DEFAULT 0,                   
        adl_trader                  BYTEA       NOT NULL,
        adl_strategy_id_hash        BYTEA       NOT NULL,
        liquidated_trader           BYTEA       NOT NULL,
        liquidated_strategy_id_hash BYTEA       NOT NULL,
        created_at                  TIMESTAMPTZ NOT NULL,
        -- Augmenting the txid with ordinal because one tx can have multiple ADLs
        PRIMARY KEY (epoch_id, tx_ordinal, ordinal),
        -- FK to liquidation. We need this to pull fills assossiated with liquidations.
        FOREIGN KEY (epoch_id, tx_ordinal, symbol, liquidated_trader,
                     liquidated_strategy_id_hash) REFERENCES liquidation (epoch_id, tx_ordinal, symbol, trader, strategy_id_hash)
            ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED,
        FOREIGN KEY (epoch_id, tx_ordinal) REFERENCES tx_log (epoch_id, tx_ordinal)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED
    )
        PARTITION BY RANGE (epoch_id)

    CREATE TABLE adl_default PARTITION OF adl default

    /*
    Reflects trade outcomes associated with their origin, including fills, liquidations, and cancellations.
    Grouping these outcomes in a single table allows for efficient querying. Traders can subscribe to a stream
    of trade outcomes and react based on the kind of outcome. This is a common pattern in exchanges,
    see for example: https://binance-docs.github.io/apidocs/spot/en/#trade-streams.

    Reasons codes include:
    - 0 (Trade) - Part or all of the order's quantity has filled.
    - 1 (Liquidation) - The order created for a liquidation has been filled.
    - 2 (Cancelation) - The order has been canceled by the user.

    These are state transitioning outcomes, linking back to the tx_log table.
    */
    CREATE TABLE order_update
    (
        /* The epoch in which the order was placed. */
        epoch_id                    BIGINT      NOT NULL,
        /* The ordinal of the transaction that resulted in the order. */
        tx_ordinal                  BIGINT      NOT NULL,
        /* The ordinal of the order, one order ordinal may have multiple rows in this table. */
        ordinal                     BIGINT      NOT NULL,
        /* The address of the trader who placed the order. */
        maker_order_trader          BYTEA       NOT NULL,
        /* The identifier of the strategy used for the order. */
        maker_order_strategy_id_hash BYTEA      NOT NULL,
        /* A unique identifier for the order. */
        maker_order_hash            BYTEA       NOT NULL,
        /* The amount of the order. */
        amount                      NUMERIC     NOT NULL,
        /* The symbol of the asset involved in the order. */
        symbol                      VARCHAR     NOT NULL,
        /* The price of the order. */
        price                       NUMERIC,
        /* The fee in USDC paid by the maker. */
        maker_fee_usdc              NUMERIC,
        /* The fee in DDX paid by the maker. */
        maker_fee_ddx               NUMERIC,
        /* The realized profit or loss for the maker in USDC. */
        maker_realized_pnl          NUMERIC,
        /* The reason for the order's outcome. */
        reason                      SMALLINT    NOT NULL,

        /* The address of the trader who took the order. */
        taker_order_trader          BYTEA,
        /* The identifier of the strategy used by the taker. */
        taker_order_strategy_id_hash BYTEA,
        /* A unique identifier for the taker's order. */
        taker_order_hash            BYTEA,
        /* The fee in USDC paid by the taker. */
        taker_fee_usdc              NUMERIC,
        /* The fee in DDX paid by the taker. */
        taker_fee_ddx               NUMERIC,
        /* The realized profit or loss for the taker. */
        taker_realized_pnl          NUMERIC,

        /* The address of the trader who was liquidated. */
        liquidated_trader           BYTEA,
        /* The identifier of the strategy of the liquidated trader. */
        liquidated_strategy_id_hash BYTEA,
        /* The timestamp when the order was created. */
        created_at                  TIMESTAMPTZ NOT NULL,

        /* Primary key includes maker_ordinal because one transaction can have multiple order_updates. */
        PRIMARY KEY (epoch_id, tx_ordinal, ordinal),

        /* Foreign keys reference the tx_log table. */
        FOREIGN KEY (epoch_id, tx_ordinal) REFERENCES tx_log (epoch_id, tx_ordinal)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED
    )
        PARTITION BY RANGE (epoch_id)

    CREATE INDEX order_update_symbol ON order_update (symbol)

    CREATE INDEX order_update_reason ON order_update (reason)

    CREATE INDEX order_update_maker_order_hash ON order_update (maker_order_hash)

    CREATE INDEX order_update_taker_order_hash ON order_update (taker_order_hash)

    CREATE TABLE order_update_default PARTITION OF order_update default

    /*
    Reflects intent rejections, situations in which intents fail expectedly somewhere during execution, and the information needs to be relayed back to the trader. Such intents have passed sequencing and validation but failed during execution because relevant state changes happened to occur between sequencing and execution.

    These include (with `rejection_type`):
    1. Order rejections (0): when orders are partially or completely canceled during execution without being added to the order book. For example, an order may be self-canceled if it fails the solvency guards.
    2. Withdraw rejections (1): for collateral currency or DDX, when withdrawals fail during execution, e.g. insufficient balance.
    3. Cancel rejections (2): when cancel or modify requests fail during execution due to a nonexistent order.
    4. Profile update rejections (3): when profile updates fail during execution due to a nonexistent trader.
    
    Each of these rejection types has a set of possible reasons for the rejection.
    1. Order rejection reasons:
        - 0 (SelfMatch) - Part or all of the order was self-canceled because the same maker owns the best match.
        - 1 (SolvencyGuard) - Part or all of the order was self-canceled for failing the solvency guards.
        - 2 (MaxTakerPriceDeviation) - Part or all of the order was self-canceled because the marker order's price deviated too much from the mark price.
        - 3 (MarketOrderNotFullyFilled) - All of the order was self-canceled for not being able to fully fill the market order.
        - 4 (InvalidStrategy) - All of the order was self-canceled because the strategy is invalid/nonexistent.
        - 5 (PostOnlyViolation) - All of the order was self-canceled because it would have matched immediately.
    2. Withdraw rejection reasons:
        - 0 (InvalidStrategy) - The collateral withdrawal failed because the strategy is invalid/nonexistent.
        - 1 (InvalidTrader) - The DDX withdrawal failed because the trader is invalid/nonexistent.
        - 2 (InvalidInsuranceFundContribution) - The insurance fund withdrawal failed because the insurance fund contribution is invalid/nonexistent.
        - 3 (MaxWithdrawalAmount) - The collateral withdrawal failed because the amount exceeds the maximum withdrawal amount. This only applies to withdrawals of collateral currencies.
        - 4 (InsufficientDDXBalance) - The DDX withdrawal failed because the trader has insufficient DDX balance. This only applies to DDX withdrawals.
        - 5 (InsufficientInsuranceFundContribution) - The insurance fund withdrawal failed because the withdrawal amount exceeds the contribution amount.
        - 6 (InsufficientRemainingInsuranceFund) - The insurance fund withdrawal failed because the remaining insurance fund after the withdrawal would be dangerously low.
    3. Cancel rejection reasons:
        - 0 (InvalidOrder) - The cancel/modify request failed because the order does not exist.
    4. Profile update rejection reasons:
        - 0 (InvalidTrader) - The profile update failed because the trader does not exist.

    Unlike with order_update, records in this table are not state transitions, so they cannot link back to the tx_log table.
    Instead, they link back to a request. Rejected orders are not state transitions because the cancelation is done atomically
    during execution, requiring no state change. For this reason, this table cannot be populated by loading the tx_log as it
    augments the state data.
    */
    CREATE TABLE intent_rejection
    (
        -- Common fields
        /* The epoch in which the order was placed. */
        epoch_id                    BIGINT      NOT NULL,
        order_match_tx_ordinal      BIGINT,     -- Can be null, only filled with tx_ordinal from order_update when partial order rejection from a set of trade outcomes
        /* The index of the request that resulted in the order. */
        request_index               BIGINT      NOT NULL,
        /* The rejection type. */
        rejection_type              SMALLINT    NOT NULL,
        /* The reason for the order's rejection, with meaning specific to the rejection type */
        reason                      SMALLINT    NOT NULL,
        /* The address of the trader. */
        trader_address              BYTEA       NOT NULL,
        /* The timestamp when the order was created. */
        created_at                  TIMESTAMPTZ NOT NULL,

        -- Rejection-specific fields
        /* A unique identifier for an order. Note that fully rejected orders do not have a record in order_intent. */
        order_hash                  BYTEA,
        /* The identifier of the strategy. */
        strategy_id_hash            BYTEA,
        /* The amount of the order that was canceled. */
        amount                      NUMERIC,
        /* The product symbol of the asset involved. */
        symbol                      VARCHAR,
        /* Currency (of a withdrawal). */
        currency                    VARCHAR,
        /* Insurance fund (withdrawal). */
        insurance_fund              BOOLEAN,

        /* Primary key must include the partitioning column, even though request_index is unique. */
        PRIMARY KEY (epoch_id, request_index)
    )
        PARTITION BY RANGE (epoch_id)

    CREATE TABLE intent_rejection_default PARTITION OF intent_rejection default

    /* Recent mark prices */
    CREATE TABLE mark_price
    (
        epoch_id      BIGINT      NOT NULL,
        request_index BIGINT      NOT NULL,
        symbol        VARCHAR     NOT NULL,
        price         NUMERIC     NOT NULL,
        funding_rate  NUMERIC,
        created_at    TIMESTAMPTZ NOT NULL,
        PRIMARY KEY (epoch_id, request_index, symbol)
    )
        PARTITION BY RANGE (epoch_id)

    CREATE INDEX mark_price_symbol ON mark_price (symbol)

    CREATE TABLE mark_price_default PARTITION OF mark_price default

    /* Price checkpoint history */
    CREATE TABLE price
    (
        epoch_id         BIGINT      NOT NULL,
        tx_ordinal       BIGINT      NOT NULL,
        symbol           VARCHAR     NOT NULL,
        index_price_hash BYTEA       NOT NULL,
        index_price      NUMERIC     NOT NULL,
        time             BIGINT      NOT NULL,
        mark_price_kind  SMALLINT    NOT NULL,
        ema              NUMERIC,
        accum            NUMERIC,
        count            BIGINT,
        metadata         JSONB       NOT NULL,
        price_ordinal    BIGINT      NOT NULL, -- TODO: can this be UNIQUE but not part of partition id?
        created_at       TIMESTAMPTZ NOT NULL,
        CONSTRAINT mark_price_metadata CHECK (
            (ema IS NOT NULL AND accum IS NULL AND count IS NULL) OR
            (ema IS NULL AND accum IS NOT NULL AND count IS NOT NULL)
        ),
        PRIMARY KEY (epoch_id, tx_ordinal, symbol),
        FOREIGN KEY (epoch_id, tx_ordinal) REFERENCES tx_log (epoch_id, tx_ordinal)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED
    )
        PARTITION BY RANGE (epoch_id)

    CREATE INDEX price_index_price_hash ON price (index_price_hash)

    CREATE TABLE price_default PARTITION OF price default

   /* The insurance fund */
    CREATE TABLE insurance_fund
    (
        epoch_id                BIGINT       NOT NULL,
        tx_ordinal              BIGINT       NOT NULL,
        /* Sequential position of the update in a Tx, insurance fund settlements may occur at the trade outcome level or liquidation sale level. */
        ordinal                 BIGINT       NOT NULL,
        symbol                  VARCHAR      NOT NULL,
        total_capitalization    NUMERIC,
        kind                    SMALLINT     NOT NULL, -- Fill = 0, Liquidation = 1, Deposit = 2, Withdraw = 3, see ops.rs
        created_at              TIMESTAMPTZ  NOT NULL,

        PRIMARY KEY (epoch_id, tx_ordinal, ordinal),
        FOREIGN KEY (epoch_id, tx_ordinal) REFERENCES tx_log (epoch_id, tx_ordinal)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED
    )
        PARTITION BY RANGE (epoch_id)

    CREATE TABLE insurance_fund_default PARTITION OF insurance_fund default

   /* Store DDX fee pool leaf values in an append-only fashion. */
    CREATE TABLE ddx_fee_pool
    (
        epoch_id                BIGINT       NOT NULL,
        tx_ordinal              BIGINT       NOT NULL,
        /* Sequential position of the update in a Tx, fee settlements occur at the trade outcome level. */
        ordinal                 BIGINT       NOT NULL,
        total_capitalization    NUMERIC,
        created_at              TIMESTAMPTZ  NOT NULL,

        PRIMARY KEY (epoch_id, tx_ordinal, ordinal),
        FOREIGN KEY (epoch_id, tx_ordinal) REFERENCES tx_log (epoch_id, tx_ordinal)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED
    )
        PARTITION BY RANGE (epoch_id)

    CREATE TABLE ddx_fee_pool_default PARTITION OF ddx_fee_pool default

    /* Strategy collateral transaction history */
    CREATE TABLE strategy_update
    (
        epoch_id             BIGINT      NOT NULL,
        tx_ordinal           BIGINT      NOT NULL,
        ordinal              BIGINT      NOT NULL,
        trader               BYTEA       NOT NULL,
        strategy_id_hash     BYTEA       NOT NULL,
        collateral_address   BYTEA       NOT NULL,
        amount               NUMERIC     NOT NULL,
        new_avail_collateral NUMERIC,
        new_locked_collateral NUMERIC,
        kind                 SMALLINT    NOT NULL, -- 0-Deposit, 1-Withdraw, 2-WithdrawIntent, 3-FundingPayment, 4-RealizedPnl
        -- Applies to events originated on-chain (like `ClaimDDXWithdrawal`).
        block_number         BIGINT,
        tx_hash              BYTEA,
        -- Realized PNL details
        pnl_realizations     JSONB, -- Filled on kind RealizedPnl, e.g. { "ETHP": {"new_avg_entry_price": "2676.114396", "realizedPnl": "5" }}
        -- Mapping for funding payments like `Map<Symbol, (Rate, Payment)>`
        -- Example usage: `SELECT funding_payments->'symbol', funding_payments->'rate' FROM strategy_update GROUP BY strategy_update->'symbol';`
        funding_payments     JSONB,
        -- UTC value derived from `tx_log.time_stamp`
        created_at           TIMESTAMPTZ NOT NULL,
        PRIMARY KEY (epoch_id, tx_ordinal, ordinal),
        FOREIGN KEY (epoch_id, tx_ordinal) REFERENCES tx_log (epoch_id, tx_ordinal)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED
    )
        PARTITION BY RANGE (epoch_id)

    CREATE INDEX strategy_update_trader ON strategy_update (trader)

    CREATE TABLE strategy_update_default PARTITION OF strategy_update default

    /* Trader transaction history */
    CREATE TABLE trader_update
    (
        epoch_id                BIGINT      NOT NULL,
        tx_ordinal              BIGINT      NOT NULL,
        ordinal                 BIGINT      NOT NULL DEFAULT 0,
        trader                  BYTEA       NOT NULL,
        kind                    SMALLINT    NOT NULL, -- 0-DepositDDX, 1-WithdrawDDX, 2-WithdrawDDXIntent, 3-TradeMiningReward, 4-ProfileUpdate, 5-FeeDistribution
        -- This contains the available balance for withdrawals, available balance for deposits, and NULL when not applicable.
        new_avail_ddx_balance   NUMERIC,
        -- This contains the locked balance for withdrawals, available balance for deposits, and NULL when not applicable.
        new_locked_ddx_balance  NUMERIC,
        amount                  NUMERIC,
        -- Applies to profile updates only, NULL when not applicable.
        pay_fees_in_ddx         BOOLEAN,
        -- Applies to events originated on-chain (like `ClaimWithdrawal`).
        block_number            BIGINT,
        tx_hash                 BYTEA,
        created_at              TIMESTAMPTZ NOT NULL,
        -- Assuming only one trader update per transaction, this pk will need to be augmented if we support batching.
        PRIMARY KEY (epoch_id, tx_ordinal, ordinal),
        FOREIGN KEY (epoch_id, tx_ordinal) REFERENCES tx_log (epoch_id, tx_ordinal)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED
    )
        PARTITION BY RANGE (epoch_id)

    CREATE INDEX trader_update_trader ON trader_update (trader)

    CREATE TABLE trader_update_default PARTITION OF trader_update default

    -- ## END TIME SERIES TABLES

    /* Currently active traders including their ddx balance */
    CREATE TABLE trader
    (
        trader          BYTEA   NOT NULL,
        avail_ddx       NUMERIC NOT NULL DEFAULT 0,
        locked_ddx      NUMERIC NOT NULL DEFAULT 0, /* Some ddx may be frozen pending withdraw */
        pay_fees_in_ddx BOOLEAN NOT NULL DEFAULT false,
        PRIMARY KEY (trader)
    )

    /* Currently active strategies including their collateral balance */
    CREATE TABLE strategy -- TODO 2435: Make a decision on handling empty strategies
    (
        trader            BYTEA   NOT NULL,
        strategy_id_hash  BYTEA   NOT NULL,
        strategy_id       VARCHAR NOT NULL,
        max_leverage      INT     NOT NULL DEFAULT 0,
        avail_usdc        NUMERIC NOT NULL DEFAULT 0,
        locked_usdc       NUMERIC NOT NULL DEFAULT 0, -- Some collateral may be frozen pending withdraw
        frozen            BOOLEAN NOT NULL DEFAULT false, -- The entire strategy may be frozen pending tokenization
        PRIMARY KEY (trader, strategy_id_hash),
        -- Ensure traders cannot leave their strategies orphaned.
        FOREIGN KEY (trader) REFERENCES trader (trader)
    )

    CREATE INDEX strategy_strategy_id ON strategy (strategy_id)

    /* Currently active positions */
    CREATE TABLE position
    (
        trader                 BYTEA   NOT NULL,
        symbol                 VARCHAR NOT NULL,
        strategy_id_hash       BYTEA   NOT NULL,
        side                   INT     NOT NULL DEFAULT 0,
        balance                NUMERIC NOT NULL DEFAULT 0,
        avg_entry_price        NUMERIC NOT NULL DEFAULT 0,
        last_modified_in_epoch INT, -- Epoch id where the position balance was last transitioned
        PRIMARY KEY (trader, strategy_id_hash, symbol)
    );
    -- ## USER TABLES - END

-- The frontend readonly role has all privileges for this schema, including write.
CREATE SCHEMA users
    /* Maintains the blockpass kyc enrollment status of each trader address */
    CREATE TABLE enrollment
    (
        trader                  BYTEA        NOT NULL,
        record_id               VARCHAR      NOT NULL,
        status                  SMALLINT     NOT NULL, -- EnrollmentStatus enum
        created_at              TIMESTAMPTZ  NOT NULL, -- This is the timestamp at which we received the user.readyToReview webhook event (the first event that contains a crypto address) for the given trader
        last_update_date        TIMESTAMPTZ  NOT NULL, -- Catch all date column, allows us to track dates for other user status events such as rejected, blocked, deleted, etc.
        approved_date           TIMESTAMPTZ,
        PRIMARY KEY (trader)
    );

CREATE SCHEMA verified_state
    /* The abi encoded leaf bytes by hash */
    CREATE UNLOGGED TABLE items
    (
        leaf_hash     BYTEA PRIMARY KEY, -- We can hash these bytes directly to verify each hash: leaf_hash=Keccak256(leaf)
        abi_schema    JSONB NOT NULL,
        leaf          BYTEA NOT NULL
    )

    /* VERSIONED verified state (SMT) values

        This is a textbook versioning scheme where leaf_key is versioned by epoch_id.
        From optimal performance, we use a append-only scheme, delete leaf versions by inserting null.

        This pseudo-query collects all leaf hashes for a given epoch:
        SELECT * FROM (SELECT max(leaf_key), leaf_hash FROM t WHERE epoch_id<=$1 GROUP BY epoch_id) WHERE value IS NOT null

        The referential integrity rule aids with maintenance. Since there is no reason for an
        orphan items row to exist, we may simply delete from versions where epoch_id <= N cascading to items.

        No partitioning needed assuming maintenance pruning of old epochs instead.
     */
    CREATE UNLOGGED TABLE versions
    (
        leaf_key       BYTEA  NOT NULL,
        epoch_id       BIGINT NOT NULL,
        leaf_hash      BYTEA,
        PRIMARY KEY (leaf_key, epoch_id),
        FOREIGN KEY (leaf_hash) REFERENCES items (leaf_hash)
            ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED
    );


/* Create and select new partition

    The processor calls the stored procedure on epoch transition based on the configured
    partition size.

    For example, let `PARTITION_SIZE` be 10: `if epoch_id % 10 == 0 { tx.execute('create_partitions', &[epoch_id, 10]) }`.

    The epoch transition db helper in `ops.rs` gives the parameters.
*/
CREATE FUNCTION create_partitions(new_epoch_id int, partition_size int) -- TODO: Partioning is not currently applied WE USE THE DEFAULT PARTITIONS ONLY. The apps state manager must call this fn after N epochs
    RETURNS void
    LANGUAGE plpgsql
AS
$$
DECLARE
    partitioned_table  varchar;
    lower_bound        varchar;
    upper_bound        varchar;
    new_table          varchar;
    sql                varchar;
BEGIN
    -- Naming convention for new partitions:
    --     [table name]_[from epoch]_[to epoch exclusive]
    -- Example:
    --     fill_0000000001_to_000000005 // fill partition for epochs 1 to 4 (not including 5)
    --     fill_0000000005_to_000000009 // fill partition for epochs 5 to 8 (not including 9)
    -- Padding is added for legibility and sorting in the sql console
    lower_bound := TO_CHAR(new_epoch_id, 'fm0000000000');
    upper_bound := TO_CHAR(new_epoch_id + partition_size, 'fm0000000000');
    -- Generate new partitions for tables that are partitioned and have an epoch_id column.
    -- Partitioned tables are initialized with a 'default' partition in this script; the first
    -- dynamic partition creation takes place at the first epoch transition.
    FOR partitioned_table IN SELECT DISTINCT B.relname FROM pg_inherits A
                JOIN pg_class B ON A.inhparent = B.oid
                JOIN information_schema.columns C ON C.table_name = B.relname
                WHERE C.column_name = 'epoch_id' and B.relkind = 'p'
    LOOP
       new_table := FORMAT('%s_%s_to_%s', partitioned_table, lower_bound, upper_bound);
       -- Only create a new partition if it does not exist.
       IF NOT EXISTS(SELECT 1
                  FROM information_schema.tables
                  WHERE table_name = new_table
        ) then
           sql := FORMAT('create table %s PARTITION OF %s for values from (%s) to (%s)',
                         new_table, partitioned_table, lower_bound, upper_bound);
           RAISE NOTICE '%', sql;
           EXECUTE SQL;
           -- TODO: Archive and/or optimize the previous partion (fill-factor, vacuum, etc.)
        END IF;
   END LOOP;
END;
$$;

/* Create a pub/sub style data feed from the tx log

   This is used by tightly coupled external components like the frontend.
*/
CREATE OR REPLACE FUNCTION notify_tx()
    RETURNS trigger AS
$$
BEGIN
    PERFORM
        pg_notify('execution_update', json_build_object('type', 'Tx',
                                                'epoch_id', CAST(NEW.epoch_id AS text),
                                                'tx_ordinal', CAST(NEW.tx_ordinal AS text),
                                                'request_index', CAST(NEW.request_index AS text),
                                                'event_kind', CAST(NEW.event_kind AS text))::text);
    RETURN NULL;
END;
$$
    LANGUAGE plpgsql VOLATILE
                     COST 100;

CREATE TRIGGER notify_tx
    AFTER INSERT OR
        UPDATE
    ON state.tx_log
    FOR EACH ROW
EXECUTE PROCEDURE notify_tx();


CREATE OR REPLACE FUNCTION notify_notx()
    RETURNS trigger AS
$$
BEGIN
    -- Provisioning for future non-state transitioning event kinds triggering this procedure.
    IF TG_TABLE_NAME = 'intent_rejection' OR TG_TABLE_NAME = 'intent_rejection_default' THEN
        PERFORM pg_notify('execution_update', json_build_object('type', 'NoTx',
                                                      'epoch_id', CAST(NEW.epoch_id AS text),
                                                      'request_index', CAST(NEW.request_index AS text),
                                                      'event_kind', 'IntentRejection')::text);
    ELSIF TG_TABLE_NAME = 'mark_price' OR TG_TABLE_NAME = 'mark_price_default' THEN
        PERFORM pg_notify('execution_update', json_build_object('type', 'NoTx',
                                                      'epoch_id', CAST(NEW.epoch_id AS text),
                                                      'request_index', CAST(NEW.request_index AS text),
                                                      'event_kind', 'MarkPrice')::text);
    ELSE
        RAISE EXCEPTION 'Unexpected table: %', TG_TABLE_NAME;
    END IF;
    RETURN NULL;
END;
$$
    LANGUAGE plpgsql VOLATILE
                     COST 100;

CREATE TRIGGER notify_intent_rejection
    AFTER INSERT OR
        UPDATE
    ON state.intent_rejection
    FOR EACH ROW
EXECUTE PROCEDURE notify_notx();

CREATE TRIGGER notify_mark_price
    AFTER INSERT OR
        UPDATE
    ON state.mark_price
    FOR EACH ROW
EXECUTE PROCEDURE notify_notx();

/* Operator schema

   Data pertaining to a given operator goes in here. This may include things like transaction signatures.
*/
CREATE SCHEMA operator

    /* Key/value store for internal state info like node_id, latest checkpoint, etc. */
    CREATE TABLE internal_state
    (
        key              VARCHAR PRIMARY KEY,
        value            JSONB NOT NULL
    )

    /* Raft config entries */
    CREATE TABLE raft
    (
        key              VARCHAR PRIMARY KEY,
        entry_index      BIGINT NOT NULL, -- Normal entries are stored in request.queue. We only keep the latest value of each entry to get the current config.
        -- Leader info --
        term             BIGINT NOT NULL,
        node_id          BIGINT NOT NULL,
        -- Entry payload variant for key --
        payload          JSONB
    )

    CREATE TABLE sealed_data
    (
        release_hash     BYTEA    NOT NULL,
        discriminant     SMALLINT NOT NULL,
        sealed_log       BYTEA    NOT NULL,
        PRIMARY KEY (release_hash, discriminant)
    );

CREATE SCHEMA request
    /* Log of all inputs (aka requests) processed by the system

        Making unlogged because request log entries always get replicated to the majority of the Raft prior to their
        deletion from the append entry log, so they are recoverable in the case of a crash.

        This table should be pruned over time.
    */
    CREATE
        UNLOGGED TABLE queue
    (
        request_index      BIGINT PRIMARY KEY,
        topic              SMALLINT NOT NULL,
        data               JSONB    NOT NULL,
        signature          BYTEA    NOT NULL,
        /* Columns below apply to requests sequenced by Raft (all but genesis) */
        entry_index        BIGINT,
        term               BIGINT,
        node_id            BIGINT,
        cluster_epoch      BIGINT NOT NULL DEFAULT 0,
        created_at         TIMESTAMPTZ NOT NULL DEFAULT NOW()
    )

    CREATE INDEX request_queue_cluster_epoch ON request.queue (cluster_epoch);
