# Suivi de transactions — base de données SQL

Projet réalisé dans le cadre de mon cours de bases de données. L'objectif :
modéliser un suivi de comptes bancaires et écrire les requêtes SQL pour
l'alimenter et l'analyser.

## Modèle de données

```
 clients                comptes                 transactions
 ----------             ----------              --------------
 client_id (PK) ──1───< client_id (FK)          transaction_id (PK)
 nom                    compte_id (PK) ──1───<   compte_id (FK)
 email                  type_compte             date_op
 ville                  solde                   libelle
 date_creation                                  montant
```

- Un **client** possède plusieurs **comptes** (relation 1—N).
- Un **compte** enregistre plusieurs **transactions** (relation 1—N).
- Lien assuré par les clés étrangères (`client_id`, `compte_id`).

## Fichiers

| Fichier | Contenu |
|---------|---------|
| `schema.sql`   | création des 3 tables + index |
| `requetes.sql` | INSERT, UPDATE, DELETE et les requêtes d'analyse |

## Requêtes d'analyse incluses

1. Solde total par client (jointure `clients`↔`comptes` + `GROUP BY`)
2. Débits / crédits par compte (`CASE WHEN` + `SUM`)
3. Comptes à découvert (`WHERE solde < 0`)

## Tester

Compatible PostgreSQL et MySQL. Pour essayer rapidement sans serveur :

```bash
sqlite3 demo.db ".read schema.sql" ".read requetes.sql"
```
