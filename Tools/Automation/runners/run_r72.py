#!/usr/bin/env python3
import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path

OUT_HEADER = [
    "sku",
    "ean",
    "exists_in_shopify",
    "anchor_match_type",
    "anchor_confidence",
    "shopify_handle",
    "shopify_variant_sku",
    "shopify_barcode",
]

def utc_now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def write_log_row(log_path: Path, level: str, message: str):
    is_new = not log_path.exists()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if is_new:
            w.writerow(["timestamp", "stage", "level", "message"])
        w.writerow([utc_now_iso(), "R72", level, message])

def _strip(s):
    return (s or "").strip()

def _norm_upper(s):
    return _strip(s).upper()

def sniff_delimiter(path: Path):
    with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        sample = f.read(8192)
    if ";" in sample and sample.count(";") >= sample.count(","):
        return ";"
    try:
        d = csv.Sniffer().sniff(sample, delimiters=";,").delimiter
        return d if d in (";", ",") else ";"
    except Exception:
        return ";"

def read_csv(path: Path):
    delim = sniff_delimiter(path)
    with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        r = csv.DictReader(f, delimiter=delim)
        for row in r:
            yield row

def get_any(row, *keys):
    for k in keys:
        if k in row and row[k] is not None:
            v = str(row[k]).strip()
            if v != "":
                return v
    return ""

def build_r91_index(r91_path: Path):
    by_sku = {}
    by_ean = {}

    for row in read_csv(r91_path):
        handle = get_any(row, "Handle", "handle")
        sku = get_any(row, "Variant SKU", "VariantSKU", "variant_sku", "sku", "SKU")
        barcode = get_any(row, "Variant Barcode", "VariantBarcode", "variant_barcode", "barcode", "EAN", "ean")

        sku_n = _norm_upper(sku)
        ean_n = _norm_upper(barcode)

        rec = {
            "shopify_handle": handle,
            "shopify_variant_sku": sku,
            "shopify_barcode": barcode,
        }

        if sku_n:
            by_sku[sku_n] = rec
        if ean_n:
            by_ean[ean_n] = rec

    return by_sku, by_ean

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-month", required=True)
    args = ap.parse_args()
    run_month = args.run_month

    r91_path = Path("Data/Inputs/R91_Live") / run_month / "R91_Live_Januari.csv"
    bb_path  = Path("Data/Inputs/BigBuy_Manual") / run_month / "BigBuy_Manual_Februari.csv"

    out_dir  = Path("Data/Exports/R72") / run_month
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "R72_SHOPIFY_ANCHOR.csv"
    log_path = out_dir / "R72_LOG.csv"

    if not r91_path.exists():
        write_log_row(log_path, "ERROR", f"Missing R91 input: {r91_path}")
        return 2
    if not bb_path.exists():
        write_log_row(log_path, "ERROR", f"Missing BigBuy input: {bb_path}")
        return 2

    r91_by_sku, r91_by_ean = build_r91_index(r91_path)

    n_in = 0
    n_out = 0
    n_exists = 0

    with out_path.open("w", newline="", encoding="utf-8") as f_out:
        w = csv.DictWriter(f_out, fieldnames=OUT_HEADER)
        w.writeheader()

        for row in read_csv(bb_path):
            n_in += 1
            sku = get_any(row, "sku", "SKU")
            ean = get_any(row, "ean", "EAN", "barcode", "Variant Barcode")

            sku_n = _norm_upper(sku)
            ean_n = _norm_upper(ean)

            rec = None
            match_type = ""
            conf = "LOW"

            if sku_n and sku_n in r91_by_sku:
                rec = r91_by_sku[sku_n]
                match_type = "SKU"
                conf = "HIGH"
            elif ean_n and ean_n in r91_by_ean:
                rec = r91_by_ean[ean_n]
                match_type = "EAN"
                conf = "MEDIUM"

            exists = "YES" if rec else "NO"
            if exists == "YES":
                n_exists += 1

            out_row = {
                "sku": sku,
                "ean": ean,
                "exists_in_shopify": exists,
                "anchor_match_type": match_type,
                "anchor_confidence": conf,
                "shopify_handle": rec.get("shopify_handle","") if rec else "",
                "shopify_variant_sku": rec.get("shopify_variant_sku","") if rec else "",
                "shopify_barcode": rec.get("shopify_barcode","") if rec else "",
            }

            w.writerow(out_row)
            n_out += 1

    write_log_row(log_path, "INFO", f"R72 OK. run-month={run_month} in={n_in} out={n_out} exists_in_shopify={n_exists} r91={r91_path} bigbuy={bb_path} out={out_path}")
    print(f"✅ R72 OK — run-month={run_month} | in={n_in} out={n_out} exists_in_shopify={n_exists}")
    print(f"   📥 R91: {r91_path}")
    print(f"   📥 BigBuy: {bb_path}")
    print(f"   📤 Out: {out_path}")
    print(f"   📝 Log: {log_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
