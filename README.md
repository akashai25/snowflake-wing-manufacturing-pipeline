# Wing Manufacturing Data Pipeline (Learning Project)

**Python · Snowflake SQL · CSV ingestion · Streams · scheduled Tasks · data validation**

An independent learning project demonstrating how synthetic aircraft-assembly-style records can be generated in Python, staged in Snowflake, inspected for ingestion errors, transformed, and processed incrementally. **All example data in this repository is synthetic**, not Boeing production data.

> **Portfolio scope:** This is a documented collection of independent Snowflake/Python learning exercises, **not** a one-command or production-deployed pipeline. The manual CSV ingestion and data-quality checks below were validated in a separate Snowflake test database on 4 November 2026. The modified Python connector scripts and scheduled Stream/Task/MERGE workflow have **not** been retested together in that sandbox; those components are documented as historical exercises.

## What I worked on

- Generated 5-column synthetic CSV data using `csv.DictWriter` and Python's `random` module.
- Used `snowflake-connector-python` with named internal stages to explore local-file `PUT` uploads, staged-file inspection, and `COPY INTO` loading into `RAW_WING`.
- Practiced `VALIDATION_MODE`, `ON_ERROR = CONTINUE`, and `VALIDATE()` diagnostics on deliberately invalid numeric CSV values.
- Created Snowflake Streams and interval-scheduled, **warehouse-backed** Tasks to test incremental inserts and MERGE-based updates; examined Task History.
- Explored SQL transformations and window functions, including `ROW_NUMBER` and `QUALIFY` in separate exercises.
- Separately tested conditional `INSERT FIRST` logic to route missing-torque rows into a quarantine table. **This worksheet exercise was not integrated into the scheduled Stream/Task workflow.**

## Conceptual data flow

```text
Local Python generator ──> synthetic CSV ──> Snowflake internal stage
                                             │
                                             ▼
                                         COPY INTO
                                             │
                                             ▼
                                           RAW_WING
                                             │
                                  Stream / scheduled Task
                                             │
                                             ▼
                                          CLEAN_WING
                                             │
                                  Separate MERGE experiment
                                             ▼
                                         CLEAN_WING_T

Separate worksheet experiment (not part of the scheduled Task):
RAW_WING ──> conditional INSERT FIRST ──> CLEAN_WING / QUARANTINE_WING

Separately: malformed CSV ──> COPY validation and rejected-row diagnostics
```

**Architecture qualification:** The diagram summarizes related development components. The preserved files do not contain one standalone Python orchestrator that executes every step in sequence. The successful scheduled INSERT Task consumed a Stream into a clean target; a distinct later scheduled MERGE Task merged `CLEAN_WING` into `CLEAN_WING_T`. The preserved MERGE Task definition does **not** contain `QUALIFY` deduplication.

## Repository layout

```text
src/                              Original Python experiments, with limited safety edits
sql/Wing_data_project_lab.sql     Historical SQL worksheet; DO NOT execute from top to bottom
data/                             Synthetic sample CSVs
  wing_data_sample.csv            100 records, 5 fields
  wing_data_corrupted.csv         3 records, including a nonnumeric torque value
tools/audit_samples.py            New local-only data inspection helper
docs/EXECUTION_GUIDE.md           Safe starting steps, caveats and execution order
docs/EVIDENCE_AND_LIMITATIONS.md   What is backed by source/history vs. reported tests
.gitignore                        Keeps local secrets and development outputs out of Git
.env.example                      Placeholder credential names only
requirements.txt                  Python dependencies found in the original connector scripts
```

## Quick start (Windows + VS Code)

1. Install Python and VS Code. Open this folder in VS Code.
2. Inspect the included sample data without needing Snowflake:
   ```powershell
   python tools/audit_samples.py
   ```
3. To create a Python environment and install dependencies, open a PowerShell terminal:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```
   If PowerShell blocks activation, use `.\.venv\Scripts\python.exe` directly without changing execution policy.
4. Copy the template to a local credential file, then fill in **your own** test account values. Never commit the filled-in file:
   ```powershell
   Copy-Item .env.example .env
   ```
5. Read [docs/EXECUTION_GUIDE.md](docs/EXECUTION_GUIDE.md) **before** executing any Snowflake statements. Choose a dedicated sandbox database and check which statements write, replace or schedule objects.

For now, do **not** run `Wing_data_project_lab.sql` wholesale. The original Python scripts refer to database `WING_DATA_PROJECT` and role `SYSADMIN`; change these to an isolated environment before using them. Scripts such as `src/wing_task.py` and `src/transform_clean_wing.py` have opt-in safety switches; these modifications have not yet been tested against Snowflake.

## Sample data and local checks

The supplied `wing_data_sample.csv` has **100 rows and 97 distinct `PLAN_ID` values** (three keys repeat). One `QC_STATUS` value is `123`, unlike the other status strings. The supplied `wing_data_corrupted.csv` has three rows, one with `TORQUE_VALUE=ERR` to test numeric-load errors. These are useful teaching inputs, not production telemetry.

### Independent manual validation — 4 November 2026

In a separate Snowflake trial-account sandbox (`WING_GITHUB_TEST.PUBLIC`), the sample file was uploaded to an internal stage and checked with `COPY INTO ... VALIDATION_MODE = RETURN_ERRORS` (no load errors returned), then loaded into an empty `RAW_WING` table. The subsequent read-only SQL analysis observed:

| Check | Observed result |
| --- | ---: |
| Rows loaded | 100 |
| Distinct `PLAN_ID` values | 97 |
| Duplicate records beyond one per ID | 3 |
| Missing torque values | 0 |
| QC status `PASS` / `FAIL` / `REWORK` | 57 / 28 / 14 |
| Unexpected QC status `123` | 1 |

The QC validation rule intentionally accepts `REWORK` as a valid business status. This is **manual ingestion and validation only**: it does not establish that the Python staging scripts, Stream/Task automation, scheduled MERGE, or separate quarantine experiment ran end-to-end in the new test database. No private Snowflake account exports, query IDs, or screenshots are committed.

The separately reported worksheet routing test of **111 RAW → 105 CLEAN + 6 QUARANTINE** is **not reproducible from these two included CSV files alone**; no corresponding stored result file is included. A future documentation update should include a self-contained, reproducible test fixture before presenting those numbers as a repository demonstration.

## What has been observed versus what remains

The original account's exported Task History recorded a successful Wing scheduled INSERT (1 inserted row) and a separate MERGE run (3 inserted, 2 updated), in September 2026. Those results were inspected privately but the account export is not included here because it may contain identifiers and account metadata. See [evidence notes](docs/EVIDENCE_AND_LIMITATIONS.md).

The project is a learning environment. It is **not** described as production-deployed, serverless, guaranteed idempotent, continuously real-time, enterprise-scale, or benchmarked for cost/performance.

## Security and responsible publication

- The included records are synthetic. Do not replace them with employer data.
- Real `.env` files, Snowflake passwords, private keys, account histories, query IDs, and employer internal diagrams are excluded.
- A `.gitignore` reduces accidental commits but cannot retroactively remove secrets that have already been committed. Inspect GitHub Desktop's **Changes** view before your first commit.
- No employer branding, proprietary work instructions, drawing numbers, company screenshots, or internal source code should be published.

## Next steps

- Validate the cleaned scripts in a dedicated sandbox, recording reproducible test outputs without private IDs.
- Separate executable setup/ingestion steps from archived experiments and document a safe execution order.
- Add a repeatable duplicate-key resolution and MERGE test before claiming end-to-end idempotency.
- Publish only after completing [the publication checklist](docs/PUBLISH_CHECKLIST.md).
