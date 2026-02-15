#!/usr/bin/env bash
set -euo pipefail

# Canonieke full pipeline runner (R70A → R75)
# Gebruik: Tools/Automation/runners/mp_run_full_pipeline.sh 2026-02
# Vereist: run_r70a_latest.py, run_r70b.py, run_r71.py, run_r72.py, run_r73.py, run_r74.py, run_r75.py

RUN_MONTH="${1:-2026-02}"
export MP_R70A_RUN="${MP_R70A_RUN:-LATEST}"

echo "🚀 Start full pipeline R70A → R75 | RUN_MONTH=$RUN_MONTH | R70A_SOURCE=$MP_R70A_RUN"

python3 Tools/Automation/runners/run_r70a_latest.py
python3 -m Tools.Automation.runners.run_r70b --run "$RUN_MONTH"
python3 -m Tools.Automation.runners.run_r71  --run "$RUN_MONTH"
python3 -m Tools.Automation.runners.run_r72  --run-month "$RUN_MONTH"

# R73 (propositie-fit) — verwacht dat run_r73.py zelf zijn input/output pakt conform repo-governance
python3 -m Tools.Automation.runners.run_r73 --run "$RUN_MONTH" || python3 Tools/Automation/runners/run_r73.py

# R74 (specialist intelligence) — placeholder call (moet bestaan/kloppen in repo)
python3 -m Tools.Automation.runners.run_r74 --run-month "$RUN_MONTH" || python3 Tools/Automation/runners/run_r74.py --run-month "$RUN_MONTH"

# R75 (market viability / DataForSEO) — placeholder call (moet bestaan/kloppen in repo)
python3 -m Tools.Automation.runners.run_r75 --run-month "$RUN_MONTH" || python3 Tools/Automation/runners/run_r75.py --run-month "$RUN_MONTH"

echo "✅ Full pipeline R70A → R75 completed"
