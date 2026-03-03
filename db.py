import streamlit as st
from sqlalchemy import text

CITIES = ["Recife", "Paulista", "Maceió"]


def get_conn():
    return st.connection("beneficios_db", type="sql")


def execute(sql: str, params=None):
    if params is None:
        params = {}
    if not isinstance(params, dict):
        raise ValueError("Use parâmetros em dicionário no formato {'campo': valor}.")
    conn = get_conn()
    with conn.session as session:
        session.execute(text(sql), params)
        session.commit()


def fetch_one(sql: str, params=None):
    if params is None:
        params = {}
    if not isinstance(params, dict):
        raise ValueError("Use parâmetros em dicionário no formato {'campo': valor}.")
    conn = get_conn()
    df = conn.query(sql, params=params, ttl=0)
    if df.empty:
        return None
    return df.iloc[0].to_dict()


def fetch_all(sql: str, params=None):
    if params is None:
        params = {}
    if not isinstance(params, dict):
        raise ValueError("Use parâmetros em dicionário no formato {'campo': valor}.")
    conn = get_conn()
    df = conn.query(sql, params=params, ttl=0)
    return df.to_dict(orient="records")


def init_db():
    execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """)

    execute("""
    CREATE TABLE IF NOT EXISTS config (
        id INTEGER PRIMARY KEY,
        vt_pe NUMERIC DEFAULT 0,
        vt_al NUMERIC DEFAULT 0,
        va_vr_pe NUMERIC DEFAULT 0,
        va_vr_al NUMERIC DEFAULT 0,
        vt_fixo_supervisor_pe NUMERIC DEFAULT 0,
        vt_fixo_supervisor_al NUMERIC DEFAULT 0,
        homeoffice_pe NUMERIC DEFAULT 0,
        homeoffice_pe_b NUMERIC DEFAULT 0,
        homeoffice_al NUMERIC DEFAULT 0,
        homeoffice_al_b NUMERIC DEFAULT 0,
        updated_at TIMESTAMP
    );
    """)
    execute("INSERT INTO config (id) VALUES (1) ON CONFLICT (id) DO NOTHING;")

    execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id SERIAL PRIMARY KEY,
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
        updated_at TIMESTAMP
    );
    """)

    execute("""
    CREATE TABLE IF NOT EXISTS holidays_city_date (
        id SERIAL PRIMARY KEY,
        city TEXT NOT NULL,
        date DATE NOT NULL,
        name TEXT,
        UNIQUE(city, date)
    );
    """)

    execute("""
    CREATE TABLE IF NOT EXISTS benefit_day_adjustments (
        id SERIAL PRIMARY KEY,
        employee_id INTEGER NOT NULL REFERENCES employees(id),
        date DATE NOT NULL,
        vt_delta INTEGER DEFAULT 0,
        va_delta INTEGER DEFAULT 0,
        note TEXT,
        pay_month TEXT,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """)

    execute("""
    CREATE TABLE IF NOT EXISTS vacations (
        id SERIAL PRIMARY KEY,
        employee_id INTEGER NOT NULL REFERENCES employees(id),
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        note TEXT,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """)