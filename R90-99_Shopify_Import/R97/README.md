# R97 — Content & Data Validator

R97 controleert of een product volledig klaar is voor Shopify.  
Het is de laatste kwaliteitscontrole vóór R190 en R91.

---

# 🎯 Doel

- Controleren of alle verplichte content aanwezig is  
- Controleren of alle metafields correct zijn  
- Controleren of SEO‑vereisten zijn ingevuld  
- Controleren of UX‑vereisten zijn ingevuld  
- Controleren of pricing logisch is  

---

# 📦 Input

- R150 content  
- R151 collectie‑architectuur  
- R152 collectie‑validatie  
- R160 metafields  
- R92 prijzen  

---

# 📤 Output

`R97_VALIDATION.csv` met:

- status: PASS / FAIL  
- ontbrekende velden  
- inconsistenties  
- waarschuwingen  

---

# 🔍 Validatiepunten

### Content
- titel  
- subline  
- bullets  
- body HTML  

### SEO
- title tag  
- meta description  
- intentie‑mapping  

### UX
- hub card  
- PDP‑structuur  

### Data
- SKU  
- EAN  
- prijs  

---

# 🔒 Governance

R97 mag **nooit**:

- content genereren  
- prijzen aanpassen  
- producten importeren  

