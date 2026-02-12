# R70A — Bron Extractie Agent

R70A is de eerste stap van het systeem.  
Deze regel haalt ruwe data op uit leveranciers (BigBuy, Eprolo) en zet deze om naar een **gestandaardiseerd, schoon, machine‑leesbaar formaat**.

---

# 🎯 Doel

- Ruwe data extraheren  
- Fouten verwijderen  
- Velden normaliseren  
- Een uniforme dataset maken voor R70B  

---

# 📦 Input

- BigBuy XML/CSV  
- Eprolo CSV/JSON  
- Handmatige managementbestanden (optioneel)

---

# 📤 Output

`R70A_RAW_PRODUCTS.csv` met:

- titel  
- beschrijving  
- SKU  
- EAN  
- prijs  
- voorraad  
- afbeeldingen  
- leverancier  
- categorie  
- tags  

---

# 🔍 Validatie

- Geen lege titels  
- Geen producten zonder SKU  
- Geen producten zonder prijs  
- Geen producten zonder categorie  

---

# 🔒 Governance

R70A mag **nooit**:

- producten uitsluiten,  
- producten classificeren,  
- producten beoordelen.  

Het is puur extractie.

