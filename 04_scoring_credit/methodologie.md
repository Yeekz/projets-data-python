# Méthodologie — scoring de risque de crédit PME

> Document rédigé pour accompagner le devoir (cours de gestion des risques, NEOMA).

## 1. Objectif

Construire un **score interne** simple permettant de hiérarchiser des PME selon
leur risque de crédit, à partir d'informations financières de base. Le but
n'est pas un modèle statistique sophistiqué, mais une grille de lecture claire
et défendable.

## 2. Les quatre critères retenus

| Critère | Ratio | Interprétation |
|--------|-------|----------------|
| Liquidité | actif court terme / passif court terme | capacité à payer à court terme |
| Endettement | dettes / actifs | poids de la dette (à minimiser) |
| Marge nette | résultat net / chiffre d'affaires | rentabilité |
| Croissance | variation du chiffre d'affaires | dynamique |

## 3. Notation

Chaque ratio est ramené sur une échelle **0 → 1** par rapport à des bornes de
référence (ce qu'on considère faible / solide pour une PME). L'endettement est
**inversé** : une dette faible doit donner une bonne note.

> Choix assumé : des bornes **fixes** (et non un min-max sur l'échantillon).
> Avantage : le score reste comparable d'une entreprise à l'autre et dans le
> temps, et le stress test fait réellement bouger les notes.

## 4. Score global et classes

Score = moyenne **pondérée** des quatre notes (× 100).
Poids : liquidité 30 %, endettement 30 %, marge 25 %, croissance 15 %.
La solvabilité court terme pèse donc le plus.

| Score | Classe | Lecture |
|------|--------|---------|
| ≥ 75 | A | risque faible |
| 50–74 | B | risque modéré |
| 25–49 | C | risque élevé |
| < 25 | D | risque très élevé |

## 5. Stress test

On simule un scénario défavorable (marge −30 %, croissance −10 points) et on
recalcule les scores. Cela révèle quelles entreprises basculent vers une classe
plus risquée si la conjoncture se dégrade.

## 6. Limites

- Échantillon réduit et ratios simplifiés.
- Poids choisis à dire d'expert, non calibrés sur un historique de défauts.
- Un vrai modèle utiliserait une régression logistique sur des données de défaut.
