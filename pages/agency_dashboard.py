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

st.title("🏢 ZAMI Agency Portal")

# ─────────────────────────────────────────────
# LOGIN / SIGNUP SECTION
# ─────────────────────────────────────────────
if not st.session_state['agency_logged_in']:
    
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
# AGENCY DASHBOARD
# ─────────────────────────────────────────────
else:
    st.markdown(f"## Welcome, {st.session_state['agency_name']}")
    
    with st.sidebar:
        st.markdown(f"### 🏢 {st.session_state['agency_name']}")
        st.markdown("---")
        menu = st.radio("Navigation", ["📋 My Leads", "💬 Messages", "💰 Quotes", "📊 Stats"])
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state['agency_logged_in'] = False
            st.session_state['agency_id'] = None
            st.session_state['agency_name'] = None
            st.rerun()
    
    leads = db.get_agency_leads(st.session_state['agency_id'])
    
    # ─────────────────────────────────────────
    # MY LEADS
    # ─────────────────────────────────────────
    if menu == "📋 My Leads":
        st.markdown("### 📋 Assigned Leads")
        
        if not leads:
            st.info("📭 No leads assigned yet. Check back soon!")
        else:
            for lead in leads:
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
                                st.session_state['selected_lead'] = lead_id
                                st.rerun()
    
    # ─────────────────────────────────────────
    # MESSAGES
    # ─────────────────────────────────────────
    elif menu == "💬 Messages":
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
            for msg in messages:
                sender = "You" if msg[2] == 'agency' else "Client"
                st.markdown(f"""
                <div style="background: {'rgba(34,197,94,0.1)' if msg[2] == 'agency' else 'rgba(255,255,255,0.05)'}; 
                            border-radius: 12px; padding: 10px; margin-bottom: 8px;">
                    <strong>{sender}:</strong> {msg[3]}<br>
                    <small>{msg[4]}</small>
                </div>
                """, unsafe_allow_html=True)
            
            # Send message
            new_msg = st.text_area("Type your message", key="new_msg")
            if st.button("Send Message", type="primary"):
                if new_msg:
                    db.add_message(selected_lead_id, 'agency', st.session_state['agency_id'], new_msg)
                    st.rerun()
    
    # ─────────────────────────────────────────
    # QUOTES
    # ─────────────────────────────────────────
    elif menu == "💰 Quotes":
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
            quote_details = st.text_area("Quote Details", placeholder="Work included, timeline, warranty...")
            
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
    
    # ─────────────────────────────────────────
    # STATS
    # ─────────────────────────────────────────
    elif menu == "📊 Stats":
        st.markdown("### 📊 Performance Statistics")
        
        if leads:
            total = len(leads)
            accepted = len([l for l in leads if l[9] == 'accepted'])
            rejected = len([l for l in leads if l[9] == 'rejected'])
            pending = len([l for l in leads if l[9] == 'pending'])
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Leads", total)
            col2.metric("Accepted", accepted)
            col3.metric("Rejected", rejected)
            col4.metric("Pending", pending)
        else:
            st.info("No data yet")