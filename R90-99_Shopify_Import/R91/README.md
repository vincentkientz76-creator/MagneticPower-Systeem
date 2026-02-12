# R91 — Shopify Import

R91 is de **enige** regel die producten daadwerkelijk in Shopify zet.  
Alle upstream‑regels (R70–R190) moeten volledig zijn afgerond voordat R91 mag draaien.

---

# 🎯 Doel

- Nieuwe producten importeren  
- Bestaande producten updaten  
- Verwijderde producten archiveren  
- Metafields vullen (via R160‑output)  
- Collecties koppelen (via R151)  

---

# 📦 Input

- `R92_FINAL.csv`  
- `R190_VALIDATED.csv`  
- Metafields uit R160  
- Content uit R150  
- Collecties uit R151  

---

# 📤 Output

- Nieuwe Shopify‑producten  
- Geüpdatete producten  
- Archief van verwijderde producten  
- Logbestand van alle wijzigingen  

---

# 🔍 Validatie

R91 controleert:

- SKU‑consistentie  
- EAN‑consistentie  
- Duplicate‑preventie  
- Vereiste metafields  
- Vereiste content  

---

# 🔒 Governance

R91 mag **nooit**:

- prijzen bepalen (dat is R92)  
- content genereren (dat is R150)  
- UX bepalen (dat is R171)  
- SEO bepalen (dat is R172)  

R91 is puur uitvoerend.
