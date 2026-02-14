#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
R70-B — Product Function Classifier (canoniek)
Doel: uitsluitend vaststellen wat een product functioneel IS.
GEEN magnetisch oordeel, GEEN Shopify-kennis, GEEN propositie-fit.

Input:
  Data/Exports/R70A/<RUN>/<Supplier>/R70A_RAW_PRODUCTS.csv

Output:
  Data/Exports/R70B/<RUN>/<Supplier>/R70B_FUNCTION_CLASSIFIED.csv
"""

import argparse
import csv
from pathlib import Path
from typing import Dict, Tuple, Optional, List

OUT_HEADER = [
    "sku",
    "ean",
    "title",
    "vendor",
    "supplier_category",
    "product_url",
    "product_function_primary",
    "product_function_secondary",
    "function_confidence",
    "function_reason",
]

SUPPLIERS = ("BigBuy", "Eprolo")


# ---------------------------
# Helpers
# ---------------------------

def _norm(s: str) -> str:
    return (s or "").strip()

def _lc(s: str) -> str:
    return _norm(s).lower()

def _join_text(title: str, desc: str, cat: str) -> str:
    return " ".join([_norm(title), _norm(desc), _norm(cat)]).strip()

def _contains_any(text: str, words: List[str]) -> bool:
    t = _lc(text)
    return any(w in t for w in words)


def detect_suppliers_from_r70a(r70a_run_dir: Path):
    found = []
    for name in SUPPLIERS:
        p = r70a_run_dir / name / "R70A_RAW_PRODUCTS.csv"
        if p.exists():
            found.append(name)
    return found


def is_garbage_row(row: Dict[str, str]) -> bool:
    """
    Filter voor rotregels / malformed regels:
    - lege regels
    - dubbele headerregels
    - regels die starten met CSV / FILE / SOURCE
    """
    if row is None or not isinstance(row, dict):
        return True

    sku = _norm(row.get("sku", ""))
    ean = _norm(row.get("ean", ""))
    title = _norm(row.get("title", ""))
    vendor = _norm(row.get("vendor", ""))
    cat = _norm(row.get("supplier_category", ""))

    # Leeg
    if not any([sku, ean, title, vendor, cat]):
        return True

    # Header herhaling
    if sku.lower() == "sku" and ean.lower() == "ean":
        return True

    # Rotregel indicatoren
    if sku.upper() in ("CSV", "CSVFILE", "FILE", "SOURCE"):
        return True
    if title.upper() in ("CSV", "FILE", "SOURCE"):
        return True

    return False


# ---------------------------
# R70B classification logic
# ---------------------------
# NB: R70B bepaalt alleen WAT het product is, geen magnetisch oordeel.


# Primary devices / hard exclusion families (as function type)
PHONE_WORDS = [
    "iphone", "smartphone", "mobile phone", "gsm", "telefoon", "phone",
    "android phone", "samsung galaxy", "pixel phone"
]
AUDIO_WORDS = [
    "earbuds", "oordop", "oortjes", "headphone", "headphones", "headset",
    "speaker", "bluetooth speaker", "airpods"
]
STORAGE_WORDS = [
    "ssd", "hdd", "hard drive", "external drive", "usb drive", "flash drive",
    "memory stick", "opslag", "extern geheugen", "nvme"
]
BAG_WORDS = [
    "wallet", "portemonnee", "pouch", "etui", "case wallet", "sleeve",
    "tas", "bag", "backpack", "handbag", "purse", "wallet case"
]

# Core families (reduce UNKNOWN)
REPLACEMENT = [
    "replacement", "spare", "spare part", "reserve", "repair", "service kit", "parts",
    "onderdeel", "reserveonderdeel", "reparatie", "battery kit", "replacement battery",
    "repair kit", "spare battery"
]

FURNITURE = [
    "tafel", "table", "kast", "cabinet", "shelf", "plank", "rek", "rack",
    "stoel", "chair", "bed", "nightstand", "nachtkast", "bureau",
    "desk", "drawer", "lade"
]

DECOR = [
    "decor", "decoration", "wall art", "poster", "canvas",
    "frame", "fotolijst", "picture frame", "wall clock", "klok",
    "sign", "bord", "ornament"
]

TEXTILE = [
    "textile", "cotton", "katoen", "blanket", "deken",
    "cushion", "kussen", "cover", "hoes", "sheet",
    "laken", "towel", "handdoek", "curtain", "gordijn"
]

BEAUTY = [
    "beauty", "skin", "skincare", "hair", "haar",
    "nail", "nagel", "massage", "groom", "trimmer",
    "shaver", "epilator", "facial", "make-up", "makeup"
]

PET = [
    "pet", "dog", "cat", "puppy", "kitten", "leash",
    "riem", "bowl", "voerbak", "scratching", "krab", "grooming"
]

TOY = [
    "toy", "toys", "puzzle", "game", "board game",
    "lego", "figure", "doll", "rc", "remote control",
    "speelgoed", "spel"
]

GENERIC_ACCESSORY = [
    "accessory", "accessories", "kit", "set", "bundle", "pack",
    "assortment", "adapter set"
]

# Specific ecom tech families (function only)
CHARGER_WORDS = [
    "oplader", "charger", "charging", "snellader",
    "wireless charger", "draadloos opladen", "qi charger",
    "charge stand", "dock", "charging dock"
]
POWERBANK_WORDS = [
    "powerbank", "portable charger", "battery pack", "external battery", "power bank"
]
CABLE_WORDS = [
    "kabel", "cable", "usb-c", "usb c", "lightning cable", "type-c",
    "charger cable", "charging cable"
]
MOUNT_WORDS = [
    "houder", "mount", "car mount", "dashboard mount", "vent mount",
    "phone holder", "telefoonhouder", "stand", "holder"
]

# Signals that increase confidence (function-only; not a magnet judgement)
QI_SIGNALS = ["qi", "qi2", "magsafe", "mag-safe"]


def classify_family(title: str, desc: str, category: str) -> Optional[Tuple[str, str, str, str]]:
    txt = _join_text(title, desc, category).lower()

    # Primary device families (as function types)
    if _contains_any(txt, PHONE_WORDS):
        return ("phone", "", "HIGH", "Primary device keywords: phone/smartphone/iphone")
    if _contains_any(txt, AUDIO_WORDS):
        return ("audio_device", "", "HIGH", "Primary device keywords: audio/earbuds/headphones/speaker")
    if _contains_any(txt, STORAGE_WORDS):
        return ("storage_device", "", "HIGH", "Storage device keywords: SSD/HDD/USB drive")
    if _contains_any(txt, BAG_WORDS):
        return ("bag_or_wallet", "", "MEDIUM", "Bag/wallet keywords")

    # Replacement / parts
    if _contains_any(txt, REPLACEMENT):
        return ("replacement_part", "", "MEDIUM", "Replacement/Spare/Repair keywords")

    # Home/lifestyle buckets
    if _contains_any(txt, FURNITURE):
        return ("home_furniture", "", "LOW", "Furniture keywords")
    if _contains_any(txt, DECOR):
        return ("decor", "", "LOW", "Decor keywords")
    if _contains_any(txt, TEXTILE):
        return ("textile", "", "LOW", "Textile keywords")
    if _contains_any(txt, PET):
        return ("pet_product", "", "LOW", "Pet keywords")
    if _contains_any(txt, TOY):
        return ("toy", "", "LOW", "Toy/Game keywords")
    if _contains_any(txt, BEAUTY):
        return ("beauty_product", "", "LOW", "Beauty/Wellness keywords")

    # Generic kit/set/accessories
    if _contains_any(txt, GENERIC_ACCESSORY):
        return ("generic_accessory", "", "LOW", "Generic accessory/kit keywords")

    return None


def classify_core(title: str, desc: str, category: str) -> Tuple[str, str, str, str]:
    """
    Core function classification (tech-first).
    Belangrijk: Powerbanks MUST vóór chargers om MagSafe/Qi2 niet fout als 'charger' te pakken.
    """
    txt = _join_text(title, desc, category).lower()

    # --- POWERBANKS FIRST ---
    if _contains_any(txt, POWERBANK_WORDS) or "mah" in txt:
        conf = "HIGH"
        reason = "Powerbank keywords or mAh capacity detected"
        if _contains_any(txt, QI_SIGNALS):
            reason = "Powerbank + Qi/Qi2/MagSafe keyword (function confidence)"
        return ("powerbank", "", conf, reason)

    # Chargers
    if _contains_any(txt, CHARGER_WORDS):
        secondary = ""
        conf = "MEDIUM"
        reason = "Charger keywords"

        if _contains_any(txt, ["stand", "dock", "houder", "station"]):
            secondary = "stand"
            reason = "Charger + stand/dock keywords"

        if _contains_any(txt, QI_SIGNALS):
            conf = "HIGH"
            reason = "Charger + Qi/Qi2/MagSafe keyword (function confidence)"

        return ("charger", secondary, conf, reason)

    # Cables
    if _contains_any(txt, CABLE_WORDS):
        return ("cable", "", "MEDIUM", "Keywords: kabel/cable/usb-c")

    # Mounts / holders / stands (non-charging)
    if _contains_any(txt, MOUNT_WORDS):
        return ("mount", "", "MEDIUM", "Keywords: houder/mount/stand")

    # Broad families (reduces unknown)
    fam = classify_family(title, desc, category)
    if fam:
        return fam

    return ("unknown", "", "LOW", "No strong keywords found (v2.2)")


# ---------------------------
# IO / Runner
# ---------------------------

def run_single_input(input_csv: Path, output_csv: Path) -> Tuple[int, int]:
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    rows_in = 0
    rows_out = 0

    with input_csv.open("r", newline="", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)
        with output_csv.open("w", newline="", encoding="utf-8") as f_out:
            writer = csv.DictWriter(f_out, fieldnames=OUT_HEADER)
            writer.writeheader()

            for row in reader:
                if is_garbage_row(row):
                    continue

                rows_in += 1

                sku = _norm(row.get("sku", ""))
                ean = _norm(row.get("ean", ""))
                title = _norm(row.get("title", ""))
                desc = _norm(row.get("description_raw", ""))
                vendor = _norm(row.get("vendor", "")) or "UNKNOWN_VENDOR"
                cat = _norm(row.get("supplier_category", ""))
                url = _norm(row.get("product_url", ""))

                pf1, pf2, conf, reason = classify_core(title, desc, cat)

                out_row = {
                    "sku": sku,
                    "ean": ean,
                    "title": title,
                    "vendor": vendor,
                    "supplier_category": cat,
                    "product_url": url,
                    "product_function_primary": pf1,
                    "product_function_secondary": pf2,
                    "function_confidence": conf,
                    "function_reason": reason,
                }
                writer.writerow(out_row)
                rows_out += 1

    return rows_in, rows_out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", help="Run folder name under Data/Exports/R70A/<RUN>/...", default=None)
    ap.add_argument("--supplier", help="Optional: only run 1 supplier (BigBuy or Eprolo)", default=None)
    ap.add_argument("--in", dest="input_csv", help="Direct input CSV (overrides --run)", default=None)
    ap.add_argument("--out", dest="output_csv", help="Direct output CSV (overrides --run)", default=None)

    args = ap.parse_args()

    # Direct mode
    if args.input_csv and args.output_csv:
        in_path = Path(args.input_csv)
        out_path = Path(args.output_csv)
        rows_in, rows_out = run_single_input(in_path, out_path)
        print("✅ R70-B direct OK")
        print(f"   📥 In:  {in_path} (rows={rows_in})")
        print(f"   📤 Out: {out_path} (rows={rows_out})")
        return 0

    # Run-based mode
    if not args.run:
        print("❌ Geef --run <RUN_TS> of gebruik --in/--out direct mode.")
        return 2

    run = args.run
    r70a_run_dir = Path("Data/Exports/R70A") / run
    r70b_run_dir = Path("Data/Exports/R70B") / run

    if not r70a_run_dir.exists():
        print(f"❌ R70A run folder niet gevonden: {r70a_run_dir}")
        return 2

    suppliers = detect_suppliers_from_r70a(r70a_run_dir)
    if args.supplier:
        suppliers = [s for s in suppliers if s.lower() == args.supplier.lower()]

    if not suppliers:
        print(f"❌ Geen suppliers met R70A input gevonden onder: {r70a_run_dir}")
        return 2

    for supplier in suppliers:
        in_csv = r70a_run_dir / supplier / "R70A_RAW_PRODUCTS.csv"
        out_csv = r70b_run_dir / supplier / "R70B_FUNCTION_CLASSIFIED.csv"

        if not in_csv.exists():
            print(f"⚠️ Skip {supplier}: input ontbreekt: {in_csv}")
            continue

        rows_in, rows_out = run_single_input(in_csv, out_csv)

        print(f"✅ R70-B v2.2 OK — supplier={supplier} | in={rows_in} out={rows_out}")
        print(f"   📥 In:  {in_csv}")
        print(f"   📤 Out: {out_csv}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

