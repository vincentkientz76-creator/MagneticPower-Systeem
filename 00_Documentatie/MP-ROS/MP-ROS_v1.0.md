# MagneticPower Retail Operating System (MP-ROS) v1.0

Versie: 0.4  
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

---

# 3. Product Intelligence Engine (R70–R74)

## 3.1 Doel

De Product Intelligence Engine bepaalt in een vaste volgorde:

1. Wat het product functioneel is (R70-B)
2. Of en hoe het magnetisch is (R71)
3. Wat de Shopify-realiteit al bevat (R72)
4. Of het past binnen MagneticPower (R73)
5. Of specialistlogica vereist is (R74)

De kernoutput is een verdedigbare selectie: technisch correct, proposition-fit en klaar voor structuur en pricing.

---

## 3.2 R70-A — Bron Extractie (geen interpretatie)

R70-A leest supplierbestanden (ZIP/XML/CSV) zonder filtering of propositie-oordeel en normaliseert ruwe velden naar een standaard raw-format.

Eigenschappen:

- Geen magnetische selectie
- Geen Shopify-logica
- Geen “fit” oordeel
- Wel encoding-sanitizer en veldnormalisatie

Outputs:

- R70A_RAW_PRODUCTS.csv
- R70A_EXTRACT_LOG.csv

---

## 3.3 R70-B — Product Function Classifier (wat is het product)

R70-B bepaalt uitsluitend de functionele productsoort.

Belangrijk:

- R70-B mag geen magnetisch oordeel vellen
- R70-B mag geen MagneticPower-propositie toepassen
- Onzekerheid leidt tot LOW confidence, niet tot gokken

Output (voorbeeldvelden):

- product_function_primary
- product_function_secondary (optioneel)
- function_confidence (LOW/MEDIUM/HIGH)
- function_reason (korte uitlegbare reden)

R70-B is leidend voor downstream beslissingen: fouten in “wat het product is” worden hier gecorrigeerd, niet later.

---

## 3.4 R71 — Magnetic Capability Detector (is/hoe magnetisch)

R71 bepaalt of het product een functionele magnetische interactie heeft en hoe deze zich uit.

Bronnen voor detectie:

- Titel / beschrijving signalen (magnetisch/magneet/magnetic)
- MagSafe / Qi2 signals
- Neodymium / magnet* context (excl. magnetron)
- Producttype-context uit R70-B (magnetisme moet functioneel passen)

R71 is geen propositie-fit; R71 is een capability-detectie.

---

## 3.5 R72 — Shopify Reality Anchor (verankering)

R72 verankert de selectie aan bestaande Shopify-realiteit:

- bestaande handles / collecties / templates
- bestaande categorieën en hubstructuur
- bestaande mappingregels (allow/deny anchors)

Doel: voorkomen dat pipeline-output “los” raakt van de echte winkel.

---

## 3.6 R73 — MagneticPower Proposition Fit (bindend)

R73 is de bindende selectie-regel: het bepaalt of een product binnen MagneticPower als propositie past.

Kernprincipes:

- Magnetisch = expliciete, functionele magneet-interactie
- Niet-magnetische producten worden uitgesloten
- Marketing/kleurnaam “magnet” wordt uitgesloten

Bindende hard exclusions:

- Primary devices zijn altijd uitgesloten (bijv. smartphones)
  - exclusion_reason: PRIMARY_DEVICE_NOT_MAGNETIC_FUNCTION
- Audio devices zijn uitgesloten (headphones/earbuds/speakers)
  - exclusion_reason: PRIMARY_DEVICE_NOT_MAGNETIC_FUNCTION
- Storage devices zijn uitgesloten (HDD/SSD/USB drives)
  - exclusion_reason: STORAGE_DEVICE_NOT_MAGNETIC_FUNCTION
- Bags/wallets/pouches met magnetische sluiting zijn uitgesloten
  - exclusion_reason: BAG_WITH_MAGNETIC_CLOSURE_NOT_MAGNETIC_FUNCTION

Contextlabels (bindend):

- r73_usage_context (charging | consumer_daily | business_daily)
- r73_collection_candidate
- r73_exclusion_reason

