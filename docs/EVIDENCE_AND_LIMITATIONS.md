# Wing Pipeline — Technical Notes

This project uses synthetic manufacturing-style CSV data to practice Python and Snowflake ingestion, data checks, and incremental processing.

## Tested components

- Loaded 100 records from the included sample CSV into a Snowflake test database using an internal stage and `COPY INTO`.
- Checked duplicate IDs, torque values, and QC statuses. The sample has 97 distinct plan IDs, three additional rows with repeated IDs, and one unexpected status (`123`).
- Previously tested a scheduled Stream/Task INSERT and a separate scheduled MERGE.
- Practiced invalid-file diagnostics and clean/quarantine routing as separate exercises.

## Limitations and safe use

- These are related exercises, not a single tested end-to-end automated workflow.
- The connector scripts and Task safety switches have not been retested together.
- The SQL worksheet contains statements that replace database objects and change Tasks. Review statements individually; do not execute the entire worksheet.
- Some Python scripts use development database and role names that must be changed for a new test environment.
- The `QUALIFY` exercise is separate from the scheduled MERGE. Duplicate plan IDs in the sample require attention when choosing a MERGE key.
- The included sample files do not reproduce the separate clean/quarantine routing test.

The sample data is synthetic. Use an isolated Snowflake environment and keep credentials outside version control.
