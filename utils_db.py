"""
utils_db.py — ZAMI Database Module
"""

import os
import time
import sqlite3
import hashlib
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zami_leads.db")


def hash_password(password):
    """Encrypt password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def init_db():
    """Initialize database with all tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Agencies table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            siret TEXT,
            address TEXT,
            password_hash TEXT NOT NULL,
            subscription_type TEXT DEFAULT 'free',
            credits INTEGER DEFAULT 0,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    
    # Agency leads table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agency_leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agency_id INTEGER,
            property_address TEXT,
            property_dpe TEXT,
            property_surface REAL,
            estimated_budget REAL,
            customer_name TEXT,
            customer_phone TEXT,
            customer_email TEXT,
            status TEXT DEFAULT 'pending',
            assigned_at TEXT,
            accepted_at TEXT,
            rejected_at TEXT
        )
    ''')
    
    # Messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lead_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER,
            sender_type TEXT,
            sender_id INTEGER,
            message TEXT,
            sent_at TEXT
        )
    ''')
    
    # Quotes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lead_quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER,
            agency_id INTEGER,
            quote_amount REAL,
            quote_details TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT
        )
    ''')
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password_hash TEXT,
            created_at TEXT
        )
    ''')
    
    # User properties table
    cursor.execute('''
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
            lon REAL
        )
    ''')
    
    # Contractors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contractors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            rge_certified INTEGER DEFAULT 1,
            service_areas TEXT,
            work_types TEXT,
            subscription_type TEXT DEFAULT 'free',
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    
    # Website leads table
    cursor.execute('''
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
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized")


def register_agency(company_name, email, phone, siret, address, password):
    """Register a new agency"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        pwd_hash = hash_password(password)
        cursor.execute('''
            INSERT INTO agencies (company_name, email, phone, siret, address, password_hash, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (company_name, email, phone, siret, address, pwd_hash, current_time, current_time))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def authenticate_agency(email, password):
    """Authenticate agency login"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        pwd_hash = hash_password(password)
        cursor.execute('SELECT id, company_name FROM agencies WHERE email = ? AND password_hash = ?', (email, pwd_hash))
        result = cursor.fetchone()
        conn.close()
        return result if result else None
    except Exception:
        return None


def get_all_agencies():
    """Get all registered agencies"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT id, company_name, email, phone FROM agencies ORDER BY created_at DESC')
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception:
        return []


def assign_lead_to_agency(agency_id, lead_data):
    """Assign a lead to agency"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO agency_leads (agency_id, property_address, property_dpe, property_surface, 
            estimated_budget, customer_name, customer_phone, customer_email, status, assigned_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (agency_id, lead_data.get('address'), lead_data.get('dpe'), lead_data.get('surface'),
              lead_data.get('budget'), lead_data.get('customer_name'), lead_data.get('customer_phone'),
              lead_data.get('customer_email'), 'pending', current_time))
        conn.commit()
        lead_id = cursor.lastrowid
        conn.close()
        return lead_id
    except Exception:
        return None


def get_agency_leads(agency_id):
    """Get all leads for an agency"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM agency_leads WHERE agency_id = ? ORDER BY assigned_at DESC', (agency_id,))
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception:
        return []


def update_lead_status(lead_id, status):
    """Update lead status (accepted/rejected)"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        if status == 'accepted':
            cursor.execute('UPDATE agency_leads SET status = ?, accepted_at = ? WHERE id = ?', 
                           (status, current_time, lead_id))
        else:
            cursor.execute('UPDATE agency_leads SET status = ?, rejected_at = ? WHERE id = ?', 
                           (status, current_time, lead_id))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def add_message(lead_id, sender_type, sender_id, message):
    """Add chat message"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO lead_messages (lead_id, sender_type, sender_id, message, sent_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (lead_id, sender_type, sender_id, message, current_time))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def get_messages(lead_id):
    """Get all messages for a lead"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM lead_messages WHERE lead_id = ? ORDER BY sent_at ASC', (lead_id,))
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception:
        return []


def add_quote(lead_id, agency_id, amount, details):
    """Add a quote for a lead"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO lead_quotes (lead_id, agency_id, quote_amount, quote_details, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (lead_id, agency_id, amount, details, 'pending', current_time))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def get_quotes_for_lead(lead_id):
    """Get all quotes for a lead"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM lead_quotes WHERE lead_id = ? ORDER BY created_at DESC', (lead_id,))
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception:
        return []


def save_property_to_portfolio(user_id, address, zipcode, dpe, surface, cost, roi, lat, lon):
    """Save property to user's portfolio"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO user_properties (user_id, timestamp, address, zipcode, dpe, surface, cost, roi, lat, lon)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, current_time, address, zipcode, dpe, float(surface), float(cost), float(roi), float(lat), float(lon)))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def fetch_user_portfolio(user_id):
    """Retrieve all saved properties for a user"""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query('SELECT * FROM user_properties WHERE user_id = ? ORDER BY id DESC', conn, params=[user_id])
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()


def create_user(username, email, password):
    """Create a new user"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        pwd_hash = hash_password(password)
        cursor.execute('INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)',
                       (username, email, pwd_hash, current_time))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def authenticate_user(username, password):
    """Authenticate user"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        pwd_hash = hash_password(password)
        cursor.execute('SELECT id FROM users WHERE username = ? AND password_hash = ?', (username, pwd_hash))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except Exception:
        return None