#!/usr/bin/env python3

import csv
from pathlib import Path
from datetime import datetime

def sniff_delimiter(path: Path) -> str:
    sample = path.read_text(encoding="utf-8", errors="replace")[:4096]
    return ";" if sample.count(";") > sample.count(",") else ","

def read_csv_any(path: Path):
    delim = sniff_delimiter(path)
    with path.open(newline="", encoding="utf-8", errors="replace") as f:
        r = csv.DictReader(f, delimiter=delim)
        for row in r:
            yield row

def main():
    run_month = "2026-02"

    r91_path = Path("Data/Inputs/R91_Live") / run_month / "R91_Live_Januari.csv"
    bb_path  = Path("Data/Inputs/BigBuy_Manual") / run_month / "BigBuy_Manual_Februari.csv"

    if not r91_path.exists():
        raise SystemExit(f"Missing R91 live: {r91_path}")
    if not bb_path.exists():
        raise SystemExit(f"Missing BigBuy manual: {bb_path}")

    # Build BigBuy manual SKU set
    bb_skus = set()
    for row in read_csv_any(bb_path):
        sku = (row.get("sku") or row.get("SKU") or row.get("Variant SKU") or "").strip()
        if sku:
            bb_skus.add(sku)

    # Output
    out_dir = Path("Data/Exports/R72") / run_month
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "R72_LIVE_NOT_IN_PIPELINE.csv"

    n_live = 0
    n_out = 0

    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["sku","ean","handle","title","vendor","reason"])
        w.writeheader()

        for row in read_csv_any(r91_path):
            sku = (row.get("Variant SKU") or row.get("sku") or row.get("SKU") or "").strip()
            if not sku:
                continue
            n_live += 1

            if sku in bb_skus:
                continue

            ean = (row.get("Variant Barcode") or row.get("ean") or row.get("EAN") or "").strip()
            handle = (row.get("Handle") or row.get("handle") or "").strip()
            title = (row.get("Title") or row.get("title") or "").strip()
            vendor = (row.get("Vendor") or row.get("vendor") or "").strip()

            w.writerow({
                "sku": sku,
                "ean": ean,
                "handle": handle,
                "title": title,
                "vendor": vendor,
                "reason": "NOT_IN_BIGBUY_MANUAL_SCOPE"
            })
            n_out += 1

    print(f"✅ R72 LIVE AUDIT OK — run-month={run_month} | live_rows={n_live} not_in_pipeline={n_out}")
    print(f"   📥 R91: {r91_path}")
    print(f"   📥 BigBuy: {bb_path}")
    print(f"   📤 Out: {out_path}")

if __name__ == "__main__":
    main()
