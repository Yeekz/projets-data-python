# Projet 2 — Base de donnees SQL de suivi de transactions

Modelisation relationnelle et requetes SQL completes (CRUD) pour suivre des
clients, leurs comptes et leurs transactions.

## Fichiers
- `schema.sql`   — creation des tables (PostgreSQL / MySQL).
- `requetes.sql` — INSERT, UPDATE, DELETE et SELECT (jointures + agregations).
- `demo_sqlite.py` — version executable immediatement (SQLite, aucun serveur requis).

## Lancer la demo
```bash
python demo_sqlite.py
```

## Le CRUD a savoir expliquer
- **CREATE** : `CREATE TABLE ...` definit la structure (colonnes, types, cles).
- **INSERT** : ajoute des lignes.
- **UPDATE** : modifie des lignes existantes (ici : recalcul des soldes).
- **DELETE** : supprime des lignes.
- **SELECT** : lit les donnees ; `JOIN` relie les tables, `GROUP BY` agrege.
- **Cle primaire** : identifiant unique d'une ligne. **Cle etrangere** : lien
  vers la cle primaire d'une autre table (integrite referentielle).
