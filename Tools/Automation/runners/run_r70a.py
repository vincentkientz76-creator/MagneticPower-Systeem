#!/usr/bin/env python3
import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path

RAW_HEADER = [
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
        w.writerow([utc_now_iso(), "R70A", level, supplier, message])


def sniff_delimiter(csv_path: Path) -> str:
    try:
        sample = csv_path.read_text(encoding="utf-8", errors="replace")[:8192]
    except Exception:
        sample = ""
    semi = sample.count(";")
    comma = sample.count(",")
    if semi > comma:
        return ";"
    if comma > semi:
        return ","
    return ";"


def strip_bom(s: str) -> str:
    return s.lstrip("\ufeff").strip() if isinstance(s, str) else s


def build_video_url(video_raw: str) -> str:
    v = (video_raw or "").strip()
    if not v or v == "0":
        return ""
    if v.startswith("http://") or v.startswith("https://"):
        return v
    return f"https://www.youtube.com/watch?v={v}"


def normalize_row(row: dict, supplier_default: str):
    row = {strip_bom(k): v for k, v in (row or {}).items()}

    def get(*keys, default=""):
        for k in keys:
            k = strip_bom(k)
            if k in row and row[k] is not None:
                return str(row[k]).strip()
        return default

    sku = get("sku", "SKU", "ID")
    ean = get("ean", "EAN", "EAN13", "GTIN", "BARCODE")
    title = get("title", "name", "Title", "NAME")
    description_raw = get("description_raw", "description", "Description", "DESCRIPTION")
    vendor = get("vendor", "brand", "Vendor", "BRAND", default=supplier_default)
    supplier_category = get("supplier_category", "category", "Category", "CATEGORY")
    product_url = get("product_url", "url", "productUrl")

    image_urls = get("image_urls", "images", "imageUrls")
    if not image_urls:
        imgs = []
        for i in range(1, 9):
            v = get(f"IMAGE{i}")
            if v:
                imgs.append(v)
        if imgs:
            image_urls = "|".join(imgs)

    weight = get("weight", "Weight", "WEIGHT")

    video_raw = get("video_url", "video", "VIDEO")
    video_url = build_video_url(video_raw)

    return {
        "sku": sku,
        "ean": ean,
        "title": title,
        "description_raw": description_raw,
        "vendor": vendor,
        "supplier_category": supplier_category,
        "product_url": product_url,
        "image_urls": image_urls,
        "weight": weight,
        "video_url": video_url,
    }


def iter_csv_files(supplier_dir: Path, supplier: str):
    for p in supplier_dir.rglob("*.csv"):
        name = p.name.lower()
        if name in ("readme.csv",) or "readme" in name:
            continue
        if supplier.lower() == "bigbuy":
            if name.startswith("categories-") or name.startswith("manufacturer-") or name == "category-map.csv":
                continue
        yield p


def parse_csv_files(supplier: str, supplier_dir: Path, raw_out: Path, log_out: Path):
    raw_out.parent.mkdir(parents=True, exist_ok=True)

    total_files = 0
    total_rows = 0
    skipped_garbage = 0

    with raw_out.open("w", newline="", encoding="utf-8") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=RAW_HEADER)
        writer.writeheader()

        for csv_path in iter_csv_files(supplier_dir, supplier=supplier):
            total_files += 1
            file_rows = 0
            delim = sniff_delimiter(csv_path)

            def process_reader(reader):
                nonlocal file_rows, total_rows, skipped_garbage
                if reader.fieldnames:
                    reader.fieldnames = [strip_bom(fn) for fn in reader.fieldnames]

                for row in reader:
                    if not row:
                        skipped_garbage += 1
                        continue

                    row = {strip_bom(k): v for k, v in row.items()}
                    norm = normalize_row(row, supplier_default=supplier)
                    norm = {k: ("" if v is None else str(v).strip()) for k, v in norm.items()}

                    if not any(v != "" for v in norm.values()):
                        skipped_garbage += 1
                        continue

                    sku = norm.get("sku", "")
                    ean = norm.get("ean", "")
                    title = norm.get("title", "")
                    if sku == "" and ean == "" and title == "":
                        skipped_garbage += 1
                        continue

                    if sku.upper() in {"CSV", "EOF"} or title.upper() in {"CSV", "EOF"}:
                        skipped_garbage += 1
                        write_log_row(log_out, supplier, "WARN", f"Skipped garbage token row in {csv_path}")
                        continue

                    non_empty_fields = [k for k, v in norm.items() if v != ""]
                    if len(non_empty_fields) <= 1:
                        skipped_garbage += 1
                        write_log_row(log_out, supplier, "WARN", f"Skipped sparse row in {csv_path}: non_empty={non_empty_fields}")
                        continue

                    writer.writerow(norm)
                    file_rows += 1
                    total_rows += 1

            try:
                with csv_path.open("r", newline="", encoding="utf-8") as f_in:
                    reader = csv.DictReader(f_in, delimiter=delim)
                    process_reader(reader)
                write_log_row(log_out, supplier, "INFO", f"Parsed CSV: {csv_path} | delim={delim} | rows={file_rows}")
            except UnicodeDecodeError:
                with csv_path.open("r", newline="", encoding="latin-1") as f_in:
                    reader = csv.DictReader(f_in, delimiter=delim)
                    process_reader(reader)
                write_log_row(log_out, supplier, "WARN", f"Parsed CSV with latin-1 fallback: {csv_path} | delim={delim} | rows={file_rows}")

    write_log_row(
        log_out,
        supplier,
        "INFO",
        f"v6 OK. Supplier map: {supplier_dir} | files={total_files} | rows={total_rows} | skipped_garbage={skipped_garbage}",
    )


def detect_suppliers(input_root: Path):
    candidates = []
    for name in ("BigBuy", "Eprolo"):
        p = input_root / name
        if p.exists() and p.is_dir():
            candidates.append((name, p))
    return candidates


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Input root folder (e.g. Data)")
    ap.add_argument("--outdir", required=True, help="Output root folder (e.g. Data/Exports/R70A/<RUN_TS>)")
    args = ap.parse_args()

    input_root = Path(args.input)
    out_root = Path(args.outdir)

    suppliers = detect_suppliers(input_root)
    if not suppliers:
        print("❌ Geen suppliers gevonden. Verwacht mappen: Data/BigBuy en/of Data/Eprolo")
        return 2

    for supplier, supplier_dir in suppliers:
        raw_out = out_root / supplier / "R70A_RAW_PRODUCTS.csv"
        log_out = out_root / supplier / "R70A_EXTRACT_LOG.csv"

        parse_csv_files(supplier, supplier_dir, raw_out, log_out)

        csv_count = sum(1 for _ in supplier_dir.rglob("*.csv"))
        xml_count = sum(1 for _ in supplier_dir.rglob("*.xml"))
        zip_count = sum(1 for _ in supplier_dir.rglob("*.zip"))

        print(f"✅ R70-A v6 OK — supplier={supplier} | csv={csv_count} xml={xml_count} zip={zip_count}")
        print(f"   📦 RAW: {raw_out}")
        print(f"   📝 LOG: {log_out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