Output van R73:

- Alleen YES + MAYBE_STRONG gaan door
- NO wordt uitgesloten met reden

---

## 3.7 R74 — Specialist Engine (Magnetische Powerbanks)

R74 is een specialistlaag voor powerbanks:

- Detecteert powerbank baseline (powerbank/portable charger/battery pack)
- Combineert dit met magnetische signals (MagSafe/Qi2/magnetic)
- Past hard exclusions toe voor niet-relevante domeinen
- Verankert aan bestaande Shopify allowlist-ankers (R91/R72)

Outputvelden (richtinggevend):

- r73_is_powerbank_v2
- r74_is_magnetic_powerbank
- r74_detection_reason
- r74_confidence
- r91_anchor_match

R74 draait na R73 en vóór verdere verrijking.

---

## 3.8 Minimale succescriteria (R70–R74)

De Product Intelligence Engine is correct als:

- R70-A nooit filtert op propositie
- R70-B functioneel classificeert zonder magnetische claims
- R71 capability detecteert zonder propositie-oordeel
- R73 hard exclusions altijd prevaleren
- R74 alleen categorie-specifieke diepte toevoegt
- elke uitsluiting een expliciete, traceerbare reden heeft

---

# 4. Commerciële Engine (R91–R92–R97–R190)

## 4.1 Doel

De Commerciële Engine zet een geselecteerd product om naar importklare waarheid met expliciete commerciële controle.

Zij borgt:

- vaste importstructuur (R91)
- reproduceerbare pricing- en marge-logica (R92)
- validatie en herstel van inconsistenties (R97)
- finale kwaliteitsbeslissing vóór livegang (R190)

Output: een dataset die technisch correct is én commercieel verdedigbaar.

---

## 4.2 R91 — Shopify Structuuranker (importwaarheid)

R91 definieert de waarheid voor import:

- verplichte kolommen en datatypes
- normalisatie van velden (titles, handles, vendors, tags)
- encoding regels (ASCII-only waar vereist)
- URL governance en consistentie
- mapping naar Shopify velden en metafields

R91 is leidend: downstream mag geen eigen kolommen “erbij verzinnen” buiten governance.

Minimale R91-successcriteria:

- elke kolom bestaat en is gevuld volgens regels
- geen verboden tekens / encoding issues
- consistente delimiter en quoting
- deterministische handle- en URL-opbouw
- verplichte metafields aanwezig waar governance dit vereist

---

## 4.3 R92 — Pricing & Margin Engine

R92 bepaalt prijs en marge op basis van:

- inkoopprijs
- verzendkosten en fulfilmentkosten (waar van toepassing)
- BTW/logistieke aannames (conform jouw governance)
- gewenste margedoelen per categorie/segment
- afrondingsregels (prijspsychologie / consistentie)

R92 is output-gedreven: het levert concrete velden (bijv. cost, selling price, margin metrics) en motiveert afwijkingen.

Minimale R92-successcriteria:

- prijs is reproduceerbaar (zelfde inputs → zelfde prijs)
- margeberekening is transparant en uitlegbaar
- uitzonderingen worden gelogd (niet stil toegepast)
- producten die marge niet halen worden gemarkeerd (NO-GO of review)

---

## 4.4 R97 — Validatie & Recovery

R97 detecteert en herstelt fouten vóór import, waaronder:

- ontbrekende verplichte velden
- inconsistenties in titles/handles/vendors
- encodingproblemen
- dubbele of conflicterende identifiers
- afwijkingen tussen productdata en Shopify-realiteit (in samenwerking met R72/R91)

R97 is geen “cosmetische fix”; het is een kwaliteitslaag:

- alles wat niet te herstellen is → expliciet gemarkeerd
- herstelacties worden gelogd (auditbaar)
- outputs worden gescheiden in GO/REVIEW/NO-GO categorieën

Minimale R97-successcriteria:

- elk defect wordt gedetecteerd of expliciet uitgesloten
- herstel is reproduceerbaar en traceerbaar
- geen stille wijzigingen zonder log

---

