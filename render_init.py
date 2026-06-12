"""
Database initialization script for Render deployment
Run this before starting the app
"""

import sqlite3
import os
from datetime import datetime

print("=== Initializing Database for Render === ")

# Ensure the database file is created
db_path = "marketplace.db"

# Remove old database if exists (start fresh)
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Removed old database: {db_path}")

# Create new database with all tables
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create homeowners table
cursor.execute('''
CREATE TABLE IF NOT EXISTS homeowners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    phone TEXT,
    address TEXT,
    password TEXT,
    created_at TEXT
)
''')

# Create contractors table
cursor.execute('''
CREATE TABLE IF NOT EXISTS contractors (
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
)
''')

# Create projects table
cursor.execute('''
CREATE TABLE IF NOT EXISTS projects (
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
)
''')

# Create quotes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    contractor_id INTEGER,
    amount REAL,
    status TEXT DEFAULT 'pending',
    created_at TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (contractor_id) REFERENCES contractors(id)
)
''')

# Create payments table
cursor.execute('''
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    amount REAL,
    status TEXT DEFAULT 'pending',
    stripe_intent_id TEXT,
    created_at TEXT,
    released_at TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id)
)
''')

# Create verifications table
cursor.execute('''
CREATE TABLE IF NOT EXISTS verifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    photo_paths TEXT,
    ai_score REAL,
    verified_at TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id)
)
''')

# Insert a test contractor for development
cursor.execute('''
INSERT OR IGNORE INTO contractors (company_name, email, status, created_at)
VALUES ('Demo Artisan', 'demo@artisan.com', 'approved', datetime('now'))
''')

# Insert a test homeowner
cursor.execute('''
INSERT OR IGNORE INTO homeowners (name, email, password, created_at)
VALUES ('Demo Client', 'demo@client.com', 'zami123', datetime('now'))
''')

conn.commit()
conn.close()

print(" Database tables created successfully!")
print(f"Database location: {db_path}")
print(" Tables: homeowners, contractors, projects, quotes, payments, verifications")
print("=== Database initialization complete ===")
