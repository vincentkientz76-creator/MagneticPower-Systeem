import math
from typing import Optional

def calculate_min_safe_price(cost: Optional[float], target_margin: float = 0.45) -> Optional[float]:
    if cost is None or (isinstance(cost, float) and math.isnan(cost)) or cost <= 0:
        return None
    denom = 1.0 - float(target_margin)
    if denom <= 0:
        return None
    return cost / denom

def price_positioning_score(avg_price: Optional[float], min_safe_price: Optional[float]) -> float:
    if avg_price is None or min_safe_price is None or avg_price <= 0:
        return 0.0
    raw = (avg_price - min_safe_price) / avg_price
    if raw < 0:
        return 0.0
    if raw > 1:
        return 1.0
    return float(raw)
