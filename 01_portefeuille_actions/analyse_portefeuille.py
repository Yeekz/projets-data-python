# -*- coding: utf-8 -*-
"""
Projet 1 — Analyse de portefeuille d'actions
--------------------------------------------
Charge un historique de prix (CSV), calcule les indicateurs cles de performance
et de risque d'un portefeuille, puis exporte un rapport Excel + un graphique.

Lancer :  python analyse_portefeuille.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")            # backend sans fenetre (sauvegarde fichier)
import matplotlib.pyplot as plt

ICI = Path(__file__).parent
JOURS_BOURSE = 252               # nb de jours de cotation dans une annee
TAUX_SANS_RISQUE = 0.02          # 2 % annuel (pour le ratio de Sharpe)

# Poids du portefeuille (doivent sommer a 1)
POIDS = {"AAPL": 0.30, "MSFT": 0.30, "MC.PA": 0.20, "AIR.PA": 0.20}


def charger_prix(chemin_csv: Path) -> pd.DataFrame:
    """Lit le CSV des prix, indexe par date, valide les colonnes attendues."""
    df = pd.read_csv(chemin_csv, parse_dates=["Date"], index_col="Date")
    manquantes = set(POIDS) - set(df.columns)
    if manquantes:
        raise ValueError(f"Colonnes manquantes dans le CSV : {manquantes}")
    return df.sort_index()


def calculer_indicateurs(prix: pd.DataFrame) -> pd.DataFrame:
    """Rendement annualise, volatilite annualisee et ratio de Sharpe par action."""
    rendements = prix.pct_change().dropna()                 # rendements quotidiens
    rdt_annuel = (1 + rendements.mean()) ** JOURS_BOURSE - 1
    vol_annuelle = rendements.std() * np.sqrt(JOURS_BOURSE)
    sharpe = (rdt_annuel - TAUX_SANS_RISQUE) / vol_annuelle
    return pd.DataFrame({
        "Rendement annualise": rdt_annuel,
        "Volatilite annualisee": vol_annuelle,
        "Ratio de Sharpe": sharpe,
    }).round(4)


def valoriser_portefeuille(prix: pd.DataFrame) -> pd.Series:
    """Valeur d'un portefeuille base 100 a partir des poids cibles."""
    base = prix / prix.iloc[0]                              # normalise a 1
    poids = pd.Series(POIDS)
    return (base[list(POIDS)] * poids).sum(axis=1) * 100


def main():
    prix = charger_prix(ICI / "prix_actions.csv")
    indic = calculer_indicateurs(prix)
    valo = valoriser_portefeuille(prix)
    correl = prix.pct_change().corr().round(3)

    print("=== Indicateurs par action ===")
    print(indic, "\n")
    print("=== Matrice de correlation des rendements ===")
    print(correl, "\n")
    print(f"Valeur finale du portefeuille (base 100) : {valo.iloc[-1]:.2f}")
    perf = valo.iloc[-1] - 100
    print(f"Performance sur la periode : {perf:+.2f} %")

    # --- Rapport Excel (plusieurs onglets) ---
    sortie_xlsx = ICI / "rapport_portefeuille.xlsx"
    with pd.ExcelWriter(sortie_xlsx) as xls:
        indic.to_excel(xls, sheet_name="Indicateurs")
        correl.to_excel(xls, sheet_name="Correlations")
        valo.round(2).to_frame("Valeur portefeuille").to_excel(xls, sheet_name="Valorisation")
    print(f"\nRapport Excel ecrit -> {sortie_xlsx.name}")

    # --- Graphique de la valorisation ---
    plt.figure(figsize=(9, 4.5))
    valo.plot(color="#102844", linewidth=1.8)
    plt.title("Valorisation du portefeuille (base 100)")
    plt.ylabel("Valeur")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    sortie_png = ICI / "valorisation_portefeuille.png"
    plt.savefig(sortie_png, dpi=120)
    print(f"Graphique ecrit          -> {sortie_png.name}")


if __name__ == "__main__":
    main()
