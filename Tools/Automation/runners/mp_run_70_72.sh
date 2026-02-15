#!/usr/bin/env bash
set -euo pipefail

# Canonieke R70A → R72 runner
# Gebruik: Tools/Automation/runners/mp_run_70_72.sh 2026-02

RUN_MONTH="${1:-2026-02}"
export MP_R70A_RUN="${MP_R70A_RUN:-LATEST}"

echo "🚀 Start pipeline R70A → R72 | RUN_MONTH=$RUN_MONTH | R70A_SOURCE=$MP_R70A_RUN"

python3 Tools/Automation/runners/run_r70a_latest.py
python3 -m Tools.Automation.runners.run_r70b --run "$RUN_MONTH"
python3 -m Tools.Automation.runners.run_r71  --run "$RUN_MONTH"
python3 -m Tools.Automation.runners.run_r72  --run-month "$RUN_MONTH"

echo "✅ Pipeline R70A → R72 completed"
