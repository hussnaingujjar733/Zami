import streamlit as st
import streamlit.components.v1 as components
import requests
import folium
import datetime
from streamlit_folium import st_folium
from utils import utils_marketplace
from utils import premium_ui
from utils.pdf_generator import generate_complete_report
from utils.email_notifications import send_new_lead_email

def track_clarity_event(event_name: str):
    components.html(
        f"""
        <script>
        if (window.clarity) {{
            window.clarity("event", "{event_name}");
        }}
        </script>
        """,
        height=0
    )


# ==================== ADEME API ====================
ADEME_BASE_URL = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant"

STANDARD_CONSUMPTION = {
    'A': 50, 'B': 80, 'C': 130, 'D': 200, 'E': 280, 'F': 380, 'G': 450
}

def get_dpe_by_address(address: str, api_key: str = None) -> dict:
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    params = {
        "q": address,
        "size": 1,
        "select": "etiquette_dpe,conso_5_usages_ef,surface_habitable_logement,annee_construction,code_postal_ban,nom_commune_ban"
    }
    
    url = f"{ADEME_BASE_URL}/lines"
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            if results and len(results) > 0:
                result = results[0]
                consumption = result.get('conso_5_usages_ef', 280)
                if consumption > 500 or consumption < 0:
                    consumption = STANDARD_CONSUMPTION.get(result.get('etiquette_dpe', 'E'), 280)
                return {
                    "success": True,
                    "dpe": result.get('etiquette_dpe', 'E'),
                    "consumption": consumption,
                    "surface": result.get('surface_habitable_logement', 75),
                    "year": result.get('annee_construction', 1970),
                    "postcode": result.get('code_postal_ban', ''),
                    "city": result.get('nom_commune_ban', ''),
                    "source": "ADEME_API"
                }
        return {"success": False, "message": "No DPE data found"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def get_dpe_by_year(year: int) -> tuple:
    if year >= 2021: return "A", 50
    elif year >= 2013: return "B", 80
    elif year >= 2006: return "C", 130
    elif year >= 1990: return "D", 200
    elif year >= 1975: return "E", 280
    elif year >= 1948: return "F", 380
    else: return "G", 450

PROPERTY_VALUES = {
    "75": 10500, "92": 7500, "93": 4500, "94": 6500, "78": 5500,
    "91": 5000, "95": 4800, "69": 4850, "13": 4350, "33": 4150,
    "31": 3750, "59": 3450, "67": 3350, "44": 3750, "38": 3650,
    "34": 3850, "37": 3200, "14": 3200, "76": 3000, "51": 2800,
}

RENOVATION_COSTS = {
    'G': 1350, 'F': 1100, 'E': 620, 'D': 280, 'C': 120, 'B': 60, 'A': 30
}

def search_address(query: str) -> list:
    try:
        response = requests.get(
            "https://api-adresse.data.gouv.fr/search/",
            params={"q": query, "limit": 5},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get('features', [])
    except:
        pass
    return []

def get_property_value(postcode: str, surface: int, property_type: str) -> tuple:
    dept = str(postcode)[:2]
    price_m2 = PROPERTY_VALUES.get(dept, 3500)
    if property_type == "Maison":
        price_m2 = int(price_m2 * 0.92)
    return surface * price_m2, price_m2

def calculate_subsidy(income: int, household_size: int, renovation_cost: int) -> tuple:
    if income < 17800: rate = 0.50; max_amount = 35000
    elif income < 26000: rate = 0.45; max_amount = 30000
    elif income < 35000: rate = 0.35; max_amount = 25000
    elif income < 55000: rate = 0.25; max_amount = 20000
    else: rate = 0.15; max_amount = 15000
    if household_size >= 3: rate += 0.05
    subsidy = min(int(renovation_cost * rate), max_amount)
    return subsidy, int(rate * 100), ""

def calculate_energy_savings(current_dpe: str, target_dpe: str, surface: int) -> int:
    current = STANDARD_CONSUMPTION.get(current_dpe, 280)
    target = STANDARD_CONSUMPTION.get(target_dpe, 130)
    return int((current - target) * surface * 0.25)

def show():
    st.markdown("<h1 style='text-align: center; color: #34d399;'>🔍 Nouvelle Estimation IA</h1>", unsafe_allow_html=True)
    
    if "estimation_step" not in st.session_state:
        st.session_state.estimation_step = "address"
    if "property_data" not in st.session_state:
        st.session_state.property_data = None
    if "report_data" not in st.session_state:
        st.session_state.report_data = None
    
    # ==================== STEP 1: ADDRESS ====================
    if st.session_state.estimation_step == "address":
        st.success("🔒 Adresse privée • Aucune inscription • Gratuit • Sans engagement")

        if st.button("🏠 Essayer une démonstration", use_container_width=True):
            st.session_state.demo_address = "39 Rue du Sergent Bobillot, 93700 Drancy"

        search_query = st.text_input(
            "Saisissez votre adresse",
            value=st.session_state.get("demo_address", ""),
            placeholder="Ex: 39 Rue du Sergent Bobillot, 93100 Montreuil"
        )

        search_clicked = st.button("🔍 Rechercher cette adresse", type="primary", use_container_width=True)

        if search_clicked and search_query and len(search_query) >= 3:
            with st.spinner("Recherche de l’adresse..."):
                features = search_address(search_query)
                st.session_state.address_features = features if features else []

        features = st.session_state.get("address_features", [])

        if features:
            st.success("✅ Adresse trouvée. Sélectionnez l’adresse exacte ci-dessous.")
            labels = [f["properties"].get("label", "") for f in features]
            selected_label = st.selectbox("Sélectionnez l'adresse exacte", labels)

            if st.button("⚡ Obtenir mon estimation gratuite", type="primary", use_container_width=True):
                for f in features:
                    if f["properties"].get("label") == selected_label:
                        with st.spinner("🔍 Recherche des données DPE ADEME..."):
                            ademe_result = get_dpe_by_address(selected_label)

                        if ademe_result.get('success'):
                            st.session_state.property_data = {
                                "address": selected_label,
                                "lat": f["geometry"]["coordinates"][1],
                                "lon": f["geometry"]["coordinates"][0],
                                "postcode": f["properties"].get("postcode", "93100"),
                                "city": f["properties"].get("city", ""),
                                "dpe": ademe_result['dpe'],
                                "consumption": ademe_result['consumption'],
                                "surface": ademe_result['surface'],
                                "year": ademe_result['year'],
                                "has_real_dpe": True
                            }
                            st.success(f"✅ Données ADEME: DPE {ademe_result['dpe']}")
                        else:
                            st.session_state.property_data = {
                                "address": selected_label,
                                "lat": f["geometry"]["coordinates"][1],
                                "lon": f["geometry"]["coordinates"][0],
                                "postcode": f["properties"].get("postcode", "93100"),
                                "city": f["properties"].get("city", ""),
                                "has_real_dpe": False
                            }
                            st.info("ℹ️ Données ADEME non disponibles")

                        st.session_state.estimation_step = "details"
                        st.rerun()
        elif search_clicked:
            st.warning("Veuillez saisir au moins 3 caractères pour rechercher une adresse.")

    # ==================== STEP 2: DETAILS ====================
    elif st.session_state.estimation_step == "details":
        prop = st.session_state.property_data
        has_real_dpe = prop.get('has_real_dpe', False)
        
        st.markdown(f"### 📍 {prop['address']}")
        st.caption(f"Code postal: {prop['postcode']}")
        
        if has_real_dpe:
            st.success(f"✅ Données ADEME: DPE {prop['dpe']} | Consommation: {prop['consumption']} kWh/m²/an")
        
        col1, col2 = st.columns(2)
        with col1:
            default_surface = prop.get('surface', 75) if has_real_dpe else 75
            if default_surface < 20: default_surface = 75
            surface = st.number_input("Surface (m²)", min_value=20, max_value=500, value=int(default_surface), step=5)
            property_type = st.selectbox("Type de bien", ["Appartement", "Maison"])
        
        with col2:
            if has_real_dpe:
                st.info(f"🏗️ Année: {prop.get('year', 1970)}")
                year_value = prop.get('year', 1970)
            else:
                year_value = st.number_input("Année de construction", min_value=1800, max_value=2025, value=1970)
            target_dpe = st.selectbox("Objectif DPE", ["A", "B", "C", "D"], index=2)
            household_income = st.number_input("Revenu fiscal (€/an)", min_value=0, max_value=200000, value=35000, step=5000)
            household_size = st.number_input("Personnes au foyer", min_value=1, max_value=10, value=2)
        
        if has_real_dpe:
            current_dpe = prop['dpe']
            current_consumption = prop['consumption']
        else:
            current_dpe, current_consumption = get_dpe_by_year(year_value)
        
        if st.button("📊 Calculer mon projet", type="primary", use_container_width=True):
            with st.status("🤖 Analyse IA ZAMI en cours...", expanded=True) as status:
                st.write("🔍 Analyse de l’adresse et des données disponibles...")
                st.write("⚡ Évaluation du DPE et du gain énergétique...")
                st.write("💶 Simulation du coût, des aides et du ROI...")
                st.write("📄 Préparation du rapport personnalisé...")
                status.update(label="✅ Analyse terminée", state="complete", expanded=False)

            target_consumption = STANDARD_CONSUMPTION.get(target_dpe, 130)
            current_value, price_m2 = get_property_value(prop['postcode'], surface, property_type)
            renovation_cost = surface * (RENOVATION_COSTS.get(current_dpe, 620) - RENOVATION_COSTS.get(target_dpe, 120))

            # Accuracy layer: show a realistic range instead of a single exact number
            if has_real_dpe:
                range_pct = 0.12
                confidence_score = 82
                confidence_label = "Élevée"
            else:
                range_pct = 0.22
                confidence_score = 68
                confidence_label = "Moyenne"

            cost_min = int(renovation_cost * (1 - range_pct))
            cost_max = int(renovation_cost * (1 + range_pct))

            subsidy, subsidy_rate, _ = calculate_subsidy(household_income, household_size, renovation_cost)
            net_investment = renovation_cost - subsidy
            uplift_pct = 0.08 if target_dpe in ['C', 'D'] else 0.12
            future_value = int(current_value * (1 + uplift_pct))
            added_value = future_value - current_value
            roi = round((added_value / net_investment) * 100, 1) if net_investment > 0 else 0
            annual_savings = calculate_energy_savings(current_dpe, target_dpe, surface)
            payback = round(net_investment / annual_savings, 1) if annual_savings > 0 else 0
            savings_percentage = round(((current_consumption - target_consumption) / current_consumption) * 100, 1) if current_consumption > 0 else 0
            
            st.session_state.report_data = {
                "address": prop['address'], "surface": surface, "postcode": prop['postcode'],
                "property_type": property_type, "current_dpe": current_dpe, "target_dpe": target_dpe,
                "current_consumption": current_consumption, "target_consumption": target_consumption,
                "savings_percentage": savings_percentage, "renovation_cost": renovation_cost,
                "cost_min": cost_min, "cost_max": cost_max,
                "confidence_score": confidence_score, "confidence_label": confidence_label,
                "subsidy": subsidy, "subsidy_rate": subsidy_rate, "net_investment": net_investment,
                "current_value": current_value, "future_value": future_value, "added_value": added_value,
                "roi": roi, "annual_savings": annual_savings, "payback": payback,
                "dpe_source": "ADEME_API" if has_real_dpe else "RT_ESTIMATION"
            }
            track_clarity_event("estimate_generated")
            st.session_state.estimation_step = "report"
            st.rerun()
    
    # ==================== STEP 3: REPORT ====================
    elif st.session_state.estimation_step == "report":
        data = st.session_state.report_data
        st.success(f"### 📄 Rapport pour : {data['address']}")

        if data.get('savings_percentage', 0) >= 45:
            potential_text = "un fort potentiel de rénovation énergétique"
        elif data.get('savings_percentage', 0) >= 25:
            potential_text = "un potentiel intéressant de rénovation énergétique"
        else:
            potential_text = "un potentiel à confirmer avec une visite technique"

        if data.get('roi', 0) >= 70:
            financial_text = "Le projet présente un équilibre financier attractif grâce aux économies, aux aides estimées et à la valorisation potentielle du bien."
        elif data.get('roi', 0) >= 40:
            financial_text = "Le projet mérite une étude plus approfondie, notamment avec plusieurs devis artisans."
        else:
            financial_text = "Le projet doit être qualifié avec un professionnel afin de confirmer sa rentabilité réelle."

        if data.get('subsidy', 0) > 0:
            subsidy_text = f"Les aides estimées peuvent réduire le coût initial d'environ {data.get('subsidy', 0):,.0f} €."
        else:
            subsidy_text = "Les aides disponibles devront être vérifiées selon votre situation."

        st.markdown(f"""
        <div class="luxury-card" style="border:1px solid rgba(52,211,153,0.35);">
            <h2 style="color:#34d399;">🤖 Analyse ZAMI</h2>
            <p style="color:#ccc; font-size:1.05rem; line-height:1.8;">
                Votre logement présente <strong>{potential_text}</strong>.
                Le passage de <strong>DPE {data.get('current_dpe')}</strong> à <strong>DPE {data.get('target_dpe')}</strong>
                pourrait réduire la consommation énergétique d'environ <strong>{data.get('savings_percentage')}%</strong>.
            </p>
            <p style="color:#ccc; line-height:1.8;">
                {financial_text}
            </p>
            <p style="color:#D4AF37; line-height:1.8;">
                {subsidy_text}
            </p>
            <p style="color:#888; font-size:0.85rem;">
                Cette analyse est indicative et doit être confirmée par une visite technique et des devis professionnels.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="luxury-card" style="border:1px solid rgba(212,175,55,0.35);">
            <h2 style="color:#D4AF37; margin-bottom:0.5rem;">🏠 Synthèse du bien</h2>
            <p style="color:#ccc; font-size:1.05rem;">{data.get('address')}</p>
            <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:1rem; margin-top:1rem;">
                <div><strong style="color:#D4AF37;">Surface</strong><br><span style="color:#fff;">{data.get('surface')} m²</span></div>
                <div><strong style="color:#D4AF37;">Type</strong><br><span style="color:#fff;">{data.get('property_type')}</span></div>
                <div><strong style="color:#D4AF37;">DPE actuel</strong><br><span style="color:#fff;">{data.get('current_dpe')}</span></div>
                <div><strong style="color:#D4AF37;">Valeur estimée</strong><br><span style="color:#fff;">{data.get('current_value', 0):,.0f} €</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        dpe_colors = {
            "A": "#16a34a",
            "B": "#22c55e",
            "C": "#84cc16",
            "D": "#facc15",
            "E": "#f97316",
            "F": "#ef4444",
            "G": "#7f1d1d",
        }

        current_color = dpe_colors.get(data.get("current_dpe"), "#f97316")
        target_color = dpe_colors.get(data.get("target_dpe"), "#84cc16")

        st.markdown(f"""
        <div class="luxury-card" style="text-align:center;">
            <h2 style="color:#D4AF37;">⚡ Transformation énergétique</h2>
            <p style="color:#ccc;">Votre logement passe de</p>
            <div style="display:flex; align-items:center; justify-content:center; gap:2rem; margin:1rem 0;">
                <div style="background:{current_color}; color:white; padding:1rem 1.6rem; border-radius:18px; font-size:2rem; font-weight:800;">
                    DPE {data.get('current_dpe')}
                </div>
                <div style="font-size:2rem; color:#D4AF37;">→</div>
                <div style="background:{target_color}; color:white; padding:1rem 1.6rem; border-radius:18px; font-size:2rem; font-weight:800;">
                    DPE {data.get('target_dpe')}
                </div>
            </div>
            <p style="color:#34d399; font-weight:700;">
                Gain énergétique estimé : {data.get('savings_percentage')}%
            </p>
        </div>
        """, unsafe_allow_html=True)

        if data.get('dpe_source') == 'ADEME_API':
            st.info("📊 Données DPE réelles de l'API ADEME")
        else:
            st.warning("📊 Données DPE estimées")
        
        # Display metrics using Streamlit's built-in metrics (safe)
        col1, col2, col3 = st.columns(3)
        with col1:
            premium_ui.premium_metric("🏷️ DPE", f"{data['current_dpe']} → {data['target_dpe']}", delta=f"Gain: {data['savings_percentage']}%")
            premium_ui.premium_metric("💰 Coût estimé", f"{data.get('cost_min', data['renovation_cost']):,.0f} € – {data.get('cost_max', data['renovation_cost']):,.0f} €")
            premium_ui.premium_metric("🎯 Confiance", f"{data.get('confidence_score', 70)}%", delta=data.get('confidence_label', 'Moyenne'))
        with col2:
            premium_ui.premium_metric("🎁 Aides", f"{data['subsidy']:,.0f} €", delta=f"{data['subsidy_rate']}%")
            premium_ui.premium_metric("💳 Reste à charge", f"{data['net_investment']:,.0f} €")
        with col3:
            premium_ui.premium_metric("🏠 Valeur actuelle", f"{data['current_value']:,.0f} €")
            premium_ui.premium_metric("📈 Valeur après travaux", f"{data['future_value']:,.0f} €", delta=f"+{data['added_value']:,.0f} €")
        
        st.markdown("---")
        with st.expander("🎛️ Simulateur rapide de scénario", expanded=False):
            sim_target = st.selectbox(
                "Comparer avec un autre objectif DPE",
                ["D", "C", "B", "A"],
                index=["D", "C", "B", "A"].index(data.get("target_dpe", "C")) if data.get("target_dpe", "C") in ["D", "C", "B", "A"] else 1,
                key="roi_simulator_target"
            )

            sim_cost = data.get("surface", 0) * (RENOVATION_COSTS.get(data.get("current_dpe"), 620) - RENOVATION_COSTS.get(sim_target, 120))
            sim_cost = max(sim_cost, 0)
            sim_target_consumption = STANDARD_CONSUMPTION.get(sim_target, 130)
            sim_savings_pct = round(((data.get("current_consumption", 280) - sim_target_consumption) / data.get("current_consumption", 280)) * 100, 1)
            sim_subsidy = min(int(sim_cost * (data.get("subsidy_rate", 25) / 100)), 35000)

            col_sim1, col_sim2, col_sim3, col_sim4 = st.columns(4)
            col_sim1.metric("Objectif", f"DPE {sim_target}")
            col_sim2.metric("Coût estimé", f"{sim_cost:,.0f} €")
            col_sim3.metric("Aides estimées", f"{sim_subsidy:,.0f} €")
            col_sim4.metric("Gain énergie", f"{sim_savings_pct}%")

        st.markdown(f"""
        <div class="luxury-card" style="border:1px solid rgba(212,175,55,0.35);">
            <h2 style="color:#D4AF37; text-align:center;">💼 Tableau de bord investissement</h2>
            <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:1rem; margin-top:1rem; text-align:center;">
                <div>
                    <p style="color:#888;">Coût travaux</p>
                    <h3 style="color:#fff;">{data.get('renovation_cost', 0):,.0f} €</h3>
                </div>
                <div>
                    <p style="color:#888;">Aides estimées</p>
                    <h3 style="color:#34d399;">-{data.get('subsidy', 0):,.0f} €</h3>
                </div>
                <div>
                    <p style="color:#888;">Reste à charge</p>
                    <h3 style="color:#D4AF37;">{data.get('net_investment', 0):,.0f} €</h3>
                </div>
                <div>
                    <p style="color:#888;">Valeur créée</p>
                    <h3 style="color:#34d399;">+{data.get('added_value', 0):,.0f} €</h3>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        opportunity_score = 0

        if data.get('savings_percentage', 0) >= 40:
            opportunity_score += 25
        elif data.get('savings_percentage', 0) >= 25:
            opportunity_score += 15

        if data.get('roi', 0) >= 70:
            opportunity_score += 25
        elif data.get('roi', 0) >= 40:
            opportunity_score += 15

        if data.get('subsidy', 0) > 0:
            opportunity_score += 20

        if data.get('confidence_score', 0) >= 80:
            opportunity_score += 20
        elif data.get('confidence_score', 0) >= 65:
            opportunity_score += 10

        if data.get('payback', 99) <= 10:
            opportunity_score += 10

        opportunity_score = min(opportunity_score, 100)

        if opportunity_score >= 80:
            opportunity_label = "Excellent projet de rénovation"
            opportunity_color = "#34d399"
        elif opportunity_score >= 60:
            opportunity_label = "Projet intéressant à étudier"
            opportunity_color = "#D4AF37"
        else:
            opportunity_label = "Projet à qualifier avec un artisan"
            opportunity_color = "#f59e0b"

        st.markdown(f"""
        <div class="luxury-card" style="text-align:center; border:1px solid {opportunity_color};">
            <h2 style="color:{opportunity_color};">🏆 Score d'Opportunité ZAMI</h2>
            <div style="font-size:3rem; font-weight:800; color:{opportunity_color};">{opportunity_score}/100</div>
            <h3 style="color:#fff;">{opportunity_label}</h3>
            <p style="color:#ccc; line-height:1.8;">
                ✓ Potentiel d'économies analysé<br>
                ✓ Valorisation du bien estimée<br>
                ✓ Aides et fiabilité prises en compte
            </p>
        </div>
        """, unsafe_allow_html=True)

        current_total_kwh = int(data.get('current_consumption', 0) * data.get('surface', 0))
        target_total_kwh = int(data.get('target_consumption', 0) * data.get('surface', 0))
        reduction_kwh = max(current_total_kwh - target_total_kwh, 0)

        st.markdown("""
        <div class="luxury-card">
            <h2 style="color:#D4AF37;">⚡ Consommation énergétique estimée</h2>
        </div>
        """, unsafe_allow_html=True)

        col_energy1, col_energy2, col_energy3 = st.columns(3)
        col_energy1.metric("Aujourd'hui", f"{current_total_kwh:,} kWh/an")
        col_energy2.metric("Après travaux", f"{target_total_kwh:,} kWh/an")
        col_energy3.metric("Réduction", f"-{reduction_kwh:,} kWh/an")

        st.progress(min(int(data.get('savings_percentage', 0)), 100))
        st.caption(f"Gain énergétique estimé : {data.get('savings_percentage')}%")

        col_a, col_b, col_c = st.columns(3)
        with col_a: premium_ui.premium_metric("📊 ROI", f"{data['roi']}%")
        with col_b: premium_ui.premium_metric("⚡ Économies annuelles", f"{data['annual_savings']:,} €")
        with col_c: premium_ui.premium_metric("⏱️ Amortissement", f"{data['payback']} ans")
        # Renovation roadmap
        current_dpe = data.get("current_dpe", "E")
        target_dpe = data.get("target_dpe", "C")
        renovation_cost = data.get("renovation_cost", 0)

        if current_dpe in ["F", "G"]:
            roadmap = [
                ("1️⃣ Isolation thermique prioritaire", "Impact très élevé", "Réduire les pertes de chaleur avant de changer le système énergétique."),
                ("2️⃣ Chauffage performant", "Impact élevé", "Pompe à chaleur ou système plus efficace selon le logement."),
                ("3️⃣ Ventilation contrôlée", "Impact moyen", "Améliorer la qualité de l’air et limiter les pertes énergétiques."),
            ]
        elif current_dpe in ["D", "E"]:
            roadmap = [
                ("1️⃣ Isolation ciblée", "Impact élevé", "Traiter les murs, combles ou planchers selon les faiblesses du logement."),
                ("2️⃣ Chauffage / régulation", "Impact élevé", "Optimiser le système de chauffage et la régulation."),
                ("3️⃣ Menuiseries performantes", "Impact moyen", "Remplacer les fenêtres anciennes si nécessaire."),
            ]
        else:
            roadmap = [
                ("1️⃣ Optimisation énergétique", "Impact moyen", "Identifier les petits travaux à fort rendement."),
                ("2️⃣ Ventilation", "Impact moyen", "Améliorer le confort et la qualité de l’air."),
                ("3️⃣ Suivi de consommation", "Impact moyen", "Contrôler les usages pour maintenir la performance."),
            ]

        st.markdown(f"""
        <div class="luxury-card" style="border:1px solid rgba(212,175,55,0.35);">
            <h2 style="color:#D4AF37; text-align:center;">🛠️ Plan de rénovation recommandé</h2>
            <p style="color:#ccc; text-align:center;">
                Objectif estimé : <strong>DPE {current_dpe}</strong> → <strong>DPE {target_dpe}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

        for title, impact, reason in roadmap:
            st.markdown(f"""
            <div style="border:1px solid rgba(255,255,255,0.12); border-radius:16px; padding:1rem; margin:0.7rem 0; background:rgba(255,255,255,0.03);">
                <h4 style="color:#D4AF37; margin-bottom:0.3rem;">{title}</h4>
                <p style="color:#34d399; margin:0;"><strong>{impact}</strong></p>
                <p style="color:#ccc; margin-top:0.4rem;">{reason}</p>
            </div>
            """, unsafe_allow_html=True)

        st.caption("Ce plan est indicatif. L’ordre final des travaux doit être validé par un audit ou un artisan qualifié.")

        st.markdown("---")
        st.markdown("### 🧪 Simulateur de scénario budget")

        scenario_budget = st.select_slider(
            "💰 Quel budget souhaitez-vous tester ?",
            options=[5000, 10000, 15000, 20000, 25000, 30000, 40000],
            value=15000,
            key="scenario_budget_slider"
        )

        if scenario_budget < 10000:
            scenario_plan = "Priorité : isolation simple et petits travaux à fort impact."
            scenario_gain = "Gain probable : amélioration partielle du confort énergétique."
        elif scenario_budget < 20000:
            scenario_plan = "Priorité : isolation ciblée + optimisation du chauffage."
            scenario_gain = "Gain probable : amélioration significative, souvent DPE +1 classe."
        elif scenario_budget < 30000:
            scenario_plan = "Projet plus complet : isolation + chauffage performant + ventilation."
            scenario_gain = "Gain probable : objectif DPE supérieur plus réaliste."
        else:
            scenario_plan = "Projet global envisageable : rénovation énergétique plus complète."
            scenario_gain = "Gain probable : forte amélioration DPE et meilleure valorisation du bien."

        st.info(f"""
        Avec un budget de **{scenario_budget:,.0f} €** :

        {scenario_plan}

        {scenario_gain}
        """)

        st.caption("Ce simulateur est indicatif. Les priorités réelles dépendent de l'audit, du bâti et des devis artisans.")


        st.markdown("---")
        st.markdown("### 🤖 Conseiller ZAMI")

        current_dpe = data.get("current_dpe", "E")

        if current_dpe in ["F", "G"]:
            priority = "🔴 Priorité élevée"
            advice = [
                "Commencer par l’isolation avant les autres travaux.",
                "Vérifier les aides MaPrimeRénov disponibles.",
                "Comparer au moins 3 devis d’artisans."
            ]
        elif current_dpe in ["D", "E"]:
            priority = "🟠 Priorité moyenne"
            advice = [
                "Identifier les principales pertes énergétiques.",
                "Optimiser le chauffage avant les travaux secondaires.",
                "Comparer plusieurs scénarios de rénovation."
            ]
        else:
            priority = "🟢 Priorité modérée"
            advice = [
                "Conserver les performances actuelles.",
                "Suivre la consommation énergétique.",
                "Planifier les améliorations futures progressivement."
            ]

        st.success(priority)

        for item in advice:
            st.write(f"✓ {item}")

        st.caption("Conseil généré automatiquement à partir des caractéristiques estimées du logement.")


        st.markdown("---")
        st.markdown("### 🏠 Impact potentiel sur la valeur du bien")

        current_value = data.get("current_value", 0)
        future_value = data.get("future_value", 0)
        added_value = data.get("added_value", future_value - current_value)

        col_v1, col_v2, col_v3 = st.columns(3)
        col_v1.metric("Valeur actuelle estimée", f"{current_value:,.0f} €")
        col_v2.metric("Valeur après rénovation", f"{future_value:,.0f} €")
        col_v3.metric("Gain potentiel", f"+{added_value:,.0f} €")

        st.caption("Cette valorisation est indicative et dépend du marché immobilier local, de la qualité des travaux et des devis réalisés.")

        st.markdown("### 🧠 Pourquoi cette estimation ?")

        source_label = "Données ADEME trouvées" if data.get('dpe_source') == 'ADEME_API' else "Estimation basée sur l'année de construction"
        st.info(
            f"""
            Cette estimation est basée sur :
            - Surface du logement : **{data.get('surface')} m²**
            - DPE actuel : **{data.get('current_dpe')}**
            - Objectif DPE : **{data.get('target_dpe')}**
            - Source DPE : **{source_label}**
            - Méthode : fourchette de coût pour éviter une fausse précision
            """
        )

        st.caption("⚠️ Cette estimation est indicative. Un devis final nécessite une visite technique par un artisan qualifié.")

        st.markdown("---")
        st.markdown("### 📄 Télécharger votre rapport")
        try:
            pdf_bytes = generate_complete_report(data)
            st.download_button(
                label="📄 Télécharger le rapport PDF",
                data=pdf_bytes,
                file_name=f"rapport_zami_{data.get('postcode', 'france')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.warning(f"Le rapport PDF n'est pas disponible pour le moment: {e}")
        
        st.markdown("---")
        
        # Publish project form
        st.subheader("🛠️ Recevoir des devis d’artisans")
        
        with st.form(key="publish_project_form"):
            col_name, col_email = st.columns(2)
            with col_name:
                name = st.text_input("Nom complet *", placeholder="Jean Dupont")
            with col_email:
                email = st.text_input("Email *", placeholder="jean.dupont@email.com")
            
            col_phone, _ = st.columns(2)
            with col_phone:
                phone = st.text_input("Téléphone *", placeholder="06 12 34 56 78")
            
            accept_terms = st.checkbox("J'accepte les conditions d'utilisation")
            
            submitted = st.form_submit_button("📩 Recevoir des devis gratuits", type="primary", use_container_width=True)
            
            if submitted:
                if not name or not email or not phone:
                    st.error("Veuillez remplir tous les champs obligatoires")
                elif not accept_terms:
                    st.error("Veuillez accepter les conditions d'utilisation")
                else:
                    try:
                        success = utils_marketplace.create_project_from_estimation(
                            name, email, phone, data['address'], 
                            data['renovation_cost'], data['current_dpe']
                        )
                        if success:
                            email_sent = send_new_lead_email(
                                name=name,
                                email=email,
                                phone=phone,
                                address=data['address'],
                                estimated_cost=data['renovation_cost'],
                                dpe_rating=data['current_dpe']
                            )
                            if email_sent:
                                st.caption("📧 Notification interne envoyée.")
                            else:
                                st.caption("⚠️ Notification email non envoyée. Le lead est quand même enregistré.")
                            track_clarity_event("lead_submitted")
                            st.balloons()
                            premium_ui.show_confetti()

                            st.markdown("""
                            <div class="luxury-card" style="text-align:center; border:1px solid rgba(52,211,153,0.35);">
                                <h2 style="color:#34d399;">🎉 Merci, votre demande est enregistrée !</h2>
                                <p style="color:#ccc; font-size:1.05rem;">
                                    Nous avons bien reçu votre projet de rénovation énergétique.
                                </p>
                                <p style="color:#D4AF37; line-height:1.9;">
                                    ✓ Estimation sauvegardée<br>
                                    ✓ Rapport PDF disponible<br>
                                    ✓ Demande transmise pour vérification<br>
                                    ✓ Un artisan partenaire pourra vous contacter
                                </p>
                                <p style="color:#888; font-size:0.85rem;">
                                    Vous pouvez suivre votre demande depuis l'onglet <strong>Mon Espace</strong>.
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error("❌ Erreur lors de l'envoi de la demande")
                    except Exception as e:
                        st.error(f"❌ Erreur: {str(e)}")
        
        st.markdown("---")
        
        if st.button("🔍 Nouvelle recherche", use_container_width=True):
            st.session_state.estimation_step = "address"
            st.session_state.report_data = None
            st.rerun()

render = show
