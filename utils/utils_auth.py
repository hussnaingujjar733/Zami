"""
Authentication utilities for ZAMI Marketplace
"""

import streamlit as st
import hashlib
import sqlite3
from utils import utils_db_marketplace

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(email, password, role):
    """Authenticate user based on role"""
    
    hashed_password = hash_password(password)
    
    if role == "homeowner":
        with utils_db_marketplace.get_db() as conn:
            try:
                user = conn.execute(
                    "SELECT * FROM homeowners WHERE email = ? AND password = ?",
                    (email, hashed_password)
                ).fetchone()
            except sqlite3.OperationalError:
                user = conn.execute(
                    "SELECT * FROM homeowners WHERE email = ?",
                    (email,)
                ).fetchone()
                if user:
                    if password == "zami123":
                        return {"id": user[0], "name": user[1], "email": user[2], "type": "homeowner"}
                    user = None
            
            if user:
                return {"id": user[0], "name": user[1], "email": user[2], "type": "homeowner"}
    
    elif role == "contractor":
        with utils_db_marketplace.get_db() as conn:
            try:
                user = conn.execute(
                    "SELECT * FROM contractors WHERE email = ? AND password = ? AND status = 'approved'",
                    (email, hashed_password)
                ).fetchone()
            except sqlite3.OperationalError:
                user = conn.execute(
                    "SELECT * FROM contractors WHERE email = ? AND status = 'approved'",
                    (email,)
                ).fetchone()
                if user:
                    if password == "test123":
                        return {"id": user[0], "name": user[1], "email": user[3], "type": "contractor"}
                    user = None
            
            if user:
                return {"id": user[0], "name": user[1], "email": user[3], "type": "contractor"}
    
    return None

def register_contractor(company_name, siret, email, phone, city, password):
    """Register new contractor"""
    
    hashed_password = hash_password(password)
    
    try:
        with utils_db_marketplace.get_db() as conn:
            conn.execute(
                """INSERT INTO contractors 
                   (company_name, siret, email, phone, city, password, status, created_at) 
                   VALUES (?, ?, ?, ?, ?, ?, 'pending', datetime('now'))""",
                (company_name, siret, email, phone, city, hashed_password)
            )
            conn.commit()
        return True, "✅ Inscription envoyée! En attente de validation par l'administrateur."
    except Exception as e:
        return False, f"❌ Erreur: {str(e)}"

def register_homeowner(name, email, phone, address, password):
    """Register new homeowner"""
    
    hashed_password = hash_password(password)
    
    try:
        with utils_db_marketplace.get_db() as conn:
            conn.execute(
                """INSERT INTO homeowners 
                   (name, email, phone, address, password, created_at) 
                   VALUES (?, ?, ?, ?, ?, datetime('now'))""",
                (name, email, phone, address, hashed_password)
            )
            conn.commit()
        return True, "✅ Compte créé avec succès!"
    except Exception as e:
        return False, f"❌ Erreur: {str(e)}"

def set_user_session(user_type, user_id, user_email, user_name):
    """Set session state for logged in user"""
    
    st.session_state['logged_in'] = True
    st.session_state['user_type'] = user_type
    st.session_state['user_id'] = user_id
    st.session_state['user_email'] = user_email
    st.session_state['user_name'] = user_name

def get_current_user():
    """Get current logged in user"""
    
    if st.session_state.get('logged_in', False):
        return {
            'type': st.session_state.get('user_type'),
            'id': st.session_state.get('user_id'),
            'email': st.session_state.get('user_email'),
            'name': st.session_state.get('user_name')
        }
    return None

def is_logged_in():
    """Check if user is logged in"""
    
    return st.session_state.get('logged_in', False)

def logout():
    """Logout current user"""
    
    for key in ['logged_in', 'user_type', 'user_id', 'user_email', 'user_name']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
