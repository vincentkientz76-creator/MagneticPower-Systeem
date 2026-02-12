# R150–R160 Content Governance — Overzicht & Architectuur

De R150–R160‑serie vormt de **content‑ en collectie‑governance‑laag** van het MagneticPower Systeem.  
Deze regels bepalen:

- hoe content wordt opgebouwd,
- hoe collecties worden gestructureerd,
- hoe metafields worden gevuld,
- hoe SEO‑intentie wordt toegepast,
- hoe UX‑flow wordt ondersteund.

Content binnen MagneticPower is **nooit willekeurig**.  
Het volgt strikte templates, regels en validatie‑lagen.

---

# 🎯 Doel van deze regelgroep

- Consistente content genereren (R150)
- Collecties logisch en schaalbaar opbouwen (R151)
- Collecties valideren (R152)
- Hub cards en UX‑blokken genereren (R154)
- Metafields vullen en beheren (R160)

---

# 🧠 Overzicht van de regels

### **R150 — Content Engine**
De centrale regel voor alle contentgeneratie.

### **R151 — Collection Architecture**
Bepaalt welke collecties bestaan en hoe ze zijn opgebouwd.

### **R152 — Collection Validator**
Controleert of collecties volledig en consistent zijn.

### **R154 — Hub Cards Engine**
Genereert hub‑kaarten en UX‑blokken.

### **R160 — Metafields Registry**
Beheert alle metafields die Shopify gebruikt.

---

# 🔄 Flow

1. R151 → collectie‑structuur  
2. R152 → validatie  
3. R150 → contentgeneratie  
4. R154 → hub cards  
5. R160 → metafields  
6. Output → R97 → R91  

---

# 🔒 Governance

- Content mag nooit handmatig in Shopify worden aangepast.  
- Collecties mogen nooit buiten
