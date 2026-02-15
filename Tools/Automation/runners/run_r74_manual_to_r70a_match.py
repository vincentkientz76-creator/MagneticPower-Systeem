#!/usr/bin/env python3
import argparse, csv
from pathlib import Path
from datetime import datetime

def iter_r70a_files_latest() -> list[Path]:
    root = Path("Data/Exports/R70A/LATEST")
    if not root.exists():
        return []
    return sorted(root.rglob("R70A_RAW_PRODUCTS.csv"))

def iter_r70a_files_older() -> list[Path]:
    root = Path("Data/Exports/R70A")
    if not root.exists():
        return []
    files = []
    for p in root.rglob("R70A_RAW_PRODUCTS.csv"):
        s = str(p).replace("\\", "/")
        if "/LATEST/" in s:
            continue
        files.append(p)
    return sorted(files)

def read_csv_any(path: Path):
    try:
        with open(path, newline="", encoding="utf-8") as f:
            sample = f.read(4096)
        delim = ";" if sample.count(";") > sample.count(",") else ","
    except Exception:
        delim = ","
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f, delimiter=delim)
        for row in r:
            yield row

def index_r70a(files: list[Path]) -> dict[str, dict]:
    idx: dict[str, dict] = {}
    for fp in files:
        supplier = fp.parent.name
        run_dir = fp.parent.parent.name
        try:
            for row in read_csv_any(fp):
                sku = (row.get("sku") or "").strip()
                if not sku or sku in idx:
                    continue
                idx[sku] = {
                    "sku": sku,
                    "ean": (row.get("ean") or "").strip(),
                    "title": (row.get("title") or "").strip(),
                    "product_url_r70a": (row.get("product_url") or "").strip(),
                    "image_urls_r70a": (row.get("image_urls") or "").strip(),
                    "supplier_category_names_r70a": (row.get("supplier_category_names") or "").strip(),
                    "source_supplier": supplier,
                    "source_run": run_dir,
                    "source_file": str(fp),
                }
        except Exception:
            continue
    return idx

def read_manual_semicolon(manual_path: Path) -> list[dict]:
    rows = []
    with open(manual_path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f, delimiter=";")
        for row in r:
            sku = (row.get("sku") or "").strip()
            if sku:
                rows.append(row)
    return rows

def write_csv(path: Path, fieldnames: list[str], rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow({k: (row.get(k, "") or "") for k in fieldnames})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-month", default="2026-02")
    ap.add_argument("--manual", default="Data/Inputs/BigBuy_Manual/2026-02/BigBuy_Manual_Februari.csv")
    ap.add_argument("--out-dir", default=None)
    args = ap.parse_args()

    manual_path = Path(args.manual)
    if not manual_path.exists():
        raise SystemExit(f"Missing manual file: {manual_path}")

    out_dir = Path(args.out_dir) if args.out_dir else Path("Data/Exports/R74") / args.run_month
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    latest_files = iter_r70a_files_latest()
    older_files  = iter_r70a_files_older()

    latest_idx = index_r70a(latest_files)
    older_idx  = index_r70a(older_files)

    manual_rows = read_manual_semicolon(manual_path)

    found_latest, found_older, not_found = [], [], []

    def enrich(base: dict, hit: dict, bucket: str) -> dict:
        out = dict(base)
        out["match_bucket"] = bucket
        out["r70a_source_run"] = hit.get("source_run", "")
        out["r70a_source_supplier"] = hit.get("source_supplier", "")
        out["r70a_source_file"] = hit.get("source_file", "")
        out["product_url_r70a"] = hit.get("product_url_r70a", "")
        out["image_urls_r70a"] = hit.get("image_urls_r70a", "")
        out["supplier_category_names_r70a"] = hit.get("supplier_category_names_r70a", "")
        return out

    for row in manual_rows:
        sku = (row.get("sku") or "").strip()
        if sku in latest_idx:
            found_latest.append(enrich(row, latest_idx[sku], "FOUND_IN_R70A_LATEST"))
        elif sku in older_idx:
            found_older.append(enrich(row, older_idx[sku], "FOUND_IN_OLDER_R70A"))
        else:
            r = dict(row)
            r["match_bucket"] = "NOT_FOUND_ANYWHERE"
            r["r70a_source_run"] = ""
            r["r70a_source_supplier"] = ""
            r["r70a_source_file"] = ""
            r["product_url_r70a"] = ""
            r["image_urls_r70a"] = ""
            r["supplier_category_names_r70a"] = ""
            not_found.append(r)

    base_fields = list(manual_rows[0].keys()) if manual_rows else ["sku","ean","title","product_url"]
    extra_fields = [
        "match_bucket",
        "r70a_source_run",
        "r70a_source_supplier",
        "r70a_source_file",
        "product_url_r70a",
        "image_urls_r70a",
        "supplier_category_names_r70a",
    ]
    out_fields = base_fields + [f for f in extra_fields if f not in base_fields]

    p_latest = out_dir / f"R74_MANUAL_MATCH_FOUND_IN_R70A_LATEST_{ts}.csv"
    p_older  = out_dir / f"R74_MANUAL_MATCH_FOUND_IN_OLDER_R70A_{ts}.csv"
    p_none   = out_dir / f"R74_MANUAL_MATCH_NOT_FOUND_ANYWHERE_{ts}.csv"
    p_log    = out_dir / f"R74_MANUAL_TO_R70A_MATCH_LOG_{ts}.csv"

    write_csv(p_latest, out_fields, found_latest)
    write_csv(p_older,  out_fields, found_older)
    write_csv(p_none,   out_fields, not_found)

    log_rows = [
        {"metric":"run_month","value":args.run_month},
        {"metric":"manual_file","value":str(manual_path)},
        {"metric":"manual_rows","value":str(len(manual_rows))},
        {"metric":"latest_files_scanned","value":str(len(latest_files))},
        {"metric":"older_files_scanned","value":str(len(older_files))},
        {"metric":"found_in_latest","value":str(len(found_latest))},
        {"metric":"found_in_older","value":str(len(found_older))},
        {"metric":"not_found_anywhere","value":str(len(not_found))},
        {"metric":"out_found_latest","value":str(p_latest)},
        {"metric":"out_found_older","value":str(p_older)},
        {"metric":"out_not_found","value":str(p_none)},
    ]
    with open(p_log, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["metric","value"])
        w.writeheader()
        for row in log_rows:
            w.writerow(row)

    print(f"✅ R74 MANUAL→R70A MATCH OK | manual={len(manual_rows)} latest={len(found_latest)} older={len(found_older)} not_found={len(not_found)}")
    print(f"   📥 Manual: {manual_path}")
    print(f"   📤 Latest: {p_latest}")
    print(f"   📤 Older : {p_older}")
    print(f"   📤 None  : {p_none}")
    print(f"   📝 Log   : {p_log}")

if __name__ == "__main__":
    main()
