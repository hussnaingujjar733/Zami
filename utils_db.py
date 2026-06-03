"""
utils_db.py — ZAMI Complete Database Module
Handles: Users, Agencies, Contractors, Leads, Messages, Quotes, Portfolio
"""

import os
import time
import sqlite3
import hashlib
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zami_leads.db")


# ─────────────────────────────────────────────
# DATABASE INITIALIZATION
# ─────────────────────────────────────────────

def init_db():
    """Creates all production-grade tables automatically"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Core Users Table (for property owners)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password_hash TEXT,
            created_at TEXT
        )
    """)
    
    # 2. Agencies Table
    cursor.execute("""
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
    """)
    
    # 3. Contractors Table (RGE Artisans)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contractors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            rge_certified BOOLEAN DEFAULT 1,
            service_areas TEXT,
            work_types TEXT,
            subscription_type TEXT DEFAULT 'free',
            created_at TEXT,
            updated_at TEXT
        )
    """)
    
    # 4. User Properties Portfolio (saved by property owners)
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
    
    # 5. Agency Leads (leads assigned to agencies)
    cursor.execute("""
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
            rejected_at TEXT,
            FOREIGN KEY(agency_id) REFERENCES agencies(id)
        )
    """)
    
    # 6. Contractor Leads (leads for contractors)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contractor_leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contractor_id INTEGER,
            lead_data TEXT,
            lead_price REAL,
            status TEXT DEFAULT 'sent',
            sent_at TEXT,
            FOREIGN KEY(contractor_id) REFERENCES contractors(id)
        )
    """)
    
    # 7. Lead Messages / Chat System
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lead_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER,
            sender_type TEXT,
            sender_id INTEGER,
            message TEXT,
            sent_at TEXT
        )
    """)
    
    # 8. Quotes Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lead_quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER,
            agency_id INTEGER,
            quote_amount REAL,
            quote_details TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT,
            FOREIGN KEY(lead_id) REFERENCES agency_leads(id),
            FOREIGN KEY(agency_id) REFERENCES agencies(id)
        )
    """)
    
    # 9. Website Leads (from contact forms)
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


# ─────────────────────────────────────────────
# HASHING UTILITY
# ─────────────────────────────────────────────

def hash_password(password):
    """Encrypts password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


# ─────────────────────────────────────────────
# USER AUTHENTICATION (Property Owners)
# ─────────────────────────────────────────────

def create_user(username, email, password):
    """Registers a new property owner"""
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
        return False


def authenticate_user(username, password):
    """Verifies property owner credentials"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    pwd_hash = hash_password(password)
    cursor.execute("SELECT id FROM users WHERE username = ? AND password_hash = ?", (username.strip(), pwd_hash))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


# ─────────────────────────────────────────────
# AGENCY AUTHENTICATION
# ─────────────────────────────────────────────

def register_agency(company_name, email, phone, siret, address, password):
    """Register a new agency"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        pwd_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO agencies (company_name, email, phone, siret, address, password_hash, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (company_name, email, phone, siret, address, pwd_hash, current_time, current_time))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def authenticate_agency(email, password):
    """Authenticate agency login"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    pwd_hash = hash_password(password)
    cursor.execute("SELECT id, company_name FROM agencies WHERE email = ? AND password_hash = ?", (email, pwd_hash))
    result = cursor.fetchone()
    conn.close()
    return result if result else None


def get_all_agencies():
    """Get all registered agencies (for admin)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, company_name, email, phone FROM agencies ORDER BY created_at DESC")
    results = cursor.fetchall()
    conn.close()
    return results


# ─────────────────────────────────────────────
# AGENCY LEADS MANAGEMENT
# ─────────────────────────────────────────────

def assign_lead_to_agency(agency_id, lead_data):
    """Assign a lead to agency"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO agency_leads (agency_id, property_address, property_dpe, property_surface, 
        estimated_budget, customer_name, customer_phone, customer_email, status, assigned_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (agency_id, lead_data.get('address'), lead_data.get('dpe'), lead_data.get('surface'),
          lead_data.get('budget'), lead_data.get('customer_name'), lead_data.get('customer_phone'),
          lead_data.get('customer_email'), 'pending', current_time))
    conn.commit()
    lead_id = cursor.lastrowid
    conn.close()
    return lead_id


