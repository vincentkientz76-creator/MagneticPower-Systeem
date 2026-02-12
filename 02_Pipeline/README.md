## 02_Pipeline — Automatisering & Datastromen

Deze map bevat alle pipeline‑logica die het MagneticPower Systeem uitvoert.  
De pipeline is deterministisch: elke stap volgt uit de vorige, zonder interpretatie.

## Pipeline‑flow

1. **R70A** — Extractie van BigBuy/Eprolo
2. **R70B** — Function Classifier
3. **R71** — Magnetische detectie
4. **R72** — Shopify reality anchor
5. **R73** — Marktdata verrijking
6. **R74–R79** — Specialist‑agents
7. **R92** — Prijsstrategie
8. **R97** — Inhoudelijke validatie
9. **R190** — Governance
10. **R91** — Shopify import

## Inhoud van deze map

- **input/** — ruwe data
- **output/** — pipeline‑resultaten
- **automation/** — scripts
- **templates/** — content‑ en data‑templates

## Doel van deze map

- Automatisering van productselectie
- Automatisering van pricing
- Automatisering van import
- Reproduceerbare runs
- Audit‑vriendelijke structuur
