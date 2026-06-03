import os
import base64
import random
import io
import sqlite3
import requests
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from fpdf import FPDF
from streamlit_folium import st_folium
import folium

# ── ⚡ IMPORT REFACTORED COMMERCIAL ENTERPRISE ENGINE MODULES ──
import utils_styles
import utils_db
import utils_charts

try:
    import ml_engine as ml
    ML_BACKEND_READY = True
except ImportError:
    ML_BACKEND_READY = False

# Boot systems databases
utils_db.init_db()

# Run Style Injection Layers
utils_styles.inject_premium_styles()

# ─────────────────────────────────────────────
# STATE INTERFACE STORAGE ROUTING
# ─────────────────────────────────────────────
if "logged_in_user_id" not in st.session_state: st.session_state["logged_in_user_id"] = None
if "logged_in_username" not in st.session_state: st.session_state["logged_in_username"] = None
if "confirmed_owner_property" not in st.session_state: st.session_state["confirmed_owner_property"] = None
if "address_suggestions" not in st.session_state: st.session_state["address_suggestions"] = []
if "selected_scenario" not in st.session_state: st.session_state["selected_scenario"] = "Essential"

# Global Variables setup
_SCENARIO_COST_MULTIPLIER = {"Essential": 1.0, "Plus": 1.65, "Zero": 2.45}
_SCENARIO_ROI_MULTIPLIER  = {"Essential": 1.0, "Plus": 1.45, "Zero": 1.95}
_SCENARIO_TARGET_DPE     = {"Essential": "D", "Plus": "C", "Zero": "B"}
_FALLBACK_RENO_COST = {"G": 1350, "F": 1100, "E": 620, "D": 280, "C": 120, "B": 0, "A": 0}
_FALLBACK_UPLIFT    = {"G": 24.2, "F": 19.8, "E": 13.1, "D": 6.8, "C": 2.0, "B": 0, "A": 0}
_DPE_COLORS         = {"A": "#319834", "B": "#33cc33", "C": "#ccff33", "D": "#f2b035", "E": "#ff6600", "F": "#ff3300", "G": "#ff0000"}
_INCOME_SUBSIDY_MAP = {"Très Modeste (Bleu)": 0.75, "Modeste (Jaune)": 0.60, "Intermédiaire (Violet)": 0.40, "Supérieur (Rose)": 0.15}

def safe_get(url, params=None):
    try:
        r = requests.get(url, params=params, timeout=10)
        return r.json()
    except Exception: return None

def ban_search(query: str, limit: int = 5):
    if not query or len(query.strip()) < 3: return []
    data = safe_get("https://api-adresse.data.gouv.fr/search/", {"q": query, "limit": limit})
    features = data.get("features", []) if data else []
    results = []
    for f in features:
        p = f.get("properties", {})
        c = f.get("geometry", {}).get("coordinates", [2.3522, 48.8566])
        results.append({"label": p.get("label", ""), "postcode": p.get("postcode", ""), "city": p.get("city", ""), "lon": c[0], "lat": c[1]})
    return results

def fetch_single_property_ademe(query_address: str, zipcode: str, lat=48.8566, lon=2.3522):
    random.seed(int(len(query_address)))
    mock_dpe = random.choice(["E", "F", "G"])
    mock_surface = random.randint(30, 95)
    if ML_BACKEND_READY and hasattr(ml, "predict_cost"):
        try: cost = ml.predict_cost(mock_surface, mock_dpe, zipcode)
        except Exception: cost = round(float(mock_surface) * _FALLBACK_RENO_COST.get(mock_dpe, 0), 0)
    else: cost = round(float(mock_surface) * _FALLBACK_RENO_COST.get(mock_dpe, 0), 0)
    roi = round(_FALLBACK_UPLIFT.get(mock_dpe, 0.0), 1)
    return {"address": query_address, "dpe": mock_dpe, "surface": mock_surface, "cost": cost, "roi": roi, "zipcode": zipcode, "lat": lat, "lon": lon}

