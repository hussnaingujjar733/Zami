import streamlit as st
from utils import utils_auth, utils_db_marketplace, utils_marketplace
from utils.stripe_payments import simple_payment_button, STRIPE_AVAILABLE

def show():
    st.markdown("<h2 style='text-align: center; color: #34d399;'>🏠 Espace Client ZAMI</h2>", unsafe_allow_html=True)
    
    # ========== LOGIN SECTION ==========
    if not st.session_state.get('client_user'):
        with st.form("client_login"):
            email = st.text_input("Email")
            password = st.text_input("Mot de passe", type="password")
            
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.form_submit_button("Se connecter", type="primary", use_container_width=True):
                    user = utils_auth.authenticate_user(email, password, role="homeowner")
                    if user:
                        st.session_state.client_user = user
                        st.rerun()
                    else:
                        st.error("❌ Identifiants incorrects.")
        
        with st.expander("📝 Pas encore de compte? Inscrivez-vous"):
            with st.form("client_signup"):
                name = st.text_input("Nom complet")
                email = st.text_input("Email")
                phone = st.text_input("Téléphone")
                address = st.text_input("Adresse")
                password = st.text_input("Mot de passe", type="password")
                
                if st.form_submit_button("Créer mon compte", type="primary"):
                    if name and email and password:
                        success, msg = utils_auth.register_homeowner(name, email, phone, address, password)
                        if success:
                            st.success(msg)
                            st.info("Vous pouvez maintenant vous connecter")
                        else:
                            st.error(msg)
                    else:
                        st.error("Veuillez remplir tous les champs obligatoires")
        return
    
    # ========== LOGGED IN VIEW ==========
    user = st.session_state.client_user
    col1, col2 = st.columns([4, 1])
    col1.success(f"👋 Bienvenue, {user['name']} !")
    if col2.button("🔓 Déconnexion", use_container_width=True):
        st.session_state.client_user = None
        st.rerun()
    
    # Get homeowner projects
    homeowner_id = user['id']
    
    with utils_db_marketplace.get_db() as conn:
        projects = conn.execute('''
            SELECT p.*, c.company_name, "" as stripe_account_id
            FROM projects p
            LEFT JOIN contractors c ON p.contractor_id = c.id
            WHERE p.homeowner_id = ? 
            ORDER BY p.created_at DESC
        ''', (homeowner_id,)).fetchall()
    
    if not projects:
        st.info("📭 Vous n'avez pas encore de projet.")
        st.markdown("👉 Allez dans **'🔍 Nouvelle Estimation'** pour estimer et publier votre premier projet!")
        return
    
    st.subheader(f"📋 Mes projets ({len(projects)})")
    
    for project in projects:
        project_id = project[0]
        address = project[3]
        dpe = project[4]
        est_cost = project[5]
        final_cost = project[6]
        project_status = project[7]
        created_at = project[8]
        company_name = project[11] if len(project) > 11 else None
        stripe_account_id = project[12] if len(project) > 12 else None
        
        # Status config
        status_config = {
            'pending': {'emoji': '⏳', 'color': 'orange', 'text': 'Demande envoyée - en attente de devis'},
            'assigned': {'emoji': '👷', 'color': 'blue', 'text': 'Artisan assigné'},
            'in_progress': {'emoji': '🔨', 'color': 'orange', 'text': 'Travaux en cours'},
            'completed': {'emoji': '✅', 'color': 'green', 'text': 'Terminé - En vérification'},
            'verified': {'emoji': '✔️', 'color': 'green', 'text': 'Vérifié - En attente paiement'},
            'paid': {'emoji': '💰', 'color': 'green', 'text': 'Payé - Projet clôturé'},
            'paid_by_homeowner': {'emoji': '💳', 'color': 'blue', 'text': 'Paiement effectué - Travaux en cours'}
        }
        config = status_config.get(project_status, {'emoji': '📋', 'color': 'gray', 'text': project_status})
        
        with st.container(border=True):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**📍 {address}**")
                st.write(f"🏷️ DPE: {dpe} | 📅 Créé: {created_at[:10] if created_at else 'N/A'}")
                st.write(f"💰 Budget estimé: {est_cost:,.0f} €")
                if final_cost:
                    st.write(f"💰 Devis accepté: {final_cost:,.0f} €")
            
            with col_b:
                st.markdown(f"<p style='color: {config['color']}; font-weight: bold;'>{config['emoji']} {config['text']}</p>", unsafe_allow_html=True)
            
            # Handle different statuses
            if project_status == 'pending':
                # Show quotes from artisans
                with utils_db_marketplace.get_db() as conn:
                    quotes = conn.execute('''
                        SELECT q.*, c.company_name, c.phone, c.email
                        FROM quotes q
                        JOIN contractors c ON q.contractor_id = c.id
                        WHERE q.project_id = ? AND q.status = 'pending'
                        ORDER BY q.amount ASC
                    ''', (project_id,)).fetchall()
                
                if quotes:
                    st.markdown("---")
                    st.markdown("### 📝 Offres reçues des artisans")
                    
                    best_price = quotes[0][3] if quotes else None

                    for quote in quotes:
                        with st.container(border=True):
                            is_best = best_price is not None and quote[3] == best_price
                            badge = "🏆 Meilleure offre" if is_best else "👷 Artisan partenaire"

                            st.markdown(f"### {badge}")
                            st.markdown(f"**Entreprise:** {quote[6]}")

                            col_q1, col_q2, col_q3 = st.columns(3)
                            col_q1.metric("💰 Devis proposé", f"{quote[3]:,.0f} €")
                            col_q2.metric("📊 Écart vs budget", f"{quote[3] - est_cost:,.0f} €")
                            col_q3.metric("📌 Statut", "En attente")

                            st.write(f"📞 Contact: {quote[7]} | {quote[8]}")
                            st.caption("Comparez le prix, contactez l'artisan si besoin, puis acceptez l'offre qui vous convient.")
                            
                            col_acc, col_rej = st.columns(2)
                            with col_acc:
                                if st.button(f"✅ Accepter cette offre", key=f"accept_{quote[0]}"):
                                    with utils_db_marketplace.get_db() as conn2:
                                        conn2.execute(
                                            "UPDATE projects SET contractor_id = ?, final_cost = ?, status = 'assigned' WHERE id = ?",
                                            (quote[2], quote[3], project_id)
                                        )
                                        conn2.execute(
                                            "UPDATE quotes SET status = 'accepted' WHERE id = ?",
                                            (quote[0],)
                                        )
                                        conn2.commit()
                                    st.success(f"✅ Offre acceptée! L'artisan va vous contacter.")
                                    st.rerun()
                            
                            with col_rej:
                                if st.button(f"❌ Refuser", key=f"reject_{quote[0]}"):
                                    with utils_db_marketplace.get_db() as conn2:
                                        conn2.execute(
                                            "UPDATE quotes SET status = 'rejected' WHERE id = ?",
                                            (quote[0],)
                                        )
                                        conn2.commit()
                                    st.rerun()
                else:
                    st.info("🕒 En attente d'offres d'artisans...")
            
            elif project_status == 'assigned':
                st.success(f"👷 Artisan sélectionné: **{company_name}**")
                st.write(f"💰 Devis accepté: {final_cost or est_cost:,.0f} €")
                st.info("✅ Votre demande est confirmée. L'artisan va vous contacter pour organiser la visite technique.")
                st.caption("Paiement en ligne bientôt disponible. Pour le lancement, le paiement se fait directement après validation du devis final.")
            
            elif project_status == 'paid_by_homeowner':
                st.success("✅ Paiement confirmé! Les travaux peuvent commencer.")
                if st.button(f"📞 Contacter l'artisan", key=f"contact_{project_id}"):
                    st.info("L'artisan sera notifié.")
            
            elif project_status == 'in_progress':
                st.warning("🔨 Travaux en cours de réalisation...")
            
            elif project_status == 'completed':
                st.success("✅ Travaux déclarés terminés. ZAMI vérifie les éléments avant clôture du projet.")
            
            elif project_status == 'verified':
                st.success("✔️ Travaux vérifiés! Veuillez procéder au paiement final.")
                
                # Final payment button
                simple_payment_button(
                    amount=final_cost or est_cost,
                    project_id=project_id,
                    homeowner_email=user['email']
                )
            
            elif project_status == 'paid':
                st.success("🎉 Projet terminé et payé! Merci pour votre confiance.")
                if st.button(f"📄 Télécharger la facture", key=f"invoice_{project_id}"):
                    st.info("Facture en cours de génération.")

render = show
