# -*- coding: utf-8 -*-
"""
Projet 4 — Scoring de risque de credit PME
-------------------------------------------
Calcule un score de risque (0-100) a partir de ratios financiers,
classe chaque PME (A/B/C/D) et applique un scenario de stress.

Lancer :  python scoring.py
"""
from pathlib import Path
import numpy as np
import pandas as pd

ICI = Path(__file__).parent

# Poids de chaque critere dans le score (somme = 1). Choix "metier".
POIDS = {
    "ratio_liquidite":   0.30,   # plus c'est haut, mieux c'est
    "ratio_endettement": 0.30,   # plus c'est bas, mieux c'est (inverse)
    "marge_nette":       0.25,   # plus c'est haut, mieux c'est
    "croissance_ca":     0.15,   # plus c'est haut, mieux c'est
}

# Bornes de reference FIXES (pas relatives a l'echantillon) : un (min, max)
# par ratio. On note chaque PME contre ces references "metier", ce qui rend
# le score comparable dans le temps et le stress test reellement parlant.
BORNES = {
    "ratio_liquidite":   (0.5, 2.5),    # < 0.5 mauvais, > 2.5 excellent
    "ratio_endettement": (0.2, 0.9),    # inverse : 0.2 excellent, 0.9 mauvais
    "marge_nette":       (-0.05, 0.20),
    "croissance_ca":     (-0.10, 0.15),
}


def normaliser(serie: pd.Series, mini: float, maxi: float,
               inverse: bool = False) -> pd.Series:
    """Ramene une colonne entre 0 et 1 contre des bornes fixes (avec clipping).
    inverse=True : une petite valeur est bonne (ex : endettement)."""
    norme = ((serie - mini) / (maxi - mini)).clip(0, 1)
    return 1 - norme if inverse else norme


def calculer_score(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["s_liquidite"]   = normaliser(df["ratio_liquidite"],   *BORNES["ratio_liquidite"])
    df["s_endettement"] = normaliser(df["ratio_endettement"], *BORNES["ratio_endettement"], inverse=True)
    df["s_marge"]       = normaliser(df["marge_nette"],       *BORNES["marge_nette"])
    df["s_croissance"]  = normaliser(df["croissance_ca"],     *BORNES["croissance_ca"])

    df["score"] = (
        df["s_liquidite"]   * POIDS["ratio_liquidite"] +
        df["s_endettement"] * POIDS["ratio_endettement"] +
        df["s_marge"]       * POIDS["marge_nette"] +
        df["s_croissance"]  * POIDS["croissance_ca"]
    ) * 100

    # Classe de risque a partir du score
    df["classe"] = pd.cut(df["score"], bins=[-1, 25, 50, 75, 101],
                          labels=["D (eleve)", "C", "B", "A (faible)"])
    return df.round(2)


def stress_test(df: pd.DataFrame) -> pd.DataFrame:
    """Scenario adverse : -30 % de marge et -10 pts de croissance."""
    stresse = df.copy()
    stresse["marge_nette"] = stresse["marge_nette"] * 0.70
    stresse["croissance_ca"] = stresse["croissance_ca"] - 0.10
    return calculer_score(stresse)[["entreprise", "score", "classe"]]


def main():
    df = pd.read_csv(ICI / "pme.csv")
    note = calculer_score(df)

    print("=== Scoring de base ===")
    print(note[["entreprise", "score", "classe"]].to_string(index=False), "\n")

    stress = stress_test(df)
    print("=== Apres stress test (-30% marge, -10pts croissance) ===")
    print(stress.to_string(index=False), "\n")

    # Recommandation simple
    note["recommandation"] = np.where(
        note["score"] >= 50, "Credit accorde", "Garanties / refus a etudier")
    note.to_csv(ICI / "resultats_scoring.csv", index=False)
    print("Resultats ecrits -> resultats_scoring.csv")


if __name__ == "__main__":
    main()
