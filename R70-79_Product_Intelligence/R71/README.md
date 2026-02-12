# R71 — Magnetic Capability Detector

R71 bepaalt of een product magnetisch is, en zo ja:

- welk type magnetisme,
- welke sterkte,
- welke compatibiliteit.

---

# 🎯 Doel

- Detecteren of een product MagSafe‑compatibel is  
- Detecteren of een product Qi2‑compatibel is  
- Detecteren of een product generiek magnetisch is  
- Detecteren of een product géén magnetisme heeft  

---

# 📦 Input

`R70B_FUNCTION_CLASSIFIED.csv`

---

# 📤 Output

`R71_MAGNETIC_DETECTED.csv` met:

- magnetisch: ja/nee  
- type: MagSafe / Qi2 / Generic  
- sterkte: low / medium / high  
- compatibiliteit: iPhone / Android / Universeel  

---

# 🔍 Validatie

- Geen product mag als magnetisch worden gemarkeerd zonder bewijs  
- Geen product mag als non‑magnetic worden gemarkeerd als er magnetische termen zijn  

---

# 🔒 Governance

R71 mag **nooit**:

- producten uitsluiten  
- producten classificeren  
- prijzen bepalen  