## 4.5 R190 — GO / NO-GO Gate (laatste autoriteit)

R190 is de finale gate voor livegang.

R190 kijkt minimaal naar:

- R91 schema compliance (structuur/encoding/kolommen)
- R92 marge/prijs compliance (business rules)
- R97 validatie status (fouten en recovery)
- Shopify-compatibiliteit (handles, templates, routing verankering)

Output is een expliciet besluit per product:

- GO → mag live
- REVIEW → vereist menselijke check
- NO-GO → uitgesloten met reden

Minimale R190-successcriteria:

- geen product gaat live zonder GO
- elke NO-GO heeft een expliciete reden
- gate is consistent (zelfde input → zelfde besluit)

---

## 4.6 Commerciële Engine: minimale KPI’s

De keten is commercieel gezond als:

- marge per categorie binnen targetband valt
- pricing geen extreme outliers produceert zonder logging
- importbestanden “clean” zijn (geen encoding/structuur issues)
- GO-rate stijgt door betere upstream selectie (R70–R74)
- REVIEW-rate beheersbaar blijft (geen bottleneck)
---
# 5. Content & UX Engine (R150–R152–R170+)

## 5.1 Doel

De Content & UX Engine borgt dat:

- De winkel consistent en professioneel oogt
- De structuur schaalbaar blijft
- SEO correct wordt toegepast
- Conversieprincipes consistent zijn
- De UX geen tegenstrijdige signalen geeft

Deze laag vertaalt technisch correcte data naar een commercieel sterke presentatie.

---

## 5.2 R150 — Content Governance

R150 definieert regels voor:

- Producttitelopbouw
- Meta title (≤ 70 tekens)
- Meta description (≤ 170 tekens)
- ASCII-only waar vereist
- Verboden tekens / encodingcontrole
- Body-structuur (koppen, bullets, scanbaarheid)
- Micro-USP en subregels
- Geen overdreven claims
- Geen inconsistent taalgebruik

R150 is geen copywriting-suggestie.  
R150 is een harde kwaliteitslaag.

Minimale R150-successcriteria:

- Geen encoding- of formattingproblemen
- SEO-limieten worden gerespecteerd
- Geen inconsistentie tussen titel, meta en body
- Elke productpagina is scanbaar en logisch opgebouwd

---

## 5.3 R151 — Collectie-Architectuur

R151 definieert:

- Hoofdhubstructuur
- Subcollecties
- Navigatielogica
- Interne routing
- Geen dubbele collectieposities
- Consistente naamgeving

De homepage bevat vaste kolommen (canoniek):

1. Opladen  
2. Onderweg  
3. Werkplek & Thuis  
4. Accessoires  

Deze structuur is niet optioneel.

R151 borgt dat:

- Elke productgroep logisch gepositioneerd is
- Geen wildcard-collecties ontstaan
- UX consistent schaalbaar blijft

---

## 5.4 R152 — Collection Registry (Single Source of Truth)

R152 is de bindende registry voor alle collecties.

Per collectie worden vaste velden vastgelegd:

- collection_title_nl
- collection_handle
- collection_type_value
- collection_subtype_value
- condition_operator
- theme_template_assigned
- seo_title_nl
- meta_description_nl
- hero_image_present
- notes_routing

R152 is leidend.

Templates, hubkoppelingen en routing mogen alleen via R152 worden aangepast.

Minimale R152-successcriteria:

- Geen collectie zonder registry entry
- Template altijd expliciet benoemd
- SEO titel ≤ 70 tekens
- Meta description ≤ 170 tekens
- Hubstructuur consistent

---

## 5.5 R170–R173 — UX, CRO & Theme Governance

Deze regels definiëren:

- Core Web Vitals als conversiehefboom
- Trust signalering vóór scroll
- Duidelijke informatie-hiërarchie
- Scanbare blokken
- Eén primaire taak per sectie
- Sticky add-to-cart op mobiel
- Snelle betaalopties (Shop Pay / Apple Pay / PayPal)
- AI alleen ondersteunend (geen ruis)

UX is geen design-experiment.
Het is een conversie-engine.

Minimale UX-successcriteria:

