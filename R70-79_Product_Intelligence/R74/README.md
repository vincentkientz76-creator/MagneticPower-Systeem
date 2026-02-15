# R74 — Specialist Intelligence Layer (v1.0 Foundation)

Status: Canoniek  
Laag: Product Intelligence (na R73, vóór R75)  
Architectuurtype: Plugin-based Specialist Engine  

---

# 🎯 Doel van R74

R74 is de **specialistische beoordelingslaag boven R73**.

Waar R73 bepaalt:
> "Past dit product binnen MagneticPower-propositie (magnetisch ja/nee)?"

Bepaalt R74:
> "Is dit binnen die selectie een strategisch juiste categorie-keuze?"

R74 voegt **expert-intelligentie per productcategorie** toe.

R74:
- Neemt alleen R73-output (YES / MAYBE_STRONG)
- Mag nooit zonder reason_code droppen
- Is geen magnetische detector (dat is R71)
- Is geen propositie-fit (dat is R73)
- Is geen marktvalidatie (dat is R75)

R74 = specialistische kwaliteitslaag.

---

# 🧱 Architectuurpositie in de keten

R70-A  → Bronextractie  
R70-B  → Function Classifier (wat is het product?)  
R71    → Magnetische capability  
R73    → MagneticPower propositie-fit  
R74    → Specialist Intelligence (categorie-expertlaag)  
R75    → Marktvalidatie / DataForSEO  
R91    → Shopify realiteit  
R190   → Import QA  

R74 draait uitsluitend op:


---

# ⚙ Architectuurmodel (v1.0 Foundation)

R74 bestaat uit:

## 1️⃣ Core Engine

Verantwoordelijk voor:
- Input inlezen (R73 output)
- Routing naar juiste specialist
- Logging
- Guarantee: no DROP without reason_code
- Output structurering

Core outputvelden:

- sku
- product_function_primary
- r74_specialist_category
- r74_specialist_verdict (KEEP / DROP / REVIEW)
- r74_specialist_confidence (LOW / MEDIUM / HIGH)
- r74_reason_code
- r74_notes_internal

---

## 2️⃣ Category Specialists (plugin-model)

Elke categorie krijgt eigen specialist-module.

Voorbeelden:

### Powerbank Specialist
Extra velden:
- r74_pb_has_capacity
- r74_pb_capacity_level
- r74_pb_form_factor
- r74_pb_positioning_score

### Charger Specialist
- r74_charger_type
- r74_charger_power_level
- r74_charger_qi_level
- r74_charger_complexity

### Mount Specialist
- r74_mount_type
- r74_mount_use_case
- r74_mount_positioning_strength

### Cable Specialist
- r74_cable_type
- r74_cable_usb_standard
- r74_cable_positioning_strength

Elke specialist mag alleen oordelen binnen zijn categorie.

---

# 🛡 Governance Regels

R74 moet:

1. No DROP without reason_code
2. No override van R73 hard-exclusions
3. Geen magnetisch oordeel doen (dat is R71)
4. Geen marktbeslissing nemen (dat is R75)
5. Geen Shopify-kennis injecteren (dat is R72/R91)

---

# 🧠 Verdict Betekenis

KEEP  
→ Strategisch passend binnen categorie.

DROP  
→ Past niet binnen MagneticPower positionering ondanks magnetisch signaal.

REVIEW  
→ Onvoldoende duidelijk. Handmatige beoordeling nodig.

---

# 🔁 Ontwikkelfases

## A) Foundation (v1.0)
- Core engine
- Powerbank specialist
- Basis verdict model
- Logging

## B) Multi-category uitbreiding
- Charger specialist
- Mount specialist
- Cable specialist
- Accessoire specialist

## C) Koppeling R75
- Marktdata integratie
- Pricing viability signal
- Demand-score integratie

## D) Optimalisatieloop (R74 ↔ R73 ↔ R70B)
- Analyse van false positives
- Verbetering function classification
- Verbetering propositie-fit
- Category-tuning op basis van R75 resultaten

---

# 🔬 Leerloop Architectuur

R74 moet loggen:

- False positives
- False drops
- Review ratio
- Verdict per categorie
- R75 conversion performance (later)

Doel:
R74 wordt steeds intelligenter via feedback.

---

# 📤 Outputlocatie

Data/Exports/R74/<RUN_MONTH>/

Belangrijke exports:

- R74_READY_FOR_R75.csv
- R74_REJECTED_BY_SPECIALIST.csv
- R74_REVIEW_REQUIRED.csv
- R74_LOG.csv

---

# 🚀 Strategische Betekenis

R74 is de laag die:

- Bulk magnetische selectie verfijnt
- Positioneringsfouten voorkomt
- Margeverlies minimaliseert
- Categorie-autoriteit opbouwt

R74 is geen filter.
R74 is een expert.

---

MagneticPower — Specialist Intelligence Architectuur
