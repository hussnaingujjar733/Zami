"""
Marketplace utilities for ZAMI
"""

import streamlit as st
from datetime import datetime
from utils import utils_db_marketplace


def row_to_dict(row, columns):
    """Convert SQLite row to dictionary"""
    if not row:
        return None
    return {columns[i]: row[i] for i in range(len(columns))}


def rows_to_dict_list(rows, columns):
    """Convert list of SQLite rows to list of dictionaries"""
    return [row_to_dict(row, columns) for row in rows]


def get_available_projects():
    """Get projects that are pending and not assigned"""
    with utils_db_marketplace.get_db() as conn:
        rows = conn.execute('''
            SELECT p.*, h.name as homeowner_name, h.email as homeowner_email
            FROM projects p
            JOIN homeowners h ON p.homeowner_id = h.id
            WHERE p.status = 'pending'
            ORDER BY p.created_at DESC
        ''').fetchall()
        
        columns = ['id', 'homeowner_id', 'contractor_id', 'property_address', 'dpe_rating', 
                   'estimated_cost', 'final_cost', 'status', 'created_at', 'assigned_at', 
                   'completed_at', 'homeowner_name', 'homeowner_email']
        return rows_to_dict_list(rows, columns)


def submit_quote(project_id, contractor_id, amount):
    """Submit a quote for a project"""
    try:
        with utils_db_marketplace.get_db() as conn:
            conn.execute(
                "INSERT INTO quotes (project_id, contractor_id, amount, status, created_at) VALUES (?,?,?,?,?)",
                (project_id, contractor_id, amount, 'pending', datetime.now().isoformat())
            )
            conn.commit()
        return True
    except Exception as e:
        print(f"Error submitting quote: {e}")
        return False


def get_all_projects_admin():
    """Get all projects with join info for admin"""
    with utils_db_marketplace.get_db() as conn:
        rows = conn.execute('''
            SELECT p.*, h.name as homeowner_name, h.email as homeowner_email, h.phone as homeowner_phone, 
                   c.company_name, c.email as contractor_email
            FROM projects p
            LEFT JOIN homeowners h ON p.homeowner_id = h.id
            LEFT JOIN contractors c ON p.contractor_id = c.id
            ORDER BY p.created_at DESC
        ''').fetchall()
        
        columns = ['id', 'homeowner_id', 'contractor_id', 'property_address', 'dpe_rating',
                   'estimated_cost', 'final_cost', 'status', 'created_at', 'assigned_at',
                   'completed_at', 'homeowner_name', 'homeowner_email', 'homeowner_phone', 'company_name', 'contractor_email']
        return rows_to_dict_list(rows, columns)


def get_all_contractors():
    """Get all contractors as dictionaries"""
    with utils_db_marketplace.get_db() as conn:
        rows = conn.execute("SELECT * FROM contractors ORDER BY created_at DESC").fetchall()
        columns = ['id', 'company_name', 'siret', 'email', 'phone', 'city', 'password', 
                   'rge_certified', 'insurance_file', 'status', 'rating', 'created_at']
        return rows_to_dict_list(rows, columns)


def update_contractor_status(contractor_id, status):
    """Update contractor status"""
    with utils_db_marketplace.get_db() as conn:
        conn.execute("UPDATE contractors SET status = ? WHERE id = ?", (status, contractor_id))
        conn.commit()


def get_homeowner_projects(homeowner_id):
    """Get projects for a homeowner with contractor info"""
    with utils_db_marketplace.get_db() as conn:
        rows = conn.execute('''
            SELECT p.*, c.company_name, c.phone as contractor_phone
            FROM projects p
            LEFT JOIN contractors c ON p.contractor_id = c.id
            WHERE p.homeowner_id = ?
            ORDER BY p.created_at DESC
        ''', (homeowner_id,)).fetchall()
        
        columns = ['id', 'homeowner_id', 'contractor_id', 'property_address', 'dpe_rating',
                   'estimated_cost', 'final_cost', 'status', 'created_at', 'assigned_at',
                   'completed_at', 'company_name', 'contractor_phone']
        return rows_to_dict_list(rows, columns)


