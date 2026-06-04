import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import data_store as db

st.set_page_config(page_title="Agency Portal - ZAMI", page_icon="🏢", layout="wide")

# Initialize session state
if 'agency_logged_in' not in st.session_state:
    st.session_state['agency_logged_in'] = False
    st.session_state['agency_id'] = None
    st.session_state['agency_name'] = None
    st.session_state['current_page'] = "Leads"

# ─────────────────────────────────────────────
# LOGIN / SIGNUP SECTION
# ─────────────────────────────────────────────
if not st.session_state['agency_logged_in']:
    st.title("🏢 ZAMI Agency Portal")
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
    
    with tab1:
        st.markdown("### Login to Your Account")
        email = st.text_input("Email Address", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
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
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company Name *", key="reg_company")
            email = st.text_input("Email *", key="reg_email")
            phone = st.text_input("Phone", key="reg_phone")
        with col2:
            siret = st.text_input("SIRET Number", key="reg_siret")
            address = st.text_area("Office Address", key="reg_address")
        
        password = st.text_input("Password *", type="password", key="reg_password")
        confirm = st.text_input("Confirm Password *", type="password", key="reg_confirm")
        
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

# ─────────────────────────────────────────────
# AGENCY DASHBOARD WITH SIDEBAR
# ─────────────────────────────────────────────
else:
    # ─── SIDEBAR NAVIGATION ───
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0 10px 0;">
            <div style="background: linear-gradient(135deg, #22c55e, #16a34a); width: 60px; height: 60px; border-radius: 30px; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px auto;">
                <span style="font-size: 30px;">🏢</span>
            </div>
            <h3 style="color: white; margin-bottom: 5px;">{st.session_state['agency_name']}</h3>
            <p style="color: #22c55e; font-size: 12px;">● Active</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation menu
        menu_options = ["📋 My Leads", "💬 Messages", "💰 Quotes", "📊 Statistics", "⚙️ Settings"]
        menu_icons = ["📋", "💬", "💰", "📊", "⚙️"]
        
        for i, option in enumerate(menu_options):
            if st.sidebar.button(f"{menu_icons[i]} {option}", key=f"nav_{option}", use_container_width=True):
                st.session_state['current_page'] = option
                st.rerun()
        
        st.markdown("---")
        
        # Agency stats in sidebar
        leads = db.get_agency_leads(st.session_state['agency_id'])
        total = len(leads)
        pending = len([l for l in leads if l[9] == 'pending'])
        accepted = len([l for l in leads if l[9] == 'accepted'])
        
        st.sidebar.markdown("### 📊 Quick Stats")
        col1, col2, col3 = st.sidebar.columns(3)
        col1.metric("Total", total)
        col2.metric("Pending", pending)
        col3.metric("Accepted", accepted)
        
        st.markdown("---")
        
        if st.sidebar.button("🚪 Logout", use_container_width=True, type="secondary"):
            st.session_state['agency_logged_in'] = False
            st.session_state['agency_id'] = None
            st.session_state['agency_name'] = None
            st.rerun()
    
    # ─── MAIN CONTENT AREA ───
    current_page = st.session_state['current_page']
    
    # Header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(34,197,94,0.02)); border-radius: 16px; padding: 20px; margin-bottom: 25px;">
        <h1 style="color: white; margin-bottom: 5px;">{current_page}</h1>
        <p style="color: #94a3b8;">Welcome back, {st.session_state['agency_name']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get leads
    leads = db.get_agency_leads(st.session_state['agency_id'])
    
    # ==========================================
    # PAGE: MY LEADS
    # ==========================================
    if current_page == "📋 My Leads":
        st.markdown("### 📋 Assigned Leads")
        
        if not leads:
            st.info("📭 No leads assigned yet. Check back soon!")
        else:
            # Filter by status
            status_filter = st.selectbox("Filter by Status", ["All", "pending", "accepted", "rejected"])
            
            filtered_leads = leads if status_filter == "All" else [l for l in leads if l[9] == status_filter]
            
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
                    badge_color = "#eab308"
                elif status == 'accepted':
                    badge = "🟢 ACCEPTED"
                    badge_color = "#22c55e"
                else:
                    badge = "🔴 REJECTED"
                    badge_color = "#ef4444"
                
                with st.expander(f"🏠 {address} - DPE: {dpe} - {badge}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Surface:** {surface} m²")
                        st.write(f"**Budget Estimé:** €{budget:,.0f}")
                        st.write(f"**Client:** {customer_name}")
                        st.write(f"**Téléphone:** {customer_phone}")
                    
                    with col2:
                        if status == 'pending':
                            col_acc, col_rej = st.columns(2)
                            with col_acc:
                                if st.button(f"✅ Accept", key=f"accept_{lead_id}"):
                                    db.update_lead_status(lead_id, 'accepted')
                                    st.rerun()
                            with col_rej:
                                if st.button(f"❌ Reject", key=f"reject_{lead_id}"):
                                    db.update_lead_status(lead_id, 'rejected')
                                    st.rerun()
                        elif status == 'accepted':
                            st.success("✅ Lead Accepted")
                            if st.button(f"💬 Message Client", key=f"msg_{lead_id}"):
                                st.session_state['current_page'] = "💬 Messages"
                                st.rerun()
    
    # ==========================================
    # PAGE: MESSAGES
    # ==========================================
    elif current_page == "💬 Messages":
        st.markdown("### 💬 Messages")
        
        accepted_leads = [l for l in leads if l[9] == 'accepted']
        
        if not accepted_leads:
            st.info("No accepted leads to message")
        else:
            lead_options = {f"{l[2]} - {l[6]}": l[0] for l in accepted_leads}
            selected = st.selectbox("Select Client", list(lead_options.keys()))
            selected_lead_id = lead_options[selected]
            
            st.markdown("---")
            
            # Show messages
            messages = db.get_messages(selected_lead_id)
            if messages:
                for msg in messages:
                    sender = "You" if msg[2] == 'agency' else "Client"
                    st.markdown(f"""
                    <div style="background: {'rgba(34,197,94,0.1)' if msg[2] == 'agency' else 'rgba(255,255,255,0.05)'}; 
                                border-radius: 12px; padding: 10px; margin-bottom: 8px;">
                        <strong>{sender}:</strong> {msg[3]}<br>
                        <small style="color: #64748b;">{msg[4]}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No messages yet. Start the conversation!")
            
            # Send message
            new_msg = st.text_area("Type your message", key="new_msg", height=80)
            if st.button("Send Message", type="primary"):
                if new_msg:
                    db.add_message(selected_lead_id, 'agency', st.session_state['agency_id'], new_msg)
                    st.success("Message sent!")
                    st.rerun()
    
    # ==========================================
    # PAGE: QUOTES
    # ==========================================
    elif current_page == "💰 Quotes":
        st.markdown("### 💰 Quotes")
        
        accepted_leads = [l for l in leads if l[9] == 'accepted']
        
        if not accepted_leads:
            st.info("No accepted leads to quote")
        else:
            lead_options = {f"{l[2]} - {l[6]}": l[0] for l in accepted_leads}
            selected = st.selectbox("Select Client", list(lead_options.keys()))
            selected_lead_id = lead_options[selected]
            
            lead = next((l for l in accepted_leads if l[0] == selected_lead_id), None)
            if lead:
                st.markdown(f"**Property:** {lead[2]}")
                st.markdown(f"**Client:** {lead[6]}")
            
            st.markdown("---")
            
            quote_amount = st.number_input("Quote Amount (€)", min_value=0, step=500, value=25000)
            quote_details = st.text_area("Quote Details", placeholder="Work included, timeline, warranty...", height=100)
            
            if st.button("Submit Quote", type="primary"):
                if quote_amount > 0 and quote_details:
                    db.add_quote(selected_lead_id, st.session_state['agency_id'], quote_amount, quote_details)
                    st.success(f"✅ Quote of €{quote_amount:,.0f} submitted!")
            
            # Show existing quotes
            quotes = db.get_quotes_for_lead(selected_lead_id)
            if quotes:
                st.markdown("---")
                st.markdown("#### Previous Quotes")
                for q in quotes:
                    st.markdown(f"**€{q[3]:,.0f}** - {q[4][:100]}...")
    
    # ==========================================
    # PAGE: STATISTICS
    # ==========================================
    elif current_page == "📊 Statistics":
        st.markdown("### 📊 Performance Statistics")
        
        if leads:
            total = len(leads)
            pending = len([l for l in leads if l[9] == 'pending'])
            accepted = len([l for l in leads if l[9] == 'accepted'])
            rejected = len([l for l in leads if l[9] == 'rejected'])
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Leads", total)
            col2.metric("Pending", pending, delta=f"{pending/total*100:.0f}%" if total > 0 else "0%")
            col3.metric("Accepted", accepted, delta=f"{accepted/total*100:.0f}%" if total > 0 else "0%")
            col4.metric("Rejected", rejected)
            
            # Chart
            import plotly.graph_objects as go
            fig = go.Figure(data=[go.Pie(
                labels=['Pending', 'Accepted', 'Rejected'],
                values=[pending, accepted, rejected],
                marker=dict(colors=['#eab308', '#22c55e', '#ef4444']),
                hole=0.4
            )])
            fig.update_layout(height=400, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.info("No data yet")
    
    # ==========================================
    # PAGE: SETTINGS
    # ==========================================
    elif current_page == "⚙️ Settings":
        st.markdown("### ⚙️ Agency Settings")
        st.info("Profile settings coming soon. You can update your contact information here.")
        
        st.markdown("---")
        st.markdown("#### Contact Information")
        st.text_input("Company Name", value=st.session_state['agency_name'])
        st.text_input("Email")
        st.text_input("Phone")
        st.text_area("Address")
        
        if st.button("Save Changes", type="primary"):
            st.success("Settings saved!")