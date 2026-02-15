#!/usr/bin/env python3

import csv
from pathlib import Path

RUN_MONTH = "2026-02"

MANUAL_PATH = Path("Data/Inputs/BigBuy_Manual") / RUN_MONTH / "BigBuy_Manual_Februari.csv"
R73_ROOT = Path("Data/Exports/R73")
EXPORT_ROOT = Path("Data/Exports/R74") / RUN_MONTH

def sniff_delimiter(path: Path) -> str:
    sample = path.read_text(encoding="utf-8", errors="replace")[:4096]
    return ";" if sample.count(";") > sample.count(",") else ","

def read_csv_any(path: Path):
    delim = sniff_delimiter(path)
    with path.open(newline="", encoding="utf-8", errors="replace") as f:
        r = csv.DictReader(f, delimiter=delim)
        for row in r:
            yield row

def latest_r73_paths():
    dirs = [d for d in R73_ROOT.iterdir() if d.is_dir()]
    if not dirs:
        return None, None
    latest = sorted(dirs, key=lambda p: p.name)[-1]
    return latest / "R73_ALLOWED.csv", latest / "R73_EXCLUDED.csv"

def main():
    if not MANUAL_PATH.exists():
        raise SystemExit(f"Missing manual input: {MANUAL_PATH}")

    EXPORT_ROOT.mkdir(parents=True, exist_ok=True)

    r73_allowed_path, r73_excluded_path = latest_r73_paths()
    if not r73_allowed_path or not r73_allowed_path.exists():
        raise SystemExit("Missing R73_ALLOWED.csv")
    if not r73_excluded_path or not r73_excluded_path.exists():
        raise SystemExit("Missing R73_EXCLUDED.csv")

    allowed_skus = set()
    excluded_map = {}

    for row in read_csv_any(r73_allowed_path):
        allowed_skus.add((row.get("sku") or "").strip())

    for row in read_csv_any(r73_excluded_path):
        sku = (row.get("sku") or "").strip()
        excluded_map[sku] = row

    ready_path = EXPORT_ROOT / "R74_READY_FOR_R75.csv"
    rejected_by_r73_path = EXPORT_ROOT / "R74_REJECTED_BY_R73.csv"
    not_evaluated_path = EXPORT_ROOT / "R74_NOT_EVALUATED_BY_R73.csv"
    feedback_path = EXPORT_ROOT / "R74_R70_FEEDBACK.csv"
    log_path = EXPORT_ROOT / "R74_LOG.csv"

    manual_delim = sniff_delimiter(MANUAL_PATH)

    with MANUAL_PATH.open(newline="", encoding="utf-8", errors="replace") as f:
        r = csv.DictReader(f, delimiter=manual_delim)
        manual_fields = r.fieldnames or []

        enrich_fields = manual_fields + [
            "r74_bucket",
            "r73_proposition_fit",
            "r73_exclusion_reason",
            "r73_confidence",
        ]

        with ready_path.open("w", newline="", encoding="utf-8") as fr, \
             rejected_by_r73_path.open("w", newline="", encoding="utf-8") as fx, \
             not_evaluated_path.open("w", newline="", encoding="utf-8") as fn, \
             feedback_path.open("w", newline="", encoding="utf-8") as ff:

            w_ready = csv.DictWriter(fr, fieldnames=manual_fields)
            w_rej = csv.DictWriter(fx, fieldnames=enrich_fields)
            w_not = csv.DictWriter(fn, fieldnames=enrich_fields)
            w_fb = csv.DictWriter(ff, fieldnames=enrich_fields)

            w_ready.writeheader()
            w_rej.writeheader()
            w_not.writeheader()
            w_fb.writeheader()

            n_manual=0
            n_ready=0
            n_rejected=0
            n_not_eval=0

            for row in r:
                n_manual += 1
                sku = (row.get("sku") or "").strip()

                if sku in allowed_skus:
                    w_ready.writerow(row)
                    n_ready += 1
                    continue

                if sku in excluded_map:
                    r73_row = excluded_map[sku]
                    out = dict(row)
                    out["r74_bucket"] = "REJECTED_BY_R73"
                    out["r73_proposition_fit"] = "NO"
                    out["r73_exclusion_reason"] = r73_row.get("r73_exclusion_reason","")
                    out["r73_confidence"] = r73_row.get("r73_confidence","")
                    w_rej.writerow(out)
                    w_fb.writerow(out)
                    n_rejected += 1
                else:
                    out = dict(row)
                    out["r74_bucket"] = "NOT_EVALUATED_BY_R73"
                    out["r73_proposition_fit"] = ""
                    out["r73_exclusion_reason"] = ""
                    out["r73_confidence"] = ""
                    w_not.writerow(out)
                    n_not_eval += 1

    with log_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["metric","value"])
        w.writerow(["manual_rows", n_manual])
        w.writerow(["ready_for_r75", n_ready])
        w.writerow(["rejected_by_r73", n_rejected])
        w.writerow(["not_evaluated_by_r73", n_not_eval])
        w.writerow(["r73_allowed_path", str(r73_allowed_path)])
        w.writerow(["r73_excluded_path", str(r73_excluded_path)])

    print(f"✅ R74-B2 OK — manual={n_manual} ready={n_ready} rejected_by_r73={n_rejected} not_evaluated={n_not_eval}")
    print(f"   📤 Ready: {ready_path}")
    print(f"   📤 Rejected_by_R73: {rejected_by_r73_path}")
    print(f"   📤 Not_evaluated: {not_evaluated_path}")
    print(f"   📤 Feedback (learning): {feedback_path}")
    print(f"   📝 Log: {log_path}")

if __name__ == "__main__":
    main()
