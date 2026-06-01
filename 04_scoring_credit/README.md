# Scoring de risque de crédit PME

Devoir réalisé pour le cours de **gestion des risques** (NEOMA). On note des PME
de 0 à 100 à partir de leurs ratios financiers, on les classe (A à D), et on
teste leur résistance à un scénario défavorable.

## Fichiers

- `scoring_credit.py` — le script de scoring
- `pme.csv` — les données (5 PME, 4 ratios)
- `methodologie.md` — la démarche détaillée (notation, poids, classes, stress test)

## Lancer

```bash
python scoring_credit.py
```

Le script affiche le scoring de base puis le stress test, et enregistre
`resultats_scoring.csv`.

👉 Voir **methodologie.md** pour les choix de modélisation et leurs limites.
