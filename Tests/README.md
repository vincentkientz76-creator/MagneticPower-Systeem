# Tests — Kwaliteit, Audit & Regressie

De map **Tests** bevat alle kwaliteitscontroles van het MagneticPower Systeem.  
Deze tests zorgen ervoor dat:

- regels correct functioneren,
- pipelines reproduceerbaar blijven,
- content consistent blijft,
- UX en SEO niet breken,
- Shopify‑implementaties stabiel blijven.

Tests zijn een essentieel onderdeel van de governance‑laag.

---

# 🎯 Doel van deze map

- Fouten vroeg detecteren  
- Regressie voorkomen  
- Consistentie bewaken  
- Agents controleren  
- DGA‑besluiten beschermen  

---

# 📁 Structuur

### **Audit/**
Controleert of het systeem voldoet aan:

- R190 governance  
- R152 collectie‑validatie  
- R97 content‑validatie  
- DGA‑besluiten  
- Pricing‑consistentie  

### **Integration/**
Test de samenwerking tussen:

- R70–R79  
- R92  
- R97  
- R151–R160  
- R170–R180  
- Shopify‑import  

### **Unit/**
Test individuele regels:

- R70A extractie  
- R70B classificatie  
- R71 magnetische detectie  
- R92 prijsstrategie  
- R150 content engine  
- R160 metafields  

---

# 🔒 Governance

- Geen enkele wijziging in regels mag live zonder tests.  
- Elke test moet reproduceerbaar zijn.  
- Elke fout moet worden gelogd en geanalyseerd.  

