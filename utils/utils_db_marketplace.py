"""
Database utilities for ZAMI Marketplace
"""

import sqlite3
from datetime import datetime

DB_PATH = "marketplace.db"

def get_db():
    """Get database connection"""
    return sqlite3.connect(DB_PATH)

def init_db():
    """Initialize all database tables"""
    with get_db() as conn:
        # Homeowners table
        conn.execute('''CREATE TABLE IF NOT EXISTS homeowners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            address TEXT,
            password TEXT,
            created_at TEXT
        )''')
        
        # Contractors table
        conn.execute('''CREATE TABLE IF NOT EXISTS contractors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            siret TEXT UNIQUE,
            email TEXT UNIQUE,
            phone TEXT,
            city TEXT,
            password TEXT,
            rge_certified BOOLEAN DEFAULT 0,
            insurance_file TEXT,
            status TEXT DEFAULT 'pending',
            rating REAL DEFAULT 0,
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
            completed_at TEXT,
            FOREIGN KEY (homeowner_id) REFERENCES homeowners(id),
            FOREIGN KEY (contractor_id) REFERENCES contractors(id)
        )''')
        
        # Payments table
        conn.execute('''CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            amount REAL,
            status TEXT DEFAULT 'pending',
            stripe_intent_id TEXT,
            created_at TEXT,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )''')
        
        # Quotes table
        conn.execute('''CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            contractor_id INTEGER,
            amount REAL,
            status TEXT DEFAULT 'pending',
            created_at TEXT,
            FOREIGN KEY (project_id) REFERENCES projects(id),
            FOREIGN KEY (contractor_id) REFERENCES contractors(id)
        )''')
        
        conn.commit()


# ========== HOMEOWNER FUNCTIONS ==========

def save_homeowner(name, email, phone, address, password):
    """Save new homeowner"""
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO homeowners (name, email, phone, address, password, created_at) VALUES (?,?,?,?,?,?)",
            (name, email, phone, address, password, datetime.now().isoformat())
        )
        return cursor.lastrowid

def get_homeowner_by_email(email):
    """Get homeowner by email"""
    with get_db() as conn:
        return conn.execute("SELECT * FROM homeowners WHERE email = ?", (email,)).fetchone()

def get_homeowner_by_id(homeowner_id):
    """Get homeowner by ID"""
    with get_db() as conn:
        return conn.execute("SELECT * FROM homeowners WHERE id = ?", (homeowner_id,)).fetchone()


# ========== CONTRACTOR FUNCTIONS ==========

def save_contractor(company_name, siret, email, phone, city, password):
    """Save new contractor"""
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO contractors (company_name, siret, email, phone, city, password, created_at) VALUES (?,?,?,?,?,?,?)",
            (company_name, siret, email, phone, city, password, datetime.now().isoformat())
        )
        return cursor.lastrowid

def get_contractor_by_email(email):
    """Get contractor by email"""
    with get_db() as conn:
        return conn.execute("SELECT * FROM contractors WHERE email = ?", (email,)).fetchone()

def get_contractor_by_id(contractor_id):
    """Get contractor by ID"""
    with get_db() as conn:
        return conn.execute("SELECT * FROM contractors WHERE id = ?", (contractor_id,)).fetchone()

def get_all_contractors(status=None):
    """Get all contractors, optionally filtered by status"""
    with get_db() as conn:
        if status:
            return conn.execute("SELECT * FROM contractors WHERE status = ? ORDER BY created_at DESC", (status,)).fetchall()
        return conn.execute("SELECT * FROM contractors ORDER BY created_at DESC").fetchall()

def update_contractor_status(contractor_id, status):
    """Update contractor approval status"""
    with get_db() as conn:
        conn.execute("UPDATE contractors SET status = ? WHERE id = ?", (status, contractor_id))
        conn.commit()


# ========== PROJECT FUNCTIONS ==========

def create_project(homeowner_id, property_address, dpe_rating, estimated_cost):
    """Create new project"""
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO projects (homeowner_id, property_address, dpe_rating, estimated_cost, status, created_at) VALUES (?,?,?,?,?,?)",
            (homeowner_id, property_address, dpe_rating, estimated_cost, 'pending', datetime.now().isoformat())
        )
        return cursor.lastrowid

def get_projects_by_homeowner(homeowner_id):
    """Get all projects for a homeowner"""
    with get_db() as conn:
        return conn.execute(
            "SELECT * FROM projects WHERE homeowner_id = ? ORDER BY created_at DESC",
            (homeowner_id,)
        ).fetchall()

