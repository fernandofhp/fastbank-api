import sqlite3
from pathlib import Path

# Caminho para o seu banco SQLite
db_path = Path(__file__).resolve().parent / "banco.db"

print(f"Criando tabelas no banco de dados em: {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Criação manual e direta da tabela accounts para o SQLite
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    balance REAL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# Aproveitando para criar a tabela de transações que você vai usar logo em seguida
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    amount REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts (id)
);
""")

conn.commit()
conn.close()
print("🟢 Tabelas 'accounts' e 'transactions' criadas com sucesso!")