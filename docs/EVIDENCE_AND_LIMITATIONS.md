# Evidence and limitations

This table distinguishes **available source**, **private account-history verification**, **user-reported experiments**, and **new preparation edits**. It does not convert separate exercises into a production deployment.

| Claim | What is actually available | Accurate public wording |
|---|---|---|
| Python data generation | `src/generate_csv.py` and synthetic CSV | Generated synthetic Wing records with Python |
| Python staging | `corrupted_csv_into_stage.py` executes PUT; original `connection.py` has commented PUT/COPY | Used Connector/Python to stage test files; no single complete Python runner preserved |
| Internal stages / COPY | Historical SQL; private execution history | Practiced stage-based ingestion and CSV loading |
| RAW Stream and scheduled Task | Python/SQL definitions; private Task History | Tested warehouse-backed Stream/Task incremental processing |
| Successful scheduled insert | Private exported Task History: 2026-09-17, 1 row inserted | Verified one successful scheduled INSERT run |
| Successful scheduled MERGE | Private exported Task History: 2026-09-30, 3 inserted and 2 updated | Verified one successful scheduled MERGE test |
| MERGE with QUALIFY | `QUALIFY` and MERGE separately present in saved SQL; no QUALIFY in verified scheduled MERGE | Practiced separate deduplication queries; do not attribute them to successful Task MERGE |
| 111 / 105 / 6 routing outcome | Self-reported Snowsight test; exact output not preserved | Separately tested clean/quarantine routing; counts are unverified by supplied artifacts |
| Malformed-file errors | Synthetic ERR numeric input, COPY validation / VALIDATE SQL | Tested invalid numeric and CSV load diagnostics |
| Task orchestration | Task SQL uses `WAREHOUSE='COMPUTE_WH'`, interval schedules | Warehouse-backed scheduled Tasks; **not** serverless or CRON |
| Transient staging | Original Python creates CLEAN_WING_T with `CREATE OR REPLACE TABLE`, no TRANSIENT | Do not call CLEAN_WING_T a verified transient table |
| Cost savings, zero downtime, production scale | No formal measurements or operational deployment | Do not claim |
| End-to-end, automated quarantining, guaranteed idempotence | No one-run orchestrator; quarantine separate; source includes duplicate PLAN_IDs | Describe modular tests and stages precisely |

## Fresh manual sandbox test — 4 November 2026

Using the synthetic `data/wing_data_sample.csv`, a separate Snowflake trial database (`WING_GITHUB_TEST.PUBLIC`) was used to create a RAW table, file format, and internal stage; upload the CSV; run `COPY INTO` validation; load the CSV; and query its data quality. The user shared successful query output showing **100 rows, 97 distinct plan IDs, three duplicate extras, zero null torque values, and 15 statuses outside PASS/FAIL**. After expanding the valid status set to include REWORK, the expected invalid status count is **one** (`123`), matching the committed synthetic CSV. The user confirmed completing the corrected query but did not supply its result table.

These are **manual Snowflake worksheet results**. No fresh execution evidence has been obtained for the Python connector scripts, warehouse-backed Tasks, MERGE or quarantine routing in the new test environment.

## New edits in this preparation package

To prevent accidental writes while learning Git, the copies of `wing_task.py` and `transform_clean_wing.py` have opt-in safety flags; `raw_wing_stream.py` uses `CREATE STREAM IF NOT EXISTS` rather than `CREATE OR REPLACE`. A new *local-only* CSV-audit helper and new documentation were added. **These changes were syntax-tested locally, not tested against Snowflake.** The user's original archives were not modified.
