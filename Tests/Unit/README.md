# Unit Tests — Regels Individueel Testen

Unit‑tests controleren of **individuele regels** correct functioneren.  
Elke regel in het MagneticPower Systeem heeft één taak — en unit‑tests bewaken dat.

---

# 🎯 Doel

- Fouten vroeg detecteren  
- Regressie voorkomen  
- Regels stabiel houden  
- Agents controleren  

---

# 📦 Wat wordt getest?

### R70A — Extractie
- correcte parsing  
- correcte normalisatie  
- geen lege velden  

### R70B — Classificatie
- juiste functie  
- juiste subfunctie  
- geen dubbele functies  

### R71 — Magnetische detectie
- correcte detectie  
- correcte compatibiliteit  

### R92 — Pricing
- margeberekening  
- marktdata‑integratie  
- floor‑rule  

### R150 — Content Engine
- correcte templates  
- correcte SEO‑structuur  
- correcte micro‑USP’s  

### R160 — Metafields
- correcte schema’s  
- correcte waarden  

---

# 🔒 Governance

Unit‑tests zijn verplicht bij:

- elke wijziging in een regel  
- elke nieuwe regel  
- elke bugfix  

