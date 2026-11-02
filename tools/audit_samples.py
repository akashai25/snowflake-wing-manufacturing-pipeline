"""Local-only inspection of included synthetic CSVs (added for portfolio preparation).

No cloud connections. Reports anomalies; does not modify input data.
"""
from pathlib import Path
import csv
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"PLAN_ID", "PART_NUM", "OP_SEQ", "TORQUE_VALUE", "QC_STATUS"}
VALID_STATUS = {"PASS", "FAIL", "REWORK"}


def check(filename: str) -> None:
    path = ROOT / "data" / filename
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        if not EXPECTED.issubset(set(reader.fieldnames or [])):
            print(f"{filename}: missing expected columns: {EXPECTED - set(reader.fieldnames or [])}")
            return
    count = Counter(row["PLAN_ID"] for row in rows)
    duplicates = [key for key, frequency in count.items() if frequency > 1]
    invalid_torque = []
    missing_torque = []
    unexpected_status = []
    for i, row in enumerate(rows, start=2):
        raw = (row["TORQUE_VALUE"] or "").strip()
        if not raw:
            missing_torque.append(i)
        else:
            try:
                float(raw)
            except ValueError:
                invalid_torque.append(i)
        if row["QC_STATUS"] not in VALID_STATUS:
            unexpected_status.append(i)
    print(f"{filename}: {len(rows)} records; {len(count)} distinct PLAN_ID; "
          f"{len(duplicates)} duplicated keys; missing torque lines {missing_torque}; "
          f"invalid torque lines {invalid_torque}; unexpected QC status lines {unexpected_status}")


if __name__ == "__main__":
    check("wing_data_sample.csv")
    check("wing_data_corrupted.csv")