# Language translation matrix mapping framework
LANG_DICT = {"FR": {"title": "Portail SaaS Propriétaire Énergétique", "subtitle": "Estimez et gérez vos actifs immobiliers", "form_name": "Nom Complet *", "form_phone": "Numéro de Téléphone *", "form_email": "Adresse Email *", "form_time": "Créneau de rappel souhaité", "form_notes": "Précisions complémentaires (facultatif)", "form_btn": "📨 Envoyer ma demande de RDV", "form_err": "⚠️ Veuillez remplir tous les champs obligatoires (*).", "form_success": "🎉 Félicitations ! Votre demande a été enregistrée.", "download_btn": "⬇️ Télécharger mon Rapport PDF Officiel", "map_title": "🗺️ Cartographie Spatiale & Cadastre Registre", "loss_title": "🌡️ Analyse AI des Déperditons Thermiques Estimées", "income_label": "💰 Sélectionnez votre Profil de Revenu (Anah) :", "loan_title": "💶 Simulateur Financement : Eco-Prêt à Taux Zéro (Eco-PTZ)", "loan_duration": "Durée du Prêt (Années)", "monthly_pay": "Mensualité Estimée", "footer": "ZAMI v8.1 SaaS Premium — Identity & Portfolio Stack Operational • Données ADEME", "budget_est": "Budget Estimé", "surface": "Surface", "uplift_label": "Uplift Patrimoine", "current_class": "Classe Initiale", "target_class": "🎯 Cible", "visual_prog": "Progression Énergétique Visuelle", "fin_title": "Cockpit Financier & Graphiques", "fin_sub": "Aides d'État Proportional Base", "subvention_label": "MaPrimeRénov'", "reste_charge": "Reste à charge", "chart_5yr_title": "📊 Évolution Prédictive du Patrimoine (5 Ans)", "chart_5yr_sub": "Rénové vs Non-Rénové Asset Value Curves", "impact_facture": "Impact Facture: En choisissant le plan {sc}, vous économisez {saving} en moyenne."}, "EN": {"title": "SaaS Energy Portal Platform", "subtitle": "Track, simulate and save your certified real-estate properties", "form_name": "Full Name *", "form_phone": "Phone Number *", "form_email": "Email Address *", "form_time": "Callback window preference", "form_notes": "Project notes (optional)", "form_btn": "📨 Submit Request to Local RGE", "form_err": "⚠️ Required fields missing.", "form_success": "🎉 Request recorded into core databases.", "download_btn": "⬇️ Download Official PDF Analytical Summary", "map_title": "🗺️ Geospatial Layer Mapping Infrastructure", "loss_title": "🌡️ Structural Defect Heat Losses Estimation", "income_label": "💰 Anah Income Profile Mapping Vector:", "loan_title": "💶 Financing Leverage Selector: Eco-PTZ Framework", "loan_duration": "Amortization Matrix (Years)", "monthly_pay": "Estimated Payment Factor", "footer": "ZAMI v8.1 SaaS Premium — Identity & Portfolio Stack Operational • ADEME Core", "budget_est": "Budget Estimate", "surface": "Surface Area", "uplift_label": "Asset Value Growth", "current_class": "Initial Class", "target_class": "🎯 Target Scenario", "visual_prog": "Energy Progression Flow Chart View", "fin_title": "Capital Deployment Analysis Charting", "fin_sub": "State Financing Allocations vs Net Capital Out", "subvention_label": "State Grants Matrix", "reste_charge": "Net out-of-pocket", "chart_5yr_title": "📊 5-Year Financial Projection Curve Track", "chart_5yr_sub": "Asset Trajectory Mapping Layout", "impact_facture": "Energy Invoices Vector: Choosing plan {sc} yields ~{saving} annual savings."}}

# Headers Layout setup
col_logo, col_lang = st.columns([2.5, 0.5])
with col_lang: selected_lang = st.selectbox("🌐 Language", ["FR", "EN"], label_visibility="collapsed")
T = LANG_DICT[selected_lang]

