# R90–R99 Shopify Import & Pricing — Overzicht & Architectuur

De R90–R99‑serie vormt de **commerciële kern** van het MagneticPower Systeem.  
Hier worden producten:

- geprijsd,
- gevalideerd,
- gecontroleerd,
- en uiteindelijk geïmporteerd in Shopify.

Deze regels bepalen **wat er live komt te staan**, tegen welke prijs, en onder welke voorwaarden.

---

# 🎯 Doel van deze regelgroep

- Prijsstrategie automatiseren (R92)
- Productvalidatie uitvoeren (R97)
- Governance toepassen (R190)
- Shopify‑import uitvoeren (R91)

---

# 🧠 Overzicht van de regels

### **R91 — Shopify Import**
De enige regel die producten daadwerkelijk in Shopify zet.

### **R92 — Pricing Engine**
Bepaalt de verkoopprijs op basis van:

- marktdata (R73),
- kosten,
- marge‑doelen,
- concurrentie,
- DGA‑regels.

### **R97 — Content & Data Validator**
Controleert of producten voldoen aan:

- contentvereisten,
- metafields,
- UX‑vereisten,
- SEO‑vereisten.

### **R190 — Governance Layer**
Bewaakt:

- uitzonderingen,
- blokkades,
- escalaties,
- DGA‑besluiten.

---

# 🔄 Flow

1. R73 → marktdata  
2. R92 → prijsstrategie  
3. R97 → validatie  
4. R190 → governance  
5. R91 → import  

---

# 🔒 Governance

- Geen enkele regel mag Shopify direct aanpassen behalve R91.  
- Geen enkele regel mag prijzen bepalen behalve R92.  
- Geen enkele regel mag blokkades opheffen behalve R190.  
