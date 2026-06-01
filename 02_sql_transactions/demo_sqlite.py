# -*- coding: utf-8 -*-
"""
Projet 2 — Demo executable de la base SQL (via SQLite, sans serveur a installer).
Joue le schema + les requetes et affiche les resultats.

Lancer :  python demo_sqlite.py

NB : le meme SQL fonctionne sur PostgreSQL/MySQL (voir schema.sql / requetes.sql).
"""
import sqlite3
from pathlib import Path

ICI = Path(__file__).parent

SCHEMA = """
CREATE TABLE clients (client_id INTEGER PRIMARY KEY, nom TEXT, email TEXT UNIQUE,
                      ville TEXT, date_creation TEXT);
CREATE TABLE comptes (compte_id INTEGER PRIMARY KEY, client_id INTEGER,
                      type_compte TEXT, solde REAL DEFAULT 0);
CREATE TABLE transactions (transaction_id INTEGER PRIMARY KEY, compte_id INTEGER,
                           date_op TEXT, libelle TEXT, montant REAL);
"""

INSERTS = """
INSERT INTO clients VALUES (1,'Yacine Ouasti','yacine@example.com','L''Hay-les-Roses','2024-01-10'),
                           (2,'Sofia Martin','sofia@example.com','Paris','2024-02-03'),
                           (3,'Liam Bernard','liam@example.com','Lyon','2024-03-21');
INSERT INTO comptes VALUES (101,1,'courant',0),(102,1,'epargne',0),
                           (103,2,'courant',0),(104,3,'courant',0);
INSERT INTO transactions VALUES
 (1,101,'2024-04-01','Salaire',2400.0),(2,101,'2024-04-03','Loyer',-950.0),
 (3,101,'2024-04-10','Courses',-180.5),(4,102,'2024-04-05','Virement epargne',300.0),
 (5,103,'2024-04-02','Salaire',1800.0),(6,103,'2024-04-08','Restaurant',-65.0),
 (7,104,'2024-04-12','Remboursement',120.0);
"""


def main():
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.executescript(SCHEMA)           # CREATE
    cur.executescript(INSERTS)          # INSERT

    # UPDATE : recalcul des soldes
    cur.execute("""UPDATE comptes SET solde =
                   (SELECT COALESCE(SUM(montant),0) FROM transactions
                    WHERE transactions.compte_id = comptes.compte_id)""")
    # DELETE : transaction annulee
    cur.execute("DELETE FROM transactions WHERE transaction_id = 7")
    cur.execute("""UPDATE comptes SET solde =
                   (SELECT COALESCE(SUM(montant),0) FROM transactions
                    WHERE transactions.compte_id = comptes.compte_id)""")
    con.commit()

    print("=== Solde total par client ===")
    for nom, solde in cur.execute("""SELECT cl.nom, SUM(co.solde)
            FROM clients cl JOIN comptes co ON co.client_id = cl.client_id
            GROUP BY cl.nom ORDER BY 2 DESC"""):
        print(f"  {nom:<18} {solde:>10.2f} EUR")

    print("\n=== Debits / credits par compte ===")
    q = """SELECT compte_id,
                  SUM(CASE WHEN montant>0 THEN montant ELSE 0 END),
                  SUM(CASE WHEN montant<0 THEN montant ELSE 0 END)
           FROM transactions GROUP BY compte_id"""
    for cid, cred, deb in cur.execute(q):
        print(f"  Compte {cid} : +{cred:.2f} / {deb:.2f}")

    con.close()


if __name__ == "__main__":
    main()