def get_projects_by_contractor(contractor_id):
    """Get all projects assigned to a contractor"""
    with get_db() as conn:
        return conn.execute(
            "SELECT * FROM projects WHERE contractor_id = ? ORDER BY created_at DESC",
            (contractor_id,)
        ).fetchall()

def get_all_projects():
    """Get all projects"""
    with get_db() as conn:
        return conn.execute("SELECT * FROM projects ORDER BY created_at DESC").fetchall()

def update_project_status(project_id, status):
    """Update project status"""
    with get_db() as conn:
        completed_at = datetime.now().isoformat() if status == 'completed' else None
        assigned_at = datetime.now().isoformat() if status == 'assigned' else None
        conn.execute(
            "UPDATE projects SET status = ?, assigned_at = COALESCE(assigned_at, ?), completed_at = ? WHERE id = ?",
            (status, assigned_at, completed_at, project_id)
        )
        conn.commit()

def assign_project(project_id, contractor_id, final_cost):
    """Assign project to contractor"""
    with get_db() as conn:
        conn.execute(
            "UPDATE projects SET contractor_id = ?, final_cost = ?, status = 'assigned', assigned_at = ? WHERE id = ?",
            (contractor_id, final_cost, datetime.now().isoformat(), project_id)
        )
        conn.commit()


# ========== QUOTE FUNCTIONS ==========

def save_quote(project_id, contractor_id, amount):
    """Save contractor quote"""
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO quotes (project_id, contractor_id, amount, created_at) VALUES (?,?,?,?)",
            (project_id, contractor_id, amount, datetime.now().isoformat())
        )
        return cursor.lastrowid

def get_quotes_by_project(project_id):
    """Get all quotes for a project"""
    with get_db() as conn:
        return conn.execute(
            "SELECT q.*, c.company_name FROM quotes q JOIN contractors c ON q.contractor_id = c.id WHERE q.project_id = ? ORDER BY q.created_at DESC",
            (project_id,)
        ).fetchall()


# ========== PAYMENT FUNCTIONS ==========

def create_payment(project_id, amount, stripe_intent_id):
    """Create payment record"""
    with get_db() as conn:
        conn.execute(
            "INSERT INTO payments (project_id, amount, stripe_intent_id, created_at) VALUES (?,?,?,?)",
            (project_id, amount, stripe_intent_id, datetime.now().isoformat())
        )
        conn.commit()

def get_payment_by_project(project_id):
    """Get payment for a project"""
    with get_db() as conn:
        return conn.execute("SELECT * FROM payments WHERE project_id = ?", (project_id,)).fetchone()


# For marketplace compatibility
def get_all_projects_admin():
    """Get all projects with join info for admin"""
    with get_db() as conn:
        return conn.execute('''
            SELECT p.*, h.name as homeowner_name, c.company_name 
            FROM projects p
            LEFT JOIN homeowners h ON p.homeowner_id = h.id
            LEFT JOIN contractors c ON p.contractor_id = c.id
            ORDER BY p.created_at DESC
        ''').fetchall()

# Add this at the top
import sqlite3

# Update init_db to include password columns if missing
def migrate_db():
    """Add missing columns to existing tables"""
    with get_db() as conn:
        # Check if password column exists in homeowners
        try:
            conn.execute("SELECT password FROM homeowners LIMIT 1")
        except sqlite3.OperationalError:
            conn.execute("ALTER TABLE homeowners ADD COLUMN password TEXT")
            print("Added password column to homeowners")
        
        # Check if password column exists in contractors
        try:
            conn.execute("SELECT password FROM contractors LIMIT 1")
        except sqlite3.OperationalError:
            conn.execute("ALTER TABLE contractors ADD COLUMN password TEXT")
            print("Added password column to contractors")
        
        conn.commit()

# Call migrate after init_db
def init_db_with_migration():
    init_db()
    migrate_db()

# Add missing get_homeowner_by_email function if not exists
def get_homeowner_by_email(email):
    """Get homeowner by email"""
    with get_db() as conn:
        return conn.execute("SELECT * FROM homeowners WHERE email = ?", (email,)).fetchone()

def save_homeowner(name, email, phone, address, password):
    """Save new homeowner"""
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO homeowners (name, email, phone, address, password, created_at) VALUES (?,?,?,?,?,?)",
            (name, email, phone, address, password, datetime.now().isoformat())
        )
        return cursor.lastrowid

def create_project(homeowner_id, address, dpe_rating, estimated_cost):
    """Create new project"""
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO projects (homeowner_id, property_address, dpe_rating, estimated_cost, status, created_at) VALUES (?,?,?,?,?,?)",
            (homeowner_id, address, dpe_rating, estimated_cost, 'pending', datetime.now().isoformat())
        )
        return cursor.lastrowid
