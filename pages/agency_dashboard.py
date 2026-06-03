import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils_db

st.set_page_config(page_title="Agency Dashboard - ZAMI", page_icon="🏢", layout="wide")

# Check if agency is logged in
if 'agency_logged_in' not in st.session_state:
    st.session_state['agency_logged_in'] = False
    st.session_state['agency_id'] = None
    st.session_state['agency_name'] = None

# Login/Signup Section
if not st.session_state['agency_logged_in']:
    st.title("🏢 Agency Portal")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", key="login_btn"):
            result = utils_db.authenticate_agency(email, password)
            if result:
                st.session_state['agency_logged_in'] = True
                st.session_state['agency_id'] = result[0]
                st.session_state['agency_name'] = result[1]
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    with tab2:
        company_name = st.text_input("Company Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        siret = st.text_input("SIRET Number")
        address = st.text_area("Office Address")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        
        if st.button("Register", key="register_btn"):
            if password == confirm:
                if utils_db.register_agency(company_name, email, phone, siret, address, password):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Email already registered")
            else:
                st.error("Passwords don't match")

else:
    # Agency Dashboard
    st.title(f"🏢 Welcome, {st.session_state['agency_name']}")
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state['agency_logged_in'] = False
        st.session_state['agency_id'] = None
        st.session_state['agency_name'] = None
        st.rerun()
    
    # Get leads
    leads = utils_db.get_agency_leads(st.session_state['agency_id'])
    
    if not leads:
        st.info("No leads assigned yet. Check back soon!")
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
            
            with st.expander(f"🏠 {address} - DPE: {dpe} - Status: {status}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Surface:** {surface} m²")
                    st.write(f"**Estimated Budget:** €{budget:,.0f}")
                    st.write(f"**Customer:** {customer_name}")
                    st.write(f"**Phone:** {customer_phone}")
                
                with col2:
                    if status == 'pending':
                        col_acc, col_rej = st.columns(2)
                        with col_acc:
                            if st.button(f"✓ Accept", key=f"accept_{lead_id}"):
                                utils_db.update_lead_status(lead_id, 'accepted')
                                st.rerun()
                        with col_rej:
                            if st.button(f"✗ Reject", key=f"reject_{lead_id}"):
                                utils_db.update_lead_status(lead_id, 'rejected')
                                st.rerun()
                    
                    elif status == 'accepted':
                        st.success("Lead Accepted")
                        
                        # Chat section
                        st.markdown("---")
                        st.markdown("### 💬 Chat with Customer")
                        
                        # Show messages
                        messages = utils_db.get_messages(lead_id)
                        for msg in messages:
                            sender = "You" if msg[2] == 'agency' else "Customer"
                            st.write(f"**{sender}:** {msg[3]}")
                        
                        # Send message
                        new_msg = st.text_area("Type your message", key=f"msg_{lead_id}")
                        if st.button("Send", key=f"send_{lead_id}"):
                            if new_msg:
                                utils_db.add_message(lead_id, 'agency', st.session_state['agency_id'], new_msg)
                                st.rerun()
                        
                        # Quote section
                        st.markdown("---")
                        st.markdown("### 💰 Submit Quote")
                        quote_amount = st.number_input("Quote Amount (€)", min_value=0, step=500, key=f"amount_{lead_id}")
                        quote_details = st.text_area("Quote Details (work included)", key=f"details_{lead_id}")
                        
                        if st.button("Submit Quote", key=f"quote_{lead_id}"):
                            if quote_amount > 0:
                                utils_db.add_quote(lead_id, st.session_state['agency_id'], quote_amount, quote_details)
                                st.success("Quote submitted!")
                    
                    elif status == 'rejected':
                        st.warning("Lead Rejected")