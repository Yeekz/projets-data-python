"""Etape EXTRACT : lecture des sources heterogenes (JSON, CSV, Excel)."""
from __future__ import annotations

import logging

import pandas as pd

import config

logger = logging.getLogger(__name__)


def lire_sources() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Charge les trois sources et renvoie (clients, ventes, budget).

    Returns:
        Un triplet de DataFrames bruts, non nettoyes.
    """
    clients = pd.read_json(config.CLIENTS_JSON)
    ventes = pd.read_csv(config.VENTES_CSV, parse_dates=["date"])
    budget = pd.read_excel(config.BUDGET_XLSX)

    logger.info("Sources lues : %d clients, %d ventes, %d lignes de budget",
                len(clients), len(ventes), len(budget))
    return clients, ventes, budget
