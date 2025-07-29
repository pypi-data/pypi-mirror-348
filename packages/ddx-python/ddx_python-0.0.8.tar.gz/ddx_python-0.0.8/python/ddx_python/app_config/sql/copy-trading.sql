CREATE SCHEMA trusted_copy_trading
    /* Key/value store for internal state info like node_id, etc. */
    CREATE TABLE internal_state
    (
        key              VARCHAR PRIMARY KEY,
        value            JSONB NOT NULL
    )
    /* Maintains the sealed enclave state data */
    CREATE TABLE sealed_data
    (
        release_hash     BYTEA     NOT NULL,
        discriminant     SMALLINT  NOT NULL,
        sealed_log       BYTEA     NOT NULL,
        PRIMARY KEY (release_hash, discriminant)
    );
    
    CREATE TABLE release_history
    (
        release_hash            BYTEA        PRIMARY KEY,
        created_at              TIMESTAMPTZ  NOT NULL
    );
    /* Maintains the sealed subaccount auth data */
    CREATE TABLE sealed_subaccount_auth
    (
        leader_address          BYTEA        NOT NULL,
        strategy_name           VARCHAR      NOT NULL,
        sealed_log              BYTEA        NOT NULL,
        release_hash            BYTEA        NOT NULL,
        created_at              TIMESTAMPTZ  NOT NULL,
        PRIMARY KEY (leader_address, strategy_name),
        FOREIGN KEY (release_hash) REFERENCES release_history (release_hash)
            ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED
    );