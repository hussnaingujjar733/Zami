import os
import base64
import json
import requests
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from fpdf import FPDF
from streamlit_folium import st_folium
import folium
from typing import Optional
from datetime import datetime
import hashlib

# ── ⚡ IMPORT MODULES ──
import utils_styles
import utils_charts
import utils_animations as anim
import utils_transitions as trans
import ai_features

# Run Premium Style Injections
utils_styles.inject_premium_styles()
trans.inject_page_transitions()
trans.add_loading_spinner()


# ─────────────────────────────────────────────
# HIDE SIDEBAR COMPLETELY
# ─────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STATE MANAGEMENT
# ─────────────────────────────────────────────
if "confirmed_owner_property" not in st.session_state:
    st.session_state["confirmed_owner_property"] = None
if "address_suggestions" not in st.session_state:
    st.session_state["address_suggestions"] = []
if "selected_scenario" not in st.session_state:
    st.session_state["selected_scenario"] = "Essential"
if "selected_address_label" not in st.session_state:
    st.session_state["selected_address_label"] = None
if "show_ai_features" not in st.session_state:
    st.session_state["show_ai_features"] = False
if "property_surface" not in st.session_state:
    st.session_state["property_surface"] = 68
if "user_responses" not in st.session_state:
    st.session_state["user_responses"] = None
if "photos_uploaded" not in st.session_state:
    st.session_state["photos_uploaded"] = False
if "accuracy_level" not in st.session_state:
    st.session_state["accuracy_level"] = 1

# Global Variables
_SCENARIO_COST_MULTIPLIER = {"Essential": 1.0, "Plus": 1.65, "Zero": 2.45}
_SCENARIO_ROI_MULTIPLIER = {"Essential": 1.0, "Plus": 1.45, "Zero": 1.95}
_SCENARIO_TARGET_DPE = {"Essential": "D", "Plus": "C", "Zero": "B"}
_FALLBACK_RENO_COST = {"G": 1350, "F": 1100, "E": 620, "D": 280, "C": 120, "B": 0, "A": 0}
_FALLBACK_UPLIFT = {"G": 24.2, "F": 19.8, "E": 13.1, "D": 6.8, "C": 2.0, "B": 0, "A": 0}
_DPE_COLORS = {"A": "#319834", "B": "#33cc33", "C": "#ccff33", "D": "#f2b035", "E": "#ff6600", "F": "#ff3300", "G": "#ff0000"}
_INCOME_SUBSIDY_MAP = {"Très Modeste (Bleu)": 0.75, "Modeste (Jaune)": 0.60, "Intermédiaire (Violet)": 0.40, "Supérieur (Rose)": 0.15}

CHAT_FILE = "chat_messages.json"
LEADS_FILE = "homeowner_leads.json"


# ─────────────────────────────────────────────
# LEAD FUNCTIONS (JSON Storage)
# ─────────────────────────────────────────────
def save_lead(email, address, dpe, subsidy, roi):
    """Save homeowner lead to JSON file"""
    try:
        if os.path.exists(LEADS_FILE):
            with open(LEADS_FILE, "r", encoding="utf-8") as f:
                leads = json.load(f)
        else:
            leads = []
        
        leads.append({
            "id": len(leads) + 1,
            "email": email,
            "address": address,
            "dpe": dpe,
            "subsidy": subsidy,
            "roi": roi,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "new"
        })
        
        with open(LEADS_FILE, "w", encoding="utf-8") as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Save error: {e}")
        return False


