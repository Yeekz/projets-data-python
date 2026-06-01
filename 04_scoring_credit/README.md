# Projet 4 — Scoring de risque de credit PME

Notation interne du risque de credit a partir de ratios financiers, avec
classes de risque (A a D) et scenario de stress.

## Donnees
`pme.csv` — 5 PME, 4 ratios : liquidite, endettement, marge nette, croissance du CA.

## Methode
1. **Normalisation contre des bornes fixes** (references metier) : chaque ratio
   est ramene entre 0 et 1 avec clipping (l'endettement est inverse : faible = bon).
   Avantage vs min-max : le score reste comparable dans le temps et le stress
   test fait reellement bouger les notes.
2. **Score pondere** (0-100) selon des poids metier.
3. **Classe de risque** A/B/C/D via `pd.cut`.
4. **Stress test** : on degrade marge et croissance, on recalcule.
5. **Recommandation** credit accorde / a etudier.

## Lancer
```bash
python scoring.py
```

## A savoir expliquer
- Le scoring transforme plusieurs indicateurs en une note unique comparable.
- La normalisation evite qu'un ratio a grande echelle ecrase les autres.
- Le stress test mesure la resilience : qui bascule en classe a risque si la
  conjoncture se degrade ?
