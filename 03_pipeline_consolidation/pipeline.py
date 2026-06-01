# -*- coding: utf-8 -*-
"""
Projet 3 — Pipeline de consolidation de donnees multi-formats
-------------------------------------------------------------
Lit 3 sources heterogenes (JSON, CSV, Excel), les nettoie, les fusionne,
puis exporte un jeu de donnees consolide (CSV + Excel).

Lancer :  python pipeline.py
"""
from pathlib import Path
import pandas as pd

ICI = Path(__file__).parent
SRC = ICI / "sources"


def lire_sources():
    """Charge les 3 formats avec le bon lecteur pandas."""
    clients = pd.read_json(SRC / "clients.json")
    ventes = pd.read_csv(SRC / "ventes.csv", parse_dates=["date"])
    budget = pd.read_excel(SRC / "budget.xlsx")
    return clients, ventes, budget


def nettoyer(clients, ventes):
    """Supprime doublons, gere les valeurs manquantes."""
    avant = len(ventes)
    ventes = ventes.drop_duplicates(subset="vente_id")          # doublon vente_id=3
    print(f"Doublons supprimes : {avant - len(ventes)}")

    # Montant manquant -> 0 (ou on pourrait l'exclure / imputer la moyenne)
    nb_na = int(ventes["montant"].isna().sum())
    ventes["montant"] = ventes["montant"].fillna(0.0)
    print(f"Montants manquants combles : {nb_na}")

    # Segment manquant -> 'Inconnu'
    clients["segment"] = clients["segment"].fillna("Inconnu")
    return clients, ventes


def consolider(clients, ventes, budget):
    """Jointures : ventes -> clients -> budget par segment."""
    df = (ventes
          .merge(clients, on="client_id", how="left")
          .merge(budget, on="segment", how="left"))
    return df


def main():
    clients, ventes, budget = lire_sources()
    clients, ventes = nettoyer(clients, ventes)
    df = consolider(clients, ventes, budget)

    # Indicateur : CA par segment
    ca_segment = (df.groupby("segment")["montant"].sum()
                    .sort_values(ascending=False).round(2))
    print("\n=== CA par segment ===")
    print(ca_segment, "\n")

    df.to_csv(ICI / "donnees_consolidees.csv", index=False)
    with pd.ExcelWriter(ICI / "donnees_consolidees.xlsx") as xls:
        df.to_excel(xls, sheet_name="Detail", index=False)
        ca_segment.to_frame("CA").to_excel(xls, sheet_name="CA_segment")
    print("Exports ecrits : donnees_consolidees.csv / .xlsx")


if __name__ == "__main__":
    main()
