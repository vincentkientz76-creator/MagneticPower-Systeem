import csv
import os
import re
from typing import Dict, List, Tuple, Optional

def _sniff_delimiter(path: str) -> str:
    with open(path, "rb") as f:
        raw = f.read(4096)
    txt = raw.decode("utf-8", errors="replace")
    try:
        d = csv.Sniffer().sniff(txt, delimiters=";,|\t")
        return d.delimiter
    except Exception:
        return ";"

def _norm_key(k: str) -> str:
    k = (k or "").strip().lower()
    k = k.replace("\ufeff", "")
    k = re.sub(r"\s+", "_", k)
    k = re.sub(r"[^a-z0-9_]", "", k)
    return k

def _read_csv_any(path: str) -> Tuple[List[Dict[str, str]], List[str], str]:
    delim = _sniff_delimiter(path)
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        r = csv.DictReader(f, delimiter=delim)
        headers = r.fieldnames or []
        rows = []
        for row in r:
            rows.append({k: (v if v is not None else "") for k, v in row.items()})
    return rows, headers, delim

def _index_rows(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    if not rows:
        return rows
    orig_headers = list(rows[0].keys())
    norm_headers = [_norm_key(h) for h in orig_headers]
    mapping = dict(zip(orig_headers, norm_headers))
    out = []
    for row in rows:
        n = {}
        for ok, nk in mapping.items():
            n[nk] = (row.get(ok, "") or "").strip()
        out.append(n)
    return out

def _pick(row: Dict[str, str], keys: List[str]) -> str:
    for k in keys:
        v = (row.get(k, "") or "").strip()
        if v:
            return v
    return ""

def _pick_first_images(row: Dict[str, str]) -> Tuple[str, str, str]:
    candidates = [
        "image_url_1","image1","image_1","img1","picture1","photo1",
        "image_url","image","img","picture","photo",
        "image_urls","images","pictures","photos",
    ]
    raw = _pick(row, candidates)
    if not raw:
        for k in list(row.keys()):
            if k.startswith("image_url_") or k.startswith("image"):
                v = (row.get(k, "") or "").strip()
                if v:
                    raw = v
                    break
    if not raw:
        return "", "", ""
    parts = re.split(r"[|,\s]+", raw.strip())
    parts = [p for p in parts if p.startswith("http")]
    if len(parts) == 0 and raw.startswith("http"):
        parts = [raw]
    p1 = parts[0] if len(parts) > 0 else ""
    p2 = parts[1] if len(parts) > 1 else ""
    p3 = parts[2] if len(parts) > 2 else ""
    return p1, p2, p3

def _to_float(x: str) -> Optional[float]:
    s = (x or "").strip()
    if not s:
        return None
    s = s.replace("€", "").replace("\u00a0", " ").strip()
    s = s.replace(",", ".")
    buf = []
    dot = False
    for ch in s:
        if ch.isdigit():
            buf.append(ch)
        elif ch == "." and not dot:
            buf.append(".")
            dot = True
    if not buf or buf == ["."]:
        return None
    try:
        return float("".join(buf))
    except Exception:
        return None

def _row_score(row: Dict[str, str]) -> int:
    return sum(1 for v in row.values() if (v or "").strip())

def dedupe_by_sku_keep_best(rows: List[Dict[str, str]]) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    buckets: Dict[str, List[Dict[str, str]]] = {}
    for row in rows:
        sku = (row.get("sku", "") or "").strip()
        if not sku:
            raise ValueError("R74 input row missing sku")
        buckets.setdefault(sku, []).append(row)

    deduped: List[Dict[str, str]] = []
    dup_audit: List[Dict[str, str]] = []

    for sku, group in buckets.items():
        if len(group) == 1:
            deduped.append(group[0])
            continue
        best = sorted(group, key=_row_score, reverse=True)[0]
        deduped.append(best)
        for g in group:
            a = dict(g)
            a["r75_dup_group_sku"] = sku
            a["r75_dup_kept"] = "YES" if g is best else "NO"
            a["r75_dup_score"] = str(_row_score(g))
            dup_audit.append(a)

    return deduped, dup_audit

def load_r74_ready(run_month: str) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    path = f"Data/Exports/R74/{run_month}/R74_READY_FOR_R75.csv"
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing R75 input: {path}")

    rows, _, _ = _read_csv_any(path)
    rows = _index_rows(rows)

    if rows:
        required = ["sku", "ean", "title"]
        missing = [c for c in required if c not in rows[0].keys()]
        if missing:
            raise ValueError(f"R74_READY_FOR_R75 missing columns: {missing}")

    deduped, dup_audit = dedupe_by_sku_keep_best(rows)
    return deduped, dup_audit

def load_bigbuy_manual(run_month: str) -> Tuple[str, List[Dict[str, str]]]:
    base = f"Data/Inputs/BigBuy_Manual/{run_month}"
    if not os.path.isdir(base):
        raise FileNotFoundError(f"Missing folder: {base}")
    files = [f for f in os.listdir(base) if f.lower().endswith(".csv")]
    if not files:
        raise FileNotFoundError(f"No CSV found in: {base}")
    path = os.path.join(base, sorted(files)[0])
    rows, _, _ = _read_csv_any(path)
    return path, _index_rows(rows)

def build_manual_index(manual_rows: List[Dict[str, str]]) -> Tuple[Dict[str, Dict[str, str]], Dict[str, Dict[str, str]]]:
    by_sku: Dict[str, Dict[str, str]] = {}
    by_ean: Dict[str, Dict[str, str]] = {}
    for r in manual_rows:
        sku = _pick(r, ["sku","reference","ref","internal_reference","supplier_sku","variant_sku"])
        ean = _pick(r, ["ean","barcode","gtin"])
        if sku and sku not in by_sku:
            by_sku[sku] = r
        if ean and ean not in by_ean:
            by_ean[ean] = r
    return by_sku, by_ean

def merge_r74_with_manual(r74_rows: List[Dict[str, str]], manual_rows: List[Dict[str, str]]) -> Tuple[List[Dict[str, str]], Dict[str, int]]:
    by_sku, by_ean = build_manual_index(manual_rows)
    out: List[Dict[str, str]] = []
    stats = {"total": 0, "matched_sku": 0, "matched_ean": 0, "unmatched": 0}

    for r in r74_rows:
        stats["total"] += 1
        sku = (r.get("sku","") or "").strip()
        ean = (r.get("ean","") or "").strip()
        m = None
        match_type = "NONE"
        if sku and sku in by_sku:
            m = by_sku[sku]
            match_type = "SKU"
            stats["matched_sku"] += 1
        elif ean and ean in by_ean:
            m = by_ean[ean]
            match_type = "EAN"
            stats["matched_ean"] += 1
        else:
            stats["unmatched"] += 1

        merged = dict(r)
        merged["r75_manual_match_type"] = match_type

        if m:
            merged["manual_brand"] = _pick(m, ["brand","vendor","manufacturer"])
            merged["manual_bigbuy_id"] = _pick(m, ["bigbuy_id","id","product_id","bb_id"])
            merged["manual_bigbuy_product_url"] = _pick(m, ["product_url","url","bigbuy_url","product_link","link"])
            i1,i2,i3 = _pick_first_images(m)
            merged["manual_bigbuy_image_url_1"] = i1
            merged["manual_bigbuy_image_url_2"] = i2
            merged["manual_bigbuy_image_url_3"] = i3
            merged["manual_supplier_cost"] = _pick(m, ["inkoopprijs","supplier_cost","cost","purchase_price","buy_price","wholesale_price"])

            for k in [
                "market_nl_low_price","market_nl_avg_price","market_nl_high_price",
                "market_eu_low_price","market_eu_avg_price","market_eu_high_price",
                "market_competitor_count_nl","competition_density",
            ]:
                if k in m and (m.get(k,"") or "").strip():
                    merged[f"manual_{k}"] = (m.get(k,"") or "").strip()

        out.append(merged)

    return out, stats

def extract_bb_fields(row: Dict[str, str]) -> Dict[str, str]:
    return {
        "bigbuy_product_url": (row.get("manual_bigbuy_product_url","") or "").strip(),
        "bigbuy_image_url_1": (row.get("manual_bigbuy_image_url_1","") or "").strip(),
        "bigbuy_image_url_2": (row.get("manual_bigbuy_image_url_2","") or "").strip(),
        "bigbuy_image_url_3": (row.get("manual_bigbuy_image_url_3","") or "").strip(),
        "brand": (row.get("manual_brand","") or "").strip(),
        "bigbuy_id": (row.get("manual_bigbuy_id","") or "").strip(),
    }

def extract_market_fields(row: Dict[str, str]) -> Dict[str, Optional[float]]:
    def gf(k: str) -> Optional[float]:
        return _to_float(row.get(k,"") or "")
    return {
        "market_nl_low_price": gf("manual_market_nl_low_price") or gf("market_nl_low_price"),
        "market_nl_avg_price": gf("manual_market_nl_avg_price") or gf("market_nl_avg_price"),
        "market_nl_high_price": gf("manual_market_nl_high_price") or gf("market_nl_high_price"),
        "market_eu_low_price": gf("manual_market_eu_low_price") or gf("market_eu_low_price"),
        "market_eu_avg_price": gf("manual_market_eu_avg_price") or gf("market_eu_avg_price"),
        "market_eu_high_price": gf("manual_market_eu_high_price") or gf("market_eu_high_price"),
    }

def extract_competition_fields(row: Dict[str, str]) -> Dict[str, str]:
    comp = (row.get("manual_market_competitor_count_nl","") or row.get("market_competitor_count_nl","") or "").strip()
    dens = (row.get("manual_competition_density","") or row.get("competition_density","") or "").strip()
    return {"market_competitor_count_nl": comp, "competition_density": dens}

def extract_supplier_cost(row: Dict[str, str]) -> Optional[float]:
    v = (row.get("manual_supplier_cost","") or row.get("supplier_cost","") or row.get("inkoopprijs","") or "").strip()
    return _to_float(v)