- Homepage volgt 4-kolommen canon
- Hubkaarten bevatten vaste structuur
- Geen visuele ruis
- Mobiel is leidend
- Checkout friction minimaal

---

## 5.6 Content & UX Integriteitsregels

De Content & UX Engine functioneert correct als:

- Copy consistent is met propositie (R73)
- Collectie-routing aansluit op R152
- Pricing logisch is geïntegreerd
- Geen conflicterende signalen bestaan tussen hubs
- De visuele rust overeenkomt met premium-positionering

Content mag nooit selectie- of pricing-logica overrulen.

---
# 6. Governance & Directielaag

## 6.1 Doel

De Governance & Directielaag borgt dat:

- Het systeem bestuurbaar blijft
- Beslissingen niet impliciet maar expliciet zijn
- AI-automatisering gecontroleerd plaatsvindt
- Regelwijzigingen traceerbaar zijn
- De DGA eindverantwoordelijkheid behoudt

Deze laag voorkomt drift, wildgroei en ongecontroleerde uitbreiding.

---

## 6.2 Canonieke hiërarchie

Binnen MagneticPower geldt de volgende beslissingsvolgorde:

1. Repository (technische implementatie)  
2. MP-ROS (bestuurlijke waarheid)  
3. Canonieke Regels (R70–R190)  
4. Collection Registry (R152)  
5. GO/NO-GO Gate (R190)  

Er bestaan geen uitzonderingen buiten deze hiërarchie.

---

## 6.3 Regelbeheer (Change Control)

Elke wijziging aan:

- Een R-regel
- De selectiecriteria (R73)
- Pricinglogica (R92)
- Importstructuur (R91)
- UX-canon (R170+)
- Hubstructuur (R151/152)

Moet voldoen aan:

1. Expliciete wijziging in repository  
2. Logvermelding in Changelogs  
3. Eventuele update in MP-ROS  
4. Geen stille aanpassing in scripts  

Wijzigingen zonder logging zijn ongeldig.

---

## 6.4 AI-rolafbakening

AI mag:

- Data classificeren binnen vastgestelde regels
- Pricing berekenen volgens R92
- Content structureren volgens R150
- Validatie uitvoeren volgens R97
- Rapportage genereren

AI mag niet:

- Regels wijzigen
- Hard exclusions overrulen
- Nieuwe categorieën creëren
- Governance-structuur aanpassen
- Livegangbeslissingen zelfstandig nemen zonder R190

---

## 6.5 Directiecontrolepunten

De DGA controleert minimaal:

- Margebandbreedte per categorie
- GO/NO-GO ratio
- Percentage MAYBE_STRONG (R73)
- Review-rate uit R97
- Aantal manual overrides (moet minimaal blijven)
- Core Web Vitals status
- Hubstructuur consistentie

Indien afwijking structureel is → systeemwijziging vereist.

---

## 6.6 Escalatie-structuur

Indien een product of regel twijfel veroorzaakt:

1. Controleer R70-B classificatie
2. Controleer R73 fit
3. Controleer R91 schema
4. Controleer R92 marge
5. Toets aan MP-ROS kernprincipes

Pas daarna mag escalatie plaatsvinden.

Geen ad-hoc beslissingen buiten ketenlogica.

---

## 6.7 Minimale Governance-Successcriteria

De Governance-laag functioneert correct als:

- Geen dubbele canonieke documenten bestaan
- Elke regel een vaste plek heeft
- Elke wijziging traceerbaar is
- Er geen stille uitzonderingen bestaan
- Repo en MP-ROS synchroon blijven
- Archief geen sturende rol heeft

---

## 6.8 Stabiliteitsprincipe

MagneticPower groeit alleen door:

- Nieuwe producten binnen bestaande structuur
- Verbetering van regels
- Optimalisatie van pricing
- Versterking van UX
- Verbetering van data-kwaliteit

Niet door:

- Verbreding zonder selectie
- Verzwakking van exclusions
- Toestaan van randgevallen buiten propositie

---

De Governance & Directielaag is het controlecentrum van het systeem.

# 7. Operations & Risicobeheer

