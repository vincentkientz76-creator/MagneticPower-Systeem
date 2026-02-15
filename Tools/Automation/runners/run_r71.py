#!/usr/bin/env python3
import argparse
import os
import csv
import re
from datetime import datetime, timezone
from pathlib import Path

from Tools.Automation.lib.mp_paths import get_r70a_dir
OUT_HEADER = [
    "sku",
    "ean",
    "title",
    "description_raw",
    "vendor",
    "supplier_category",
    "product_url",
    "image_urls",
    "weight",
    "video_url",
    "product_function_primary",
    "product_function_secondary",
    "function_confidence",
    "function_reason",
    "r71_is_magnetic",
    "r71_magnetic_signal",
    "r71_confidence",
    "r71_reason",
]

def utc_now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def write_log_row(log_path: Path, supplier: str, level: str, message: str):
    is_new = not log_path.exists()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if is_new:
            w.writerow(["timestamp", "stage", "level", "supplier", "message"])
        w.writerow([utc_now_iso(), "R71", level, supplier, message])

def norm_get(row: dict, *keys, default=""):
    for k in keys:
        if k in row and row[k] is not None:
            return str(row[k]).strip()
    return default

def load_r70a_map(r70a_path: Path):
    m = {}
    with r70a_path.open("r", newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            sku = norm_get(row, "sku", "SKU")
            if not sku:
                continue
            m[sku] = {
                "ean": norm_get(row, "ean", "EAN"),
                "title": norm_get(row, "title", "name", "Title", "NAME"),
                "description_raw": norm_get(row, "description_raw", "description", "Description", "DESCRIPTION"),
                "vendor": norm_get(row, "vendor", "brand", "Vendor", "BRAND"),
                "supplier_category": norm_get(row, "supplier_category", "category", "Category", "CATEGORY"),
                "product_url": norm_get(row, "product_url", "url", "productUrl"),
                "image_urls": norm_get(row, "image_urls", "images", "imageUrls"),
                "weight": norm_get(row, "weight", "Weight", "WEIGHT"),
                "video_url": norm_get(row, "video_url", "VIDEO"),
            }
    return m

def joined_text(title, desc):
    return ((title or "") + " " + (desc or "")).lower()

def detect_magnetic(title: str, desc: str, func_primary: str):
    text = joined_text(title, desc)

    if "magnetron" in text:
        return ("NO", "none", "LOW", "Contains 'magnetron' (microwave)")

    strong_signals = [
        ("qi2", "qi2"),
        ("magsafe", "magsafe"),
        ("mag-safe", "magsafe"),
        ("mag safe", "magsafe"),
    ]

    magnet_signals = [
        ("magnetisch", "magnetisch"),
        ("magneet", "magneet"),
        ("magnetic", "magnetic"),
        ("neodym", "neodymium"),
        ("neodim", "neodymium"),
        ("ndfeb", "neodymium"),
    ]

    weak_false_positive_domains = [
        "nagellak","haar","shampoo","conditioner","cosmet","make-up","make up",
        "lipstick","parfum","eau de toilette","deo","deodorant","bodylotion","crème",
        "cream","serum",
    ]

    if ("magnet" in text or "magnetisch" in text or "magnetic" in text):
        for w in weak_false_positive_domains:
            if w in text:
                return ("NO", "marketing", "LOW", "Magnet keyword appears as cosmetic marketing context")

    for token, label in strong_signals:
        if token in text:
            return ("YES", label, "HIGH", f"Strong signal: {label}")

    for token, label in magnet_signals:
        if token in text:
            fp = (func_primary or "").lower()
            if fp in {"charger","powerbank","mount","cable","generic_accessory","replacement_part"}:
                return ("YES", label, "HIGH", f"Magnet signal + function={fp}")
            return ("YES", label, "MEDIUM", f"Magnet signal: {label}")

    if " qi " in (" " + text + " ") or "wireless" in text:
        return ("MAYBE", "wireless_no_magnet", "LOW", "Wireless/Qi mentioned without explicit magnet signal")

    return ("NO", "none", "LOW", "No magnetic signals found")

def detect_suppliers(run_ts: str):
    base_b = Path("Data/Exports/R70B") / run_ts
    suppliers = []
    for name in ("BigBuy", "Eprolo"):
        r70b = base_b / name / "R70B_FUNCTION_CLASSIFIED.csv"
        if r70b.exists() and r70b.is_file():
            suppliers.append(name)
    return suppliers

def main():
    ap = argparse.ArgumentParser()

    ap.add_argument("--run", required=True)
    args = ap.parse_args()
    run_ts = args.run

    suppliers = detect_suppliers(run_ts)
    if not suppliers:
        print("❌ R71: No R70B inputs found. Expected: Data/Exports/R70B/<RUN_TS>/<Supplier>/R70B_FUNCTION_CLASSIFIED.csv")
        return 2

    for supplier in suppliers:
        r70b_path = Path("Data/Exports/R70B") / run_ts / supplier / "R70B_FUNCTION_CLASSIFIED.csv"
        r70a_path = get_r70a_dir(os.environ.get("MP_R70A_RUN")) / supplier / "R70A_RAW_PRODUCTS.csv"

        out_dir = Path("Data/Exports/R71") / run_ts / supplier
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "R71_MAGNETIC_CAPABILITY.csv"
        log_path = out_dir / "R71_LOG.csv"

        if not r70a_path.exists():
            write_log_row(log_path, supplier, "WARN", f"Missing R70A input (no enrichment): {r70a_path}")
            r70a_map = {}
        else:
            r70a_map = load_r70a_map(r70a_path)

        n_in = 0
        n_out = 0
        n_enriched = 0

        with r70b_path.open("r", newline="", encoding="utf-8") as f_in, out_path.open("w", newline="", encoding="utf-8") as f_out:
            reader = csv.DictReader(f_in)
            writer = csv.DictWriter(f_out, fieldnames=OUT_HEADER)
            writer.writeheader()

            for row in reader:
                n_in += 1
                sku = norm_get(row, "sku", "SKU")
                base = r70a_map.get(sku, {})

                out_row = {
                    "sku": sku,
                    "ean": norm_get(row, "ean", "EAN") or base.get("ean",""),
                    "title": norm_get(row, "title", "name", "Title", "NAME") or base.get("title",""),
                    "description_raw": norm_get(row, "description_raw", "description") or base.get("description_raw",""),
                    "vendor": norm_get(row, "vendor", "brand") or base.get("vendor",""),
                    "supplier_category": norm_get(row, "supplier_category", "category") or base.get("supplier_category",""),
                    "product_url": norm_get(row, "product_url", "url") or base.get("product_url",""),
                    "image_urls": norm_get(row, "image_urls", "images") or base.get("image_urls",""),
                    "weight": norm_get(row, "weight", "Weight") or base.get("weight",""),
                    "video_url": norm_get(row, "video_url", "VIDEO") or base.get("video_url",""),
                    "product_function_primary": norm_get(row, "product_function_primary"),
                    "product_function_secondary": norm_get(row, "product_function_secondary"),
                    "function_confidence": norm_get(row, "function_confidence"),
                    "function_reason": norm_get(row, "function_reason"),
                }

                if sku in r70a_map:
                    n_enriched += 1

                r71_is_magnetic, r71_signal, r71_conf, r71_reason = detect_magnetic(
                    out_row["title"], out_row["description_raw"], out_row["product_function_primary"]
                )
                out_row["r71_is_magnetic"] = r71_is_magnetic
                out_row["r71_magnetic_signal"] = r71_signal
                out_row["r71_confidence"] = r71_conf
                out_row["r71_reason"] = r71_reason

                for k in OUT_HEADER:
                    if k not in out_row or out_row[k] is None:
                        out_row[k] = ""

                writer.writerow(out_row)
                n_out += 1

        write_log_row(log_path, supplier, "INFO", f"R71 OK. in={n_in} out={n_out} enriched={n_enriched} input_r70b={r70b_path} input_r70a={r70a_path} output={out_path}")
        print(f"✅ R71 OK — supplier={supplier} | in={n_in} out={n_out} enriched={n_enriched}")
        print(f"   📥 R70B: {r70b_path}")
        print(f"   ➕ R70A: {r70a_path}")
        print(f"   📤 Out: {out_path}")
        print(f"   📝 Log: {log_path}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
