import streamlit as st
import pandas as pd
from utils import utils_marketplace, utils_db_marketplace

def show():
    st.markdown("<h2 style='text-align: center; color: #D4AF37;'>⚜️ Panneau d'Administration</h2>", unsafe_allow_html=True)
    
    if not st.session_state.get('admin_logged_in', False):
        with st.container(border=True):
            st.info("🔐 Espace sécurisé - Réservé à l'administration")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                password = st.text_input("Mot de passe administrateur", type="password")
                if st.button("Se connecter", type="primary", use_container_width=True):
                    if password == "admin2026":
                        st.session_state.admin_logged_in = True
                        st.rerun()
                    else:
                        st.error("❌ Mot de passe incorrect")
        return
    
    st.success("✅ Connecté en tant qu'Administrateur")
    
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🔓 Déconnexion", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.rerun()
    
    tab_art, tab_proj, tab_fin = st.tabs(["👥 Validation Artisans", "📊 Gestion des Projets", "💰 Finances"])
    
    # ========== TAB 1: ARTISANS ==========
    with tab_art:
        st.subheader("📋 Demandes d'inscription (Artisans en attente)")
        
        try:
            contractors = utils_marketplace.get_all_contractors()
            pending = [c for c in contractors if c.get('status') == 'pending'] if contractors else []
            
            if not pending:
                st.info("✅ Aucun artisan en attente de validation.")
            else:
                st.warning(f"⚠️ {len(pending)} artisan(s) en attente d'approbation")
                
                for c in pending:
                    with st.container(border=True):
                        st.markdown(f"**🏢 {c.get('company_name', 'N/A')}**")
                        col_info1, col_info2 = st.columns(2)
                        with col_info1:
                            st.write(f"📧 Email: {c.get('email', 'N/A')}")
                            st.write(f"📞 Téléphone: {c.get('phone', 'N/A')}")
                        with col_info2:
                            st.write(f"📍 Ville: {c.get('city', 'N/A')}")
                            st.write(f"📄 SIRET: {c.get('siret', 'N/A')}")
                        
                        if c.get('rge_certified'):
                            st.success("✅ Certifié RGE")
                        
                        col_approve, col_reject = st.columns(2)
                        with col_approve:
                            if st.button(f"✅ Approuver", key=f"app_{c['id']}", type="primary"):
                                utils_marketplace.update_contractor_status(c['id'], 'approved')
                                st.success(f"✅ {c.get('company_name')} a été approuvé!")
                                st.rerun()
                        with col_reject:
                            if st.button(f"❌ Rejeter", key=f"rej_{c['id']}"):
                                utils_marketplace.update_contractor_status(c['id'], 'rejected')
                                st.warning(f"❌ {c.get('company_name')} a été rejeté.")
                                st.rerun()
            
            with st.expander("👷 Voir les artisans validés"):
                approved = [c for c in contractors if c.get('status') == 'approved'] if contractors else []
                for c in approved:
                    st.write(f"✅ {c.get('company_name', 'N/A')} - {c.get('city', 'N/A')}")
                    
        except Exception as e:
            st.error(f"Erreur: {e}")
    
    # ========== TAB 2: PROJECTS ==========
    with tab_proj:
        st.subheader("📊 Supervision Globale des Projets")

        try:
            projects = utils_marketplace.get_all_projects_admin()

            if not projects:
                st.info("Aucun projet dans la base de données.")
            else:
                pending_projects = [p for p in projects if p.get('status') == 'pending']

                st.markdown("### 🔥 Nouveaux Leads à Traiter")

                if not pending_projects:
                    st.success("✅ Aucun nouveau lead en attente.")
                else:
                    st.warning(f"⚠️ {len(pending_projects)} nouveau(x) lead(s) en attente")

                    for p in pending_projects:
                        with st.container(border=True):
                            st.markdown(f"### 🏠 Projet #{p.get('id')}")

                            col1, col2 = st.columns(2)

                            with col1:
                                st.write(f"📍 **Adresse:** {p.get('property_address', 'N/A')}")
                                st.write(f"👤 **Client:** {p.get('homeowner_name', 'N/A')}")
                                st.write(f"📧 **Email:** {p.get('homeowner_email', 'N/A')}")

                            with col2:
                                cost = p.get('estimated_cost') or 0
                                st.write(f"🏷️ **DPE:** {p.get('dpe_rating', 'N/A')}")
                                st.write(f"💶 **Estimation:** {cost:,.0f} €")
                                st.write(f"📌 **Statut:** {p.get('status', 'N/A')}")

                            st.info("Action recommandée: contacter le client ou assigner un artisan validé.")

                st.markdown("---")
                st.markdown("### 📋 Tous les Projets")

                df = pd.DataFrame(projects)
                display_cols = [
                    'id',
                    'property_address',
                    'homeowner_name',
                    'homeowner_email',
                    'company_name',
                    'status',
                    'estimated_cost',
                    'created_at'
                ]
                available = [c for c in display_cols if c in df.columns]
                st.dataframe(df[available], use_container_width=True)

        except Exception as e:
            st.error(f"Erreur lors du chargement des projets: {e}")
    
    # ========== TAB 3: FINANCES ==========
    with tab_fin:
        st.subheader("💰 Vue d'ensemble Financière")
        try:
            projects = utils_marketplace.get_all_projects_admin()
            df = pd.DataFrame(projects) if projects else pd.DataFrame()
            
            if not df.empty and 'estimated_cost' in df.columns:
                total_volume = df['estimated_cost'].sum()
                commission = total_volume * 0.10
                
                col1, col2, col3 = st.columns(3)
                col1.metric("📊 Projets", len(projects) if projects else 0)
                col2.metric("💶 Volume Total", f"{total_volume:,.0f} €")
                col3.metric("✨ Commission ZAMI (10%)", f"{commission:,.0f} €")
            else:
                st.info("Pas assez de données pour afficher les finances.")
        except:
            st.info("Données financières non disponibles")

render = show
