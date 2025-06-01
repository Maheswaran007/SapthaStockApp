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
            return os.path.join(os.path.expanduser("~"), ".SapthaStockApp", "db")
    else:
        return os.path.join(os.path.expanduser("~"), ".SapthaStockApp", "db")

DB_DIR = get_db_dir()
DB_PATH = os.path.join(DB_DIR, "stock.db")

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stock'")
    if not c.fetchone():
        c.execute('''
            CREATE TABLE stock (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT,
                size REAL,
                gsm REAL,
                bf REAL,
                reels INTEGER,
                weight REAL,
                date TEXT
            )
        ''')
    else:
        # Check if `id` column exists
        c.execute("PRAGMA table_info(stock)")
        columns = [col[1] for col in c.fetchall()]
        if 'id' not in columns:
            c.execute("ALTER TABLE stock RENAME TO stock_old")
            c.execute('''
                CREATE TABLE stock (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_name TEXT,
                    size REAL,
                    gsm REAL,
                    bf REAL,
                    reels INTEGER,
                    weight REAL,
                    date TEXT
                )
            ''')
            c.execute('''
                INSERT INTO stock (item_name, size, gsm, bf, reels, weight, date)
                SELECT item_name, size, gsm, bf, reels, weight, date FROM stock_old
            ''')
            c.execute("DROP TABLE stock_old")

    conn.commit()
    conn.close()

def add_stock(item_name, size, gsm, bf, reels, weight):
    date = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Check for duplicates
    c.execute('''
        SELECT COUNT(*) FROM stock
        WHERE item_name = ? AND size = ? AND gsm = ? AND bf = ?
    ''', (item_name, size, gsm, bf))
    
    count = c.fetchone()[0]
    if count > 0:
        conn.close()
        raise ValueError("Stock already exists")

    c = conn.cursor()
    c.execute('''
        INSERT INTO stock (item_name, size, gsm, bf, reels, weight, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (item_name, size, gsm, bf, reels, weight, date))
    conn.commit()
    conn.close()

def get_all_stock_with_ids():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT rowid, item_name, size, gsm, bf, reels, weight
        FROM stock
    ''')
    rows = c.fetchall()
    conn.close()
    return rows

def delete_stock(stock_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM stock WHERE rowid = ?', (stock_id,))
    conn.commit()
    conn.close()


def get_stock_report():
    date = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT item_name, size, gsm, bf, reels, weight
        FROM stock
        ORDER BY size ASC
    ''')
    rows = c.fetchall()
    conn.close()
    return rows

def get_all_stock():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT id, item_name, size, gsm, bf, SUM(reels), SUM(weight)
        FROM stock
        GROUP BY item_name, size, gsm, bf
    ''')
    rows = c.fetchall()
    conn.close()
    return rows

def update_stock_by_id(stock_id, item_name, size, gsm, bf, reels, weight):
    date = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        UPDATE stock SET 
            item_name = ?, size = ?, gsm = ?, bf = ?, reels = ?, weight = ?, date = ?
        WHERE rowid = ?
    ''', (item_name, size, gsm, bf, reels, weight, date, stock_id))
    conn.commit()
    conn.close()

def update_stock_quantity(stock_id, qty_change, reels_change):
    date = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Assuming you only want to update weight, reels should not change
    c.execute('''
        UPDATE stock
        SET weight = weight + ?, date = ?, reels = reels + ?
        WHERE rowid = ?
    ''', (qty_change, date, reels_change, stock_id))
    conn.commit()
    conn.close()
