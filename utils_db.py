import os
import time
import sqlite3
import hashlib

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zami_leads.db")

def init_db():
    """Creates the production-grade multi-tenant tables automatically if not existing"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Core Leads Tracking Table
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
    
    # 2. 🔐 SaaS Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password_hash TEXT,
            created_at TEXT
        )
    """)
    
    # 3. 💾 Saved Properties Portfolio Portfolio Vector
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            timestamp TEXT,
            address TEXT,
            zipcode TEXT,
            dpe TEXT,
            surface REAL,
            cost REAL,
            roi REAL,
            lat REAL,
            lon REAL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    
    conn.commit()
    conn.close()

# ── 🔐 AUTHENTICATION ENGINE UTILS ──
def hash_password(password):
    """Encrypts raw text password keys using secure SHA-256 bits masking"""
    return hashlib.sha256(str.encode(password)).hexdigest()

def create_user(username, email, password):
    """Registers a new premium profile tenant into the secure user matrix"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        pwd_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (username.strip(), email.strip().lower(), pwd_hash, current_time)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False  # Username or Email already exists

def authenticate_user(username, password):
    """Verifies profile credentials against internal system parameters"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    pwd_hash = hash_password(password)
    cursor.execute("SELECT id FROM users WHERE username = ? AND password_hash = ?", (username.strip(), pwd_hash))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# ── 💾 PORTFOLIO ENGINE UTILS ──
def save_property_to_portfolio(user_id, address, zipcode, dpe, surface, cost, roi, lat, lon):
    """Links and locks a certified property valuation inside the owner's permanent vault"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO user_properties (user_id, timestamp, address, zipcode, dpe, surface, cost, roi, lat, lon)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, current_time, address, zipcode, dpe, float(surface), float(cost), float(roi), float(lat), float(lon)))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

def fetch_user_portfolio(user_id):
    """Retrieves all tracked real-estate assets linked to the active logged-in instance"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM user_properties WHERE user_id = ? ORDER BY id DESC", conn, params=[user_id])
    conn.close()
    return df

# External dependency runtime alignment bypass injection
import pandas as pd