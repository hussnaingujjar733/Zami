import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

st.set_page_config(page_title="ZAMI Admin Panel", page_icon="🔐", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    [data-testid="stSidebarCollapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.admin-header {
    background: linear-gradient(135deg, #0F172A, #020617);
    border-radius: 28px;
    padding: 30px 20px;
    text-align: center;
    margin-bottom: 30px;
    border: 1px solid rgba(34,197,94,0.3);
}
.admin-header h1 {
    color: #22c55e;
    margin-bottom: 10px;
}
.admin-header p {
    color: #94a3b8;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="admin-header">
    <h1>🔐 ZAMI Admin Vault</h1>
    <p>Secure Lead Management System</p>
</div>
""", unsafe_allow_html=True)

LEADS_FILE = "leads.json"

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔑 Admin Access Required")
        password = st.text_input("Enter Password", type="password")
        if st.button("🔐 Authenticate", type="primary", use_container_width=True):
            if password == "ZAMI2026":
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("❌ Invalid Password")
    st.stop()

st.success("✅ Admin Access Granted")

col1, col2, col3 = st.columns(3)

with col1:
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "r", encoding="utf-8") as f:
            leads_data = json.load(f)
        total = len(leads_data)
        new = len([l for l in leads_data if l.get("status") == "new"])
        st.metric("📊 Total Leads", total)
        st.metric("🆕 New Leads", new)
    else:
        st.metric("📊 Total Leads", "0")
        st.metric("🆕 New Leads", "0")

with col2:
    st.markdown("### 📈 Quick Stats")
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "r", encoding="utf-8") as f:
            leads_data = json.load(f)
        dpe_counts = {}
        for lead in leads_data:
            dpe = lead.get("dpe", "Unknown")
            dpe_counts[dpe] = dpe_counts.get(dpe, 0) + 1
        if dpe_counts:
            st.write("**DPE Distribution:**")
            for dpe, count in dpe_counts.items():
                st.write(f"- DPE {dpe}: {count} leads")
    else:
        st.info("No data yet")

with col3:
    st.markdown("### 🎯 Actions")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

st.markdown("---")
st.markdown("### 📋 All Leads")

if os.path.exists(LEADS_FILE):
    with open(LEADS_FILE, "r", encoding="utf-8") as f:
        leads_data = json.load(f)
    
    if leads_data:
        df = pd.DataFrame(leads_data)
        st.dataframe(df, use_container_width=True, height=500)
        
        col_export1, col_export2 = st.columns(2)
        with col_export1:
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Export to CSV",
                data=csv,
                file_name=f"zami_leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True,
                type="primary"
            )
        with col_export2:
            st.info(f"📊 Total: {len(leads_data)} leads captured")
    else:
        st.info("No leads captured yet")
else:
    st.info("No leads file found")

st.markdown("---")
if st.button("🏠 Back to Main App", use_container_width=True):
    st.switch_page("app.py")