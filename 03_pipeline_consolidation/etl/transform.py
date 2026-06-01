"""Etape TRANSFORM : nettoyage et fusion des donnees."""
from __future__ import annotations

import logging

import pandas as pd

import config

logger = logging.getLogger(__name__)


def nettoyer(clients: pd.DataFrame, ventes: pd.DataFrame
             ) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Supprime les doublons et comble les valeurs manquantes.

    Args:
        clients: referentiel clients brut.
        ventes: ventes brutes (peuvent contenir doublons et NaN).

    Returns:
        Les deux DataFrames nettoyes.
    """
    nb_doublons = int(ventes.duplicated(subset="vente_id").sum())
    ventes = ventes.drop_duplicates(subset="vente_id").copy()
    logger.info("Doublons de ventes supprimes : %d", nb_doublons)

    nb_montants_na = int(ventes["montant"].isna().sum())
    ventes["montant"] = ventes["montant"].fillna(config.MONTANT_PAR_DEFAUT)
    logger.info("Montants manquants combles : %d", nb_montants_na)

    clients = clients.copy()
    clients["segment"] = clients["segment"].fillna(config.VALEUR_SEGMENT_INCONNU)
    return clients, ventes


def consolider(clients: pd.DataFrame, ventes: pd.DataFrame,
               budget: pd.DataFrame) -> pd.DataFrame:
    """Fusionne ventes -> clients -> budget via des jointures a gauche."""
    consolide = (
        ventes
        .merge(clients, on="client_id", how="left")
        .merge(budget, on="segment", how="left")
    )
    logger.info("Jeu consolide : %d lignes, %d colonnes", *consolide.shape)
    return consolide
