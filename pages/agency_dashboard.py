import streamlit as st
import sys
import os
import base64
from datetime import datetime
import plotly.graph_objects as go
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import data_store as db

st.set_page_config(page_title="ZAMI Agency Portal", page_icon="🏢", layout="wide")


# ─────────────────────────────────────────────
# LOGO FUNCTION (Same as main app)
# ─────────────────────────────────────────────
def get_logo_html():
    logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "zami_logo.png")
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as img_f:
                logo_base64 = base64.b64encode(img_f.read()).decode()
                return f'<img src="data:image/png;base64,{logo_base64}" style="height:50px; width:auto;">'
        except:
            pass
    return '<div style="font-family:\'Space Grotesk\', sans-serif; font-size:1.8rem; font-weight:800; color:#22c55e;">ZAMI</div>'


# Custom CSS for premium look
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display: none;}
    
    .stApp {
        background: linear-gradient(135deg, #0a0c15 0%, #0f1119 100%);
    }
    
    .premium-card {
        background: linear-gradient(135deg, rgba(15, 25, 45, 0.8), rgba(10, 15, 30, 0.9));
        backdrop-filter: blur(15px);
        border: 1px solid rgba(34, 197, 94, 0.15);
        border-radius: 24px;
        padding: 24px;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .premium-card:hover {
        border-color: rgba(34, 197, 94, 0.4);
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(34, 197, 94, 0.1);
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #22c55e, #16a34a, #22c55e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff, #22c55e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .logo-container {
        animation: fadeInDown 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .welcome-text {
        animation: fadeInUp 0.6s ease-out 0.2s both;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agency_logged_in' not in st.session_state:
    st.session_state['agency_logged_in'] = False
    st.session_state['agency_id'] = None
    st.session_state['agency_name'] = None

# ─────────────────────────────────────────────
# LOGO SECTION (Using same logo as main app)
# ─────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"""
    <div class="logo-container" style="text-align: center; padding: 20px 0;">
        {get_logo_html()}
        <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 2rem; margin: 10px 0 0 0;">
            Agency <span style="color: #22c55e;">Portal</span>
        </h1>
        <p style="color: #64748b; margin-top: 5px;">Professional Real Estate Partner Portal</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────
# LOGIN / SIGNUP SECTION
# ─────────────────────────────────────────────
if not st.session_state['agency_logged_in']:
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register Agency"])
        
        with tab1:
            st.markdown("### Welcome Back")
            st.markdown("<p style='color:#64748b; margin-bottom:20px;'>Sign in to manage your leads and proposals</p>", unsafe_allow_html=True)
            
            email = st.text_input("Email Address", placeholder="agency@example.com", key="login_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="login_password")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                if st.button("Login", type="primary", use_container_width=True):
                    if email and password:
                        result = db.authenticate_agency(email, password)
                        if result:
                            st.session_state['agency_logged_in'] = True
                            st.session_state['agency_id'] = result[0]
                            st.session_state['agency_name'] = result[1]
                            st.rerun()
                        else:
                            st.error("❌ Invalid email or password")
                    else:
                        st.warning("Please enter email and password")
        
        with tab2:
            st.markdown("### Register Your Agency")
            st.markdown("<p style='color:#64748b; margin-bottom:20px;'>Join ZAMI network and get quality leads</p>", unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                company_name = st.text_input("Company Name *", placeholder="ABC Real Estate", key="reg_company")
                email = st.text_input("Email *", placeholder="contact@abcrealty.com", key="reg_email")
                phone = st.text_input("Phone", placeholder="+33 1 23 45 67 89", key="reg_phone")
            with col_b:
                siret = st.text_input("SIRET Number", placeholder="123 456 789 00012", key="reg_siret")
                address = st.text_area("Office Address", placeholder="15 Rue de Rivoli, 75004 Paris", key="reg_address")
            
            password = st.text_input("Password *", type="password", placeholder="••••••••", key="reg_password")
            confirm = st.text_input("Confirm Password *", type="password", placeholder="••••••••", key="reg_confirm")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                if st.button("Register Agency", type="primary", use_container_width=True):
                    if company_name and email and password:
                        if password == confirm:
                            success = db.register_agency(company_name, email, phone, siret, address, password)
                            if success:
                                st.success("✅ Registration successful! Please login.")
                            else:
                                st.error("❌ Email already registered")
                        else:
                            st.error("❌ Passwords do not match")
                    else:
                        st.warning("Please fill all required fields (*)")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# AGENCY DASHBOARD
# ─────────────────────────────────────────────
else:
    # Header with agency info
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="welcome-text" style="text-align: center; padding: 10px 0;">
            <p style="color: #22c55e; font-size: 0.8rem; letter-spacing: 2px;">WELCOME BACK</p>
            <h2 style="font-size: 2rem; margin: 0;">{st.session_state['agency_name']}</h2>
            <p style="color: #64748b;">Your dashboard is ready</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Get leads data
    leads = db.get_agency_leads(st.session_state['agency_id'])
    
    # Statistics Cards
    total = len(leads)
    pending = len([l for l in leads if l[9] == 'pending']) if leads else 0
    accepted = len([l for l in leads if l[9] == 'accepted']) if leads else 0
    rejected = len([l for l in leads if l[9] == 'rejected']) if leads else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="premium-card" style="text-align: center;">
            <p style="color:#64748b; font-size:0.8rem;">TOTAL LEADS</p>
            <div class="stat-number">{total}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="premium-card" style="text-align: center;">
            <p style="color:#eab308; font-size:0.8rem;">PENDING</p>
            <div class="stat-number" style="background: linear-gradient(135deg, #eab308, #fbbf24); -webkit-background-clip: text;">{pending}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="premium-card" style="text-align: center;">
            <p style="color:#22c55e; font-size:0.8rem;">ACCEPTED</p>
            <div class="stat-number">{accepted}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="premium-card" style="text-align: center;">
            <p style="color:#ef4444; font-size:0.8rem;">REJECTED</p>
            <div class="stat-number" style="background: linear-gradient(135deg, #ef4444, #f87171); -webkit-background-clip: text;">{rejected}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 My Leads", "💬 Messages", "💰 Quotes", "📊 Analytics", "⚙️ Settings"])
    
    # TAB 1: MY LEADS
    with tab1:
        st.markdown("### 📋 Assigned Leads")
        
        if not leads:
            st.info("📭 No leads assigned yet. Check back soon!")
        else:
            status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Accepted", "Rejected"], key="status_filter", label_visibility="collapsed")
            
            filter_map = {"All": "all", "Pending": "pending", "Accepted": "accepted", "Rejected": "rejected"}
            filter_value = filter_map.get(status_filter, "all")
            
            if filter_value == "all":
                filtered_leads = leads
            else:
                filtered_leads = [l for l in leads if l[9] == filter_value]
            
            for lead in filtered_leads:
                lead_id = lead[0]
                address = lead[2]
                dpe = lead[3]
                surface = lead[4]
                budget = lead[5]
                customer_name = lead[6]
                customer_phone = lead[7]
                status = lead[9]
                
                if status == 'pending':
                    badge = "🟡 PENDING"
                elif status == 'accepted':
                    badge = "🟢 ACCEPTED"
                else:
                    badge = "🔴 REJECTED"
                
                with st.expander(f"🏠 {address} - DPE: {dpe} - {badge}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**📍 Property Details**")
                        st.write(f"• Surface: **{surface} m²**")
                        st.write(f"• Budget Estimé: **€{budget:,.0f}**")
                        st.write(f"• Current DPE: **{dpe}**")
                    with col2:
                        st.markdown(f"**👤 Client Information**")
                        st.write(f"• Name: **{customer_name}**")
                        st.write(f"• Phone: **{customer_phone}**")
                    
                    st.markdown("---")
                    
                    if status == 'pending':
                        col_acc, col_rej = st.columns(2)
                        with col_acc:
                            if st.button(f"✅ Accept Lead", key=f"accept_{lead_id}", use_container_width=True, type="primary"):
                                db.update_lead_status(lead_id, 'accepted')
                                st.rerun()
                        with col_rej:
                            if st.button(f"❌ Decline Lead", key=f"reject_{lead_id}", use_container_width=True):
                                db.update_lead_status(lead_id, 'rejected')
                                st.rerun()
                    elif status == 'accepted':
                        st.success("✅ Lead Accepted")
                        st.info("You can now message the client using the Messages tab.")
    
    # TAB 2: MESSAGES
    with tab2:
        st.markdown("### 💬 Client Messages")
        
        accepted_leads = [l for l in leads if l[9] == 'accepted'] if leads else []
        
        if not accepted_leads:
            st.info("No accepted leads to message. Accept a lead first.")
        else:
            lead_options = {f"{l[2]} - {l[6]}": l[0] for l in accepted_leads}
            selected = st.selectbox("Select Client", list(lead_options.keys()), key="client_select")
            selected_lead_id = lead_options[selected]
            
            st.markdown("---")
            
            st.markdown('<div class="premium-card" style="height: 400px; overflow-y: auto;">', unsafe_allow_html=True)
            
            messages = db.get_messages(selected_lead_id)
            if messages:
                for msg in messages:
                    sender = "You" if msg[2] == 'agency' else "Client"
                    align = "right" if msg[2] == 'agency' else "left"
                    color = "rgba(34,197,94,0.15)" if msg[2] == 'agency' else "rgba(255,255,255,0.05)"
                    st.markdown(f"""
                    <div style="text-align: {align}; margin-bottom: 12px;">
                        <div style="display: inline-block; background: {color}; border-radius: 18px; padding: 10px 16px; max-width: 70%;">
                            <strong>{sender}:</strong> {msg[3]}<br>
                            <small style="color: #64748b;">{msg[4]}</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No messages yet. Start the conversation!")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            new_msg = st.text_area("Type your message", key="new_msg", height=80)
            col_send1, col_send2, col_send3 = st.columns([1, 1, 1])
            with col_send2:
                if st.button("📤 Send Message", type="primary", use_container_width=True):
                    if new_msg:
                        db.add_message(selected_lead_id, 'agency', st.session_state['agency_id'], new_msg)
                        st.success("Message sent!")
                        st.rerun()
    
    # TAB 3: QUOTES
    with tab3:
        st.markdown("### 💰 Quotes & Proposals")
        
        accepted_leads = [l for l in leads if l[9] == 'accepted'] if leads else []
        
        if not accepted_leads:
            st.info("No accepted leads to quote. Accept a lead first.")
        else:
            lead_options = {f"{l[2]} - {l[6]}": l[0] for l in accepted_leads}
            selected = st.selectbox("Select Client", list(lead_options.keys()), key="quote_select")
            selected_lead_id = lead_options[selected]
            
            lead = next((l for l in accepted_leads if l[0] == selected_lead_id), None)
            if lead:
                st.markdown(f"""
                <div class="premium-card">
                    <strong>🏠 Property:</strong> {lead[2]}<br>
                    <strong>👤 Client:</strong> {lead[6]}<br>
                    <strong>📞 Phone:</strong> {lead[7]}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            col_q1, col_q2 = st.columns(2)
            with col_q1:
                quote_amount = st.number_input("Quote Amount (€)", min_value=0, step=500, value=25000, key="quote_amount")
            with col_q2:
                quote_duration = st.selectbox("Project Duration", ["2-3 weeks", "4-5 weeks", "6-8 weeks", "2-3 months"], key="quote_duration")
            
            quote_details = st.text_area("Quote Details", placeholder="Describe work included: materials, labor, timeline, warranty...", height=120, key="quote_details")
            
            col_submit1, col_submit2, col_submit3 = st.columns([1, 2, 1])
            with col_submit2:
                if st.button("💰 Submit Quote", type="primary", use_container_width=True):
                    if quote_amount > 0 and quote_details:
                        db.add_quote(selected_lead_id, st.session_state['agency_id'], quote_amount, quote_details)
                        st.success(f"✅ Quote of €{quote_amount:,.0f} submitted!")
                        st.balloons()
                    else:
                        st.warning("Please fill amount and details")
            
            quotes = db.get_quotes_for_lead(selected_lead_id)
            if quotes:
                st.markdown("---")
                st.markdown("#### 📜 Previous Quotes")
                for q in quotes:
                    st.markdown(f"""
                    <div class="premium-card" style="margin-bottom: 10px;">
                        <strong>€{q[3]:,.0f}</strong><br>
                        {q[4][:150]}...<br>
                        <small>Status: {q[5]} | {q[6]}</small>
                    </div>
                    """, unsafe_allow_html=True)
    
    # TAB 4: ANALYTICS
    with tab4:
        st.markdown("### 📊 Performance Analytics")
        
        if leads:
            fig = go.Figure(data=[go.Pie(
                labels=['Pending', 'Accepted', 'Rejected'],
                values=[pending, accepted, rejected],
                marker=dict(colors=['#eab308', '#22c55e', '#ef4444']),
                hole=0.4,
                textinfo='label+percent'
            )])
            fig.update_layout(height=400, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
            st.plotly_chart(fig, use_container_width=True)
            
            conversion_rate = (accepted / total * 100) if total > 0 else 0
            st.metric("🎯 Conversion Rate", f"{conversion_rate:.1f}%")
            
            st.markdown("---")
            st.markdown("#### 📈 Lead Trend")
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            trend_data = [4, 7, 12, 15, 18, 22]
            
            fig_line = go.Figure(data=[go.Scatter(
                x=months, y=trend_data,
                mode='lines+markers',
                line=dict(color='#22c55e', width=3),
                marker=dict(size=10, color='#22c55e'),
                fill='tozeroy',
                fillcolor='rgba(34,197,94,0.1)'
            )])
            fig_line.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("No data yet. Start accepting leads to see analytics.")
    
    # TAB 5: SETTINGS
    with tab5:
        st.markdown("### ⚙️ Agency Settings")
        st.info("Profile settings coming soon.")
        
        st.markdown("---")
        st.markdown("#### 📞 Contact Information")
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.text_input("Company Name", value=st.session_state['agency_name'])
            st.text_input("Email")
            st.text_input("Phone")
        with col_s2:
            st.text_area("Office Address", height=100)
            st.selectbox("Notification Preferences", ["Email only", "SMS only", "Both"])
        
        col_save1, col_save2, col_save3 = st.columns([1, 2, 1])
        with col_save2:
            if st.button("💾 Save Changes", type="primary", use_container_width=True):
                st.success("Settings saved!")
    
    # Logout button
    st.markdown("---")
    col_logout1, col_logout2, col_logout3 = st.columns([1, 2, 1])
    with col_logout2:
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            st.session_state['agency_logged_in'] = False
            st.session_state['agency_id'] = None
            st.session_state['agency_name'] = None
            st.rerun()