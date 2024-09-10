import sqlite3

from models import Deposit

DB_FILE = 'deposits.db'

import sqlite3

def initialize_db():
    conn = sqlite3.connect(DB_FILE)  # Connect to or create the database
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deposits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            blockNumber TEXT NOT NULL,
            blockTimestamp TEXT NOT NULL,
            hash TEXT NOT NULL,
            fee TEXT,
            pubkey TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# Function to insert log data into SQLite database
def insert_deposit(deposit: Deposit):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO deposits (blockNumber, blockTimestamp, hash, fee, pubkey)
        VALUES (?, ?, ?, ?, ?)
    ''', (deposit.blockNumber, deposit.blockTimestamp, deposit.hash, deposit.fee, deposit.pubkey))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Initialize the database and create tables
    initialize_db()
    print("Database initialized and ready.")
