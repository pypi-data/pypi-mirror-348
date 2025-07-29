CREATE SCHEMA trusted_kyc
/* Key/value store for internal state info like node_id, latest checkpoint, etc. */
    CREATE TABLE internal_state
    (
        key              VARCHAR PRIMARY KEY,
        value            JSONB NOT NULL
    )
    
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

    /* Maintains the trusted kyc status of each trader address */
    CREATE TABLE sealed_kyc
    (
        trader                  BYTEA        PRIMARY KEY,
        sealed_log              BYTEA        NOT NULL,
        release_hash            BYTEA        NOT NULL,
        created_at              TIMESTAMPTZ  NOT NULL, -- This is the timestamp at which kyc service received the initial KYC request for the given trader
        FOREIGN KEY (release_hash) REFERENCES release_history (release_hash)
            ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED
    );

    CREATE INDEX idx_sealed_kyc_created_at ON sealed_kyc(created_at);

    /* Clean up sealed_kyc table based on timestamp from old to new */
    CREATE OR REPLACE FUNCTION cleanup_expired_sealed_kyc(valid_period INTERVAL DEFAULT '1 year')
        RETURNS void AS
    $$
    BEGIN
        DELETE FROM sealed_kyc
        WHERE created_at < NOW() - valid_period;
    END;
    $$ LANGUAGE plpgsql VOLATILE;

    /* Cleanup sealed_kyc from outdated release hashes*/
    CREATE OR REPLACE FUNCTION cleanup_outdated_sealed_kyc(num_releases_to_keep INTEGER DEFAULT 1)
        RETURNS void AS $$
    DECLARE
        cutoff_hash BYTEA;
    BEGIN
        -- Get the cutoff release hash
        SELECT hash INTO cutoff_hash
        FROM (
            SELECT release_hash, 
                ROW_NUMBER() OVER (ORDER BY created_at DESC) as rn
            FROM release_history
        ) subquery
        WHERE rn = num_releases_to_keep;

        -- Delete entries from sealed_kyc that are associated with older release hashes
        DELETE FROM sealed_kyc
        WHERE release_hash NOT IN (
            SELECT release_hash
            FROM release_history
            WHERE created_at >= (SELECT created_at FROM release_history WHERE hash = cutoff_hash)
        );

        -- Optionally, delete old entries from release_hash table
        -- DELETE FROM release_hash
        -- WHERE created_at < (SELECT created_at FROM release_history WHERE release_hash = cutoff_hash);

        RAISE NOTICE 'Cleanup completed. Kept % most recent releases.', num_releases_to_keep;
    END;
    $$ LANGUAGE plpgsql VOLATILE;