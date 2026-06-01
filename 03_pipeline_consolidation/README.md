# Pipeline de consolidation de données (ETL)

Pipeline qui consolide trois sources hétérogènes (**JSON**, **CSV**, **Excel**) en
un jeu de données propre et exploitable. Code organisé en modules, avec
journalisation (`logging`) et annotations de types.

## Architecture

```
03_pipeline_consolidation/
├── run.py              # orchestration (point d'entrée)
├── config.py           # chemins et paramètres
├── etl/
│   ├── extract.py      # lecture JSON / CSV / Excel
│   ├── transform.py    # dédoublonnage, valeurs manquantes, jointures
│   └── load.py         # KPI + export CSV/Excel
└── sources/            # données d'entrée
```

Découpage volontaire en **Extract / Transform / Load** : chaque étape est isolée,
testable et remplaçable.

## Lancer

```bash
python run.py
```

Sortie attendue (extrait des logs) :

```
INFO | etl.extract   | Sources lues : 4 clients, 6 ventes, 2 lignes de budget
INFO | etl.transform | Doublons de ventes supprimes : 1
INFO | etl.transform | Montants manquants combles : 1
INFO | pipeline      | Pipeline termine avec succes
```

Les fichiers consolidés sont écrits dans `output/`.

## Choix techniques

- **`logging`** plutôt que `print` : niveaux, horodatage, traçabilité.
- **Annotations de types** sur toutes les fonctions publiques.
- **Jointures à gauche** (`how="left"`) pour ne perdre aucune vente.
