"""Point d'entree du pipeline de consolidation.

Usage:
    python run.py
"""
from __future__ import annotations

import logging

from etl import consolider, exporter, kpi_ca_par_segment, lire_sources, nettoyer


def configurer_logs() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def main() -> None:
    configurer_logs()
    log = logging.getLogger("pipeline")
    log.info("Demarrage du pipeline")

    clients, ventes, budget = lire_sources()
    clients, ventes = nettoyer(clients, ventes)
    consolide = consolider(clients, ventes, budget)

    ca = kpi_ca_par_segment(consolide)
    log.info("CA par segment :\n%s", ca.to_string())

    exporter(consolide, ca)
    log.info("Pipeline termine avec succes")


if __name__ == "__main__":
    main()