## 7.1 Doel

De Operations & Risicobeheer-laag borgt dat:

- De winkel technisch stabiel draait
- Klantverwachtingen worden waargemaakt
- Financiële stromen correct worden verwerkt
- Juridische en compliance-risico’s beheerst blijven
- Performance en conversie actief worden bewaakt

Deze laag vertaalt systeemlogica naar dagelijkse bedrijfsvoering.

---

## 7.2 Livegangcontrole (Pre-Launch Checklist)

Voor elke structurele wijziging (nieuwe collectie, template, bulkimport, prijsupdate) geldt een minimale controle:

- HTTPS actief, geen mixed content
- Geen test- of dummycollecties zichtbaar
- Collectie-routing conform R152
- SEO-titels ≤ 70 tekens
- Meta-descriptions ≤ 170 tekens
- Encoding foutloos (geen rare tekens)
- Trust-signalen zichtbaar vóór scroll
- Mobiele weergave gecontroleerd (Android/Samsung S23)
- Checkout test succesvol (incl. Shop Pay / Apple Pay / PayPal waar actief)

Geen vink = geen livegang.

---

## 7.3 Checkout & Betalingsverwerking

Minimale vereisten:

- Frictionless checkout
- Snelle betaalopties actief (Shop Pay / Apple Pay / PayPal waar mogelijk)
- Geen overbodige velden
- Orderbevestiging correct
- BTW-berekening correct
- Synchronisatie met boekhouding consistent

Testscenario’s:

1. Testorder lage prijs  
2. Testorder hoge prijs  
3. Test met kortingscode  
4. Test retourverwerking  
5. Test mislukte betaling  

Elke test wordt minimaal 1× per structurele wijziging uitgevoerd.

---

## 7.4 Levering & Retour

Verplicht zichtbaar vóór scroll:

- Levertijd
- Verzendkosten
- Retourtermijn
- Garantiebeleid
- Contactmogelijkheid

Risicobeheersing:

- Geen onduidelijke levertijden
- Geen verborgen kosten
- Geen vage retourvoorwaarden
- Klantcommunicatie consistent

---

## 7.5 Boekhouding & Financiële Controle

Minimale controlepunten:

- Betalingsproviders correct gekoppeld
- BTW juist geboekt
- Debiteurenrekeningen correct
- Transacties consistent met Shopify-orders
- Periodieke controle van marge vs. R92 output

Financiële afwijking → escalatie naar Governance-laag.

---

## 7.6 Performance & Conversie Monitoring

Wordt periodiek gecontroleerd op:

- Core Web Vitals
- Paginasnelheid mobiel
- Add-to-cart ratio
- Checkout completion rate
- Bounce rate op hubs
- Review-ratio uit R97

Structurele daling → UX-audit verplicht.

---

## 7.7 Risicocategorieën

### Technisch risico
- Scriptfouten
- Encodingproblemen
- Importafwijkingen
- Template-conflicten

### Commercieel risico
- Te lage marge
- Verkeerde prijspositionering
- Onjuiste categorie-indeling

### Juridisch risico
- Onvolledige productinformatie
- Onjuiste contactgegevens
- Onduidelijke voorwaarden

### Operationeel risico
- Niet-synchroniserende boekhouding
- Ongeteste betaalflow
- Ongeteste retourprocedure

Alle risico’s vallen terug op R190 indien impact op livegang.

---

## 7.8 Minimale Operationele Succescriteria

Operations functioneren correct als:

- Geen structurele checkoutfouten
- Geen massale R97 validatiefouten
- Geen conflicten tussen collectie en template
- Geen openstaande kritieke changelog-items
- Financiële data sluit aan bij Shopify-werkelijkheid
- Performance binnen acceptabele bandbreedte blijft

---

## 7.9 Continuïteitsprincipe

Het systeem blijft stabiel wanneer:

- Regels niet ad-hoc worden aangepast
- Releases gecontroleerd plaatsvinden
- Elke wijziging commit-gedreven is
- Archief geen actieve rol krijgt
- MP-ROS en repo synchroon blijven

Operations zijn uitvoerend; governance blijft leidend.


