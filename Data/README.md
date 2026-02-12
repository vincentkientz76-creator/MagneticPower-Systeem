# Data – Overzicht & Doel

Deze map bevat alle ruwe en verrijkte databronnen die worden gebruikt binnen het MagneticPower‑systeem.  
Data is nooit leidend; het ondersteunt de regels R70–R99 en de commerciële governance (R92, R190).

## Structuur

- **BigBuy/** – Leveranciersdata (ZIP/XML/CSV)
- **Eprolo/** – Leveranciersdata (CSV/JSON)
- **Marketdata/** – DataForSEO + prijsobservaties
- **Exports/** – Uitvoerbestanden uit R70–R99

## Governance

- Data wordt nooit handmatig aangepast.
- Elke dataset moet herleidbaar zijn tot bron + timestamp.
- Alleen FINAL‑bestanden worden gebruikt voor Shopify (via R91).

## Relatie met regels

- R70A: extractie van BigBuy
- R73: marktdata
- R92: prijsstrategie
- R121: management & monitoring
