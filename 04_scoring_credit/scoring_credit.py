# -*- coding: utf-8 -*-
#
# Scoring de risque de credit - PME
# Devoir realise dans le cadre du cours de gestion des risques (NEOMA).
#
# Idee : a partir de quelques ratios financiers, attribuer a chaque entreprise
# une note de 0 a 100 (100 = tres bon profil) puis une classe de risque.
# On termine par un test de resistance (stress test).
#
# Yacine Ouasti

import pandas as pd


# --- Parametres du modele ---------------------------------------------------
#
# Chaque ratio est note entre 0 et 1 par rapport a des bornes de reference
# (issues de ce qu'on considere "normal" pour une PME). On combine ensuite
# ces notes avec des poids. Les poids refletent l'importance qu'on accorde
# a chaque critere : la solvabilite court terme (liquidite, endettement)
# pese plus que la croissance.

POIDS = {
    "liquidite":   0.30,   # capacite a honorer les dettes a court terme
    "endettement": 0.30,   # niveau de dette (plus c'est bas, mieux c'est)
    "marge":       0.25,   # rentabilite
    "croissance":  0.15,   # dynamique du chiffre d'affaires
}

# (borne_basse, borne_haute) pour ramener chaque ratio entre 0 et 1.
BORNES = {
    "liquidite":   (0.5, 2.5),
    "endettement": (0.2, 0.9),
    "marge":       (-0.05, 0.20),
    "croissance":  (-0.10, 0.15),
}


def noter_ratio(valeur, borne_basse, borne_haute, inverser=False):
    """Ramene un ratio entre 0 et 1.

    On fait une regle de trois bornee : en dessous de borne_basse -> 0,
    au dessus de borne_haute -> 1. Si inverser=True, c'est l'inverse
    (utile pour l'endettement : une dette faible doit donner une bonne note).
    """
    note = (valeur - borne_basse) / (borne_haute - borne_basse)
    note = max(0.0, min(1.0, note))     # on borne dans [0, 1]
    if inverser:
        note = 1 - note
    return note


def calculer_score(ligne):
    """Calcule le score /100 d'une entreprise (une ligne du tableau)."""
    note_liquidite   = noter_ratio(ligne["ratio_liquidite"],   *BORNES["liquidite"])
    note_endettement = noter_ratio(ligne["ratio_endettement"], *BORNES["endettement"], inverser=True)
    note_marge       = noter_ratio(ligne["marge_nette"],       *BORNES["marge"])
    note_croissance  = noter_ratio(ligne["croissance_ca"],     *BORNES["croissance"])

    score = (note_liquidite   * POIDS["liquidite"]
             + note_endettement * POIDS["endettement"]
             + note_marge       * POIDS["marge"]
             + note_croissance  * POIDS["croissance"])
    return round(score * 100, 1)


def classe_de_risque(score):
    """Traduit un score en classe de risque (A = faible, D = eleve)."""
    if score >= 75:
        return "A"
    elif score >= 50:
        return "B"
    elif score >= 25:
        return "C"
    else:
        return "D"


def main():
    pme = pd.read_csv("pme.csv")

    # On applique le scoring ligne par ligne (volontairement lisible :
    # une PME = une ligne, comme on raisonnerait a la main).
    pme["score"] = pme.apply(calculer_score, axis=1)
    pme["classe"] = pme["score"].apply(classe_de_risque)

    print("=== Scoring des PME ===")
    print(pme[["entreprise", "score", "classe"]].to_string(index=False))

    # --- Stress test --------------------------------------------------------
    # Scenario defavorable : la marge baisse de 30 % et la croissance perd
    # 10 points. On regarde comment les scores evoluent.
    print("\n=== Stress test (marge -30 %, croissance -10 pts) ===")
    pme_stress = pme.copy()
    pme_stress["marge_nette"] = pme_stress["marge_nette"] * 0.70
    pme_stress["croissance_ca"] = pme_stress["croissance_ca"] - 0.10
    pme_stress["score"] = pme_stress.apply(calculer_score, axis=1)
    pme_stress["classe"] = pme_stress["score"].apply(classe_de_risque)
    print(pme_stress[["entreprise", "score", "classe"]].to_string(index=False))

    pme.to_csv("resultats_scoring.csv", index=False)
    print("\nResultats sauvegardes dans resultats_scoring.csv")


if __name__ == "__main__":
    main()
