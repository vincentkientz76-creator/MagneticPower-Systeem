#!/usr/bin/env python3
from pathlib import Path
import argparse, glob, os, shutil, sys

def newest_dir(pattern: str) -> Path:
    dirs=[Path(d) for d in glob.glob(pattern) if os.path.isdir(d)]
    if not dirs:
        raise SystemExit("No dirs found for pattern: " + pattern)
    return sorted(dirs, key=lambda p: p.stat().st_mtime)[-1]

def copy_if_exists(src: Path, dst: Path) -> bool:
    if not src.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="Data/Exports/R70A", help="Base folder containing timestamped runs")
    ap.add_argument("--run-id", default="", help="Specific run folder name, e.g. 2026-02-13_18-55-54")
    args = ap.parse_args()

    base = Path(args.base)
    if args.run_id:
        latest_run = base / args.run_id
        if not latest_run.exists():
            raise SystemExit(f"Run not found: {latest_run}")
    else:
        latest_run = newest_dir(str(base / "20*-*-*_*-*-*"))

    src_bigbuy = latest_run / "BigBuy" / "R70A_RAW_PRODUCTS.csv"
    src_eprolo = latest_run / "Eprolo" / "R70A_RAW_PRODUCTS.csv"

    dst_base = base / "LATEST"
    wrote = []

    if copy_if_exists(src_bigbuy, dst_base / "BigBuy" / "R70A_RAW_PRODUCTS.csv"):
        wrote.append(str(dst_base / "BigBuy" / "R70A_RAW_PRODUCTS.csv"))
    if copy_if_exists(src_eprolo, dst_base / "Eprolo" / "R70A_RAW_PRODUCTS.csv"):
        wrote.append(str(dst_base / "Eprolo" / "R70A_RAW_PRODUCTS.csv"))

    if not wrote:
        raise SystemExit("Nothing copied. Missing expected source files in: " + str(latest_run))

    print("✅ R70A LATEST updated")
    print("LATEST_RUN:", latest_run)
    for p in wrote:
        print("WROTE:", p)

if __name__ == "__main__":
    main()
