#!/usr/bin/env bash
set -euo pipefail

RUN_MONTH="${1:-2026-02}"
export MP_R70A_RUN="${MP_R70A_RUN:-LATEST}"

python3 Tools/Automation/runners/run_r70a_latest.py
python3 -m Tools.Automation.runners.run_r70b --run "$RUN_MONTH"
python3 -m Tools.Automation.runners.run_r71  --run "$RUN_MONTH"
python3 -m Tools.Automation.runners.run_r72  --run "$RUN_MONTH"
