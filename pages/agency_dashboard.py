import streamlit as st
import sys
import os
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils_db

st.set_page_config(page_title="Agency Portal - ZAMI", page_icon="🏢", layout="wide")

# Initialize session state
if 'agency_logged_in' not in st.session_state:
    st.session_state['agency_logged_in'] = False
    st.session_state['agency_id'] = None
    st.session_state['agency_name'] = None
    st.session_state['selected_lead_id'] = None

# Title
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
                result = utils_db.authenticate_agency(email, password)
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
                    success = utils_db.register_agency(company_name, email, phone, siret, address, password)
                    if success:
                        st.success("✅ Registration successful! Please login.")
                    else:
                        st.error("❌ Email already registered")
                else:
                    st.error("❌ Passwords do not match")
            else:
                st.warning("Please fill all required fields (*)")

# ─────────────────────────────────────────────
# AGENCY DASHBOARD (AFTER LOGIN)
# ─────────────────────────────────────────────
else:
    st.markdown(f"## Welcome, {st.session_state['agency_name']}")
    
    # Sidebar Menu
    with st.sidebar:
        st.markdown(f"### 🏢 {st.session_state['agency_name']}")
        st.markdown("---")
        menu = st.radio("Navigation", ["📋 My Leads", "💬 Messages", "💰 Quotes", "📊 Stats", "⚙️ Settings"])
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state['agency_logged_in'] = False
            st.session_state['agency_id'] = None
            st.session_state['agency_name'] = None
            st.session_state['selected_lead_id'] = None
            st.rerun()
    
    # Get leads for this agency
    leads = utils_db.get_agency_leads(st.session_state['agency_id'])
    
    # ─────────────────────────────────────────
    # MENU: MY LEADS
    # ─────────────────────────────────────────
    if menu == "📋 My Leads":
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
                customer_email = lead[8]
                status = lead[9]
                
                # Status badge
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
                        st.write(f"**Email:** {customer_email}")
                    
                    with col2:
                        if status == 'pending':
                            col_acc, col_rej = st.columns(2)
                            with col_acc:
                                if st.button(f"✅ Accept", key=f"accept_{lead_id}"):
                                    utils_db.update_lead_status(lead_id, 'accepted')
                                    st.success("Lead accepted! You can now message the client.")
                                    time.sleep(1)
                                    st.rerun()
                            with col_rej:
                                if st.button(f"❌ Reject", key=f"reject_{lead_id}"):
                                    utils_db.update_lead_status(lead_id, 'rejected')
                                    st.warning("Lead rejected")
                                    time.sleep(1)
                                    st.rerun()
                        
                        elif status == 'accepted':
                            st.success("✅ Lead Accepted")
                            
                            # Chat button
                            if st.button(f"💬 Message Client", key=f"chat_{lead_id}"):
                                st.session_state['selected_lead_id'] = lead_id
                                st.rerun()
                            
                            # Quote button
                            if st.button(f"💰 Submit Quote", key=f"quote_{lead_id}"):
                                st.session_state['selected_lead_id'] = lead_id
                                st.rerun()
    
    # ─────────────────────────────────────────
    # MENU: MESSAGES
    # ─────────────────────────────────────────
    elif menu == "💬 Messages":
        st.markdown("### 💬 Messages")
        
        if not leads:
            st.info("No leads to message")
        else:
            # Select lead to chat with
            lead_options = {f"{l[2]} - {l[6]}": l[0] for l in leads if l[9] == 'accepted'}
            
            if lead_options:
                selected_lead_name = st.selectbox("Select Client", list(lead_options.keys()))
                selected_lead_id = lead_options[selected_lead_name]
                
                st.markdown("---")
                st.markdown(f"#### 💬 Chat with Client")
                
                # Display messages
                messages = utils_db.get_messages(selected_lead_id)
                if messages:
                    for msg in messages:
                        sender = "You" if msg[2] == 'agency' else "Client"
                        st.markdown(f"""
                        <div style="background: {'rgba(34,197,94,0.1)' if msg[2] == 'agency' else 'rgba(255,255,255,0.05)'}; 
                                    border-radius: 12px; 
                                    padding: 10px; 
                                    margin-bottom: 8px;">
                            <strong>{sender}:</strong> {msg[3]}<br>
                            <small style="color:#64748b;">{msg[4]}</small>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No messages yet. Start the conversation!")
                
                # Send new message
                st.markdown("---")
                new_message = st.text_area("Type your message", key="new_msg")
                if st.button("Send Message", type="primary"):
                    if new_message:
                        utils_db.add_message(selected_lead_id, 'agency', st.session_state['agency_id'], new_message)
                        st.success("Message sent!")
                        st.rerun()
                    else:
                        st.warning("Please type a message")
            else:
                st.info("No accepted leads to message. Accept a lead first.")
    
    # ─────────────────────────────────────────
    # MENU: QUOTES
    # ─────────────────────────────────────────
    elif menu == "💰 Quotes":
        st.markdown("### 💰 Quotes")
        
        if not leads:
            st.info("No leads to quote")
        else:
            # Select lead to quote
            lead_options = {f"{l[2]} - {l[6]}": l[0] for l in leads if l[9] == 'accepted'}
            
            if lead_options:
                selected_lead_name = st.selectbox("Select Client for Quote", list(lead_options.keys()))
                selected_lead_id = lead_options[selected_lead_name]
                
                # Get lead details
                lead = next((l for l in leads if l[0] == selected_lead_id), None)
                if lead:
                    st.markdown(f"**Property:** {lead[2]}")
                    st.markdown(f"**Client:** {lead[6]}")
                
                st.markdown("---")
                st.markdown("#### Submit Your Quote")
                
                quote_amount = st.number_input("Quote Amount (€)", min_value=0, step=500, value=25000, key="quote_amount")
                quote_details = st.text_area("Quote Details (work included, timeline, conditions)", 
                                            placeholder="e.g., Installation of heat pump, insulation of attic, new windows...\nTimeline: 4 weeks\nWarranty: 2 years",
                                            key="quote_details")
                
                if st.button("Submit Quote", type="primary"):
                    if quote_amount > 0 and quote_details:
                        utils_db.add_quote(selected_lead_id, st.session_state['agency_id'], quote_amount, quote_details)
                        st.success(f"✅ Quote of €{quote_amount:,.0f} submitted successfully!")
                        st.balloons()
                    else:
                        st.warning("Please fill both amount and details")
                
                # Show existing quotes
                quotes = utils_db.get_quotes_for_lead(selected_lead_id)
                if quotes:
                    st.markdown("---")
                    st.markdown("#### Previous Quotes")
                    for q in quotes:
                        st.markdown(f"""
                        <div style="background:rgba(34,197,94,0.05); border-radius:12px; padding:10px; margin-bottom:8px;">
                            <strong>€{q[3]:,.0f}</strong><br>
                            {q[4][:100]}...<br>
                            <small>Status: {q[5]} | {q[6]}</small>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No accepted leads to quote. Accept a lead first.")
    
    # ─────────────────────────────────────────
    # MENU: STATS
    # ─────────────────────────────────────────
    elif menu == "📊 Stats":
        st.markdown("### 📊 Performance Statistics")
        
        if leads:
            total_leads = len(leads)
            accepted = len([l for l in leads if l[9] == 'accepted'])
            rejected = len([l for l in leads if l[9] == 'rejected'])
            pending = len([l for l in leads if l[9] == 'pending'])
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Leads", total_leads)
            col2.metric("Accepted", accepted, delta=f"{accepted/total_leads*100:.0f}%")
            col3.metric("Rejected", rejected)
            col4.metric("Pending", pending)
            
            # Quotes submitted
            quotes_count = 0
            for l in leads:
                quotes = utils_db.get_quotes_for_lead(l[0])
                quotes_count += len(quotes)
            st.metric("Quotes Submitted", quotes_count)
        else:
            st.info("No data yet")
    
    # ─────────────────────────────────────────
    # MENU: SETTINGS
    # ─────────────────────────────────────────
    elif menu == "⚙️ Settings":
        st.markdown("### ⚙️ Agency Settings")
        st.info("Profile settings coming soon. You can update your contact information here.")