def get_agency_leads(agency_id):
    """Get all leads assigned to an agency"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agency_leads WHERE agency_id = ? ORDER BY assigned_at DESC", (agency_id,))
    results = cursor.fetchall()
    conn.close()
    return results


def update_lead_status(lead_id, status):
    """Update lead status (accepted/rejected)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    if status == 'accepted':
        cursor.execute("UPDATE agency_leads SET status = ?, accepted_at = ? WHERE id = ?", 
                       (status, current_time, lead_id))
    else:
        cursor.execute("UPDATE agency_leads SET status = ?, rejected_at = ? WHERE id = ?", 
                       (status, current_time, lead_id))
    conn.commit()
    conn.close()


# ─────────────────────────────────────────────
# MESSAGING / CHAT SYSTEM
# ─────────────────────────────────────────────

def add_message(lead_id, sender_type, sender_id, message):
    """Add chat message"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO lead_messages (lead_id, sender_type, sender_id, message, sent_at)
        VALUES (?, ?, ?, ?, ?)
    """, (lead_id, sender_type, sender_id, message, current_time))
    conn.commit()
    conn.close()


def get_messages(lead_id):
    """Get all messages for a lead"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lead_messages WHERE lead_id = ? ORDER BY sent_at ASC", (lead_id,))
    results = cursor.fetchall()
    conn.close()
    return results


# ─────────────────────────────────────────────
# QUOTE SYSTEM
# ─────────────────────────────────────────────

def add_quote(lead_id, agency_id, amount, details):
    """Add a quote for a lead"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO lead_quotes (lead_id, agency_id, quote_amount, quote_details, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (lead_id, agency_id, amount, details, 'pending', current_time))
    conn.commit()
    conn.close()


def get_quotes_for_lead(lead_id):
    """Get all quotes for a lead"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lead_quotes WHERE lead_id = ? ORDER BY created_at DESC", (lead_id,))
    results = cursor.fetchall()
    conn.close()
    return results


# ─────────────────────────────────────────────
# CONTRACTOR MANAGEMENT
# ─────────────────────────────────────────────

def add_contractor(company_name, email, phone, service_areas, work_types, rge_certified=True):
    """Add a new contractor to database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        work_types_str = ",".join(work_types) if isinstance(work_types, list) else work_types
        cursor.execute("""
            INSERT INTO contractors (company_name, email, phone, rge_certified, service_areas, work_types, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (company_name, email, phone, rge_certified, service_areas, work_types_str, current_time, current_time))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def get_contractors_by_zip(zipcode):
    """Get contractors serving this zipcode"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM contractors WHERE service_areas LIKE ? OR service_areas LIKE ?
    """, (f'%{zipcode[:2]}%', f'%{zipcode}%'))
    results = cursor.fetchall()
    conn.close()
    return results


def save_contractor_lead(contractor_id, lead_data, lead_price=15):
    """Save lead sent to contractor"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO contractor_leads (contractor_id, lead_data, lead_price, status, sent_at)
        VALUES (?, ?, ?, ?, ?)
    """, (contractor_id, lead_data, lead_price, 'sent', current_time))
    conn.commit()
    conn.close()


# ─────────────────────────────────────────────
# USER PORTFOLIO (Saved Properties)
# ─────────────────────────────────────────────

def save_property_to_portfolio(user_id, address, zipcode, dpe, surface, cost, roi, lat, lon):
    """Save property to user's portfolio"""
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
    """Retrieve all saved properties for a user"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM user_properties WHERE user_id = ? ORDER BY id DESC", conn, params=[user_id])
    conn.close()
    return df


# ─────────────────────────────────────────────
# WEBSITE LEADS (Contact Form)
# ─────────────────────────────────────────────

def log_lead_to_db(address, zipcode, initial_dpe, target_dpe, scenario, cost, name, phone, email, time_slot, notes):
    """Save lead from website contact form"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO leads (timestamp, property_address, zipcode, initial_dpe, target_dpe, 
            selected_scenario, estimated_cost, owner_name, owner_phone, owner_email, callback_time, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (current_time, address, zipcode, initial_dpe, target_dpe, scenario, cost, name, phone, email, time_slot, notes))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False