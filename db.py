import sqlite3
from pathlib import Path

# ✅ Caminho fixo (pra nunca "sumir")
DB_DIR = Path(r"C:\Users\Daniela_WS\Documents\BeneficiosWS")
DB_DIR.mkdir(parents=True, exist_ok=True)  # cria a pasta se não existir
DB_PATH = DB_DIR / "beneficios.db"

CITIES = ["Recife", "Paulista", "Maceió"]

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def execute(sql: str, params=()):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        return cur.rowcount

def fetch_one(sql: str, params=()):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        return cur.fetchone()

def fetch_all(sql: str, params=()):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()

def init_db():
    # users (auth)
    execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT DEFAULT (datetime('now'))
    );
    """)

    # config (1 linha)
    execute("""
    CREATE TABLE IF NOT EXISTS config (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        vt_pe REAL DEFAULT 0,
        vt_al REAL DEFAULT 0,
        va_vr_pe REAL DEFAULT 0,
        va_vr_al REAL DEFAULT 0,
        vt_fixo_supervisor_pe REAL DEFAULT 0,
        vt_fixo_supervisor_al REAL DEFAULT 0,
        homeoffice_pe REAL DEFAULT 0,
        homeoffice_pe_b REAL DEFAULT 0,
        homeoffice_al REAL DEFAULT 0,
        homeoffice_al_b REAL DEFAULT 0,
        updated_at TEXT
    );
    """)
    execute("INSERT OR IGNORE INTO config (id) VALUES (1);")

    # employees
    execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        cpf TEXT NOT NULL,
        uf TEXT NOT NULL,
        city TEXT,
        vt_per_day INTEGER DEFAULT 0,
        work_schedule TEXT DEFAULT 'SEG-SEX',

        pres_mon INTEGER DEFAULT 0,
        pres_tue INTEGER DEFAULT 0,
        pres_wed INTEGER DEFAULT 0,
        pres_thu INTEGER DEFAULT 0,
        pres_fri INTEGER DEFAULT 0,
        pres_sat INTEGER DEFAULT 0,

        benefit_vt INTEGER DEFAULT 0,
        benefit_va_vr INTEGER DEFAULT 0,
        benefit_homeoffice INTEGER DEFAULT 0,
        is_supervisor INTEGER DEFAULT 0,
        homeoffice_type TEXT DEFAULT 'A',

        updated_at TEXT
    );
    """)

    # holidays
    execute("""
    CREATE TABLE IF NOT EXISTS holidays_city_date (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT NOT NULL,
        date TEXT NOT NULL,
        name TEXT,
        UNIQUE(city, date)
    );
    """)

    # ajustes manuais
    execute("""
    CREATE TABLE IF NOT EXISTS benefit_day_adjustments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        vt_delta INTEGER DEFAULT 0,
        va_delta INTEGER DEFAULT 0,
        note TEXT,
        pay_month TEXT,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY(employee_id) REFERENCES employees(id)
    );
    """)

    # ✅ férias
    execute("""
    CREATE TABLE IF NOT EXISTS vacations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        end_date   TEXT NOT NULL,
        note TEXT,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY(employee_id) REFERENCES employees(id)
    );
    """)