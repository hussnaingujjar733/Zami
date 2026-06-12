"""
Database utilities for ZAMI Marketplace
With automatic schema migration
"""

import sqlite3
from datetime import datetime

DB_PATH = "marketplace.db"

def get_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    """Initialize database with all tables"""
    
    with get_db() as conn:
        # Homeowners table
        conn.execute('''CREATE TABLE IF NOT EXISTS homeowners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            address TEXT,
            password TEXT,
            created_at TEXT
        )''')
        
        # Contractors table
        conn.execute('''CREATE TABLE IF NOT EXISTS contractors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            siret TEXT UNIQUE,
            email TEXT UNIQUE,
            phone TEXT,
            city TEXT,
            password TEXT,
            rge_certified INTEGER DEFAULT 0,
            insurance_file TEXT,
            status TEXT DEFAULT 'pending',
            rating REAL DEFAULT 0,
            stripe_account_id TEXT,
            created_at TEXT
        )''')
        
        # Projects table
        conn.execute('''CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            homeowner_id INTEGER,
            contractor_id INTEGER,
            property_address TEXT,
            dpe_rating TEXT,
            estimated_cost REAL,
            final_cost REAL,
            status TEXT DEFAULT 'pending',
            created_at TEXT,
            assigned_at TEXT,
            completed_at TEXT
        )''')
        
        # Quotes table
        conn.execute('''CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            contractor_id INTEGER,
            amount REAL,
            status TEXT DEFAULT 'pending',
            created_at TEXT
        )''')
        
        # Payments table
        conn.execute('''CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            amount REAL,
            status TEXT DEFAULT 'pending',
            stripe_intent_id TEXT,
            created_at TEXT,
            released_at TEXT
        )''')
        
        # Verifications table
        conn.execute('''CREATE TABLE IF NOT EXISTS verifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            photo_paths TEXT,
            ai_score REAL,
            verified_at TEXT
        )''')
        
        # Agencies table
        conn.execute('''CREATE TABLE IF NOT EXISTS agencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            created_at TEXT
        )''')
        
        conn.commit()
    
    # Run migrations to add any missing columns
    migrate_db()


def migrate_db():
    """Add missing columns to existing tables"""
    
    with get_db() as conn:
        # Check and add stripe_account_id to contractors
        try:
            conn.execute("SELECT stripe_account_id FROM contractors LIMIT 1")
        except sqlite3.OperationalError:
            try:
                conn.execute("ALTER TABLE contractors ADD COLUMN stripe_account_id TEXT")
                conn.commit()
            except:
                pass
        
        # Check and add final_cost to projects
        try:
            conn.execute("SELECT final_cost FROM projects LIMIT 1")
        except sqlite3.OperationalError:
            try:
                conn.execute("ALTER TABLE projects ADD COLUMN final_cost REAL")
                conn.commit()
            except:
                pass
        
        # Check and add assigned_at to projects
        try:
            conn.execute("SELECT assigned_at FROM projects LIMIT 1")
        except sqlite3.OperationalError:
            try:
                conn.execute("ALTER TABLE projects ADD COLUMN assigned_at TEXT")
                conn.commit()
            except:
                pass
        
        # Check and add completed_at to projects
        try:
            conn.execute("SELECT completed_at FROM projects LIMIT 1")
        except sqlite3.OperationalError:
            try:
                conn.execute("ALTER TABLE projects ADD COLUMN completed_at TEXT")
                conn.commit()
            except:
                pass
        
        # Check and add released_at to payments
        try:
            conn.execute("SELECT released_at FROM payments LIMIT 1")
        except sqlite3.OperationalError:
            try:
                conn.execute("ALTER TABLE payments ADD COLUMN released_at TEXT")
                conn.commit()
            except:
                pass


# ========== HELPER FUNCTIONS ==========

def get_homeowner_by_email(email):
    with get_db() as conn:
        return conn.execute("SELECT * FROM homeowners WHERE email = ?", (email,)).fetchone()

def get_homeowner_by_id(homeowner_id):
    with get_db() as conn:
        return conn.execute("SELECT * FROM homeowners WHERE id = ?", (homeowner_id,)).fetchone()

def save_homeowner(name, email, phone, address, password):
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO homeowners (name, email, phone, address, password, created_at) VALUES (?,?,?,?,?,?)",
            (name, email, phone, address, password, datetime.now().isoformat())
        )
        return cursor.lastrowid

def get_contractor_by_email(email):
    with get_db() as conn:
        return conn.execute("SELECT * FROM contractors WHERE email = ?", (email,)).fetchone()

def get_contractor_by_id(contractor_id):
    with get_db() as conn:
        return conn.execute("SELECT * FROM contractors WHERE id = ?", (contractor_id,)).fetchone()

def get_all_contractors():
    with get_db() as conn:
        return conn.execute("SELECT * FROM contractors ORDER BY created_at DESC").fetchall()

def update_contractor_status(contractor_id, status):
    with get_db() as conn:
        conn.execute("UPDATE contractors SET status = ? WHERE id = ?", (status, contractor_id))
        conn.commit()

def create_project(homeowner_id, address, dpe_rating, estimated_cost):
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO projects (homeowner_id, property_address, dpe_rating, estimated_cost, status, created_at) VALUES (?,?,?,?,?,?)",
            (homeowner_id, address, dpe_rating, estimated_cost, 'pending', datetime.now().isoformat())
        )
        return cursor.lastrowid

def get_projects_by_homeowner(homeowner_id):
    with get_db() as conn:
        return conn.execute('''
            SELECT p.*, c.company_name
            FROM projects p
            LEFT JOIN contractors c ON p.contractor_id = c.id
            WHERE p.homeowner_id = ?
            ORDER BY p.created_at DESC
        ''', (homeowner_id,)).fetchall()

def get_projects_by_contractor(contractor_id):
    with get_db() as conn:
        return conn.execute('''
            SELECT p.*, h.name as homeowner_name
            FROM projects p
            JOIN homeowners h ON p.homeowner_id = h.id
            WHERE p.contractor_id = ?
            ORDER BY p.created_at DESC
        ''', (contractor_id,)).fetchall()

def update_project_status(project_id, status):
    with get_db() as conn:
        if status == 'completed':
            conn.execute("UPDATE projects SET status = ?, completed_at = ? WHERE id = ?", (status, datetime.now().isoformat(), project_id))
        elif status == 'assigned':
            conn.execute("UPDATE projects SET status = ?, assigned_at = ? WHERE id = ?", (status, datetime.now().isoformat(), project_id))
        else:
            conn.execute("UPDATE projects SET status = ? WHERE id = ?", (status, project_id))
        conn.commit()

def save_quote(project_id, contractor_id, amount):
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO quotes (project_id, contractor_id, amount, created_at) VALUES (?,?,?,?)",
            (project_id, contractor_id, amount, datetime.now().isoformat())
        )
        return cursor.lastrowid
