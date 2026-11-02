# Execution guide — read before running anything

## Safe local-only actions

From the project root:

```powershell
python tools/audit_samples.py
python src/generate_csv.py
python src/corrupted_csv.py
```

The two generator scripts overwrite the *local* `wing_data_sample.csv` and `wing_data_corrupted.csv` in the current working directory. The committed sample files live in `data/`; if you want to regenerate them there, run from that directory with the correct relative script path, or edit the output paths first. **Do not confuse new random output with the already committed baseline samples.**

## Snowflake account prerequisites (not automatic)

- A Snowflake account with a warehouse that you are authorized to use.
- A separate test database and schema under your control; do not run against company or production objects.
- Created `RAW_WING`, `CLEAN_WING`, `CLEAN_WING_T` tables, a named internal stage, and a CSV file format (from a reviewed subset of the historical SQL).
- A Stream created **before** new ingestion events if you want the Stream to capture those changes.
- Appropriate grants for creating Tasks if you choose to run scheduled code.

## Historical SQL — HIGH RISK if executed wholesale

`sql/Wing_data_project_lab.sql` is a chronological collection of experiments. It includes:

- `CREATE OR REPLACE DATABASE Wing_data_project;` — can replace the entire database and its objects.
- `CREATE OR REPLACE TABLE RAW_WING`, `BAD_WING_DATA` — can replace existing tables.
- `COPY ... FORCE = TRUE` — can reload already loaded files and duplicate rows.
- `UPDATE`, `DELETE`, `INSERT` — mutate records.
- `CREATE OR REPLACE TASK` and `ALTER TASK ... RESUME` — can schedule ongoing credit-consuming work.
- A `QUALIFY` example referring to `INGEST_TIME`, which is not defined in the visible `CLEAN_WING` table DDL.
- A MERGE with `PLAN_ID` as the match key, while the sample has duplicate keys.

**Do not select and run all statements.** Copy only the small, relevant examples into a fresh worksheet after verifying their objects and assumptions.

## Python script status

| Script | Meaning | Safety / limitation |
|---|---|---|
| `generate_csv.py` | Local synthetic CSV generator | Safe locally; writes to current working directory |
| `corrupted_csv.py` | Local malformed numeric test generator | Safe locally; writes to current working directory |
| `connection.py` | Connects to Snowflake and reads local/staged/table row counts | PUT and COPY calls are commented out; not a one-command uploader |
| `corrupted_csv_into_stage.py` | Puts corrupted CSV into an internal stage | Upload mutates stage; verify account, database and file path first |
| `raw_wing_stream.py` | Creates and inspects a Stream | Portfolio copy changed OR REPLACE to IF NOT EXISTS; not live-retested |
| `stream_clean_wing.py` | SQL definitions/inspection of clean table | Creation/insertion lines commented in preserved source |
| `transform_clean_wing.py` | Creates/replaces and fills CLEAN_WING_T | Portfolio copy has safety switch `ENABLE_DESTRUCTIVE_TRANSFORM=false` |
| `wing_task.py` | Creates and resumes a warehouse-backed Task | Portfolio copy has safety switch `ENABLE_TASK_CHANGES=false` |

All Python scripts were syntax-checked during preparation. A live connector/login/DDL test has **not** been run in your account from this package.

## Suggested safe manual walkthrough (only after reviewing SQL)

1. In a new isolated Snowflake database/schema, create the stage, file format, RAW table, and clean targets using reviewed DDL.
2. Create a new standard Stream on RAW **before** the relevant inserts/COPY.
3. Run the local generator, ensure the `.env` is excluded from Git, and upload a synthetic CSV to the internal stage via the Connector/Python PUT script once you have verified paths and privileges.
4. Execute a `COPY INTO` for the clean sample and inspect `COPY` output and `RAW_WING` row counts; do not use `FORCE=TRUE` by default.
5. Run read-only Stream checks; then, if you choose, create/resume a warehouse-backed Task, inspect the targeted insert/merge results, and suspend the Task again.
6. For `INSERT FIRST` and numeric-load diagnostics, use a **separate isolated test** so repeated loads and Task runs do not distort the counts.
7. Save only non-sensitive SQL snippets and anonymized aggregate results for the README.

Do not share live Snowflake account locators, environment files, query IDs, or real employer data in screenshots or logs.
