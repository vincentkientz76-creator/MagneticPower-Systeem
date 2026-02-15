#!/usr/bin/env python3

import os
import csv
from datetime import datetime

EXPORT_ROOT = "Data/Exports/R75"

def ensure_export_path():
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    export_path = os.path.join(EXPORT_ROOT, now)
    os.makedirs(export_path, exist_ok=True)
    return export_path

def write_dummy_output(export_path):
    output_file = os.path.join(export_path, "R75_MARKETDATA.csv")

    header = [
        "sku",
        "ean",
        "title",
        "market_nl_low_price",
        "market_nl_avg_price",
        "market_nl_high_price",
        "market_competitor_count_nl",
        "competition_density",
        "r75_candidate_urls"
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)

    print(f"✅ R75 export created at: {output_file}")

def main():
    export_path = ensure_export_path()
    write_dummy_output(export_path)

if __name__ == "__main__":
    main()
