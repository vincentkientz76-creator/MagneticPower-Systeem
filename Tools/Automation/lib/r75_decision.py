from typing import Optional, Tuple

def _to_int(x: str) -> int:
    try:
        return int(str(x).strip())
    except Exception:
        return 0

def market_confidence(avg_price: Optional[float], has_bb_match: bool) -> str:
    if avg_price is None:
        return "LOW"
    return "MEDIUM" if has_bb_match else "LOW"

def decide(
    competitor_count: int,
    avg_price: Optional[float],
    min_safe_price: Optional[float],
    confidence: str,
    high_competition_drop: int = 50,
    keep_competition_max: int = 20,
) -> Tuple[str, str]:
    if competitor_count >= high_competition_drop:
        return "DROP", "EXTREME_COMPETITION"

    if confidence == "LOW":
        return "REVIEW", "LOW_CONFIDENCE_OR_MISSING_MARKETDATA"

    if competitor_count > keep_competition_max:
        return "REVIEW", "HIGH_COMPETITION"

    if avg_price is not None and min_safe_price is not None and avg_price < min_safe_price:
        return "DROP", "MARKET_BELOW_MARGIN_SAFE_PRICE"

    return "KEEP", "MEETS_THRESHOLDS"
