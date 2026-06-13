import streamlit as st
import os
import json
from datetime import datetime
from utils import utils_auth, utils_db_marketplace, utils_marketplace

def show():
    st.markdown("<h2 style='text-align: center; color: #D4AF37;'>👷 Espace Artisan</h2>", unsafe_allow_html=True)

    if not st.session_state.get('artisan_user'):
        st.markdown("""
        <div class="luxury-card" style="text-align:center;">
            <h3 style="color:#D4AF37;">Développez votre activité avec des projets qualifiés</h3>
            <p style="color:#ccc;">
                Rejoignez ZAMI pour recevoir des demandes de rénovation énergétique de propriétaires intéressés.
            </p>
            <p style="color:#D4AF37; font-weight:600;">
                ✓ Leads qualifiés &nbsp; ✓ Devis libres &nbsp; ✓ Visibilité locale &nbsp; ✓ Sans engagement au lancement
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        col1.info("📍 Projets près de votre zone")
        col2.info("💶 Déposez vos devis")
        col3.info("✅ Validation artisan")

    # ========== LOGIN SECTION ==========
    if not st.session_state.get('artisan_user'):
        tab_login, tab_signup = st.tabs(["Connexion", "Inscription"])
        
        with tab_login:
            with st.form("artisan_login_form"):
                email = st.text_input("Email", placeholder="artisan@email.com")
                password = st.text_input("Mot de passe", type="password")
                
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    submitted = st.form_submit_button("Se connecter", type="primary", use_container_width=True)
                
                if submitted:
                    if email and password:
                        user = utils_auth.authenticate_user(email, password, role="contractor")
                        if user:
                            st.session_state.artisan_user = user
                            st.success(f"✅ Bienvenue {user['name']}!")
                            st.rerun()
                        else:
                            st.error("❌ Identifiants incorrects ou compte en attente de validation")
                    else:
                        st.error("Veuillez remplir tous les champs")
        
        with tab_signup:
            with st.form("artisan_signup_form"):
                col1, col2 = st.columns(2)
                with col1:
                    company_name = st.text_input("Nom de l'entreprise *")
                    siret = st.text_input("Numéro SIRET *")
                    city = st.text_input("Ville d'intervention *")
                with col2:
                    email = st.text_input("Email professionnel *")
                    phone = st.text_input("Téléphone *")
                    password = st.text_input("Mot de passe *", type="password")
                
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    submitted_signup = st.form_submit_button("Créer mon compte", type="primary", use_container_width=True)
                
                if submitted_signup:
                    if company_name and email and password:
                        success, message = utils_auth.register_contractor(
                            company_name, siret, email, phone, city, password
                        )
                        if success:
                            st.success(message)
                            st.info("📧 Vous serez notifié par email une fois votre compte approuvé.")
                        else:
                            st.error(message)
                    else:
                        st.error("Veuillez remplir tous les champs obligatoires")
        return
    
    # ========== LOGGED IN VIEW ==========
    artisan_user = st.session_state.artisan_user
    col1, col2 = st.columns([4, 1])
    col1.success(f"👋 Bienvenue, {artisan_user['name']} !")
    if col2.button("🔓 Déconnexion", use_container_width=True):
        st.session_state.artisan_user = None
        st.rerun()
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🆕 Projets disponibles",
        "📊 Mes offres",
        "📋 Mes chantiers",
        "🤖 Upload + IA"
    ])
    
    # ========== TAB 1: AVAILABLE PROJECTS ==========
    with tab1:
        st.subheader("Projets en attente d'offres")
        
        with utils_db_marketplace.get_db() as conn:
            projects = conn.execute('''
                SELECT * FROM projects 
                WHERE status = 'pending' 
                ORDER BY created_at DESC
            ''').fetchall()
        
        if not projects:
            st.info("📭 Aucun projet disponible pour le moment.")
            st.caption("Les nouvelles demandes de rénovation apparaîtront ici dès qu’elles seront disponibles dans votre zone.")
        else:
            for project in projects:
                with st.container(border=True):
                    st.markdown(f"**📍 {project[3]}**")
                    st.write(f"🏷️ DPE: {project[4]} | 💰 Budget: {project[5]:,.0f} €")
                    
                    with st.form(key=f"quote_form_{project[0]}"):
                        quote_amount = st.number_input(
                            "Votre devis (€)",
                            min_value=0.0,
                            value=float(project[5]),
                            step=500.0,
                            key=f"quote_input_{project[0]}"
                        )
                        
                        if st.form_submit_button("📝 Soumettre offre", type="primary"):
                            success = utils_marketplace.submit_quote(
                                project[0], artisan_user['id'], quote_amount
                            )
                            if success:
                                st.success(f"✅ Offre soumise: {quote_amount:,.0f} €")
                                st.rerun()
    
    # ========== TAB 2: MY QUOTES ==========
    with tab2:
        st.subheader("Mes offres soumises")
        
        with utils_db_marketplace.get_db() as conn:
            quotes = conn.execute('''
                SELECT q.*, p.property_address, p.estimated_cost
                FROM quotes q
                JOIN projects p ON q.project_id = p.id
                WHERE q.contractor_id = ?
                ORDER BY q.created_at DESC
            ''', (artisan_user['id'],)).fetchall()
        
        if not quotes:
            st.info("📭 Aucune offre soumise pour le moment. Consultez les projets disponibles et déposez votre premier devis.")
        else:
            for quote in quotes:
                with st.container(border=True):
                    st.markdown(f"**📍 {quote[6]}**")
                    st.write(f"💰 Offre: {quote[3]:,.0f} € | Budget: {quote[7]:,.0f} €")
                    st.write(f"🏷️ Statut: {quote[4]}")
                    
                    if quote[4] == 'pending':
                        st.info("⏳ En attente de validation par le propriétaire")
                    elif quote[4] == 'accepted':
                        st.success("✅ Offre acceptée! Vous serez contacté.")
                    elif quote[4] == 'rejected':
                        st.error("❌ Offre non retenue")
    
    # ========== TAB 3: MY PROJECTS ==========
    with tab3:
        st.subheader("Mes chantiers")
        
        with utils_db_marketplace.get_db() as conn:
            projects = conn.execute('''
                SELECT p.*, h.name as homeowner_name
                FROM projects p
                JOIN homeowners h ON p.homeowner_id = h.id
                WHERE p.contractor_id = ?
                ORDER BY p.created_at DESC
            ''', (artisan_user['id'],)).fetchall()
        
        if not projects:
            st.info("📭 Aucun chantier assigné pour le moment. Lorsqu’un propriétaire accepte votre devis, le chantier apparaîtra ici.")
        else:
            for project in projects:
                with st.container(border=True):
                    st.markdown(f"**📍 {project[3]}**")
                    st.write(f"🏷️ DPE: {project[4]} | 💰 Montant: {project[6]:,.0f} €")
                    st.write(f"📊 Statut: {project[7]} | 👤 Client: {project[11]}")
                    
                    if project[7] == 'assigned':
                        if st.button(f"🔨 Démarrer les travaux", key=f"start_{project[0]}"):
                            utils_marketplace.update_project_status(project[0], 'in_progress')
                            st.rerun()
                    elif project[7] == 'in_progress':
                        if st.button(f"✅ Terminer les travaux", key=f"complete_{project[0]}"):
                            utils_marketplace.update_project_status(project[0], 'completed')
                            st.rerun()
    
    # ========== TAB 4: AI UPLOAD ==========
    with tab4:
        st.subheader("🤖 Upload des photos - Vérification IA")
        
        with utils_db_marketplace.get_db() as conn:
            completed_projects = conn.execute('''
                SELECT * FROM projects 
                WHERE contractor_id = ? AND status = 'completed'
                ORDER BY created_at DESC
            ''', (artisan_user['id'],)).fetchall()
        
        if not completed_projects:
            st.info("Aucun projet terminé en attente d'upload de photos.")
        else:
            for project in completed_projects:
                with st.expander(f"📍 Projet #{project[0]} - {project[3]}", expanded=False):
                    st.info("📸 Upload des photos - Fonctionnalité disponible prochainement")

render = show
