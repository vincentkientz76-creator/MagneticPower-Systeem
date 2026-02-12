# R92 — Pricing Engine

R92 is de **commerciële kern** van het MagneticPower Systeem.  
Deze regel bepaalt de verkoopprijs van elk product op basis van:

- marktdata (R73),
- kosten,
- marge‑doelen,
- concurrentie,
- DGA‑strategie.

---

# 🎯 Doel

- Een eerlijke, winstgevende en marktconforme prijs bepalen  
- Prijsconsistentie bewaken  
- Prijsfouten voorkomen  
- DGA‑strategie afdwingen  

---

# 📦 Input

- `R73_MARKETDATA.csv`  
- Kostenbestand (BigBuy/Eprolo)  
- DGA‑prijsregels  
- Historische prijsdata  

---

# 📤 Output

`R92_FINAL.csv` met:

- verkoopprijs  
- marge  
- prijsstatus (FINAL / PROVISIONAL / BLOCKED)  
- reden van prijskeuze  

---

# 🧠 Prijslogica

### 1. Marktdata
- low / average / high price  
- merchant count  
- concurrentiedichtheid  

### 2. Kosten
- inkoopprijs  
- verzendkosten  
- transactiekosten  

### 3. Strategie
- premium positionering  
- geen race‑to‑the‑bottom  
- geen onrealistische marges  

---

# 🔍 Validatie

- Geen prijs onder kostprijs  
- Geen prijs boven marktlogica  
- Geen prijs zonder marktdata → PROVISIONAL  
- Geen prijs zonder DGA‑goedkeuring → BLOCKED  

---

# 🔒 Governance

R92 is de **enige** regel die prijzen mag bepalen.  
Geen enkele andere regel mag prijzen wijzigen.

