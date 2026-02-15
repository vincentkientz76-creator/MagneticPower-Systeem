#!/usr/bin/env python3

import os
import csv
import re
from datetime import datetime
from typing import Dict, Tuple, List

INPUT_FILE = "Data/Exports/R72/2026-02/R72_NEW_ONLY.csv"
EXPORT_ROOT = "Data/Exports/R73"

# --- Hard exclusions (governance v3.2) ---
PRIMARY_DEVICE_PATTERNS = [
    r"\bsmartphone\b", r"\bmobile phone\b", r"\bcell phone\b", r"\bphone\b", r"\btelefoon\b"
]
AUDIO_DEVICE_PATTERNS = [
    r"\bearbuds?\b", r"\bheadphones?\b", r"\bheadset\b", r"\bspeaker\b", r"\boordop(jes)?\b", r"\bkoptelefoon\b"
]
STORAGE_DEVICE_PATTERNS = [
    r"\bhdd\b", r"\bssd\b", r"\bexternal drive\b", r"\bflash drive\b", r"\busb stick\b", r"\busb drive\b",
    r"\bportable ssd\b", r"\bportable hdd\b", r"\bgeheugenstick\b", r"\bflashdisk\b"
]
BAG_PATTERNS = [
    r"\bwallet\b", r"\bpouch\b", r"\bsleeve\b", r"\bbag\b", r"\bcase\b", r"\betui\b", r"\btas\b", r"\bportemonnee\b"
]
COSMETIC_MARKETING_PATTERNS = [
    r"\bnail\b", r"\bnagel\b", r"\bpolish\b", r"\bnagellak\b", r"\bhair\b", r"\bhaar\b", r"\bshampoo\b",
    r"\bcosmetic\b", r"\bmake-?up\b"
]
APPLIANCE_PATTERNS = [
    r"\bvacc?uum\b", r"\bblender\b", r"\bmixer\b", r"\bmicrowave\b", r"\bmagnetron\b", r"\bprinter\b",
    r"\bcoffee\b", r"\bespresso\b"
]

# Allow signals (for confidence only; R71 is magnet-truth)
MAGNET_SIGNALS = [
    r"\bmagnetic\b", r"\bmagnetisch\b", r"\bmagneet\b", r"\bmagsafe\b", r"\bqi2\b", r"\bneodym(ium)?\b", r"\bmagnet\b"
]

def _norm(s: str) -> str:
    return (s or "").strip().lower()

def _has_any(text: str, patterns: List[str]) -> bool:
    t = _norm(text)
    return any(re.search(p, t, flags=re.IGNORECASE) for p in patterns)

def classify_usage_and_collection(title: str, collections: str) -> Tuple[str, str]:
    t = _norm(title)
    c = _norm(collections)

    # charging
    if any(k in t for k in ["charger", "oplaad", "oplader", "qi", "qi2", "wireless charging", "magsafe"]) or "oplad" in c:
        return "charging", "opladers_powerbanks"
    # car / onderweg
    if any(k in t for k in ["car", "auto", "dashboard", "vent", "mount", "houder"]) or "auto" in c:
        return "consumer_daily", "magnetische_autohouders"
    # desk / work
    if any(k in t for k in ["desk", "bureau", "stand", "houder", "organizer", "whiteboard", "board", "holder"]) or "werk" in c:
        return "business_daily", "werkplek_thuis_accessoires"
    # default daily
    return "consumer_daily", "magnetische_accessoires"

