"""
Fix database schema for Render deployment
Adds missing columns and creates tables
"""

import sqlite3
import os

def fix_database():
    """Add missing columns to existing tables"""
    
    db_path = 'marketplace.db'
    
    # Check if database exists
    if not os.path.exists(db_path):
        print("Database not found, creating new one...")
        from utils import utils_db_marketplace
        utils_db_marketplace.init_db()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check and add missing column to contractors table
    try:
        cursor.execute("SELECT stripe_account_id FROM contractors LIMIT 1")
        print("✅ stripe_account_id column exists")
    except sqlite3.OperationalError:
        print("Adding stripe_account_id column to contractors...")
        cursor.execute("ALTER TABLE contractors ADD COLUMN stripe_account_id TEXT")
        conn.commit()
        print("✅ stripe_account_id column added")
    
    # Check and add other missing columns
    missing_columns = [
        ("contractors", "rating", "REAL DEFAULT 0"),
        ("contractors", "insurance_file", "TEXT"),
        ("projects", "final_cost", "REAL"),
        ("projects", "assigned_at", "TEXT"),
        ("projects", "completed_at", "TEXT"),
        ("payments", "released_at", "TEXT"),
    ]
    
    for table, column, col_type in missing_columns:
        try:
            cursor.execute(f"SELECT {column} FROM {table} LIMIT 1")
            print(f"✅ {table}.{column} exists")
        except sqlite3.OperationalError:
            print(f"Adding {table}.{column}...")
            try:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")
                conn.commit()
                print(f"✅ {table}.{column} added")
            except Exception as e:
                print(f"⚠️ Could not add {table}.{column}: {e}")
    
    # Create verifications table if not exists
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
    
    # Create agencies table if not exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS agencies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        address TEXT,
        created_at TEXT
    )
    ''')
    
    conn.commit()
    conn.close()
    
    print("\n✅ Database schema update complete!")

if __name__ == "__main__":
    fix_database()
