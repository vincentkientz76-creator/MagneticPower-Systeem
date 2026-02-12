# R73 — Market Data Engine

R73 verrijkt producten met marktdata via DataForSEO:

- prijsranges  
- concurrentiedichtheid  
- EAN‑matching  
- merchant‑URL’s  

---

# 🎯 Doel

- Marktpositie bepalen  
- Prijsstrategie voeden (R92)  
- Concurrentie detecteren  

---

# 📦 Input

`R72_SHOPIFY_ANCHORED.csv`  
DataForSEO API

---

# 📤 Output

`R73_MARKETDATA.csv` met:

- low price  
- average price  
- high price  
- merchant count  
- EAN‑match score  

---

# 🔍 Validatie

- Geen prijsdata = product krijgt PROVISIONAL status in R92  
- Geen EAN‑match = fallback op titel‑matching  

---

# 🔒 Governance

R73 mag **nooit**:

- prijzen bepalen  
- producten uitsluiten  
