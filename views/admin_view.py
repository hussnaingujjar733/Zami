import streamlit as st
import os
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
                    if password == os.environ.get("ADMIN_PASSWORD", ""):
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

            new_leads = [p for p in projects if p.get('status') == 'pending'] if projects else []
            contacted_leads = [p for p in projects if p.get('status') == 'contacted'] if projects else []
            assigned_projects = [p for p in projects if p.get('status') == 'assigned'] if projects else []
            revenue_potential = sum((p.get('estimated_cost') or 0) for p in projects) if projects else 0

            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            col_m1.metric("🆕 New leads", len(new_leads))
            col_m2.metric("📞 Contactés", len(contacted_leads))
            col_m3.metric("👷 Assignés", len(assigned_projects))
            col_m4.metric("💶 Potentiel", f"{revenue_potential:,.0f} €")

            if not projects:
                st.info("Aucun projet dans la base de données.")
            else:
                pending_projects = [p for p in projects if p.get('status') == 'pending']

                st.markdown("### 🔥 Nouveaux Leads à Traiter")

                col_filter1, col_filter2 = st.columns(2)

                with col_filter1:
                    priority_filter = st.selectbox(
                        "Priorité",
                        ["Tous les leads", "Priorité haute", "Priorité normale"],
                        key="admin_priority_filter"
                    )

                with col_filter2:
                    contact_filter = st.selectbox(
                        "Contact",
                        ["Tous", "Non contactés", "Contactés"],
                        key="admin_contact_filter"
                    )

                if priority_filter == "Priorité haute":
                    pending_projects = [p for p in pending_projects if (p.get('estimated_cost') or 0) >= 30000]
                elif priority_filter == "Priorité normale":
                    pending_projects = [p for p in pending_projects if (p.get('estimated_cost') or 0) < 30000]

                if contact_filter == "Non contactés":
                    pending_projects = [p for p in pending_projects if not p.get('contacted_at')]
                elif contact_filter == "Contactés":
                    pending_projects = [p for p in pending_projects if p.get('contacted_at')]

                if not pending_projects:
                    st.success("✅ Aucun nouveau lead en attente.")
                else:
                    st.warning(f"⚠️ {len(pending_projects)} nouveau(x) lead(s) en attente")

                    for p in pending_projects:
                        with st.container(border=True):
                            st.markdown(f"### 🏠 Projet #{p.get('id')}")

                            col1, col2 = st.columns(2)

                            with col1:
                                email = p.get('homeowner_email', 'N/A')
                                phone = p.get('homeowner_phone', 'N/A')
                                st.write(f"📍 **Adresse:** {p.get('property_address', 'N/A')}")
                                st.write(f"👤 **Client:** {p.get('homeowner_name', 'N/A')}")
                                st.write(f"📧 **Email:** {email}")
                                st.write(f"📞 **Téléphone:** {phone}")

                                if email != 'N/A' or phone != 'N/A':
                                    st.markdown(
                                        f"""
                                        <div style="margin-top: 0.5rem;">
                                            <a href="mailto:{email}" target="_blank">📧 Envoyer un email</a>
                                            &nbsp; | &nbsp;
                                            <a href="tel:{phone}" target="_blank">📞 Appeler</a>
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )

                            with col2:
                                cost = p.get('estimated_cost') or 0
                                priority = "🔥 Priorité haute" if cost >= 30000 else "🟡 Priorité normale"

                                lead_score = 0
                                if p.get('homeowner_email') and p.get('homeowner_email') != 'N/A':
                                    lead_score += 20
                                if p.get('homeowner_phone') and p.get('homeowner_phone') != 'N/A':
                                    lead_score += 20
                                if p.get('property_address') and len(str(p.get('property_address'))) > 10:
                                    lead_score += 20
                                if cost >= 30000:
                                    lead_score += 25
                                elif cost >= 12000:
                                    lead_score += 15
                                if p.get('dpe_rating') in ['E', 'F', 'G']:
                                    lead_score += 15

                                if lead_score >= 85:
                                    lead_label = "🔥 Hot Lead"
                                elif lead_score >= 60:
                                    lead_label = "🟡 Warm Lead"
                                else:
                                    lead_label = "⚪ Lead à qualifier"

                                st.write(f"🏷️ **DPE:** {p.get('dpe_rating', 'N/A')}")
                                st.write(f"💶 **Estimation:** {cost:,.0f} €")
                                st.write(f"📌 **Statut:** {p.get('status', 'N/A')}")
                                st.write(f"🚦 **Priorité:** {priority}")
                                st.write(f"⭐ **Lead Score:** {lead_score}/100 — {lead_label}")

                            approved_contractors = [
                                c for c in utils_marketplace.get_all_contractors()
                                if c.get('status') == 'approved'
                            ]

                            if approved_contractors:
                                st.markdown("#### 🎯 Artisans recommandés")
                                for contractor in approved_contractors[:3]:
                                    match_score = 70

                                    project_address = str(p.get('property_address', '')).lower()
                                    contractor_city = str(contractor.get('city', '')).lower()

                                    if contractor_city and contractor_city in project_address:
                                        match_score += 20
                                    if contractor.get('rge_certified'):
                                        match_score += 10

                                    match_score = min(match_score, 100)

                                    st.write(
                                        f"👷 **{contractor.get('company_name', 'N/A')}** — "
                                        f"Match: **{match_score}%** | "
                                        f"{contractor.get('city', 'N/A')} | "
                                        f"{contractor.get('phone', 'N/A')}"
                                    )
                            else:
                                st.caption("Aucun artisan approuvé pour le moment.")

                            contacted_at = p.get('contacted_at')
                            if contacted_at:
                                st.success(f"✅ Client contacté le {contacted_at[:10]}")
                            else:
                                if st.button("✅ Marquer comme contacté", key=f"contacted_{p.get('id')}"):
                                    with utils_db_marketplace.get_db() as conn:
                                        conn.execute(
                                            "UPDATE projects SET contacted_at = datetime('now'), status = 'contacted' WHERE id = ?",
                                            (p.get('id'),)
                                        )
                                        conn.commit()
                                    st.success("Client marqué comme contacté.")
                                    st.rerun()

                            st.info("Action recommandée: contacter le client rapidement, puis suivre l’avancement dans le tableau.")

                st.markdown("---")
                st.markdown("### 📋 Tous les Projets")

                df = pd.DataFrame(projects)
                display_cols = [
                    'id',
                    'property_address',
                    'homeowner_name',
                    'homeowner_email',
                    'homeowner_phone',
                    'company_name',
                    'status',
                    'estimated_cost',
                    'created_at'
                ]
                available = [c for c in display_cols if c in df.columns]
                st.dataframe(df[available], use_container_width=True)

                csv_data = df.to_csv(index=False).encode("utf-8")

                st.download_button(
                    "📥 Exporter tous les projets (CSV)",
                    data=csv_data,
                    file_name="zami_projects_export.csv",
                    mime="text/csv",
                    use_container_width=True
                )

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
                avg_project_value = df['estimated_cost'].mean()
                pending_count = len(df[df['status'] == 'pending']) if 'status' in df.columns else 0
                contacted_count = len(df[df['status'] == 'contacted']) if 'status' in df.columns else 0
                assigned_count = len(df[df['status'] == 'assigned']) if 'status' in df.columns else 0
                conversion_rate = round((assigned_count / len(df)) * 100, 1) if len(df) > 0 else 0
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("📊 Projets", len(projects) if projects else 0)
                col2.metric("💶 Volume Total", f"{total_volume:,.0f} €")
                col3.metric("💰 Valeur moyenne", f"{avg_project_value:,.0f} €")
                col4.metric("🎯 Conversion", f"{conversion_rate}%")

                col5, col6, col7 = st.columns(3)
                col5.metric("🆕 New Leads", pending_count)
                col6.metric("📞 Contactés", contacted_count)
                col7.metric("👷 Assignés", assigned_count)

                st.markdown("---")
                st.metric("✨ Commission potentielle ZAMI (10%)", f"{commission:,.0f} €")
            else:
                st.info("Pas assez de données pour afficher les finances.")
        except:
            st.info("Données financières non disponibles")

render = show
