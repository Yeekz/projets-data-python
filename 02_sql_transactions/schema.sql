-- Projet 2 — Schema de suivi de transactions
-- Compatible PostgreSQL et MySQL (types standards).

CREATE TABLE clients (
    client_id     INTEGER PRIMARY KEY,
    nom           VARCHAR(80)  NOT NULL,
    email         VARCHAR(120) UNIQUE NOT NULL,
    ville         VARCHAR(80),
    date_creation DATE NOT NULL
);

CREATE TABLE comptes (
    compte_id   INTEGER PRIMARY KEY,
    client_id   INTEGER NOT NULL,
    type_compte VARCHAR(20) NOT NULL,        -- 'courant' | 'epargne'
    solde       DECIMAL(12,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
);

CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY,
    compte_id      INTEGER NOT NULL,
    date_op        DATE NOT NULL,
    libelle        VARCHAR(120),
    montant        DECIMAL(12,2) NOT NULL,    -- positif = credit, negatif = debit
    FOREIGN KEY (compte_id) REFERENCES comptes(compte_id)
);

-- Index pour accelerer les recherches par compte et par date
CREATE INDEX idx_tx_compte ON transactions(compte_id);
CREATE INDEX idx_tx_date   ON transactions(date_op);
