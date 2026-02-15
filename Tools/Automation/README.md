# Automation — MagneticPower Retail Operating System

Deze map bevat alle uitvoerende automatiseringen binnen MagneticPower.
Automatisering is uitvoerend, niet beslissend. Governance ligt in de Regels (01_Regels).

---

# 🎯 Doel van Automation Layer

- Leveranciersdata inlezen
- Normaliseren
- Functioneel classificeren
- Magnetische capability detecteren
- Shopify-reality verankeren
- Marktdata ophalen (DataForSEO)
- Pricing intelligence berekenen
- Logging & audit genereren

---

# 🧩 Architectuur Overzicht

R70A → Bron Extractie  
R70B → Product Function Classifier  
R71  → Magnetic Capability Detector  
R72  → Shopify Reality Anchor  
R73  → MagneticPower Proposition Fit  
R74  → Specialist Agent (Powerbank Intelligence)  
R75  → DataForSEO Market Intelligence  
R92  → Pricing & Market Intelligence Engine  
R97  → Review / Media Intelligence  
R190 → Import QA & Encoding Validation  

---

# 🔁 R70A + LATEST Alias Systeem

R70A schrijft altijd naar:

Data/Exports/R70A/<timestamp>/<Supplier>/R70A_RAW_PRODUCTS.csv

Daarna draait:

run_r70a_latest.py

Dit maakt een alias:

Data/Exports/R70A/LATEST/<Supplier>/R70A_RAW_PRODUCTS.csv

Alle downstream regels lezen uitsluitend vanuit:

Data/Exports/R70A/LATEST

Voordelen:
- Geen timestamp afhankelijkheid
- Reproduceerbaar
- CI-ready
- Stabiele leerloop (R74 feedback)

---

# 🚀 Standaard Pipeline Run (70 → 72)

Gebruik:

Tools/Automation/runners/mp_run_70_72.sh 2026-02

Dit voert uit:

1. R70A → update LATEST
2. R70B → function classification
3. R71 → magnetic capability
4. R72 → Shopify anchor check

---

# 🚀 Uitgebreide Pipeline (70 → 75 → 92)

Manuele volgorde:

export MP_R70A_RUN=LATEST

python3 Tools/Automation/runners/run_r70a_latest.py
python3 -m Tools.Automation.runners.run_r70b --run 2026-02
python3 -m Tools.Automation.runners.run_r71  --run 2026-02
python3 -m Tools.Automation.runners.run_r72  --run 2026-02
python3 -m Tools.Automation.runners.run_r73  --run 2026-02
python3 -m Tools.Automation.runners.run_r74  --run 2026-02
python3 -m Tools.Automation.runners.run_r75  --run 2026-02
python3 -m Tools.Automation.runners.run_r92  --run 2026-02

---

# 📦 Structuur

core/      → generieke utilities  
lib/       → gedeelde helpers (mp_paths)  
runners/   → uitvoerbare regels  
docs/      → API & setup documentatie  

---

# ⚠️ Governance Regel

- Downstream regels mogen NOOIT timestamp-mappen lezen.
- Alleen R70A mag timestamp-gebonden schrijven.
- Alle andere regels gebruiken LATEST alias.

---

# 🧠 Leerloop

R74 (specialist agent) analyseert afwijkingen
R72 detecteert Shopify mismatches
R92 valideert pricing realiteit
R190 voorkomt foutieve import

Automation ondersteunt — Governance beslist.

---

MagneticPower Retail Operating System  
Automation Layer — Canoniek
