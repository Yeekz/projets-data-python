-- Projet 2 — Requetes CRUD + analyse
-- =========================================================
-- C(REATE) / INSERT : alimentation des tables
-- =========================================================
INSERT INTO clients (client_id, nom, email, ville, date_creation) VALUES
 (1, 'Yacine Ouasti', 'yacine@example.com', 'L''Hay-les-Roses', '2024-01-10'),
 (2, 'Sofia Martin',  'sofia@example.com',  'Paris',            '2024-02-03'),
 (3, 'Liam Bernard',  'liam@example.com',   'Lyon',             '2024-03-21');

INSERT INTO comptes (compte_id, client_id, type_compte, solde) VALUES
 (101, 1, 'courant', 0),
 (102, 1, 'epargne', 0),
 (103, 2, 'courant', 0),
 (104, 3, 'courant', 0);

INSERT INTO transactions (transaction_id, compte_id, date_op, libelle, montant) VALUES
 (1, 101, '2024-04-01', 'Salaire',        2400.00),
 (2, 101, '2024-04-03', 'Loyer',          -950.00),
 (3, 101, '2024-04-10', 'Courses',        -180.50),
 (4, 102, '2024-04-05', 'Virement epargne', 300.00),
 (5, 103, '2024-04-02', 'Salaire',        1800.00),
 (6, 103, '2024-04-08', 'Restaurant',      -65.00),
 (7, 104, '2024-04-12', 'Remboursement',   120.00);

-- =========================================================
-- U(PDATE) : recalcul du solde d'un compte
-- =========================================================
UPDATE comptes c
SET solde = (
    SELECT COALESCE(SUM(t.montant), 0)
    FROM transactions t
    WHERE t.compte_id = c.compte_id
);

-- =========================================================
-- D(ELETE) : suppression d'une transaction annulee
-- =========================================================
DELETE FROM transactions WHERE transaction_id = 7;

-- =========================================================
-- R(EAD) / SELECT : analyses avec jointures et agregations
-- =========================================================
-- 1) Solde courant par client
SELECT cl.nom, SUM(co.solde) AS solde_total
FROM clients cl
JOIN comptes co ON co.client_id = cl.client_id
GROUP BY cl.nom
ORDER BY solde_total DESC;

-- 2) Total des debits et credits par compte
SELECT compte_id,
       SUM(CASE WHEN montant > 0 THEN montant ELSE 0 END) AS total_credits,
       SUM(CASE WHEN montant < 0 THEN montant ELSE 0 END) AS total_debits
FROM transactions
GROUP BY compte_id;

-- 3) Clients ayant un solde negatif (decouvert)
SELECT cl.nom, co.compte_id, co.solde
FROM comptes co
JOIN clients cl ON cl.client_id = co.client_id
WHERE co.solde < 0;