# Render logo html container parameters 
st.markdown('<div class="brand-header-flex" style="margin-top:-30px;"><div style="font-family:\'DM Sans\', serif; font-size:2.2rem; color:#fff; font-weight:700;">🏢 ZA<span style="color:#22c55e;">MI</span></div><div><span class="brand-status-tag">ZAMI PLATINUM SAAS V8.1</span></div></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 🔐 THE SAAS ACCUMULATION & ENTRY CONTROL LAYER
# ─────────────────────────────────────────────
if st.session_state["logged_in_user_id"] is None:
    st.markdown('<div class="card" style="max-width: 500px; margin: 4rem auto;">', unsafe_allow_html=True)
    auth_mode = st.radio("Access Control Gate", ["Connexion (Login)", "Inscription (Sign Up)"], horizontal=True, label_visibility="collapsed")
    
    with st.form("identity_auth_form"):
        username_f = st.text_input("Username *", placeholder="hussnain_zami")
        email_f = st.text_input("Email Address *", placeholder="owner@zami.fr") if auth_mode == "Inscription (Sign Up)" else None
        password_f = st.text_input("Password *", type="password", placeholder="••••••••")
        submit_auth = st.form_submit_button("Execute Authentication Token")
        
        if submit_auth:
            if not username_f or not password_f:
                st.error("Please fill in all mandatory parameters.")
            else:
                if auth_mode == "Inscription (Sign Up)":
                    if utils_db.create_user(username_f, email_f if email_f else "", password_f):
                        st.success("Registration Successful! Shifting to login console...")
                        time.sleep(1)
                    else: st.error("Username or Email already mapped inside the matrix.")
                else:
                    user_id_check = utils_db.authenticate_user(username_f, password_f)
                    if user_id_check:
                        st.session_state["logged_in_user_id"] = user_id_check
                        st.session_state["logged_in_username"] = username_f
                        st.rerun()
                    else: st.error("Access Denied: Invalid credential arrays.")
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 🏢 ACTIVE DEPLOYED SaaS CONSOLE INTERACTION
# ─────────────────────────────────────────────
else:
    # Sidebar Profile Operations Container Frame Layout
    st.sidebar.markdown(f"<h4>👤 Client: {st.session_state['logged_in_username']}</h4>", unsafe_allow_html=True)
    
    # ✅ THE "MY PORTFOLIO" SAVED DATA SIDEBAR RENDERER
    st.sidebar.markdown("---")
    st.sidebar.markdown("📂 **Votre Portefeuille Immobilier**", unsafe_allow_html=True)
    user_saved_portfolio_df = utils_db.fetch_user_portfolio(st.session_state["logged_in_user_id"])
    
    if not user_saved_portfolio_df.empty:
        for idx, row in user_saved_portfolio_df.iterrows():
            if st.sidebar.button(f"🏠 {row['address'][:25]}...", key=f"saved_prop_{row['id']}", use_container_width=True):
                st.session_state["confirmed_owner_property"] = {
                    "address": row["address"], "dpe": row["dpe"], "surface": row["surface"],
                    "cost": row["cost"], "roi": row["roi"], "zipcode": row["zipcode"],
                    "lat": row["lat"], "lon": row["lon"]
                }
                st.rerun()
    else: st.sidebar.info("Portfolio empty. Analyze an asset to save.")
    
    if st.sidebar.button("🚪 Déconnexion (Log Out)", use_container_width=True, type="secondary"):
        st.session_state["logged_in_user_id"] = None
        st.session_state["logged_in_username"] = None
        st.session_state["confirmed_owner_property"] = None
        st.rerun()

    # Main workflow search triggers
    if st.session_state["confirmed_owner_property"] is None:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<p class="section-label">{T["title"]}</p><p class="section-title">{T["subtitle"]}</p>', unsafe_allow_html=True)
        search_query = st.text_input(T["input_label"], placeholder="Ex: 39 Rue du Sergent Bobillot, Montreuil")
        if search_query and len(search_query.strip()) >= 3:
            st.session_state["address_suggestions"] = ban_search(search_query)
        suggestions = st.session_state["address_suggestions"]
        if suggestions:
            labels = [f"{s['label']} ({s['postcode']} {s['city']})" for s in suggestions]
            selected_label = st.selectbox(T["select_certified"], labels)
            chosen_property = suggestions[labels.index(selected_label)]
            if st.button(T["btn_analyze"], type="primary", use_container_width=True):
                st.session_state["confirmed_owner_property"] = fetch_single_property_ademe(chosen_property["label"], chosen_property["postcode"], chosen_property["lat"], chosen_property["lon"])
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        base_prop = st.session_state["confirmed_owner_property"]
        dpe_color = _DPE_COLORS.get(base_prop["dpe"], "#475569")
        
        # Upper control button dashboard frames row
        btn_col1, btn_col2 = st.columns([4, 1])
        with btn_col1:
            if st.button(T["btn_back"]): st.session_state["confirmed_owner_property"] = None; st.rerun()
        with btn_col2:
            # ✅ THE RE-ENGINEERED SAAS SEAMLESS PORTFOLIO INJECT BUTTON TRIGGER
            if st.button("💾 Sauvegarder l'Actif", type="primary", use_container_width=True):
                utils_db.save_property_to_portfolio(
                    st.session_state["logged_in_user_id"], base_prop["address"], base_prop["zipcode"],
                    base_prop["dpe"], base_prop["surface"], base_prop["cost"], base_prop["roi"],
                    base_prop["lat"], base_prop["lon"]
                )
                st.success("Asset locked inside portfolio registry! Saved inside sidebar panels.")
                time.sleep(0.5)
                st.rerun()
            
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="owner-exclusive-title">{base_prop["address"]}</div>', unsafe_allow_html=True)
        
        sc_col1, sc_col2, sc_col3 = st.columns(3)
        with sc_col1:
            if st.button(T["eco_ess"], key="ess", use_container_width=True): st.session_state["selected_scenario"] = "Essential"; st.rerun()
        with sc_col2:
            if st.button(T["conf_plus"], key="plus", use_container_width=True): st.session_state["selected_scenario"] = "Plus"; st.rerun()
        with sc_col3:
            if st.button(T["carb_zero"], key="zero", use_container_width=True): st.session_state["selected_scenario"] = "Zero"; st.rerun()

        current_scenario = st.session_state["selected_scenario"]
        active_cost = round(base_prop["cost"] * _SCENARIO_COST_MULTIPLIER[current_scenario], 0)
        active_roi  = round(base_prop["roi"] * _SCENARIO_ROI_MULTIPLIER[current_scenario], 1)
        target_dpe  = _SCENARIO_TARGET_DPE[current_scenario]

        col_left_dpe, col_right_metrics = st.columns([0.9, 2.1], gap="large")
        with col_left_dpe:
            st.markdown(f'<div style="text-align: center; background: rgba(255,255,255,0.01); border: 1px solid rgba(255,255,255,0.03); padding: 20px; border-radius:20px;"><p class="metric-label-sub">{T["current_class"]}</p><div class="dpe-badge-big" style="background-color:{dpe_color}; margin-bottom:15px;">{base_prop["dpe"]}</div><p class="metric-label-sub" style="color:#22c55e;">{T["target_class"]} {target_dpe}</p></div>', unsafe_allow_html=True)
            
        with col_right_metrics:
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1: st.markdown(f'<span class="metric-value-huge">{base_prop["surface"]}</span><span style="font-size:1.5rem;"> m²</span><br><span class="metric-label-sub">{T["surface"]}</span>', unsafe_allow_html=True)
            with m_col2: st.markdown(f'<span class="metric-value-huge">€{active_cost:,.0f}</span><br><span class="metric-label-sub">{T["budget_est"]}</span>', unsafe_allow_html=True)
            with m_col3: st.markdown(f'<span class="metric-value-huge" style="color:#22c55e;">+{active_roi}%</span><br><span class="metric-label-sub">{T["uplift_label"]}</span>', unsafe_allow_html=True)

            st.markdown(f'<br><p class="metric-label-sub" style="color:#fff; font-weight:600;">{T["visual_prog"]}</p>', unsafe_allow_html=True)
            dpe_sequence = ["G", "F", "E", "D", "C", "B", "A"]
            if base_prop["dpe"] in dpe_sequence and target_dpe in dpe_sequence:
                c_idx, t_idx = dpe_sequence.index(base_prop["dpe"]), dpe_sequence.index(target_dpe)
                fig_progress = go.Figure()
                fig_progress.add_trace(go.Scatter(x=dpe_sequence, y=[1]*7, mode='markers+text', text=dpe_sequence, textposition="top center", marker=dict(size=24, color=["#ff0000", "#ff3300", "#ff6600", "#f2b035", "#ccff33", "#33cc33", "#319834"]), showlegend=False))
                if c_idx < 6 and c_idx != t_idx:
                    fig_progress.add_annotation(x=dpe_sequence[t_idx], y=1, ax=dpe_sequence[c_idx], ay=1, text="", showarrow=True, arrowhead=3, arrowsize=1.5, arrowwidth=4, arrowcolor="#fff")
                fig_progress.update_layout(height=110, margin=dict(l=20,r=20,t=20,b=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(visible=False), yaxis=dict(visible=False))
                st.plotly_chart(fig_progress, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

        # ── MAP LAYERS VIEW CONTROL ──
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col_map_h, col_map_t = st.columns([2.0, 1.0])
        with col_map_h: st.markdown(f'<p class="section-label">Geospatial Registry</p><p class="section-title">{T["map_title"]}</p>', unsafe_allow_html=True)
        with col_map_t: map_style_selection = st.radio("Style Map Layer", ["Road Canvas View", "High-Res Satellite View"], horizontal=True, label_visibility="collapsed")
        
        f_map = folium.Map(location=[base_prop["lat"], base_prop["lon"]], zoom_start=17)
        if map_style_selection == "High-Res Satellite View":
            folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Satellite').add_to(f_map)
        else:
            folium.TileLayer('cartodbpositron', name='Dark Canvas').add_to(f_map)
        folium.Marker([base_prop["lat"], base_prop["lon"]], icon=folium.Icon(color='green', icon='home')).add_to(f_map)
        st_folium(f_map, use_container_width=True, height=340, returned_objects=[])
        st.markdown("</div>", unsafe_allow_html=True)

        # ── FINANCIAL CALCULATOR ENGINE BLOCK ──
        if active_cost > 0:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f'<p class="section-label">{T["fin_title"]}</p><p class="section-title">{T["fin_sub"]}</p>', unsafe_allow_html=True)
            selected_income_bracket = st.selectbox(T["income_label"], list(_INCOME_SUBSIDY_MAP.keys()), index=2)
            subsidy_rate = _INCOME_SUBSIDY_MAP[selected_income_bracket]
            if current_scenario == "Plus": subsidy_rate = min(subsidy_rate + 0.05, 0.85)
            elif current_scenario == "Zero": subsidy_rate = min(subsidy_rate + 0.12, 0.90)
                
            estimated_subsidy = round(active_cost * subsidy_rate, 0)
            net_cost = active_cost - estimated_subsidy
            energy_saving = "€1,200 / an" if current_scenario == "Essential" else ("€1,850 / an" if current_scenario == "Plus" else "€2,600 / an")
            
            chart_col, metrics_col = st.columns([1.2, 1.8], gap="large")
            with chart_col:
                fig_financial = utils_charts.generate_financial_pie(estimated_subsidy, net_cost, T["subvention_label"], T["reste_charge"])
                st.plotly_chart(fig_financial, use_container_width=True, config={'displayModeBar': False})
            with metrics_col:
                sub1, sub2 = st.columns(2)
                sub1.metric(T["subvention_label"], f"€{estimated_subsidy:,.0f}", f"~{int(subsidy_rate*100)}%")
                sub2.metric(T["reste_charge"], f"€{net_cost:,.0f}", "Net remaining")
                st.markdown(f'<div style="background: rgba(255,255,255,0.02); padding: 12px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">{T["impact_facture"].format(sc=current_scenario, saving=energy_saving)}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # ── ECO-PTZ RE-COMPILING GENERATOR LOAN MATRIX
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f'<p class="section-label">Financing Leverage</p><p class="section-title">{T["loan_title"]}</p>', unsafe_allow_html=True)
            loan_years_duration = st.slider(T["loan_duration"], 5, 20, 15)
            calculated_monthly_installment = net_cost / (loan_years_duration * 12)
            col_ln_m1, col_ln_m2 = st.columns(2)
            with col_ln_m1: st.markdown(f'<br><span class="metric-value-huge" style="color:#22c55e;">€{calculated_monthly_installment:,.2f}</span><span style="font-size:1.2rem;color:#94a3b8;"> / mois</span><br><span class="metric-label-sub">{T["monthly_pay"]} (0% TAEG)</span>', unsafe_allow_html=True)
            with col_ln_m2:
                fig_gauge = go.Figure(go.Indicator(mode = "gauge+number", value = calculated_monthly_installment, domain = {'x': [0, 1], 'y': [0, 1]}, gauge = {'axis': {'range': [0, 500 if net_cost < 20000 else 1200]}, 'bar': {'color': "#22c55e"}}))
                fig_gauge.update_layout(height=110, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<p class="section-label">{T["chart_5yr_title"]}</p><p class="section-title">{T["chart_5yr_sub"]}</p>', unsafe_allow_html=True)
        fig_5yr = utils_charts.generate_five_year_trajectory(active_roi)
        st.plotly_chart(fig_5yr, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

        # ── LEAD INTERCEPT FORM CONTROL STRUCTURE ──
        if active_cost > 0:
            st.markdown('<div class="card" style="border: 1px solid rgba(34,197,94,0.25); background: #080d14;">', unsafe_allow_html=True)
            st.markdown(f'<h3 style="color:#f8fafc; margin-top:0;">{T["form_title"]}</h3>', unsafe_allow_html=True)
            with st.form("rge_lead_capture_form"):
                col_lead1, col_lead2 = st.columns(2)
                with col_lead1:
                    owner_name = st.text_input(T["form_name"], placeholder="M. Jean Dupont")
                    owner_phone = st.text_input(T["form_phone"], placeholder="06 12 34 56 78")
                with col_lead2:
                    owner_email = st.text_input(T["form_email"], placeholder="jean.dupont@gmail.com")
                    time_slot = st.selectbox(T["form_time"], ["Matin (9h - 12h)", "Après-midi (14h - 17h)"])
                additional_notes = st.text_area(T["form_notes"])
                if st.form_submit_button(T["form_btn"]):
                    if owner_name and owner_phone and owner_email:
                        db_logged = utils_db.log_lead_to_db(base_prop["address"], base_prop["zipcode"], base_prop["dpe"], target_dpe, current_scenario, active_cost, owner_name, owner_phone, owner_email, time_slot, additional_notes)
                        if db_logged: st.success(T["form_success"])
                    else: st.error(T["form_err"])
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        try:
            pdf_string_data = generate_zami_pdf_bytes(base_prop, current_scenario, target_dpe, active_cost, net_cost)
            pdf_bytes_io = io.BytesIO(pdf_string_data.encode('latin1') if isinstance(pdf_string_data, str) else pdf_string_data)
            st.download_button(label=T["download_btn"], data=pdf_bytes_io, file_name=f"ZAMI_Rapport_{base_prop['zipcode']}.pdf", mime="application/pdf", use_container_width=True)
        except Exception: pass
        st.markdown("</div>", unsafe_allow_html=True)

    # ── 🛡️ OPERATIONAL ENVIRONMENT SECURED VAULT MONITORING ──
    st.markdown('<hr style="border-color:rgba(255,255,255,0.05); margin: 3rem 0;">', unsafe_allow_html=True)
    if st.checkbox("🔑 Open ZAMI Secure Admin Database Vault Viewer"):
        admin_password_input = st.text_input("Enter Secret Admin System Password :", type="password")
        if admin_password_input:
            SECRET_MASTER_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "HussnainZami2026")
            if admin_password_input == SECRET_MASTER_PASSWORD:
                st.markdown('<div class="card" style="border:1px solid rgba(34,197,94,0.3); background: #070f14;">', unsafe_allow_html=True)
                try:
                    conn = sqlite3.connect(utils_db.DB_PATH)
                    leads_df = pd.read_sql_query("SELECT * FROM leads ORDER BY id DESC", conn)
                    conn.close()
                    if not leads_df.empty: st.dataframe(leads_df, use_container_width=True)
                    else: st.info("La base de données est vide.")
                except Exception as e: st.error(f"Error: {e}")
                st.markdown('</div>', unsafe_allow_html=True)
            else: st.markdown('<span style="color:#dc2626; font-size:0.85rem; font-weight:600;">❌ ACCESS DENIED: Invalid Password token.</span>', unsafe_allow_html=True)

st.markdown(f'<div class="footer">{T["footer"]}</div>', unsafe_allow_html=True)