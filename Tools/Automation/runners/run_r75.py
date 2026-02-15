import argparse
import csv
import os
from typing import Optional

from Tools.Automation.lib.r75_core import (
    load_r74_ready,
    load_bigbuy_manual,
    merge_r74_with_manual,
    extract_bb_fields,
    extract_market_fields,
    extract_competition_fields,
    extract_supplier_cost,
)
from Tools.Automation.lib.r75_pricing import calculate_min_safe_price, price_positioning_score
from Tools.Automation.lib.r75_decision import market_confidence, decide, _to_int
from Tools.Automation.lib.r75_logging import R75Logger

def _fmt_float(x: Optional[float]) -> str:
    if x is None:
        return ""
    return f"{x:.2f}"

R75_MARKETDATA_FIELDS = [
    "sku","ean","title",
    "r75_market_low_price","r75_market_avg_price","r75_market_high_price",
    "r75_competitor_count","r75_market_confidence",
    "r75_margin_safe_price","r75_price_positioning_score",
    "r75_decision","r75_reason",
]

R75_QA_VIEW_FIELDS = [
    "sku","ean","title",
    "brand","bigbuy_id",
    "bigbuy_product_url",
    "bigbuy_image_url_1","bigbuy_image_url_2","bigbuy_image_url_3",
    "r75_manual_match_type",
    "r75_market_query_used",
    "r75_market_source",
    "market_nl_low_price","market_nl_avg_price","market_nl_high_price",
    "market_eu_low_price","market_eu_avg_price","market_eu_high_price",
    "market_competitor_count_nl","competition_density",
    "supplier_cost",
    "r75_margin_safe_price","r75_price_positioning_score",
    "r75_decision","r75_reason",
    "qa_bb_url_ok","qa_bb_images_ok","qa_internet_match_ok",
    "qa_notes","qa_checked_by","qa_checked_at",
]

