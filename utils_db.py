import os
import time
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zami_leads.db")

def init_db():
    """Creates the commercial-grade business tracking layout if not existing"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            property_address TEXT,
            zipcode TEXT,
            initial_dpe TEXT,
            target_dpe TEXT,
            selected_scenario TEXT,
            estimated_cost REAL,
            owner_name TEXT,
            owner_phone TEXT,
            owner_email TEXT,
            callback_time TEXT,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_lead_to_db(address, zipcode, initial_dpe, target_dpe, scenario, cost, name, phone, email, callback_time, notes):
    """Safely logs and isolates new customer acquisition leads row-by-row"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO leads (
                timestamp, property_address, zipcode, initial_dpe, target_dpe, 
                selected_scenario, estimated_cost, owner_name, owner_phone, 
                owner_email, callback_time, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (current_time, address, zipcode, initial_dpe, target_dpe, scenario, float(cost), name, phone, email, callback_time, notes))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False