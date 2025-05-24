from datetime import datetime
import os
import sys
import sqlite3

def get_db_dir():
    """Return a writable directory for the database, using %APPDATA% on Windows."""
    if sys.platform == "win32":
        appdata = os.getenv("APPDATA")
        if appdata:
            return os.path.join(appdata, "SapthaStockApp", "db")
        else:
            # fallback if APPDATA not found
            return os.path.join(os.path.expanduser("~"), ".SapthaStockApp", "db")
    else:
        # For other OSes (Linux/Mac), store in home directory
        return os.path.join(os.path.expanduser("~"), ".SapthaStockApp", "db")

DB_DIR = get_db_dir()
DB_PATH = os.path.join(DB_DIR, "stock.db")

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stock (
        item_name TEXT,
        size REAL,
        gsm REAL,
        bf REAL,
        reels INTEGER,
        weight REAL,
        date TEXT
    )''')
    conn.commit()
    conn.close()

def add_stock(item_name, size, gsm, bf, reels, weight):
    date = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO stock (item_name, size, gsm, bf, reels, weight, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (item_name, size, gsm, bf, reels, weight, date))
    conn.commit()
    conn.close()

def get_today_stock():
    date = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT item_name, size, gsm, bf, SUM(reels), SUM(weight)
        FROM stock
        WHERE date = ?
        GROUP BY item_name, size, gsm, bf
    ''', (date,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_all_stock():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT item_name, size, gsm, bf, SUM(reels), SUM(weight)
        FROM stock
        GROUP BY item_name, size, gsm, bf
    ''')
    rows = c.fetchall()
    conn.close()
    return rows
