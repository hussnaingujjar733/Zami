import streamlit as st
import os
import json
from datetime import datetime
from utils import utils_auth, utils_db_marketplace, utils_marketplace

# Import AI module
try:
    from utils.ai_quality_check import analyze_project_photos, save_analysis
    AI_AVAILABLE = True
except:
    AI_AVAILABLE = False

def show():
    st.markdown("<h2 style='text-align: center; color: #f59e0b;'>👷 Espace Artisan</h2>", unsafe_allow_html=True)
    
    # ========== LOGIN SECTION ==========
    if not st.session_state.get('artisan_user'):
        st.subheader("Connexion Artisan")
        
        with st.form("artisan_login_form"):
            email = st.text_input("Email", placeholder="artisan@email.com")
            password = st.text_input("Mot de passe", type="password", placeholder="test123")
            
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                submitted = st.form_submit_button("Se connecter", type="primary", use_container_width=True)
            
            if submitted:
                if email and password:
                    with utils_db_marketplace.get_db() as conn:
                        contractor = conn.execute(
                            "SELECT * FROM contractors WHERE email = ?", (email,)
                        ).fetchone()
                        
                        if contractor:
                            if contractor[9] == 'approved':
                                st.session_state.artisan_user = {
                                    'id': contractor[0],
                                    'name': contractor[1],
                                    'email': contractor[3]
                                }
                                st.success(f"✅ Bienvenue {contractor[1]}!")
                                st.rerun()
                            else:
                                st.warning("⚠️ Compte en attente de validation")
                        else:
                            cursor = conn.execute(
                                "INSERT INTO contractors (company_name, email, status, created_at) VALUES (?, ?, 'approved', datetime('now'))",
                                (email.split('@')[0], email)
                            )
                            conn.commit()
                            st.session_state.artisan_user = {
                                'id': cursor.lastrowid,
                                'name': email.split('@')[0],
                                'email': email
                            }
                            st.success(f"✅ Compte créé!")
                            st.rerun()
                else:
                    st.error("Veuillez remplir tous les champs")
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
            st.info("Aucun projet disponible.")
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
                            with utils_db_marketplace.get_db() as conn2:
                                existing = conn2.execute(
                                    "SELECT id FROM quotes WHERE project_id = ? AND contractor_id = ?",
                                    (project[0], artisan_user['id'])
                                ).fetchone()
                                
                                if existing:
                                    conn2.execute(
                                        "UPDATE quotes SET amount = ?, created_at = datetime('now') WHERE id = ?",
                                        (quote_amount, existing[0])
                                    )
                                else:
                                    conn2.execute(
                                        "INSERT INTO quotes (project_id, contractor_id, amount, status, created_at) VALUES (?,?,?,?,datetime('now'))",
                                        (project[0], artisan_user['id'], quote_amount, 'pending')
                                    )
                                conn2.commit()
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
            st.info("Aucune offre soumise.")
        else:
            for quote in quotes:
                with st.container(border=True):
                    st.markdown(f"**📍 {quote[6]}**")
                    st.write(f"💰 Offre: {quote[3]:,.0f} € | Budget: {quote[7]:,.0f} €")
                    st.write(f"🏷️ Statut: {quote[4]}")
    
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
            st.info("Aucun chantier assigné.")
        else:
            for project in projects:
                with st.container(border=True):
                    st.markdown(f"**📍 {project[3]}**")
                    st.write(f"🏷️ DPE: {project[4]} | 💰 Montant: {project[6]:,.0f} €")
                    st.write(f"📊 Statut: {project[7]} | 👤 Client: {project[11]}")
                    
                    if project[7] == 'assigned':
                        if st.button(f"🔨 Démarrer", key=f"start_{project[0]}"):
                            utils_marketplace.update_project_status(project[0], 'in_progress')
                            st.rerun()
                    elif project[7] == 'in_progress':
                        if st.button(f"✅ Terminer", key=f"complete_{project[0]}"):
                            utils_marketplace.update_project_status(project[0], 'completed')
                            st.rerun()
    
    # ========== TAB 4: AI UPLOAD ==========
    with tab4:
        st.subheader("🤖 Upload des photos - Vérification IA")
        st.caption("L'IA analysera vos photos et vérifiera la qualité des travaux")
        
        if not AI_AVAILABLE:
            st.warning("Module IA non disponible. Installation en cours...")
        else:
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
                    project_id = project[0]
                    address = project[3]
                    
                    with st.expander(f"📍 Projet #{project_id} - {address}", expanded=True):
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**📸 Photos AVANT travaux**")
                            before_photos = st.file_uploader(
                                "Choisir les photos avant",
                                type=['jpg', 'jpeg', 'png'],
                                accept_multiple_files=True,
                                key=f"before_{project_id}",
                                label_visibility="collapsed"
                            )
                        
                        with col2:
                            st.write("**📸 Photos APRÈS travaux**")
                            after_photos = st.file_uploader(
                                "Choisir les photos après",
                                type=['jpg', 'jpeg', 'png'],
                                accept_multiple_files=True,
                                key=f"after_{project_id}",
                                label_visibility="collapsed"
                            )
                        
                        if st.button("🤖 Lancer l'analyse IA", key=f"analyze_{project_id}", type="primary"):
                            if before_photos and after_photos:
                                project_dir = f"uploads/projects/project_{project_id}"
                                os.makedirs(project_dir, exist_ok=True)
                                
                                before_paths = []
                                after_paths = []
                                
                                for i, photo in enumerate(before_photos):
                                    path = os.path.join(project_dir, f"before_{i}.jpg")
                                    with open(path, "wb") as f:
                                        f.write(photo.getbuffer())
                                    before_paths.append(path)
                                
                                for i, photo in enumerate(after_photos):
                                    path = os.path.join(project_dir, f"after_{i}.jpg")
                                    with open(path, "wb") as f:
                                        f.write(photo.getbuffer())
                                    after_paths.append(path)
                                
                                with st.spinner("🤖 Analyse IA en cours..."):
                                    from utils.ai_quality_check import analyze_project_photos, save_analysis
                                    results = analyze_project_photos(project_id, before_paths, after_paths)
                                    save_analysis(project_id, results)
                                
                                score = results['overall_score']
                                if score >= 70:
                                    st.success(f"✅ Score: {score}/100 - Travaux validés!")
                                    st.balloons()
                                    utils_marketplace.update_project_status(project_id, 'verified')
                                elif score >= 50:
                                    st.warning(f"⚠️ Score: {score}/100 - Vérification manuelle requise")
                                else:
                                    st.error(f"❌ Score: {score}/100 - Veuillez reprendre les photos")
                                
                                st.rerun()
                            else:
                                st.error("Veuillez uploader des photos AVANT et APRÈS")

render = show
