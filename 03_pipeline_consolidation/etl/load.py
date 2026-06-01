"""Etape LOAD : calcul d'indicateurs et export des resultats."""
from __future__ import annotations

import logging

import pandas as pd

import config

logger = logging.getLogger(__name__)


def kpi_ca_par_segment(consolide: pd.DataFrame) -> pd.Series:
    """Chiffre d'affaires total par segment, trie par ordre decroissant."""
    return (consolide.groupby("segment")["montant"]
            .sum()
            .sort_values(ascending=False)
            .round(2))


def exporter(consolide: pd.DataFrame, ca_segment: pd.Series) -> None:
    """Ecrit le jeu consolide (CSV + Excel) dans le dossier output/."""
    config.OUTPUT_DIR.mkdir(exist_ok=True)

    chemin_csv = config.OUTPUT_DIR / "donnees_consolidees.csv"
    consolide.to_csv(chemin_csv, index=False)

    chemin_xlsx = config.OUTPUT_DIR / "donnees_consolidees.xlsx"
    with pd.ExcelWriter(chemin_xlsx) as writer:
        consolide.to_excel(writer, sheet_name="Detail", index=False)
        ca_segment.to_frame("CA").to_excel(writer, sheet_name="CA_segment")

    logger.info("Exports ecrits dans %s", config.OUTPUT_DIR.name)
