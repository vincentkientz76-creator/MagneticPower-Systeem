# R72 — Shopify Reality Anchor

R72 koppelt ruwe data aan bestaande Shopify‑producten om:

- duplicaten te voorkomen,
- bestaande producten te beschermen,
- en consistentie te bewaren.

---

# 🎯 Doel

- SKU‑matching  
- EAN‑matching  
- Titel‑matching  
- Duplicate‑detectie  

---

# 📦 Input

`R71_MAGNETIC_DETECTED.csv`  
Shopify product export

---

# 📤 Output

`R72_SHOPIFY_ANCHORED.csv` met:

- match: ja/nee  
- match‑type: SKU / EAN / Titel  
- bestaande Shopify‑ID  
- status: nieuw / update / skip  

---

# 🔍 Validatie

- Geen dubbele producten  
- Geen SKU‑conflicten  
- Geen EAN‑conflicten  

---

# 🔒 Governance

R72 mag **nooit**:

- producten uitsluiten  
- prijzen bepalen  

