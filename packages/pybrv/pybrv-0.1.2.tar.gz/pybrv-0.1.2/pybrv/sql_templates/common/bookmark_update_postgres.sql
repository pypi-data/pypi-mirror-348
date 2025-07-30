WITH source AS (
    SELECT 
        <UNIQUE_RULE_IDENTIFIER> AS UNIQUE_RULE_IDENTIFIER,
        '<BOOKMARK_START_DATE>'::DATE AS min_bookmark,
        '<BOOKMARK_END_DATE>'::DATE AS max_bookmark
)
UPDATE com_data_validator.pybrv_meta.pybrv_metadata AS target
SET
    BOOKMARK_START_DATE = source.min_bookmark,
    BOOKMARK_END_DATE = source.max_bookmark,
    LAST_MODIFIED_TS = CURRENT_TIMESTAMP AT TIME ZONE 'UTC'
FROM source
WHERE target.UNIQUE_RULE_IDENTIFIER = source.UNIQUE_RULE_IDENTIFIER;


INSERT INTO com_data_validator.pybrv_meta.pybrv_metadata (
    UNIQUE_RULE_IDENTIFIER,
    BOOKMARK_START_DATE,
    BOOKMARK_END_DATE,
    LAST_MODIFIED_TS
)
SELECT 
    UNIQUE_RULE_IDENTIFIER,
    min_bookmark,
    max_bookmark,
    CURRENT_TIMESTAMP AT TIME ZONE 'UTC'
FROM source
WHERE NOT EXISTS (
    SELECT 1 FROM com_data_validator.pybrv_meta.pybrv_METADATA 
    WHERE com_data_validator.pybrv_meta.pybrv_METADATA.UNIQUE_RULE_IDENTIFIER = source.UNIQUE_RULE_IDENTIFIER
);
