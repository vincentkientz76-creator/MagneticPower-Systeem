from pathlib import Path
import os
from typing import Optional

def get_r70a_dir(r70a_run: Optional[str]) -> Path:
    r = (r70a_run or os.environ.get("MP_R70A_RUN") or "LATEST").strip()
    if r.upper() == "LATEST":
        return Path("Data/Exports/R70A/LATEST")
    return Path("Data/Exports/R70A") / r
