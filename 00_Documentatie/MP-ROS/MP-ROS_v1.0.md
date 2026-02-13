# MagneticPower Retail Operating System (MP-ROS) v1.0

Versie: 0.2  
Status: In ontwikkeling  
Datum: 13-02-2026  
Bron: Repo is technisch leidend. Dit document is bestuurlijk leidend.

---

# 1. Executive Overview

## 1.1 Doel van het systeem

MagneticPower is een gespecialiseerd retailplatform dat uitsluitend producten voert met functionele magnetische interactie binnen de domeinen:

- Opladen
- Dagelijks gebruik
- Onderweg
- Werkplek & Thuis

Het systeem is ontworpen om:

- Productselectie te objectiveren
- Marge te waarborgen
- Governance hard af te dwingen
- Importfouten te minimaliseren
- Volledig schaalbaar te automatiseren

Dit document beschrijft de bestuurlijke kern van het systeem.  
Technische implementatie bevindt zich uitsluitend in de repository.

---

## 1.2 Positionering

MagneticPower is:

- Geen algemene gadgetstore
- Geen dropship-winkel zonder selectie
- Geen prijsvechter
- Geen marketinggedreven assortiment

MagneticPower is:

- Selectief
- Functioneel
- Premium gepositioneerd
- Gericht op rust, controle en slimme toepassing

Magnetisch betekent binnen dit systeem:

Een product moet een expliciete, functionele magnetische interactie bezitten.

Marketingtermen, kleurnamen of secundaire magnetische sluitingen vallen niet onder deze definitie.

---

## 1.3 End-to-End Keten

Leverancier  
↓  
R70-A — Bron Extractie  
↓  
R70-B — Product Function Classification  
↓  
R73 — MagneticPower Proposition Fit  
↓  
R74 — Specialist Intelligence (indien van toepassing)  
↓  
R91 — Shopify Structuuranker  
↓  
R92 — Prijs- en Margebepaling  
↓  
R150 — Content Governance  
↓  
R190 — GO / NO-GO Gate  
↓  
Publicatie in Shopify  

Indien één schakel faalt, vindt geen publicatie plaats.

---

## 1.4 Kernprincipes

1. Repo is technisch leidend.
2. Dit handboek is bestuurlijk leidend.
3. Geen regel bestaat zonder vaste plaats in het systeem.
4. Geen product wordt gepubliceerd zonder volledige ketendoorgang.
5. Er bestaan geen uitzonderingen buiten governance.

---

## 1.5 Afbakening

Dit document bevat:

- Geen code
- Geen uitvoeringsscripts
- Geen CSV-schema details
- Geen productteksten

Deze bevinden zich uitsluitend in de repository.

---

## 1.6 Bestuurlijke Samenvatting

MagneticPower draait op vier samenwerkende motoren:

1. Product Intelligence Engine  
2. Commerciële Engine  
3. Content & UX Engine  
4. Governance Engine  

Zolang deze vier synchroon functioneren, is het systeem stabiel en schaalbaar.

---

# 2. Systeemarchitectuur

## 2.1 Doel van de architectuur

De architectuur borgt dat MagneticPower schaalbaar kan groeien zonder kwaliteitsverlies door:

- vaste ketenstappen
- harde gates vóór livegang
- scheiding tussen classificatie, selectie, verrijking en publicatie
- reproduceerbare runs met logs en outputs

De architectuur is opgebouwd rondom een dataflow: elk product is een record dat stapsgewijs verrijkt wordt.

---

## 2.2 Kernmodules en verantwoordelijkheden

### Product Intelligence Engine (R70–R74)
Doel: bepalen wat een product is en of het past binnen de MagneticPower propositie.

- R70-A: bronextractie zonder interpretatie
- R70-B: functionele productclassificatie (wat is het)
- R71: magnetische capability detectie (is/hoe magnetisch)
- R72: verankering aan Shopify-realiteit (wat bestaat al)
- R73: propositie-fit (past dit bij MagneticPower)
- R74: specialist-laag (diepte per categorie, bv. powerbanks)

Output: een selectie die zowel technisch als commercieel verdedigbaar is.

---

### Commerciële Engine (R91–R92–R97–R190)
Doel: van geselecteerd product naar importklare waarheid.

- R91: schema/structuuranker (kolommen, normalisatie, encoding)
- R92: prijs- en marge-engine (commerciële berekening)
- R97: validatie en recovery (fouten detecteren, inconsistenties opschonen)
- R190: GO/NO-GO gate (laatste kwaliteitscontrole)

Output: importklare dataset en een expliciet kwaliteitsbesluit.

---

### Content & UX Engine (R150–R152–R170+)
Doel: consistente presentatie, vindbaarheid en conversie.

- R150: content governance (copy/SEO/HTML/ASCII/limieten)
- R151: collectie-architectuur (structuur en routing)
- R152: collectie-registry (single source of truth per collectie)
- R170–R173: UX/CRO/SEO/Theme implementatielaag (canoniek)

Output: consistente storefront-structuur en schaalbare contentproductie.

---

### Governance Engine
Doel: beslissingen en veranderingen bestuurbaar maken.

- Canonieke regels en gatekeeping (o.a. R190)
- Document-samenvoeging en canonisering (R300)
- Audittrail via changelogs
- Rolafbakening: repo = technisch leidend, MP-ROS = bestuurlijk leidend

Output: controle, herleidbaarheid en consistentie over tijd.

---

## 2.3 Dataflow op hoofdlijnen

1. Extractie  
   Brondata wordt ongewijzigd ingelezen en genormaliseerd naar een ruwe basis.

2. Functieclassificatie  
   Vaststellen wat het product functioneel is (zonder magnetische conclusie).

3. Magnetische capability + propositie-fit  
   Vaststellen of er functionele magnetische interactie is en of het binnen MagneticPower past.

4. Verankering aan Shopify  
   Matchen aan bestaande realiteit (handles, templates, bestaande collecties).

5. Structureren en prijzen  
   Importschema toepassen + prijs/marge bepalen.

6. Content governance  
   Titles, meta, body governance, encoding en URL-governance.

7. GO/NO-GO  
   Laatste gate: alleen “GO” mag live.

---

## 2.4 System-of-Record regels

Voor bestuur en uitvoering gelden onderstaande waarheden:

1. De repository is de technische waarheid (scripts, pipelines, tests).
2. MP-ROS is de bestuurlijke waarheid (architectuur, gates, verantwoordelijkheden).
3. R152 is de single source of truth voor collectie-routing en template-koppeling.
4. R91 is de single source of truth voor importstructuur en CSV-kwaliteitseisen.
5. R190 is de finale autoriteit voor livegangbesluit.

---

## 2.5 Minimale succescriteria (architectuur)

De architectuur is correct ingericht als:

- elke run reproduceerbaar is (zelfde input → zelfde output)
- elke stap een expliciet outputbestand/log oplevert
- onzekere classificaties gelabeld worden (niet ingevuld)
- elke livegang aantoonbaar door R190 “GO” is gegaan
- wijzigingen traceerbaar zijn via changelogs