def decide(row: Dict[str, str]) -> Dict[str, str]:
    title = row.get("title", "")
    vendor = row.get("vendor", "")
    collections = row.get("collections", "")

    exclusion_reason = ""
    fit = "YES"

    # Hard exclusions
    if _has_any(title, PRIMARY_DEVICE_PATTERNS):
        fit = "NO"
        exclusion_reason = "PRIMARY_DEVICE_NOT_MAGNETIC_FUNCTION"
    elif _has_any(title, AUDIO_DEVICE_PATTERNS):
        fit = "NO"
        exclusion_reason = "PRIMARY_DEVICE_NOT_MAGNETIC_FUNCTION"
    elif _has_any(title, STORAGE_DEVICE_PATTERNS):
        fit = "NO"
        exclusion_reason = "STORAGE_DEVICE_NOT_MAGNETIC_FUNCTION"
    elif _has_any(title, BAG_PATTERNS) and _has_any(title, [r"\bmagnet\b", r"\bmagnetic\b", r"\bmagnetisch\b", r"\bmagneet\b"]):
        fit = "NO"
        exclusion_reason = "BAG_WITH_MAGNETIC_CLOSURE_NOT_MAGNETIC_FUNCTION"
    elif _has_any(title, COSMETIC_MARKETING_PATTERNS) and _has_any(title, [r"\bmagnet\b", r"\bmagnetic\b", r"\bmagnetisch\b"]):
        fit = "NO"
        exclusion_reason = "COSMETIC_MARKETING_MAGNET"
    elif _has_any(title, APPLIANCE_PATTERNS):
        fit = "NO"
        exclusion_reason = "APPLIANCE_NOT_MAGNETIC_PRODUCT"

    usage_context, collection_candidate = ("", "")
    if fit == "YES":
        usage_context, collection_candidate = classify_usage_and_collection(title, collections)

    # Confidence (simple heuristic)
    conf = "LOW"
    if fit == "NO":
        conf = "HIGH"
    else:
        if _has_any(title, MAGNET_SIGNALS) or _norm(collections) != "":
            conf = "MEDIUM"
        if _has_any(title, [r"\bmagsafe\b", r"\bqi2\b", r"\bmagnetic\b", r"\bmagnetisch\b"]):
            conf = "HIGH"

    out = dict(row)
    out["r73_proposition_fit"] = fit
    out["r73_usage_context"] = usage_context
    out["r73_collection_candidate"] = collection_candidate
    out["r73_exclusion_reason"] = exclusion_reason
    out["r73_confidence"] = conf
    return out

def ensure_export_path():
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    export_path = os.path.join(EXPORT_ROOT, now)
    os.makedirs(export_path, exist_ok=True)
    return export_path

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Input file not found: {INPUT_FILE}")
        return

    export_path = ensure_export_path()

    allowed_file = os.path.join(export_path, "R73_ALLOWED.csv")
    excluded_file = os.path.join(export_path, "R73_EXCLUDED.csv")
    log_file = os.path.join(export_path, "R73_LOG.csv")

    with open(INPUT_FILE, newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        base_fields = reader.fieldnames or []
        extra_fields = [
            "r73_proposition_fit",
            "r73_usage_context",
            "r73_collection_candidate",
            "r73_exclusion_reason",
            "r73_confidence"
        ]
        fieldnames = base_fields + extra_fields

        counts = {"YES": 0, "NO": 0}

        with open(allowed_file, "w", newline="", encoding="utf-8") as aout, \
             open(excluded_file, "w", newline="", encoding="utf-8") as xout:

            aw = csv.DictWriter(aout, fieldnames=fieldnames)
            xw = csv.DictWriter(xout, fieldnames=fieldnames)
            aw.writeheader()
            xw.writeheader()

            for row in reader:
                out = decide(row)
                if out["r73_proposition_fit"] == "YES":
                    counts["YES"] += 1
                    aw.writerow(out)
                else:
                    counts["NO"] += 1
                    xw.writerow(out)

    with open(log_file, "w", newline="", encoding="utf-8") as lf:
        w = csv.writer(lf)
        w.writerow(["metric", "value"])
        w.writerow(["input_file", INPUT_FILE])
        w.writerow(["allowed_yes", counts["YES"]])
        w.writerow(["excluded_no", counts["NO"]])

    print(f"✅ R73 completed | YES={counts['YES']} NO={counts['NO']} | out={export_path}")

if __name__ == "__main__":
    main()
