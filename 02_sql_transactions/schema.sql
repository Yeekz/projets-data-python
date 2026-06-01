/* =============================================================
   Suivi de transactions bancaires - schema de la base
   Auteur : Yacine Ouasti
   SGBD cible : PostgreSQL / MySQL (types standards)
   ============================================================= */

/* Un client peut avoir plusieurs comptes.
   Un compte contient plusieurs transactions. */

CREATE TABLE clients (
    client_id      INT          PRIMARY KEY,
    nom            VARCHAR(80)  NOT NULL,
    email          VARCHAR(120) NOT NULL UNIQUE,
    ville          VARCHAR(80),
    date_creation  DATE         NOT NULL
);

CREATE TABLE comptes (
    compte_id    INT           PRIMARY KEY,
    client_id    INT           NOT NULL REFERENCES clients(client_id),
    type_compte  VARCHAR(20)   NOT NULL,          -- 'courant' ou 'epargne'
    solde        DECIMAL(12,2) NOT NULL DEFAULT 0
);

CREATE TABLE transactions (
    transaction_id  INT           PRIMARY KEY,
    compte_id       INT           NOT NULL REFERENCES comptes(compte_id),
    date_op         DATE          NOT NULL,
    libelle         VARCHAR(120),
    montant         DECIMAL(12,2) NOT NULL          -- > 0 credit, < 0 debit
);

-- on indexe ce qui est souvent filtre
CREATE INDEX idx_tx_compte ON transactions(compte_id);
CREATE INDEX idx_tx_date   ON transactions(date_op);
