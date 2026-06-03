"""
utils_db.py — ZAMI Minimal Database Module
"""

import os
import time
import sqlite3
import hashlib

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zami_leads.db")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def init_db():
    """Create only essential tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Only agencies table for now
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            siret TEXT,
            address TEXT,
            password_hash TEXT,
            created_at TEXT
        )
    """)
    
    conn.commit()
    conn.close()


def register_agency(company_name, email, phone, siret, address, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        pwd_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO agencies (company_name, email, phone, siret, address, password_hash, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (company_name, email, phone, siret, address, pwd_hash, current_time))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def authenticate_agency(email, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        pwd_hash = hash_password(password)
        cursor.execute("SELECT id, company_name FROM agencies WHERE email = ? AND password_hash = ?", (email, pwd_hash))
        result = cursor.fetchone()
        conn.close()
        return result
    except:
        return None


def get_all_agencies():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, company_name, email, phone FROM agencies ORDER BY created_at DESC")
        results = cursor.fetchall()
        conn.close()
        return results
    except:
        return []


def assign_lead_to_agency(agency_id, lead_data):
    # Simplified for now - just return success
    return 1


def get_agency_leads(agency_id):
    return []


def update_lead_status(lead_id, status):
    pass


def add_message(lead_id, sender_type, sender_id, message):
    pass


def get_messages(lead_id):
    return []


def add_quote(lead_id, agency_id, amount, details):
    pass


def get_quotes_for_lead(lead_id):
    return []


def save_property_to_portfolio(user_id, address, zipcode, dpe, surface, cost, roi, lat, lon):
    pass


def fetch_user_portfolio(user_id):
    import pandas as pd
    return pd.DataFrame()


def create_user(username, email, password):
    pass


def authenticate_user(username, password):
    return None