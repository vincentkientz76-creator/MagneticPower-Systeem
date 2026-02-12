# R190 — Governance Layer

R190 is de **beslissingslaag** die bepaalt of een product:

- door mag naar Shopify,
- geblokkeerd moet worden,
- of eerst door de DGA moet worden beoordeeld.

---

# 🎯 Doel

- Uitzonderingen beheren  
- Blokkades afdwingen  
- DGA‑besluiten verwerken  
- Risico’s minimaliseren  

---

# 📦 Input

- R92 prijzen  
- R97 validatie  
- DGA‑besluiten  
- Historische data  

---

# 📤 Output

`R190_VALIDATED.csv` met:

- status: GO / NO‑GO / DGA‑REQUIRED  
- reden  
- escalatie‑niveau  

---

# 🧠 Governance‑logica

### GO
- prijs is FINAL  
- content is volledig  
- metafields zijn compleet  
- SEO is correct  

### NO‑GO
- ontbrekende content  
- ontbrekende metafields  
- prijsfouten  
- inconsistenties  

### DGA‑REQUIRED
- twijfelgevallen  
- strategische producten  
- nieuwe categorieën  

---

# 🔒 Governance

R190 is de **enige** regel die:

- producten mag blokkeren,  
- producten mag escaleren,  
- DGA‑besluiten mag afdwingen.  

