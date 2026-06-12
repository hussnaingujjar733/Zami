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
        search_query = st.text_input("Saisissez votre adresse", placeholder="Ex: 39 Rue du Sergent Bobillot, 93100 Montreuil")
        
        if search_query and len(search_query) >= 3:
            with st.spinner("Recherche BAN API..."):
                features = search_address(search_query)
                if features:
                    labels = [f["properties"].get("label", "") for f in features]
                    selected_label = st.selectbox("Sélectionnez l'adresse exacte", labels)
                    if st.button("🚀 Continuer", type="primary", use_container_width=True):
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
        col_a, col_b, col_c = st.columns(3)
        with col_a: premium_ui.premium_metric("📊 ROI", f"{data['roi']}%")
        with col_b: premium_ui.premium_metric("⚡ Économies annuelles", f"{data['annual_savings']:,} €")
        with col_c: premium_ui.premium_metric("⏱️ Amortissement", f"{data['payback']} ans")

        st.markdown("---")
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
                            st.success("✅ Votre demande a bien été envoyée.")
                            st.balloons()
                            premium_ui.show_confetti()
                            st.info("Un artisan partenaire pourra vous contacter après vérification de votre projet.")
                            st.caption("Votre espace client a été créé automatiquement. Vous pourrez suivre vos demandes depuis l'onglet Mon Espace.")
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
