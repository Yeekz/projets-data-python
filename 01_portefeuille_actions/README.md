# Projet 1 — Analyse de portefeuille d'actions

Analyse de la performance et du risque d'un portefeuille a partir d'un historique
de prix.

## Donnees
`prix_actions.csv` — 252 jours de cotation, 4 actions (AAPL, MSFT, MC.PA, AIR.PA).

## Ce que fait le script
1. Charge et valide le CSV avec **pandas**.
2. Calcule les **rendements quotidiens**, le rendement et la volatilite annualises,
   et le **ratio de Sharpe** (NumPy).
3. Calcule la **matrice de correlation** des rendements.
4. Valorise un portefeuille pondere (base 100).
5. Exporte un **rapport Excel** multi-onglets + un **graphique PNG**.

## Lancer
```bash
python analyse_portefeuille.py
```

## Notions cles a savoir expliquer
- Rendement quotidien = (P_t / P_t-1) - 1  → `pct_change()`
- Annualisation : x252 (jours de bourse), volatilite x √252
- Ratio de Sharpe = (rendement - taux sans risque) / volatilite → rendement par
  unite de risque. Plus il est eleve, mieux c'est.
- Correlation proche de 1 = les actions bougent ensemble (peu de diversification).
