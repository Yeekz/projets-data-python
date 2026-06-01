# Projet 3 — Pipeline de consolidation de donnees multi-formats

Mini-ETL : lire plusieurs formats, nettoyer, fusionner, exporter.

## Sources (`sources/`)
- `clients.json` — referentiel clients (avec un segment manquant).
- `ventes.csv`   — ventes (avec un doublon et un montant manquant).
- `budget.xlsx`  — budget par segment.

## Etapes (E-T-L)
1. **Extract** : `read_json`, `read_csv`, `read_excel`.
2. **Transform** : `drop_duplicates`, `fillna` (valeurs manquantes), jointures `merge`.
3. **Load** : export CSV + Excel + indicateur CA par segment.

## Lancer
```bash
python pipeline.py
```

## A savoir expliquer
- Pourquoi nettoyer : des doublons faussent les totaux, les valeurs manquantes
  cassent les calculs. On choisit une strategie (supprimer / combler / imputer).
- `merge` = jointure SQL en pandas (`how='left'` garde toutes les ventes).
