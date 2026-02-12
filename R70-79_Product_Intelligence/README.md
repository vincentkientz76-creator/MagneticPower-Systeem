# R70–R79 Product Intelligence — Overzicht & Architectuur

De R70–R79‑serie vormt de **intelligentie‑laag** van het MagneticPower Systeem.  
Hier worden producten:

- geëxtraheerd,
- geclassificeerd,
- verrijkt,
- gefilterd,
- beoordeeld,
- en voorbereid voor pricing en import.

Deze regels bepalen **welke producten überhaupt in aanmerking komen** voor verkoop.  
Alles wat hier wordt uitgesloten, komt nooit meer terug in het systeem.

---

# 🎯 Doel van deze regelgroep

- Chaos voorkomen in productaanbod  
- Alleen producten toelaten die passen bij MagneticPower  
- Magnetische producten correct detecteren  
- Producten verrijken met marktdata  
- Specialistische beslissingen automatiseren  
- Een schone dataset leveren aan R92 (prijsstrategie)

---

# 🧠 Overzicht van de regels

### **R70A — Bron Extractie Agent**
Haalt ruwe data op uit BigBuy/Eprolo en zet dit om naar een gestandaardiseerd formaat.

### **R70B — Function Classifier**
Bepaalt de primaire functie van een product (charger, powerbank, mount, etc.).

### **R71 — Magnetic Capability Detector**
Detecteert of een product magnetisch is, en zo ja: welk type.

### **R72 — Shopify Reality Anchor**
Verbindt ruwe data met bestaande Shopify‑producten om duplicaten te voorkomen.

### **R73 — Market Data Engine**
Haalt marktdata op (prijzen, concurrentie, EAN‑matching) en verrijkt producten.

### **R74–R79 — Specialist Agents**
Regels die per categorie bepalen of een product geschikt is:

- R74: Magnetic Powerbanks  
- R75: Magnetic Chargers  
- R76: Mounts & Holders  
- R77: Workplace & Daily  
- R78: Accessoires  
- R79: Lighting  

---

# 🔄 Flow

1. R70A → extractie  
2. R70B → classificatie  
3. R71 → magnetische detectie  
4. R72 → Shopify‑matching  
5. R73 → marktdata  
6. R74–R79 → specialistische filtering  
7. Output → R92 prijsstrategie  

---

# 🔒 Governance

- Geen enkele regel mag buiten zijn domein treden.  
- Geen enkele regel mag beslissingen van een andere regel overschrijven.  
- Alleen de DGA mag uitzonderingen toestaan.  
