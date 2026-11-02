# Public GitHub publication checklist

Do this **before** selecting Publish repository as Public.

- [ ] Confirm all included data is synthetic, not Boeing or third-party confidential data.
- [ ] Search every `.py`, `.sql`, `.md`, `.csv`, `.json` for passwords, tokens, Snowflake account locators, employee IDs, query IDs and internal links.
- [ ] Confirm `.env`, `.env.*` (except `.env.example`), local `.venv`, credential files and private screenshots are absent.
- [ ] Run `python tools/audit_samples.py` and examine the duplicate IDs and invalid sample values.
- [ ] Read the warning in `sql/Wing_data_project_lab.sql`: NEVER execute it wholesale.
- [ ] Review the safety changes in `src/wing_task.py`, `src/transform_clean_wing.py` and `src/raw_wing_stream.py`.
- [ ] Test the publishable scripts in a dedicated Snowflake sandbox and record any changes needed.
- [ ] Verify the README does not imply automated quarantine, fully idempotent production upserts, serverless Tasks, or measured savings.
- [ ] Check GitHub Desktop Changes and file diffs before the first commit.
- [ ] Start with repository **Private**, then switch to Public only after the checks pass.
- [ ] In a private/incognito browser window, check the public README and source layout after publishing.
- [ ] Add the final GitHub profile URL to the reserved resume placeholder only after the repo is viewable.
