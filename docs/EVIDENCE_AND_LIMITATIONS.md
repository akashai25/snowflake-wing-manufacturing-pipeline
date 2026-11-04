# Wing Pipeline — Technical Notes

This project uses synthetic manufacturing-style CSV data to practice Python and Snowflake ingestion, data checks, and incremental processing.

## What was tested

- In a separate Snowflake test database, I uploaded the included sample CSV to an internal stage, validated the load with `COPY INTO ... VALIDATION_MODE = RETURN_ERRORS`, and loaded 100 records into `RAW_WING`.
- The sample contains 97 distinct `PLAN_ID` values and three additional rows with repeated IDs. There are no missing torque values. `PASS`, `FAIL`, and `REWORK` are accepted QC statuses; one record contains an unexpected status (`123`).
- Earlier exercises included a successful scheduled Stream/Task INSERT and a separate scheduled MERGE. These were tested at different times and were not rerun together in the current repository version.
- I separately practiced malformed-CSV load diagnostics and clean/quarantine routing.

## Current limitations

- The files represent related exercises, not a single end-to-end Python orchestrator.
- The modified connector scripts and Task safety guards have not been live-retested together.
- The historical SQL worksheet includes `CREATE OR REPLACE`, data changes, and Task resume commands. **Do not run the worksheet from top to bottom.**
- Some Python scripts use the original database and role names and need adapting before execution in another Snowflake account.
- The `QUALIFY` deduplication example is separate from the preserved scheduled MERGE. The included CSV has repeated `PLAN_ID` values, so key-handling must be considered before using MERGE.
- Clean/quarantine routing was a separate worksheet test; the included sample files do not reproduce the previously tested routing totals.

All committed CSV samples are synthetic. Credentials and employer data are not included. Use an isolated Snowflake database and review statements that create, replace, or schedule objects.
