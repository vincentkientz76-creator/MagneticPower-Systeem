# Tools — Automatisering, Scripts & Pipeline‑Hulpmiddelen

De map **Tools** bevat alle ondersteunende hulpmiddelen van het MagneticPower Systeem.  
Deze tools worden gebruikt door:

- de pipeline (R70–R99),
- de content engine (R150),
- de UX/SEO‑architectuur (R170–R180),
- en de Shopify‑import (R91).

Tools zijn **nooit leidend** — ze voeren alleen uit wat de regels bepalen.

---

# 🎯 Doel van deze map

- Automatisering van repetitieve taken  
- Ondersteuning van pipeline‑runs  
- Validatie van data en content  
- Koppelingen met externe systemen  
- Logging en debugging  

---

# 📁 Structuur

### **Automation/**
Automatische processen zoals:

- DataForSEO calls  
- BigBuy/Eprolo downloads  
- Cron‑achtige taken  
- Validatie‑scripts  

### **Pipeline/**
Hulpmiddelen die de pipeline ondersteunen:

- CSV‑processors  
- Normalisatie‑scripts  
- Mapping‑tools  
- Logging‑tools  

### **Scripts/**
Losse scripts voor:

- debugging  
- conversies  
- kleine taken  
- ad‑hoc analyses  

---

# 🔒 Governance

- Tools mogen nooit beslissingen nemen.  
- Tools mogen nooit regels overschrijven.  
- Tools mogen alleen uitvoeren wat upstream‑regels bepalen.  