def get_contractor_projects(contractor_id):
    """Get projects for a contractor"""
    with utils_db_marketplace.get_db() as conn:
        rows = conn.execute('''
            SELECT p.*, h.name as homeowner_name, h.phone as homeowner_phone
            FROM projects p
            JOIN homeowners h ON p.homeowner_id = h.id
            WHERE p.contractor_id = ?
            ORDER BY p.created_at DESC
        ''', (contractor_id,)).fetchall()
        
        columns = ['id', 'homeowner_id', 'contractor_id', 'property_address', 'dpe_rating',
                   'estimated_cost', 'final_cost', 'status', 'created_at', 'assigned_at',
                   'completed_at', 'homeowner_name', 'homeowner_phone']
        return rows_to_dict_list(rows, columns)


def update_project_status(project_id, status):
    """Update project status"""
    with utils_db_marketplace.get_db() as conn:
        completed_at = datetime.now().isoformat() if status == 'completed' else None
        assigned_at = datetime.now().isoformat() if status == 'assigned' else None
        conn.execute(
            "UPDATE projects SET status = ?, assigned_at = COALESCE(assigned_at, ?), completed_at = ? WHERE id = ?",
            (status, assigned_at, completed_at, project_id)
        )
        conn.commit()


def get_project_by_id(project_id):
    """Get project by ID as dictionary"""
    with utils_db_marketplace.get_db() as conn:
        row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
        if row:
            columns = ['id', 'homeowner_id', 'contractor_id', 'property_address', 'dpe_rating',
                       'estimated_cost', 'final_cost', 'status', 'created_at', 'assigned_at', 'completed_at']
            return row_to_dict(row, columns)
    return None


def create_project_from_estimation(name, email, phone, address, estimated_cost, dpe_rating):
    """Create project from estimation form"""
    try:
        from utils import utils_auth
        
        # Check if homeowner exists
        homeowner = utils_db_marketplace.get_homeowner_by_email(email)
        
        if not homeowner:
            # Create new homeowner (homeowner is a tuple)
            homeowner_id = utils_db_marketplace.save_homeowner(
                name, email, phone, address, 
                utils_auth.hash_password("zami123")
            )
        else:
            homeowner_id = homeowner[0]  # Tuple, first element is id

        # Prevent duplicate pending/active lead for same homeowner and same address
        with utils_db_marketplace.get_db() as conn:
            existing_project = conn.execute(
                """
                SELECT id FROM projects
                WHERE homeowner_id = ?
                  AND property_address = ?
                  AND status IN ('pending', 'assigned', 'in_progress')
                LIMIT 1
                """,
                (homeowner_id, address)
            ).fetchone()

        if existing_project:
            print(f"Duplicate project ignored: homeowner={homeowner_id}, address={address}")
            return True
        
        # Create project
        project_id = utils_db_marketplace.create_project(
            homeowner_id, address, dpe_rating, estimated_cost
        )
        
        return project_id is not None
    except Exception as e:
        print(f"Error creating project: {e}")
        return False


def accept_quote(project_id, quote_id):
    """Accept a contractor's quote"""
    with utils_db_marketplace.get_db() as conn:
        quote = conn.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,)).fetchone()
        if quote:
            conn.execute(
                "UPDATE projects SET contractor_id = ?, final_cost = ?, status = 'assigned' WHERE id = ?",
                (quote[2], quote[3], project_id)
            )
            conn.execute("UPDATE quotes SET status = 'accepted' WHERE id = ?", (quote_id,))
            conn.commit()
            return True
    return False

def submit_quote(project_id, contractor_id, amount):
    """Submit a quote for a project - FIXED VERSION"""
    try:
        with utils_db_marketplace.get_db() as conn:
            # Check if quote already exists for this contractor
            existing = conn.execute(
                "SELECT id FROM quotes WHERE project_id = ? AND contractor_id = ?",
                (project_id, contractor_id)
            ).fetchone()
            
            if existing:
                # Update existing quote
                conn.execute(
                    "UPDATE quotes SET amount = ?, created_at = ? WHERE id = ?",
                    (amount, datetime.now().isoformat(), existing[0])
                )
                st.success("✅ Devis mis à jour!")
            else:
                # Insert new quote
                conn.execute(
                    "INSERT INTO quotes (project_id, contractor_id, amount, status, created_at) VALUES (?,?,?,?,?)",
                    (project_id, contractor_id, amount, 'pending', datetime.now().isoformat())
                )
                st.success("✅ Offre soumise avec succès!")
            conn.commit()
            return True
    except Exception as e:
        st.error(f"❌ Erreur: {str(e)}")
        return False