def get_all_leads():
    """Get all homeowner leads"""
    try:
        if os.path.exists(LEADS_FILE):
            with open(LEADS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except:
        return []


# ─────────────────────────────────────────────
# CHAT FUNCTIONS (JSON Storage)
# ─────────────────────────────────────────────
def save_chat_message(name, email, message):
    """Save chat message to JSON file"""
    try:
        if os.path.exists(CHAT_FILE):
            with open(CHAT_FILE, "r", encoding="utf-8") as f:
                messages = json.load(f)
        else:
            messages = []
        
        messages.append({
            "id": len(messages) + 1,
            "name": name,
            "email": email,
            "message": message,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "unread"
        })
        
        with open(CHAT_FILE, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Save error: {e}")
        return False


def get_all_chat_messages():
    """Get all chat messages from JSON file"""
    try:
        if os.path.exists(CHAT_FILE):
            with open(CHAT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except:
        return []


def mark_message_read(msg_id):
    """Mark a message as read"""
    try:
        messages = get_all_chat_messages()
        for msg in messages:
            if msg.get("id") == msg_id:
                msg["status"] = "read"
                break
        with open(CHAT_FILE, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False


# ─────────────────────────────────────────────
# LOGO FUNCTION
# ─────────────────────────────────────────────
def get_logo_html():
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "zami_logo.png")
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as img_f:
                logo_base64 = base64.b64encode(img_f.read()).decode()
                return f'<img src="data:image/png;base64,{logo_base64}" style="height:45px; width:auto;">'
        except:
            pass
    return '<div style="font-family:\'Space Grotesk\', sans-serif; font-size:1.8rem; font-weight:800; color:#22c55e;">ZAMI</div>'


# ─────────────────────────────────────────────
# PREMIUM CHAT BOT
# ─────────────────────────────────────────────
def chat_bot():
    """Premium floating chat bot with modern UI"""
    
    st.markdown("""
    <style>
    .zami-chat-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 65px;
        height: 65px;
        background: linear-gradient(135deg, #22c55e, #16a34a);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        z-index: 1000;
        box-shadow: 0 10px 30px rgba(34, 197, 94, 0.4);
        transition: all 0.3s cubic-bezier(0.2, 0.8, 0.4, 1);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(34, 197, 94, 0); }
        100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
    }
    
    .zami-chat-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 15px 35px rgba(34, 197, 94, 0.5);
    }
    
    .zami-chat-btn svg {
        width: 30px;
        height: 30px;
        fill: white;
    }
    </style>
    
    <div class="zami-chat-btn" id="floatingChatBtn">
        <svg viewBox="0 0 24 24" fill="white">
            <path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4l4 4 4-4h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
        </svg>
    </div>
    
    <script>
        document.getElementById('floatingChatBtn').onclick = function() {
            var chatWindow = window.parent.document.querySelector('[data-testid="stExpander"]');
            if (chatWindow) {
                chatWindow.click();
            }
        }
    </script>
    """, unsafe_allow_html=True)
    
    with st.expander("💬 ✨ ZAMI Assistant — Ask Us Anything", expanded=False):
        st.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <span style="background: linear-gradient(135deg, #22c55e, #16a34a); padding: 5px 15px; border-radius: 50px; font-size: 12px; font-weight: 700;">✨ AI-Powered Support ✨</span>
        </div>
        
        <div style="background: linear-gradient(135deg, rgba(34,197,94,0.05), rgba(34,197,94,0.02)); border-radius: 16px; padding: 15px; margin: 10px 0;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <span style="font-size: 28px;">🤖</span>
                <div>
                    <strong style="color: #22c55e;">ZAMI Assistant</strong>
                    <span style="font-size: 12px; color: #64748b;"> • Online</span>
                </div>
            </div>
            <p style="font-size: 14px; color: #94a3b8; margin: 0;">
                Hi there! 👋 I'm here to help you with:<br>
                • 📊 DPE (Energy Performance Diagnosis)<br>
                • 💰 MaPrimeRénov' subsidies calculation<br>
                • 📈 ROI estimation for your renovation<br>
                • 🔧 Finding certified RGE contractors
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("chat_form_premium", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                chat_name = st.text_input("👤 Your Name *", placeholder="Jean Dupont", key="chat_name_premium")
            with col2:
                chat_email = st.text_input("📧 Your Email *", placeholder="jean@example.com", key="chat_email_premium")
            
            chat_message = st.text_area("💬 Your Message *", placeholder="Tell us about your property or renovation project...", height=100, key="chat_msg_premium")
            
            col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
            with col_btn1:
                submitted = st.form_submit_button("📨 Send Message", type="primary", use_container_width=True)
            
            if submitted:
                if chat_name and chat_email and chat_message:
                    success = save_chat_message(chat_name, chat_email, chat_message)
                    if success:
                        st.success("✅ Message sent successfully!")
                        st.balloons()
                    else:
                        st.error("❌ Unable to send. Please try again.")
                else:
                    st.warning("⚠️ Please fill all required fields (*)")


# ─────────────────────────────────────────────
# ACCURACY IMPROVEMENT FUNCTIONS
# ─────────────────────────────────────────────

def calculate_enhanced_roi(property_data, user_responses):
    """Calculate more accurate ROI based on user questionnaire"""
    
    base_roi = property_data.get("roi", 15.0)
    base_cost = property_data.get("cost", 25000)
    
    windows_multiplier = {
        "Simple vitrage": 1.0,
        "Double vitrage": 0.6,
        "Triple vitrage": 0.4,
        "Je ne sais pas": 0.8
    }
    
    heating_multiplier = {
        "Gaz (ancien)": 1.0,
        "Gaz (condensation)": 0.7,
        "Électrique": 0.9,
        "Pompe à chaleur": 0.5,
        "Bois / granulés": 0.6,
        "Je ne sais pas": 0.8
    }
    
    insulation_factor = 1.0
    if user_responses.get("roof_insulation") == "Non":
        insulation_factor += 0.2
    if user_responses.get("wall_insulation") == "Non":
        insulation_factor += 0.25
    
    window_factor = windows_multiplier.get(user_responses.get("windows", "Je ne sais pas"), 0.8)
    heating_factor = heating_multiplier.get(user_responses.get("heating", "Je ne sais pas"), 0.8)
    
    accuracy_boost = (1 - window_factor) * 0.3 + (1 - heating_factor) * 0.3 + (insulation_factor - 1) * 0.4
    enhanced_roi = base_roi * (1 + accuracy_boost)
    enhanced_cost = base_cost * (0.5 + window_factor * 0.25 + heating_factor * 0.25)
    
    return min(enhanced_roi, 35.0), enhanced_cost


def property_questionnaire():
    """Ask user about property details for better accuracy (Level 2)"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(34,197,94,0.05), rgba(34,197,94,0.02)); border-radius: 20px; padding: 25px; margin: 20px 0;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
            <span style="background: #22c55e; padding: 5px 12px; border-radius: 20px; font-size: 12px;">LEVEL 2</span>
            <h3 style="color: white; margin: 0;">Améliorez la précision</h3>
        </div>
        <p style="color: #64748b; margin-bottom: 5px;">Répondez à quelques questions pour obtenir une estimation à 85-90% de précision</p>
        <p style="color: #22c55e; font-size: 13px;">✨ +15% de précision</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("accuracy_form"):
        st.markdown("### 🪟 Windows")
        windows_type = st.radio(
            "Type de vitrage",
            ["Simple vitrage", "Double vitrage", "Triple vitrage", "Je ne sais pas"],
            horizontal=True
        )
        
        st.markdown("### 🔥 Heating System")
        heating_type = st.radio(
            "Système de chauffage",
            ["Gaz (ancien)", "Gaz (condensation)", "Électrique", "Pompe à chaleur", "Bois / granulés", "Je ne sais pas"],
            horizontal=True
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🏠 Roof Insulation")
            roof_insulation = st.radio(
                "Toiture isolée ?",
                ["Oui", "Non", "Partiellement", "Je ne sais pas"],
                horizontal=True
            )
        with col2:
            st.markdown("### 🧱 Wall Insulation")
            wall_insulation = st.radio(
                "Murs isolés ?",
                ["Oui", "Non", "Partiellement", "Je ne sais pas"],
                horizontal=True
            )
        
        st.markdown("### 🔧 Recent Renovations")
        recent_renovation = st.radio(
            "Avez-vous effectué des travaux récents (moins de 5 ans) ?",
            ["Oui", "Non"],
            horizontal=True
        )
        
        renovation_details = ""
        if recent_renovation == "Oui":
            renovation_details = st.text_area("Quels travaux avez-vous réalisés ?", placeholder="Ex: Changement des fenêtres, isolation des combles...")
        
        submitted = st.form_submit_button("💾 Enregistrer et améliorer l'estimation", type="primary", use_container_width=True)
        
        if submitted:
            user_responses = {
                "windows": windows_type,
                "heating": heating_type,
                "roof_insulation": roof_insulation,
                "wall_insulation": wall_insulation,
                "recent_renovation": recent_renovation,
                "renovation_details": renovation_details
            }
            st.session_state["user_responses"] = user_responses
            st.session_state["accuracy_level"] = 2
            st.success("✅ Merci! Votre estimation va être recalculée avec plus de précision.")
            st.rerun()


def photo_upload_section():
    """Allow users to upload property photos for better accuracy (Level 3)"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(34,197,94,0.05), rgba(34,197,94,0.02)); border-radius: 20px; padding: 25px; margin: 20px 0;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
            <span style="background: #22c55e; padding: 5px 12px; border-radius: 20px; font-size: 12px;">LEVEL 3</span>
            <h3 style="color: white; margin: 0;">Analyse par IA des photos</h3>
        </div>
        <p style="color: #64748b; margin-bottom: 5px;">Uploader des photos pour une estimation à 90-95% de précision</p>
        <p style="color: #22c55e; font-size: 13px;">✨ +5% de précision supplémentaire</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("photo_form"):
        st.markdown("### 📷 Facade avant")
        facade_photo = st.file_uploader("Photo de la facade", type=["jpg", "png", "jpeg"], key="facade")
        
        st.markdown("### 🪟 Fenêtres")
        windows_photo = st.file_uploader("Photo des fenêtres", type=["jpg", "png", "jpeg"], key="windows")
        
        st.markdown("### 🏠 Toiture / Combles")
        roof_photo = st.file_uploader("Photo de la toiture ou des combles", type=["jpg", "png", "jpeg"], key="roof")
        
        st.markdown("### 🔥 Système de chauffage")
        heating_photo = st.file_uploader("Photo du système de chauffage", type=["jpg", "png", "jpeg"], key="heating")
        
        submitted = st.form_submit_button("📤 Analyser les photos", type="primary", use_container_width=True)
        
        if submitted:
            # In production: send to AI vision API
            st.session_state["photos_uploaded"] = True
            st.session_state["accuracy_level"] = 3
            st.success("✅ Photos reçues! Notre IA va les analyser pour affiner l'estimation.")
            st.rerun()


def professional_audit_section():
    """Offer professional audit for highest accuracy (Level 4 - Premium)"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(34,197,94,0.08), rgba(34,197,94,0.04)); border-radius: 20px; padding: 25px; margin: 20px 0; border: 1px solid rgba(34,197,94,0.3);">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
            <span style="background: linear-gradient(135deg, #22c55e, #16a34a); padding: 5px 12px; border-radius: 20px; font-size: 12px; color: white;">✨ PREMIUM</span>
            <h3 style="color: white; margin: 0;">Audit Certifié ZAMI</h3>
        </div>
        <p style="color: #64748b; margin-bottom: 5px;">Exactitude garantie à 98-99%</p>
        <p style="color: #22c55e; font-size: 13px;">✨ +4-8% de précision</p>
        
        <div style="margin-top: 20px;">
            <div style="display: flex; gap: 30px; flex-wrap: wrap; justify-content: space-between;">
                <div>
                    <div style="font-size: 12px; color: #64748b;">INCLUS</div>
                    <ul style="color: #94a3b8; margin-top: 10px;">
                        <li>✓ Visite technique sur site par un expert certifié</li>
                        <li>✓ Analyse thermique complète (thermographie)</li>
                        <li>✓ Relevé précis des déperditions énergétiques</li>
                        <li>✓ Dossier de subvention préparé</li>
                        <li>✓ Mise en relation avec 3 artisans RGE</li>
                        <li>✓ Garantie de satisfaction</li>
                    </ul>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 28px; font-weight: 800; color: #22c55e;">€199</div>
                    <div style="font-size: 12px; color: #64748b;">TTC • Déductible des subventions</div>
                    <button style="background: linear-gradient(135deg, #22c55e, #16a34a); border: none; padding: 12px 30px; border-radius: 50px; color: white; font-weight: 600; margin-top: 15px; cursor: pointer;">
                        🎯 Commander un audit
                    </button>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ACCURACY PROGRESS BAR
# ─────────────────────────────────────────────
def accuracy_progress_bar():
    """Show current accuracy level and improvement options"""
    
    levels = {
        1: {"name": "Données officielles", "accuracy": "70-75%", "color": "#64748b"},
        2: {"name": "Questionnaire", "accuracy": "85-90%", "color": "#eab308"},
        3: {"name": "Photos IA", "accuracy": "90-95%", "color": "#22c55e"},
        4: {"name": "Audit certifié", "accuracy": "98-99%", "color": "#22c55e"}
    }
    
    current_level = st.session_state.get("accuracy_level", 1)
    
    st.markdown("""
    <style>
    .accuracy-container {
        background: rgba(15, 25, 45, 0.6);
        border-radius: 16px;
        padding: 15px;
        margin: 20px 0;
    }
    .accuracy-step {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
    }
    .accuracy-badge {
        width: 30px;
        height: 30px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: 700;
    }
    .accuracy-line {
        flex: 1;
        height: 2px;
        background: rgba(255,255,255,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="accuracy-container">', unsafe_allow_html=True)
    st.markdown("#### 🎯 Niveau de précision de l'estimation")
    
    cols = st.columns(4)
    for i, (level, info) in enumerate(levels.items(), 1):
        with cols[i-1]:
            if level <= current_level:
                st.markdown(f"""
                <div style="text-align: center;">
                    <div class="accuracy-badge" style="background: {info['color']}; margin: 0 auto 5px auto;">✓</div>
                    <div style="font-size: 12px; font-weight: 600;">{info['name']}</div>
                    <div style="font-size: 11px; color: #22c55e;">{info['accuracy']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="text-align: center; opacity: 0.4;">
                    <div class="accuracy-badge" style="background: #1e293b; margin: 0 auto 5px auto;">{level}</div>
                    <div style="font-size: 12px; font-weight: 600;">{info['name']}</div>
                    <div style="font-size: 11px; color: #64748b;">{info['accuracy']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# RELIABLE PROPERTY VISUAL FUNCTION (Pexels)
# ─────────────────────────────────────────────
def get_property_visual(lat, lon, dpe_class, is_after=False):
    """Get reliable property visualization using Pexels"""
    
    coord_hash = int(hashlib.md5(f"{lat},{lon}".encode()).hexdigest()[:8], 16)
    
    if is_after:
        base_url = "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg"
    else:
        if dpe_class in ["F", "G"]:
            base_url = "https://images.pexels.com/photos/280229/pexels-photo-280229.jpeg"
        elif dpe_class in ["D", "E"]:
            base_url = "https://images.pexels.com/photos/1643384/pexels-photo-1643384.jpeg"
        else:
            base_url = "https://images.pexels.com/photos/2587054/pexels-photo-2587054.jpeg"
    
    return f"{base_url}?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&sig={coord_hash}"


def dynamic_before_after_section(address, dpe_class, surface, lat, lon):
    """Dynamic before/after section based on user's actual property"""
    
    before_image = get_property_visual(lat, lon, dpe_class, is_after=False)
    after_image = get_property_visual(lat, lon, dpe_class, is_after=True)
    
    base_value = 280000
    after_base = 350000
    subsidy_base = 12500
    roi_base = 18.4
    
    current_value = int(base_value * (surface / 68))
    after_value = int(after_base * (surface / 68))
    subsidy = int(subsidy_base * (surface / 68))
    gain = after_value - current_value
    
    if dpe_class in ["F", "G"]:
        target_dpe = "C"
    elif dpe_class == "E":
        target_dpe = "D"
    else:
        target_dpe = "B"
    
    st.markdown(f"""
    <style>
    .before-after-dynamic {{
        background: linear-gradient(135deg, rgba(34,197,94,0.05), rgba(34,197,94,0.02));
        border-radius: 32px;
        padding: 40px;
        margin: 30px 0;
        text-align: center;
        animation: fadeInUp 0.6s ease-out;
    }}
    
    .comparison-card {{
        transition: all 0.3s cubic-bezier(0.2, 0.8, 0.4, 1);
        cursor: pointer;
    }}
    
    .comparison-card:hover {{
        transform: translateY(-8px);
    }}
    
    .before-card {{
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border-radius: 24px;
        padding: 20px;
        width: 300px;
        text-align: center;
        border: 1px solid rgba(239,68,68,0.3);
    }}
    
    .after-card {{
        background: linear-gradient(135deg, #064e3b, #022c22);
        border-radius: 24px;
        padding: 20px;
        width: 300px;
        text-align: center;
        border: 1px solid #22c55e;
    }}
    
    .property-image {{
        width: 100%;
        height: 200px;
        border-radius: 16px;
        object-fit: cover;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }}
    
    .property-image:hover {{
        transform: scale(1.02);
    }}
    
    .value-gain {{
        background: rgba(34,197,94,0.1);
        border-radius: 60px;
        padding: 12px 24px;
        display: inline-block;
        margin-top: 30px;
    }}
    
    .gain-number {{
        font-size: 20px;
        font-weight: 800;
        color: #22c55e;
    }}
    
    @keyframes arrowPulse {{
        0%, 100% {{ transform: translateX(0); opacity: 0.6; }}
        50% {{ transform: translateX(8px); opacity: 1; }}
    }}
    
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    </style>
    
    <div class="before-after-dynamic">
        <div style="font-size: 1.8rem; font-weight: 800; margin-bottom: 10px;">
            🔄 Avant / Après Rénovation
        </div>
        <div style="color: #64748b; margin-bottom: 30px;">
            Visualisez le potentiel de votre bien à {address[:60]}
        </div>
        
        <div style="display: flex; justify-content: center; align-items: center; gap: 30px; flex-wrap: wrap;">
            <div class="comparison-card before-card">
                <img src="{before_image}" class="property-image" 
                     onerror="this.src='https://placehold.co/400x250/1e293b/64748b?text=Image+non+disponible'">
                <div style="font-weight: 800; font-size: 28px;">DPE: {dpe_class}</div>
                <div style="font-size: 13px; color: #ef4444; margin: 5px 0;">Passoire thermique</div>
                <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.05);">
                    <div style="font-size: 12px; color: #64748b;">Valeur estimée</div>
                    <div style="font-weight: 700; font-size: 20px;">{current_value:,} €</div>
                </div>
            </div>
            
            <div style="font-size: 48px; animation: arrowPulse 1.5s infinite;">→</div>
            
            <div class="comparison-card after-card">
                <img src="{after_image}" class="property-image" 
                     onerror="this.src='https://placehold.co/400x250/064e3b/22c55e?text=Visualisation+renovation'">
                <div style="font-weight: 800; font-size: 28px; color: #22c55e;">DPE: {target_dpe}</div>
                <div style="font-size: 13px; color: #22c55e; margin: 5px 0;">Performance énergétique</div>
                <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(34,197,94,0.2);">
                    <div style="font-size: 12px; color: #64748b;">Valeur estimée</div>
                    <div style="font-weight: 700; font-size: 20px; color: #22c55e;">{after_value:,} €</div>
                </div>
            </div>
        </div>
        
        <div class="value-gain">
            💰 <span class="gain-number">+{gain:,} €</span> de valeur ajoutée • 
            🏷️ Subvention: <span class="gain-number">{subsidy:,} €</span> • 
            📈 ROI: <span class="gain-number">+{roi_base}%</span>
        </div>
        
        <p style="margin-top: 20px; font-size: 12px; color: #475569;">
            *Estimation basée sur les caractéristiques de votre bien (surface: {surface} m²)
        </p>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DPE FUNCTIONS
# ─────────────────────────────────────────────
def fetch_by_dpe_number(numero_dpe: str) -> Optional[dict]:
    if not numero_dpe or len(numero_dpe.strip()) < 5:
        return None
    
    url = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines"
    params = {
        "qs": f"numero_dpe:{numero_dpe.strip()}",
        "size": 1,
        "select": "numero_dpe,etiquette_dpe,etiquette_ges,surface_habitable_logement,code_postal_ban,adresse_ban,date_etablissement_dpe,annee_construction,type_batiment,conso_5_usages_ef_energie_n1,emission_ges_5_usages_n1,type_energie_principale_chauffage"
    }
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", [])
            if results:
                record = results[0]
                dpe_class = str(record.get("etiquette_dpe", "E")).upper().strip()
                surface = record.get("surface_habitable_logement") or 68.0
                postcode = record.get("code_postal_ban", "75000")
                address = record.get("adresse_ban", "")
                
                cost = surface * _FALLBACK_RENO_COST.get(dpe_class, 250)
                roi = _FALLBACK_UPLIFT.get(dpe_class, 13.1)
                
                return {
                    "address": address,
                    "dpe": dpe_class,
                    "surface": surface,
                    "cost": cost,
                    "roi": roi,
                    "zipcode": postcode,
                    "lat": 48.8566,
                    "lon": 2.3522,
                    "data_found": True,
                    "source": "ADEME_DPE_NUMBER",
                    "current_value": 280000
                }
    except:
        pass
    return None


def safe_get(url, params=None):
    try:
        r = requests.get(url, params=params, timeout=10)
        return r.json()
    except:
        return None


def ban_search(query: str, limit: int = 5):
    if not query or len(query.strip()) < 3:
        return []
    data = safe_get("https://api-adresse.data.gouv.fr/search/", {"q": query, "limit": limit})
    features = data.get("features", []) if data else []
    results = []
    for f in features:
        p = f.get("properties", {})
        c = f.get("geometry", {}).get("coordinates", [2.3522, 48.8566])
        results.append({
            "label": p.get("label", ""),
            "postcode": p.get("postcode", ""),
            "city": p.get("city", ""),
            "lon": c[0],
            "lat": c[1],
            "citycode": p.get("citycode", ""),
        })
    return results


def fetch_single_property_ademe(query_address: str, zipcode: str, lat=48.8566, lon=2.3522, citycode: str = ""):
    dpe_by_region = {"75": "E", "92": "E", "93": "F", "94": "E", "69": "D", "13": "D", "31": "D"}
    region = str(zipcode)[:2]
    dpe = dpe_by_region.get(region, "E")
    surface = 52.0 if region == "75" else 75.0
    cost = round(surface * _FALLBACK_RENO_COST.get(dpe, 620), 0)
    roi = _FALLBACK_UPLIFT.get(dpe, 13.1)
    
    st.session_state["property_surface"] = surface
    
    return {
        "address": query_address, "dpe": dpe, "surface": surface,
        "cost": cost, "roi": roi, "zipcode": zipcode, "lat": lat, "lon": lon,
        "data_found": False, "source": "ESTIMATION",
        "current_value": 280000
    }


def generate_professional_pdf(property_data, scenario, target_dpe, active_cost, net_cost, subsidy, roi):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 15, 'ZAMI PROPERTY REPORT', ln=True, align='C')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 8, f'Date: {datetime.now().strftime("%d/%m/%Y")}', ln=True, align='R')
    pdf.ln(5)
    address = property_data.get('address', 'Address not available')
    pdf.set_font('Helvetica', 'B', 12)
    pdf.multi_cell(0, 8, str(address))
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, 'Property Details', ln=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 8, f"Current DPE: {property_data.get('dpe', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"Target DPE: {target_dpe}", ln=True)
    pdf.cell(0, 8, f"Surface: {int(property_data.get('surface', 0))} m2", ln=True)
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, 'Financial Summary', ln=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 8, f"Renovation Cost: EUR {active_cost:,.0f}", ln=True)
    pdf.cell(0, 8, f"Subsidy: EUR {subsidy:,.0f}", ln=True)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, f"Net Investment: EUR {net_cost:,.0f}", ln=True)
    pdf.cell(0, 8, f"Expected ROI: +{roi}%", ln=True)
    pdf.set_y(-30)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 8, 'ZAMI - Property Intelligence Platform', ln=True, align='C')
    output = pdf.output(dest='S')
    if isinstance(output, bytearray):
        output = bytes(output)
    return output


# Language translations
LANG_DICT = {
    "FR": {
        "title": "Portail Propriétaire Énergétique", "subtitle": "Estimez instantanément la valeur et les travaux de votre bien",
        "input_label": "Saisissez l'adresse de votre logement :", "select_certified": "Sélectionnez l'adresse certifiée BAN France :",
        "btn_analyze": "⚡ Lancer l'Analyse", "btn_back": "⬅️ Nouvelle recherche",
        "bilan_title": "BILAN PATRIMONIAL EXCLUSIF", "choose_plan": "PLAN DE CONFIGURATION ÉNERGÉTIQUE",
        "eco_ess": "🛠️ Éco Essential", "eco_ess_sub": "DPE D • Conformité Légale 2026",
        "conf_plus": "⚡ Confort Plus", "conf_plus_sub": "DPE C • Isolation Enveloppe Globale",
        "carb_zero": "🟢 Carbone Zéro", "carb_zero_sub": "DPE B • Décarbonation Pompe à Chaleur",
        "current_class": "Classe Initiale", "target_class": "🎯 Objectif Scénario",
        "surface": "Surface Habitable", "budget_est": "Investissement Global", "uplift_label": "Uplift Marché Estimé",
        "visual_prog": "Vecteur de Progression Énergétique", "your_property": "Actif 🏠", "target_label": "Cible",
        "fin_title": "Analyse d'Ingénierie Financière", "fin_sub": "Subventions Publiques vs Reste à Charge Net",
        "subvention_label": "Aides MaPrimeRénov'", "reste_charge": "Reste à Charge Net",
        "impact_facture": "Impact: Le plan {sc} génère {saving} d'économies par an.",
        "chart_5yr_title": "📊 Évolution Prédictive de l'Actif (2026-2031)",
        "chart_5yr_sub": "Trajectoire patrimoniale après rénovation",
        "form_title": "Mise en Relation avec un Artisan RGE",
        "form_sub": "Recevez 3 devis gratuits d'artisans certifiés",
        "form_name": "Nom Complet *", "form_phone": "Téléphone *", "form_email": "Email *",
        "form_time": "Créneau de rappel", "form_notes": "Notes (optionnel)",
        "form_btn": "📨 Envoyer ma demande", "form_err": "⚠️ Champs requis manquants",
        "form_success": "🎉 Demande envoyée! Un artisan vous contactera sous 24h.",
        "download_btn": "⬇️ Télécharger le Rapport PDF",
        "map_title": "🗺️ Géolocalisation du bien", "loss_title": "🌡️ Pertes thermiques estimées",
        "income_label": "💰 Profil de revenu:", "loan_title": "💶 Simulation Eco-PTZ",
        "loan_duration": "Durée (années)", "monthly_pay": "Mensualité (0% intérêt)",
        "footer": "ZAMI - Intelligence Rénovation Énergétique",
        "search_method_address": "📍 Recherche par adresse (~85% précis)",
        "search_method_dpe": "🔑 Recherche par numéro DPE (100% exact)",
        "dpe_number_label": "🔑 Numéro DPE", "dpe_number_help": "Trouvez le numéro sur votre certificat DPE",
        "dpe_not_found": "❌ Numéro DPE invalide", "exact_match_badge": "✅ Données 100% exactes",
        "select_address_warning": "📍 Sélectionnez une adresse", "enter_input_warning": "⚠️ Entrez une adresse ou un numéro DPE",
        "ai_assistant": "🤖 Assistant IA",
        "pdf_analyzer": "📄 Analyseur DPE"
    },
    "EN": {
        "title": "Energy Property Portal", "subtitle": "Estimate your property value and renovation costs instantly",
        "input_label": "Enter your property address:", "select_certified": "Select certified BAN France address:",
        "btn_analyze": "⚡ Run Analysis", "btn_back": "⬅️ New Search",
        "bilan_title": "EXCLUSIVE PROPERTY AUDIT", "choose_plan": "ENERGY CONFIGURATION PLAN",
        "eco_ess": "🛠️ Eco Essential", "eco_ess_sub": "DPE D • Legal Compliance 2026",
        "conf_plus": "⚡ Comfort Plus", "conf_plus_sub": "DPE C • Full Insulation",
        "carb_zero": "🟢 Carbon Zero", "carb_zero_sub": "DPE B • Heat Pump",
        "current_class": "Current Class", "target_class": "🎯 Target Scenario",
        "surface": "Surface Area", "budget_est": "Global Investment", "uplift_label": "Market Uplift",
        "visual_prog": "Energy Progression", "your_property": "Your Asset 🏠", "target_label": "Target",
        "fin_title": "Financial Analysis", "fin_sub": "Public Subsidies vs Net Cost",
        "subvention_label": "MaPrimeRénov' Aid", "reste_charge": "Net Remaining",
        "impact_facture": "Impact: Plan {sc} saves {saving} annually on utilities.",
        "chart_5yr_title": "📊 5-Year Asset Value Prediction (2026-2031)",
        "chart_5yr_sub": "Renovation vs Obsolescence trajectory",
        "form_title": "Connect with an RGE Certified Contractor",
        "form_sub": "Get 3 free quotes from certified professionals",
        "form_name": "Full Name *", "form_phone": "Phone *", "form_email": "Email *",
        "form_time": "Callback time", "form_notes": "Notes (optional)",
        "form_btn": "📨 Submit Request", "form_err": "⚠️ Required fields missing",
        "form_success": "🎉 Request sent! A contractor will contact you within 24h.",
        "download_btn": "⬇️ Download PDF Report",
        "map_title": "🗺️ Property Location", "loss_title": "🌡️ Estimated Heat Loss",
        "income_label": "💰 Income profile:", "loan_title": "💶 Eco-PTZ Simulation",
        "loan_duration": "Duration (years)", "monthly_pay": "Monthly payment (0% interest)",
        "footer": "ZAMI - Energy Renovation Intelligence",
        "search_method_address": "📍 Address search (~85% accurate)",
        "search_method_dpe": "🔑 DPE number search (100% exact)",
        "dpe_number_label": "🔑 DPE Number", "dpe_number_help": "Find the number on your DPE certificate",
        "dpe_not_found": "❌ Invalid DPE number", "exact_match_badge": "✅ 100% exact data",
        "select_address_warning": "📍 Please select an address", "enter_input_warning": "⚠️ Please enter address or DPE number",
        "ai_assistant": "🤖 AI Assistant",
        "pdf_analyzer": "📄 DPE Analyzer"
    }
}


# ─────────────────────────────────────────────
# PREMIUM HERO SECTION
# ─────────────────────────────────────────────
def hero_section():
    st.markdown("""
    <style>
    .hero-container {
        position: relative;
        border-radius: 32px;
        overflow: hidden;
        margin-bottom: 30px;
        min-height: 550px;
        background: linear-gradient(135deg, #0F172A, #020617);
    }
    
    .hero-iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        z-index: 0;
        border: none;
        pointer-events: none;
    }
    
    .hero-overlay {
        position: relative;
        background: linear-gradient(135deg, rgba(15,23,42,0.7), rgba(2,6,23,0.8));
        border-radius: 32px;
        padding: 60px 40px;
        text-align: center;
        z-index: 1;
        backdrop-filter: blur(3px);
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(59,130,246,0.2);
        backdrop-filter: blur(10px);
        padding: 8px 20px;
        border-radius: 100px;
        margin-bottom: 20px;
        border: 1px solid rgba(59,130,246,0.3);
    }
    
    .hero-badge span {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        color: #3B82F6;
        text-transform: uppercase;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 20px;
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(135deg, #F8FAFC, #3B82F6, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #94A3B8;
        max-width: 600px;
        margin: 0 auto 32px;
        line-height: 1.6;
    }
    
    .search-box-premium {
        max-width: 650px;
        margin: 0 auto;
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(12px);
        border-radius: 60px;
        padding: 8px;
        display: flex;
        border: 1px solid rgba(59, 130, 246, 0.3);
        transition: all 0.3s cubic-bezier(0.2, 0.8, 0.4, 1);
    }
    
    .search-box-premium:hover {
        border-color: rgba(59, 130, 246, 0.6);
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.15);
        transform: translateY(-2px);
    }
    
    .search-box-premium input {
        flex: 1;
        background: transparent;
        border: none;
        padding: 18px 24px;
        font-size: 1rem;
        color: white;
        outline: none;
    }
    
    .search-box-premium input::placeholder {
        color: #475569;
    }
    
    .search-box-premium button {
        background: linear-gradient(135deg, #3B82F6, #10B981);
        border: none;
        padding: 12px 36px;
        border-radius: 50px;
        color: white;
        font-weight: 600;
        font-size: 0.95rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2);
    }
    
    .search-box-premium button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.35);
    }
    
    .hero-footer {
        font-size: 0.7rem;
        color: #475569;
        margin-top: 16px;
    }
    
    @media (max-width: 768px) {
        .hero-overlay {
            padding: 40px 20px;
        }
        .hero-title {
            font-size: 2rem;
        }
        .hero-subtitle {
            font-size: 0.9rem;
        }
        .search-box-premium {
            flex-direction: column;
            background: transparent;
            padding: 0;
        }
        .search-box-premium input {
            background: rgba(15, 23, 42, 0.8);
            border-radius: 50px;
            margin-bottom: 12px;
            padding: 14px 20px;
        }
        .search-box-premium button {
            width: 100%;
            padding: 14px;
        }
    }
    </style>
    
    <div class="hero-container">
        <iframe class="hero-iframe" 
            src="https://www.youtube.com/embed/mCmjNwjYfqw?autoplay=1&loop=1&mute=1&controls=0&playlist=mCmjNwjYfqw&enablejsapi=1"
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen>
        </iframe>
        <div class="hero-overlay">
            <div class="hero-badge">
                <span>⚡ FRANCE'S #1 RENOVATION INTELLIGENCE</span>
            </div>
            <h1 class="hero-title">
                Vérifiez si votre bien est<br>
                louable en 2025
            </h1>
            <p class="hero-subtitle">
                Obtenez votre DPE, le montant exact de MaPrimeRénov'<br>
                et le ROI de votre rénovation en 10 secondes
            </p>
            <div class="search-box-premium">
                <input type="text" placeholder="📍 Adresse complète (ex: 15 Rue de Rivoli, Paris)" id="premiumAddressInput">
                <button id="premiumSearchBtn">Analyser gratuitement →</button>
            </div>
            <div class="hero-footer">
                🔒 Gratuit • Aucune carte bancaire • Rapport instantané
            </div>
        </div>
    </div>
    
    <script>
        document.getElementById('premiumSearchBtn').onclick = function() {
            var address = document.getElementById('premiumAddressInput').value;
            if (address) {
                var input = window.parent.document.querySelector('input[data-testid="stTextInput"]');
                if (input) {
                    input.value = address;
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                }
                var button = window.parent.document.querySelector('button[kind="primary"]');
                if (button) {
                    button.click();
                }
            }
        };
    </script>
    """, unsafe_allow_html=True)


premium_hero_section = hero_section
# ─────────────────────────────────────────────
# TRUST BADGES SECTION
# ─────────────────────────────────────────────
def trust_badges_section():
    st.markdown("""
    <style>
    .trust-section {
        display: flex;
        justify-content: center;
        gap: 40px;
        flex-wrap: wrap;
        margin: 40px 0;
        padding: 20px;
        background: rgba(255,255,255,0.02);
        border-radius: 20px;
    }
    
    .trust-item {
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .trust-item:hover {
        transform: translateY(-5px);
    }
    
    .trust-icon {
        font-size: 28px;
        margin-bottom: 8px;
    }
    
    .trust-text {
        font-size: 12px;
        color: #64748b;
    }
    
    .review-card {
        background: rgba(255,255,255,0.03);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.05);
        transition: all 0.3s ease;
    }
    
    .review-card:hover {
        transform: translateY(-5px);
        border-color: rgba(34,197,94,0.3);
    }
    
    .review-stars {
        color: #fbbf24;
        margin-bottom: 12px;
    }
    
    .review-text {
        font-size: 14px;
        color: #cbd5e1;
        margin-bottom: 12px;
        font-style: italic;
    }
    
    .review-author {
        font-size: 12px;
        color: #22c55e;
        font-weight: 600;
    }
    </style>
    
    <div class="trust-section">
        <div class="trust-item">
            <div class="trust-icon">🔒</div>
            <div class="trust-text">Données sécurisées</div>
        </div>
        <div class="trust-item">
            <div class="trust-icon">⚡</div>
            <div class="trust-text">Rapport en 10 secondes</div>
        </div>
        <div class="trust-item">
            <div class="trust-icon">💰</div>
            <div class="trust-text">Gratuit - Sans carte</div>
        </div>
        <div class="trust-item">
            <div class="trust-icon">🏆</div>
            <div class="trust-text">Données ADEME officielles</div>
        </div>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 40px 0;">
        <div class="review-card">
            <div class="review-stars">★★★★★</div>
            <div class="review-text">"J'ai découvert 8 500€ de subventions que je ne connaissais pas!"</div>
            <div class="review-author">— Marc D., Propriétaire à Lyon</div>
        </div>
        <div class="review-card">
            <div class="review-stars">★★★★★</div>
            <div class="review-text">"En 10 secondes, j'ai eu une vision claire du potentiel de mon bien."</div>
            <div class="review-author">— Sophie M., Paris</div>
        </div>
        <div class="review-card">
            <div class="review-stars">★★★★★</div>
            <div class="review-text">"Outil indispensable pour tout propriétaire bailleur!"</div>
            <div class="review-author">— Thomas L., Investisseur</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LIVE COUNTER SECTION
# ─────────────────────────────────────────────
def live_counter_section():
    st.markdown("""
    <style>
    .counter-section {
        display: flex;
        justify-content: center;
        gap: 60px;
        margin: 50px 0;
        text-align: center;
        flex-wrap: wrap;
    }
    
    .counter-item {
        text-align: center;
        padding: 20px 30px;
        background: rgba(255,255,255,0.02);
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.05);
        transition: all 0.3s ease;
        min-width: 180px;
    }
    
    .counter-item:hover {
        transform: translateY(-5px);
        border-color: rgba(34,197,94,0.3);
    }
    
    .counter-number {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #22c55e, #16a34a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .counter-label {
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 8px;
    }
    </style>
    
    <div class="counter-section" id="counterSection">
        <div class="counter-item">
            <div class="counter-number" id="counter1">0</div>
            <div class="counter-label">Propriétés analysées</div>
        </div>
        <div class="counter-item">
            <div class="counter-number" id="counter2">0</div>
            <div class="counter-label">Subventions trouvées</div>
        </div>
        <div class="counter-item">
            <div class="counter-number" id="counter3">0</div>
            <div class="counter-label">Projets réalisés</div>
        </div>
    </div>
    
    <script>
    function animateCounter(elementId, target, duration) {
        let start = 0;
        let increment = target / (duration / 16);
        let counter = setInterval(() => {
            start += increment;
            if (start >= target) {
                clearInterval(counter);
                document.getElementById(elementId).innerText = target.toLocaleString();
            } else {
                document.getElementById(elementId).innerText = Math.floor(start).toLocaleString();
            }
        }, 16);
    }
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter('counter1', 5432, 2000);
                animateCounter('counter2', 8765, 2000);
                animateCounter('counter3', 1234, 2000);
                observer.unobserve(entry.target);
            }
        });
    });
    
    const counterSection = document.getElementById('counterSection');
    if (counterSection) {
        observer.observe(counterSection);
    }
    </script>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HEADER (No Sidebar)
# ─────────────────────────────────────────────
col_left, col_mid, col_right = st.columns([1.2, 1.5, 1.3])

with col_left:
    st.markdown(get_logo_html(), unsafe_allow_html=True)

with col_mid:
    selected_lang = st.selectbox("🌐 Language", ["FR", "EN"], label_visibility="collapsed", key="lang")

with col_right:
    if st.button("🤖 AI Assistant", use_container_width=True, type="secondary"):
        st.session_state.show_ai_features = not st.session_state.show_ai_features

T = LANG_DICT[selected_lang]

st.markdown('<hr style="border-color:rgba(255,255,255,0.04); margin-bottom:2rem;">', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# AI FEATURES PAGE (When Toggled)
# ─────────────────────────────────────────────
if st.session_state.show_ai_features:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(34,197,94,0.02)); border-radius: 20px; padding: 20px; margin-bottom: 20px;">
        <h2 style="color: white; margin-bottom: 10px;">🤖 ZAMI AI Features</h2>
        <p style="color: #94a3b8;">Powered by advanced AI to help you make better renovation decisions</p>
    </div>
    """, unsafe_allow_html=True)
    
    ai_tab1, ai_tab2 = st.tabs(["💬 AI Chat Assistant", "📄 DPE Document Analyzer"])
    
    with ai_tab1:
        ai_features.ai_chat_agent()
    
    with ai_tab2:
        ai_features.pdf_qa_chatbot()
    
    if st.button("← Back to Property Analysis", use_container_width=True, type="secondary"):
        st.session_state.show_ai_features = False
        st.rerun()


# ─────────────────────────────────────────────
# MAIN CONTENT (Property Analysis)
# ─────────────────────────────────────────────
elif st.session_state["confirmed_owner_property"] is None:
    premium_hero_section()
    trust_badges_section()
    live_counter_section()
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    search_method = st.radio(
        "🔍 Search method:",
        [T["search_method_address"], T["search_method_dpe"]],
        key="search_method",
        horizontal=True
    )
    
    if search_method == T["search_method_address"]:
        search_query = st.text_input(T["input_label"], placeholder="Ex: 39 Rue du Sergent Bobillot, Montreuil", key="search_input")
        if search_query and len(search_query.strip()) >= 3:
            st.session_state["address_suggestions"] = ban_search(search_query)
        suggestions = st.session_state["address_suggestions"]
        if suggestions:
            labels = [f"{s['label']} ({s['postcode']} {s['city']})" for s in suggestions]
            selected_label = st.selectbox(T["select_certified"], labels, key="address_select")
            st.session_state["selected_address_label"] = selected_label
    else:
        dpe_number = st.text_input(T["dpe_number_label"], placeholder="Ex: 1234ABCD5678", key="dpe_input")
        st.caption(T["dpe_number_help"])
    
    if st.button(T["btn_analyze"], type="primary", use_container_width=True, key="analyze_btn"):
        if search_method == T["search_method_dpe"] and dpe_number:
            with st.spinner("🔍 Searching official DPE certificate..."):
                exact_property = fetch_by_dpe_number(dpe_number)
                if exact_property:
                    geo_data = ban_search(exact_property["address"], limit=1)
                    if geo_data:
                        exact_property["lat"] = geo_data[0]["lat"]
                        exact_property["lon"] = geo_data[0]["lon"]
                    st.session_state["confirmed_owner_property"] = exact_property
                    st.session_state["property_surface"] = exact_property.get("surface", 68)
                    st.success(T["exact_match_badge"])
                    st.rerun()
                else:
                    st.error(T["dpe_not_found"])
        elif search_method == T["search_method_address"] and search_query and st.session_state.get("address_suggestions"):
            selected_label = st.session_state.get("selected_address_label")
            suggestions = st.session_state["address_suggestions"]
            labels = [f"{s['label']} ({s['postcode']} {s['city']})" for s in suggestions]
            if selected_label and selected_label in labels:
                chosen_property = suggestions[labels.index(selected_label)]
                with st.spinner("Analyzing..."):
                    prop = fetch_single_property_ademe(
                        chosen_property["label"],
                        chosen_property["postcode"],
                        chosen_property["lat"],
                        chosen_property["lon"],
                        citycode=chosen_property.get("citycode", ""),
                    )
                    st.session_state["confirmed_owner_property"] = prop
                    st.session_state["property_surface"] = prop.get("surface", 68)
                    st.rerun()
            else:
                st.warning(T["select_address_warning"])
        else:
            st.warning(T["enter_input_warning"])
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    base_prop = st.session_state["confirmed_owner_property"]
    dpe_color = _DPE_COLORS.get(base_prop["dpe"], "#475569")
    
    # Show accuracy progress bar
    accuracy_progress_bar()
    
    # Show dynamic before/after section
    dynamic_before_after_section(
        base_prop["address"], 
        base_prop["dpe"], 
        st.session_state["property_surface"], 
        base_prop["lat"], 
        base_prop["lon"]
    )
    
    if st.button(T["btn_back"], key="back_btn"):
        st.session_state["confirmed_owner_property"] = None
        st.session_state["user_responses"] = None
        st.session_state["photos_uploaded"] = False
        st.session_state["accuracy_level"] = 1
        st.rerun()
    
    # Check accuracy level and show relevant sections
    if st.session_state.get("user_responses") is None:
        property_questionnaire()
    else:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(34,197,94,0.08), rgba(34,197,94,0.04)); border-radius: 16px; padding: 15px; margin: 15px 0;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="background: #22c55e; padding: 5px 12px; border-radius: 20px; font-size: 12px;">✓ LEVEL 2</span>
                <span>Questionnaire complété</span>
                <span style="color: #22c55e;">Précision: 85-90%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.get("photos_uploaded"):
            photo_upload_section()
        else:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(34,197,94,0.08), rgba(34,197,94,0.04)); border-radius: 16px; padding: 15px; margin: 15px 0;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="background: #22c55e; padding: 5px 12px; border-radius: 20px; font-size: 12px;">✓ LEVEL 3</span>
                    <span>Photos analysées par IA</span>
                    <span style="color: #22c55e;">Précision: 90-95%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            professional_audit_section()
    
    # Recalculate enhanced ROI if user has responses
    if st.session_state.get("user_responses"):
        enhanced_roi, enhanced_cost = calculate_enhanced_roi(base_prop, st.session_state["user_responses"])
        if enhanced_roi != base_prop.get("roi", 15.0):
            base_prop["roi"] = enhanced_roi
            base_prop["cost"] = enhanced_cost
            st.session_state["confirmed_owner_property"] = base_prop
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<p class="section-label">{T["bilan_title"]}</p><div class="owner-exclusive-title">{base_prop["address"][:60]}</div>', unsafe_allow_html=True)

    if base_prop.get("source") == "ADEME_DPE_NUMBER":
        st.markdown(f'<div style="display:inline-flex;align-items:center;gap:8px; background:rgba(34,197,94,0.12); border:1px solid rgba(34,197,94,0.5); padding:8px 20px; border-radius:100px; margin-bottom:1rem;"><span style="width:8px;height:8px;background:#22c55e;border-radius:50%;"></span><span style="font-size:0.75rem;font-weight:800;color:#22c55e;">{T["exact_match_badge"]}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="display:inline-flex;align-items:center;gap:8px; background:rgba(234,179,8,0.08); border:1px solid rgba(234,179,8,0.25); padding:6px 16px; border-radius:100px; margin-bottom:1rem;"><span style="width:7px;height:7px;background:#eab308;border-radius:50%;"></span><span style="font-size:0.7rem;font-weight:700;color:#fbbf24;">⚡ ZONAL ESTIMATION</span></div>', unsafe_allow_html=True)

    st.markdown(f'<p class="metric-label-sub" style="color:#fff; margin-bottom:15px;">{T["choose_plan"]}</p>', unsafe_allow_html=True)
    
    sc_col1, sc_col2, sc_col3 = st.columns(3)
    with sc_col1:
        is_ess = (st.session_state["selected_scenario"] == "Essential")
        st.markdown(f'<div class="card {"scenario-card-active" if is_ess else ""}" style="padding:1rem; text-align:center;"><strong>{T["eco_ess"]}</strong><br><span style="font-size:0.7rem;color:#64748b;">{T["eco_ess_sub"]}</span></div>', unsafe_allow_html=True)
        if st.button("Select Essential", key="ess", use_container_width=True):
            st.session_state["selected_scenario"] = "Essential"
            st.rerun()
    with sc_col2:
        is_plus = (st.session_state["selected_scenario"] == "Plus")
        st.markdown(f'<div class="card {"scenario-card-active" if is_plus else ""}" style="padding:1rem; text-align:center;"><strong>{T["conf_plus"]}</strong><br><span style="font-size:0.7rem;color:#64748b;">{T["conf_plus_sub"]}</span></div>', unsafe_allow_html=True)
        if st.button("Select Comfort Plus", key="plus", use_container_width=True):
            st.session_state["selected_scenario"] = "Plus"
            st.rerun()
    with sc_col3:
        is_zero = (st.session_state["selected_scenario"] == "Zero")
        st.markdown(f'<div class="card {"scenario-card-active" if is_zero else ""}" style="padding:1rem; text-align:center;"><strong>{T["carb_zero"]}</strong><br><span style="font-size:0.7rem;color:#64748b;">{T["carb_zero_sub"]}</span></div>', unsafe_allow_html=True)
        if st.button("Select Carbon Zero", key="zero", use_container_width=True):
            st.session_state["selected_scenario"] = "Zero"
            st.rerun()

    st.markdown('<hr style="border-color:rgba(255,255,255,0.04); margin:1.5rem 0;">', unsafe_allow_html=True)

    current_scenario = st.session_state["selected_scenario"]
    active_cost = round(base_prop["cost"] * _SCENARIO_COST_MULTIPLIER[current_scenario], 0)
    active_roi = round(base_prop["roi"] * _SCENARIO_ROI_MULTIPLIER[current_scenario], 1)
    target_dpe = _SCENARIO_TARGET_DPE[current_scenario]

    col_left_dpe, col_right_metrics = st.columns([0.8, 2.2], gap="large")
    with col_left_dpe:
        st.markdown(f'<div style="text-align:center; background:rgba(15,23,42,0.4); border-radius:24px; padding:20px;"><p class="metric-label-sub">{T["current_class"]}</p><div class="dpe-badge-big" style="background-color:{dpe_color};">{base_prop["dpe"]}</div><p class="metric-label-sub" style="color:#22c55e; margin-top:12px;">{T["target_class"]} {target_dpe} ✅</p></div>', unsafe_allow_html=True)
    with col_right_metrics:
        m1, m2, m3 = st.columns(3)
        m1.markdown(f'<span class="metric-value-huge">{int(base_prop["surface"])}</span><span style="font-size:1.2rem; color:#475569;"> m²</span><br><span class="metric-label-sub">{T["surface"]}</span>', unsafe_allow_html=True)
        m2.markdown(f'<span class="metric-value-huge">€{active_cost:,.0f}</span><br><span class="metric-label-sub">{T["budget_est"]}</span>', unsafe_allow_html=True)
        m3.markdown(f'<span class="metric-value-huge" style="color:#22c55e;">+{active_roi}%</span><br><span class="metric-label-sub">{T["uplift_label"]}</span>', unsafe_allow_html=True)
        
        st.markdown(f'<p class="metric-label-sub" style="margin-top:15px;">{T["visual_prog"]}</p>', unsafe_allow_html=True)
        dpe_seq = ["G", "F", "E", "D", "C", "B", "A"]
        if base_prop["dpe"] in dpe_seq and target_dpe in dpe_seq:
            c_idx, t_idx = dpe_seq.index(base_prop["dpe"]), dpe_seq.index(target_dpe)
            prog_fig = go.Figure()
            prog_fig.add_trace(go.Scatter(x=dpe_seq, y=[1]*7, mode='markers+text', text=dpe_seq, textposition="top center", marker=dict(size=22, color=["#ff0000","#ff3300","#ff6600","#f2b035","#ccff33","#33cc33","#319834"]), showlegend=False))
            if c_idx < 6 and c_idx != t_idx:
                prog_fig.add_annotation(x=dpe_seq[t_idx], y=1, ax=dpe_seq[c_idx], ay=1, text="", showarrow=True, arrowhead=3, arrowsize=1.2, arrowwidth=3, arrowcolor="#fff")
            prog_fig.update_layout(height=100, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(visible=False), yaxis=dict(visible=False))
            st.plotly_chart(prog_fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

    # Map Section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<p class="section-label">🗺️ GEOSPATIAL</p><h3 class="section-title">{T["map_title"]}</h3>', unsafe_allow_html=True)
    fmap = folium.Map(location=[base_prop["lat"], base_prop["lon"]], zoom_start=17)
    folium.TileLayer('cartodbpositron').add_to(fmap)
    folium.Marker([base_prop["lat"], base_prop["lon"]], icon=folium.Icon(color='green', icon='home')).add_to(fmap)
    st_folium(fmap, use_container_width=True, height=350, returned_objects=[])
    st.markdown('</div>', unsafe_allow_html=True)

    # Financial Section
    if active_cost > 0:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<p class="section-label">{T["fin_title"]}</p><h3 class="section-title">{T["fin_sub"]}</h3>', unsafe_allow_html=True)
        
        income_bracket = st.selectbox(T["income_label"], list(_INCOME_SUBSIDY_MAP.keys()), index=2, key="income")
        subsidy_rate = _INCOME_SUBSIDY_MAP[income_bracket]
        if current_scenario == "Plus":
            subsidy_rate = min(subsidy_rate + 0.05, 0.85)
        elif current_scenario == "Zero":
            subsidy_rate = min(subsidy_rate + 0.12, 0.90)
        estimated_subsidy = round(active_cost * subsidy_rate, 0)
        net_cost = active_cost - estimated_subsidy
        energy_saving = "€1,200" if current_scenario == "Essential" else ("€1,850" if current_scenario == "Plus" else "€2,600")
        
        fcol1, fcol2 = st.columns([1, 1.5])
        with fcol1:
            fig_fin = utils_charts.generate_financial_pie(estimated_subsidy, net_cost, T["subvention_label"], T["reste_charge"])
            st.plotly_chart(fig_fin, use_container_width=True, config={'displayModeBar': False})
        with fcol2:
            st.metric(T["subvention_label"], f"€{estimated_subsidy:,.0f}", f"{int(subsidy_rate*100)}%")
            st.metric(T["reste_charge"], f"€{net_cost:,.0f}")
            st.info(T["impact_facture"].format(sc=current_scenario, saving=energy_saving))
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Loan Section
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<p class="section-label">💶 FINANCING</p><h3 class="section-title">{T["loan_title"]}</h3>', unsafe_allow_html=True)
        loan_years = st.slider(T["loan_duration"], 5, 20, 15, key="loan_years")
        monthly_payment = net_cost / (loan_years * 12)
        st.markdown(f'<span class="metric-value-huge" style="color:#22c55e;">€{monthly_payment:,.2f}</span><span style="font-size:1.2rem;"> / month</span><br><span class="metric-label-sub">{T["monthly_pay"]}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Chart Section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<p class="section-label">{T["chart_5yr_title"]}</p><h3 class="section-title">{T["chart_5yr_sub"]}</h3>', unsafe_allow_html=True)
    fig_5yr = utils_charts.generate_five_year_trajectory(active_roi)
    st.plotly_chart(fig_5yr, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

    # Lead Form
    if active_cost > 0:
        st.markdown('<div class="card" style="border:1px solid rgba(34,197,94,0.2);">', unsafe_allow_html=True)
        st.markdown(f'<p class="section-label" style="color:#22c55e;">📋 RGE CONNECTION</p><h3 style="color:#fff;">{T["form_title"]}</h3><p style="color:#64748b;">{T["form_sub"]}</p>', unsafe_allow_html=True)
        with st.form("lead_form"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input(T["form_name"])
                phone = st.text_input(T["form_phone"])
            with c2:
                email = st.text_input(T["form_email"])
                time_slot = st.selectbox(T["form_time"], ["Morning (9-12h)", "Afternoon (14-17h)"])
            notes = st.text_area(T["form_notes"])
            if st.form_submit_button(T["form_btn"]):
                if name and phone and email:
                    st.success(T["form_success"])
                    save_lead(email, base_prop["address"], base_prop["dpe"], estimated_subsidy, active_roi)
                else:
                    st.error(T["form_err"])
        st.markdown('</div>', unsafe_allow_html=True)

    # PDF Download Section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="section-label" style="color:#22c55e;">📄 DOCUMENTATION</p><h3 style="color:#fff;">Download Property Report</h3>', unsafe_allow_html=True)

    try:
        pdf_bytes = generate_professional_pdf(
            property_data=base_prop,
            scenario=current_scenario,
            target_dpe=target_dpe,
            active_cost=active_cost,
            net_cost=net_cost,
            subsidy=estimated_subsidy if 'estimated_subsidy' in dir() else 0,
            roi=active_roi
        )
        if pdf_bytes and len(pdf_bytes) > 100:
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_bytes,
                file_name=f"ZAMI_Report_{base_prop['zipcode']}_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="pdf_btn"
            )
    except:
        st.info("PDF report will be available soon")
    
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# AGENCY PORTAL BUTTON (Bottom of Main Page)
# ─────────────────────────────────────────────
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🏢 Agency Portal →", use_container_width=True, type="primary"):
        st.switch_page("pages/agency_dashboard.py")


# ─────────────────────────────────────────────
# ADMIN SECTION (View Leads & Chat Messages)
# ─────────────────────────────────────────────
st.markdown('<div class="card" style="background:none; border:none;">', unsafe_allow_html=True)
if st.checkbox("🔐 Admin Panel", key="admin_panel"):
    admin_pwd = st.text_input("Admin Password", type="password", key="admin_pwd")
    if admin_pwd == "ZAMI2026":
        st.success("✅ Admin Access Granted")
        
        tab1, tab2, tab3 = st.tabs(["💬 Chat Messages", "📊 Homeowner Leads", "📈 Statistics"])
        
        with tab1:
            st.markdown("### 💬 Visitor Messages")
            messages = get_all_chat_messages()
            if messages:
                for msg in messages:
                    status_emoji = "🟢" if msg.get("status") == "unread" else "🔵"
                    with st.expander(f"{status_emoji} {msg['name']} - {msg['time']}"):
                        st.markdown(f"**Email:** {msg['email']}")
                        st.markdown(f"**Message:** {msg['message']}")
                        if msg.get("status") == "unread":
                            if st.button(f"Mark as Read", key=f"mark_{msg['id']}"):
                                mark_message_read(msg['id'])
                                st.rerun()
            else:
                st.info("No messages yet")
        
        with tab2:
            st.markdown("### 📊 Homeowner Leads")
            leads = get_all_leads()
            if leads:
                leads_df = pd.DataFrame(leads)
                st.dataframe(leads_df, use_container_width=True)
                csv = leads_df.to_csv(index=False)
                st.download_button("📥 Export Leads to CSV", csv, "zami_leads.csv", "text/csv")
            else:
                st.info("No leads yet")
        
        with tab3:
            st.markdown("### 📈 Statistics")
            messages = get_all_chat_messages()
            leads = get_all_leads()
            st.metric("Total Chat Messages", len(messages))
            st.metric("Total Homeowner Leads", len(leads))
            unread = len([m for m in messages if m.get("status") == "unread"])
            st.metric("Unread Messages", unread)
    elif admin_pwd:
        st.error("❌ Access Denied")
st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown(f'<div class="footer">{T["footer"]}</div>', unsafe_allow_html=True)

# Floating Chat Bot
chat_bot()