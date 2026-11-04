# Wing Manufacturing Data Pipeline

**Python · Snowflake SQL · CSV ingestion · Streams · scheduled Tasks · data validation**

An independent Python and Snowflake SQL project using **synthetic manufacturing records** to explore file ingestion, data validation, transformations, and incremental processing. All committed data is synthetic; no employer production data is included.

**Project scope:** The repository preserves related, separately developed components—not a single automatically orchestrated application. Manual CSV ingestion and data-quality checks were validated in a Snowflake test database on **4 November 2026**. Earlier scheduled INSERT and MERGE exercises have separate execution-history evidence; the modified repository scripts have **not** been retested together.

## Results at a glance

| Component | Evidence |
| --- | --- |
| Sample CSV ingestion | 100 rows loaded into a sandbox `RAW_WING` table |
| Data quality | 97 distinct `PLAN_ID` values; 3 duplicate extras; 0 null torque values |
| Status validation | `PASS`, `FAIL`, and `REWORK` accepted; 1 unexpected status (`123`) in the sample |
| Scheduled Stream/Task INSERT | Earlier Task History: 1 inserted row (September 2026) |
| Separate scheduled MERGE | Earlier Task History: 3 inserts and 2 updates (September 2026) |

The sample-file validation and historical scheduled Task runs were **separate tests**, not evidence of a fully retested end-to-end automated workflow. Details: [evidence and limitations](docs/EVIDENCE_AND_LIMITATIONS.md).

## What I worked on

- Generated 5-column synthetic CSV data using `csv.DictWriter` and Python's `random` module.
- Used `snowflake-connector-python` with named internal stages to explore local-file `PUT` uploads, staged-file inspection, and `COPY INTO` loading into `RAW_WING`.
- Practiced `VALIDATION_MODE`, `ON_ERROR = CONTINUE`, and `VALIDATE()` diagnostics on deliberately invalid numeric CSV values.
- Created Snowflake Streams and interval-scheduled, **warehouse-backed** Tasks to test incremental inserts and MERGE-based updates; examined Task History.
- Explored SQL transformations and window functions, including `ROW_NUMBER` and `QUALIFY` in separate exercises.
- Separately tested conditional `INSERT FIRST` logic to route missing-torque rows into a quarantine table. **This worksheet exercise was not integrated into the scheduled Stream/Task workflow.**

## Architecture — related components

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

**How to read the diagram:** The stages summarize separate development activities. There is no single Python orchestrator that runs them all in sequence. The scheduled INSERT used a Stream; a different scheduled MERGE later read from `CLEAN_WING`. `QUALIFY` was explored separately and is not part of the preserved scheduled MERGE definition.

## Repository layout

```text
src/                              Original Python experiments, with limited safety edits
sql/Wing_data_project_lab.sql     Historical SQL worksheet; DO NOT execute from top to bottom
data/                             Synthetic sample CSVs
  wing_data_sample.csv            100 records, 5 fields
  wing_data_corrupted.csv         3 records, including a nonnumeric torque value
tools/audit_samples.py            Local-only sample data inspection
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

**Safety:** Do **not** run `Wing_data_project_lab.sql` wholesale. The original Python scripts refer to database `WING_DATA_PROJECT` and role `SYSADMIN`; change these to an isolated environment before using them. Scripts such as `src/wing_task.py` and `src/transform_clean_wing.py` have opt-in safety switches; these modifications have not yet been tested against Snowflake.

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

## Scope, security and limitations

- This is a learning portfolio, **not** a deployed production system, serverless implementation, or measured performance benchmark.
- The preserved SQL file is a **historical worksheet**, including destructive DDL and Task-control commands. Never execute the entire file. See the [execution guide](docs/EXECUTION_GUIDE.md).
- Python scripts reference the original development database and role; they must be reviewed and adapted before running against a fresh sandbox. Safety switches added during portfolio preparation have not been live-retested.
- The separate clean/quarantine routing exercise (reported as 111 RAW → 105 CLEAN + 6 QUARANTINE) does **not** have a corresponding reproducible fixture in this repository.
- All committed CSV examples are synthetic. Local credentials, private keys, internal employer materials, and account-history exports are intentionally excluded. The `.gitignore` helps prevent accidental inclusion of local credentials.

## Potential enhancements

- Provide one reproducible setup and ingestion workflow for a dedicated sandbox.
- Add automated data-quality tests and a deterministic duplicate-key resolution strategy.
- Validate the repository's modified connector scripts and scheduled Tasks together, including a safe MERGE test.
