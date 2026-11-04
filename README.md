# Wing Manufacturing Data Pipeline

**Python | Snowflake SQL | CSV | Streams & Tasks**

I built this project while learning how to process manufacturing-style data with Python and Snowflake. It uses synthetic records, so no company data is included.

## What I worked on

- Generated sample CSV records in Python, including some deliberately incorrect values.
- Uploaded CSV data to a Snowflake internal stage and loaded it into a RAW table using `COPY INTO`.
- Checked for loading errors, duplicate IDs, missing values, and unexpected quality statuses.
- Practiced cleaning data with SQL and using Streams, scheduled Tasks, and MERGE for incremental processing.
- Tried a separate SQL exercise for routing records into clean and quarantine tables.

## Data flow

```text
Python-generated CSV
        |
Snowflake internal stage
        |
      COPY INTO
        |
      RAW_WING
        |
  Stream + scheduled Task
        |
     CLEAN_WING
```

I also worked on a separate MERGE into `CLEAN_WING_T`, a quarantine-routing exercise, and handling malformed CSV files. These were related exercises, **not one fully automated workflow**.

## What I tested

I loaded 100 synthetic records into a Snowflake test database and used SQL to find duplicate IDs and an unexpected quality status. Earlier development work also included successful scheduled INSERT and MERGE tests. The modified Python scripts in this repository have not been retested together.

## Project files

- `src/` — Python scripts used during development
- `sql/Wing_data_project_lab.sql` — my original SQL practice worksheet
- `data/` — synthetic CSV samples
- `tools/audit_samples.py` — a local Python script for inspecting sample data
- `docs/` — execution notes and more detailed test information

## Getting started

You can inspect the sample data without a Snowflake account:

```powershell
py tools/audit_samples.py
```

To explore the Snowflake scripts, start with [the execution guide](docs/EXECUTION_GUIDE.md) and use a separate test database. The original SQL worksheet contains commands that replace tables and modify Tasks, so **do not run the entire worksheet at once**. Some Python scripts still reference the original development database and must be adapted before running.

This is a personal learning project, not a production deployment. More details are in [evidence and limitations](docs/EVIDENCE_AND_LIMITATIONS.md).
