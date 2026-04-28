import sqlite3
import pandas as pd



DB_NAME = "trades.db"

def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        trade_numero TEXT,
        data_trade TEXT,
        emozione TEXT,
        asset TEXT,
        risultato TEXT,
        mercato TEXT,
        trigger_entrata TEXT,
        motivo_uscita TEXT,
        contratti INTEGER,
        chiusura TEXT,
        prezzo_entrata TEXT,
        prezzo_uscita TEXT,
        direzione TEXT,
        pnl REAL
    )
    """)
    conn.commit()
    conn.close()

def salva_trade(dati):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO trades (
        nome, trade_numero, data_trade, emozione, asset, risultato, mercato,
        trigger_entrata, motivo_uscita, contratti, chiusura,
        prezzo_entrata, prezzo_uscita, direzione, pnl
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, dati)

    conn.commit()
    conn.close()

def carica_trades():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM trades ORDER BY id DESC", conn)
    conn.close()
    return df