def _market_query_used(ean: str, title: str) -> str:
    e = (ean or "").strip()
    t = (title or "").strip()
    if e:
        return f"EAN:{e}"
    return f"TITLE:{t[:80]}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True, help="YYYY-MM")
    args = ap.parse_args()
    run_month = args.run

    out_dir = f"Data/Exports/R75/{run_month}"
    os.makedirs(out_dir, exist_ok=True)

    out_market = f"{out_dir}/R75_MARKETDATA.csv"
    out_qa = f"{out_dir}/R75_QA_VIEW.csv"
    out_log = f"{out_dir}/R75_LOG.csv"
    out_dupes = f"{out_dir}/R75_R74_DUPLICATE_SKUS.csv"

    logger = R75Logger(out_log)

    r74_rows, dup_audit = load_r74_ready(run_month)
    manual_path, manual_rows = load_bigbuy_manual(run_month)
    merged_rows, stats = merge_r74_with_manual(r74_rows, manual_rows)

    if dup_audit:
        cols = sorted(set().union(*[set(r.keys()) for r in dup_audit]))
        with open(out_dupes, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(dup_audit)
        logger.log("DUPES", "WARN", "", f"exported={out_dupes} rows={len(dup_audit)}")

    logger.metrics["total_input"] = stats["total"]
    logger.log("LOAD", "INFO", "", f"run={run_month} r74_deduped={len(r74_rows)} dup_rows={len(dup_audit)} manual_file={manual_path} manual_rows={len(manual_rows)} matched_sku={stats['matched_sku']} matched_ean={stats['matched_ean']} unmatched={stats['unmatched']}")

    with open(out_market, "w", newline="", encoding="utf-8") as fm, open(out_qa, "w", newline="", encoding="utf-8") as fq:
        wm = csv.DictWriter(fm, fieldnames=R75_MARKETDATA_FIELDS)
        wq = csv.DictWriter(fq, fieldnames=R75_QA_VIEW_FIELDS)
        wm.writeheader()
        wq.writeheader()

        for row in merged_rows:
            sku = (row.get("sku","") or "").strip()
            ean = (row.get("ean","") or "").strip()
            title = (row.get("title","") or "").strip()

            try:
                bb = extract_bb_fields(row)
                market = extract_market_fields(row)
                comp = extract_competition_fields(row)
                cost = extract_supplier_cost(row)

                has_bb_match = (row.get("r75_manual_match_type","") or "") in ("SKU","EAN")
                if has_bb_match:
                    logger.metrics["matched_bb_manual"] += 1
                else:
                    logger.metrics["missing_bb_manual"] += 1

                competitor_count = _to_int(comp.get("market_competitor_count_nl",""))
                avg_nl = market.get("market_nl_avg_price")
                low_nl = market.get("market_nl_low_price")
                high_nl = market.get("market_nl_high_price")

                conf = market_confidence(avg_nl, has_bb_match)

                min_safe = calculate_min_safe_price(cost, target_margin=0.45)
                score = price_positioning_score(avg_nl, min_safe)

                decision, reason = decide(
                    competitor_count=competitor_count,
                    avg_price=avg_nl,
                    min_safe_price=min_safe,
                    confidence=conf,
                    high_competition_drop=50,
                    keep_competition_max=20,
                )

                if not has_bb_match:
                    decision = "REVIEW"
                    reason = "MISSING_BIGBUY_MANUAL_MATCH"

                if decision == "KEEP":
                    logger.metrics["keep_count"] += 1
                elif decision == "REVIEW":
                    logger.metrics["review_count"] += 1
                else:
                    logger.metrics["drop_count"] += 1

                wm.writerow({
                    "sku": sku,
                    "ean": ean,
                    "title": title,
                    "r75_market_low_price": _fmt_float(low_nl),
                    "r75_market_avg_price": _fmt_float(avg_nl),
                    "r75_market_high_price": _fmt_float(high_nl),
                    "r75_competitor_count": str(competitor_count),
                    "r75_market_confidence": conf,
                    "r75_margin_safe_price": _fmt_float(min_safe),
                    "r75_price_positioning_score": f"{score:.3f}",
                    "r75_decision": decision,
                    "r75_reason": reason,
                })

                wq.writerow({
                    "sku": sku,
                    "ean": ean,
                    "title": title,
                    "brand": bb.get("brand",""),
                    "bigbuy_id": bb.get("bigbuy_id",""),
                    "bigbuy_product_url": bb.get("bigbuy_product_url",""),
                    "bigbuy_image_url_1": bb.get("bigbuy_image_url_1",""),
                    "bigbuy_image_url_2": bb.get("bigbuy_image_url_2",""),
                    "bigbuy_image_url_3": bb.get("bigbuy_image_url_3",""),
                    "r75_manual_match_type": row.get("r75_manual_match_type",""),
                    "r75_market_query_used": _market_query_used(ean, title),
                    "r75_market_source": "MANUAL",
                    "market_nl_low_price": _fmt_float(market.get("market_nl_low_price")),
                    "market_nl_avg_price": _fmt_float(market.get("market_nl_avg_price")),
                    "market_nl_high_price": _fmt_float(market.get("market_nl_high_price")),
                    "market_eu_low_price": _fmt_float(market.get("market_eu_low_price")),
                    "market_eu_avg_price": _fmt_float(market.get("market_eu_avg_price")),
                    "market_eu_high_price": _fmt_float(market.get("market_eu_high_price")),
                    "market_competitor_count_nl": comp.get("market_competitor_count_nl",""),
                    "competition_density": comp.get("competition_density",""),
                    "supplier_cost": _fmt_float(cost),
                    "r75_margin_safe_price": _fmt_float(min_safe),
                    "r75_price_positioning_score": f"{score:.3f}",
                    "r75_decision": decision,
                    "r75_reason": reason,
                    "qa_bb_url_ok": "",
                    "qa_bb_images_ok": "",
                    "qa_internet_match_ok": "",
                    "qa_notes": "",
                    "qa_checked_by": "",
                    "qa_checked_at": "",
                })

            except Exception as ex:
                logger.metrics["errors"] += 1
                logger.log("ROW", "ERROR", sku, str(ex)[:2000])

                wm.writerow({
                    "sku": sku,
                    "ean": ean,
                    "title": title,
                    "r75_market_low_price": "",
                    "r75_market_avg_price": "",
                    "r75_market_high_price": "",
                    "r75_competitor_count": "0",
                    "r75_market_confidence": "LOW",
                    "r75_margin_safe_price": "",
                    "r75_price_positioning_score": "0.000",
                    "r75_decision": "REVIEW",
                    "r75_reason": "ERROR_PROCESSING_ROW",
                })

                wq.writerow({
                    "sku": sku,
                    "ean": ean,
                    "title": title,
                    "brand": "",
                    "bigbuy_id": "",
                    "bigbuy_product_url": "",
                    "bigbuy_image_url_1": "",
                    "bigbuy_image_url_2": "",
                    "bigbuy_image_url_3": "",
                    "r75_manual_match_type": row.get("r75_manual_match_type",""),
                    "r75_market_query_used": _market_query_used(ean, title),
                    "r75_market_source": "MANUAL",
                    "market_nl_low_price": "",
                    "market_nl_avg_price": "",
                    "market_nl_high_price": "",
                    "market_eu_low_price": "",
                    "market_eu_avg_price": "",
                    "market_eu_high_price": "",
                    "market_competitor_count_nl": "",
                    "competition_density": "",
                    "supplier_cost": "",
                    "r75_margin_safe_price": "",
                    "r75_price_positioning_score": "0.000",
                    "r75_decision": "REVIEW",
                    "r75_reason": "ERROR_PROCESSING_ROW",
                    "qa_bb_url_ok": "",
                    "qa_bb_images_ok": "",
                    "qa_internet_match_ok": "",
                    "qa_notes": "",
                    "qa_checked_by": "",
                    "qa_checked_at": "",
                })

    logger.log("SUMMARY", "INFO", "", f"metrics={logger.metrics}")
    logger.close()

if __name__ == "__main__":
    main()
