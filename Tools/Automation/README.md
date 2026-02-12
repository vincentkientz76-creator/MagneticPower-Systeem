# Automation — Automatische Processen & Externe Koppelingen

De map **Tools/Automation** bevat alle automatische processen die het MagneticPower Systeem ondersteunen.
Deze automatisering is **uitvoerend**, niet beslissend.

Automatiseringen draaien:
- handmatig (door de DGA)
- via geplande runs (later eventueel CI/cron)
- als onderdeel van pipeline-runs (R70 → R92 → R190 → R91)

---

## 🎯 Doel

- Data ophalen (leveranciers, marktdata)
- Data normaliseren/verrijken (zonder interpretatie)
- Validatie uitvoeren (QA, governance checks)
- Externe API’s aanroepen (bv. DataForSEO)
- Logging genereren (pipeline/audit/error)

---

## 🧩 Structuur

- `core/`  
  Basiscomponenten: config, logging, IO utilities (CSV/JSON), helpers.

- `runners/`  
  Uitvoerbare scripts per regel/pijplinestap (bijv. `run_r70a.py`).

- `docs/`  
  Aanvullende documentatie (API keys, setup, flow).

- `logs/`  
  Lokale logbestanden (niet bedoeld voor Git).  
  *(Let op: logs blijven lokaal via .gitignore.)*

- `tmp/`  
  Tijdelijke output / tussenbestanden (niet bedoeld voor Git).

---

## ▶ Hoe run je automatiseringen?

Voorbeelden (vanuit repo-root):

```bash
python Tools/Automation/runners/run_r70a.py --input "Data/BigBuy/source.csv" --out "Data/Exports/R70A_RAW_PRODUCTS.csv"
python Tools/Automation/runners/run_r70b.py --input "Data/Exports/R70A_RAW_PRODUCTS.csv" --out "Data/Exports/R70B_FUNCTION_CLASSIFIED.csv"
python Tools/Automation/runners/run_r73.py  --input "Data/Exports/R70B_FUNCTION_CLASSIFIED.csv" --out "Data/Exports/R73_SELECTION.csv"
python Tools/Automation/runners/run_r92.py  --input "Data/Exports/R73_SELECTION.csv" --out "Data/Exports/R92_PRICING.csv"

