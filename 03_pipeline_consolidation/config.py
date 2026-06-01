"""Configuration centrale du pipeline (chemins et parametres)."""
from __future__ import annotations

from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent
SOURCES_DIR: Path = BASE_DIR / "sources"
OUTPUT_DIR: Path = BASE_DIR / "output"

# Sources d'entree
CLIENTS_JSON: Path = SOURCES_DIR / "clients.json"
VENTES_CSV: Path = SOURCES_DIR / "ventes.csv"
BUDGET_XLSX: Path = SOURCES_DIR / "budget.xlsx"

# Strategie de nettoyage
VALEUR_SEGMENT_INCONNU: str = "Inconnu"
MONTANT_PAR_DEFAUT: float = 0.0
