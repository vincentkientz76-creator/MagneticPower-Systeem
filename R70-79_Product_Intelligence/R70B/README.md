# R70B — Function Classifier

R70B bepaalt de **primaire functie** van een product.  
Dit is cruciaal, want alle downstream‑regels (R74–R79) zijn functie‑gebaseerd.

---

# 🎯 Doel

- Producten indelen in één van de vaste MagneticPower‑functies:
  - Magnetic Powerbank  
  - Magnetic Charger  
  - Mount / Holder  
  - Workplace / Daily  
  - Accessoire  
  - Lighting  
  - Non‑Magnetic (uitsluiten)  

---

# 📦 Input

`R70A_RAW_PRODUCTS.csv`

---

# 📤 Output

`R70B_FUNCTION_CLASSIFIED.csv` met:

- functie  
- subfunctie  
- classificatie‑zekerheid  
- reden van classificatie  

---

# 🔍 Validatie

- Geen product mag meerdere functies krijgen  
- Geen product mag zonder functie doorgaan  
- Non‑magnetic producten worden gemarkeerd voor uitsluiting  

---

# 🔒 Governance

R70B mag **nooit**:

- prijzen bepalen  
- SEO bepalen  
- UX bepalen  
- content genereren  
