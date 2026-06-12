"""
Simple email notifications for ZAMI leads.
Uses SMTP credentials from Streamlit secrets.
"""

import smtplib
from email.message import EmailMessage
import streamlit as st


def send_new_lead_email(name, email, phone, address, estimated_cost, dpe_rating):
    try:
        smtp_host = st.secrets.get("SMTP_HOST", "")
        smtp_port = int(st.secrets.get("SMTP_PORT", 587))
        smtp_user = st.secrets.get("SMTP_USER", "")
        smtp_password = st.secrets.get("SMTP_PASSWORD", "")
        admin_email = st.secrets.get("ADMIN_EMAIL", "thezamifrance@gmail.com")

        if not smtp_host or not smtp_user or not smtp_password:
            return False

        msg = EmailMessage()
        msg["Subject"] = "Nouveau lead ZAMI"
        msg["From"] = smtp_user
        msg["To"] = admin_email

        msg.set_content(f"""
Nouveau lead ZAMI

Nom: {name}
Email: {email}
Téléphone: {phone}
Adresse: {address}
DPE: {dpe_rating}
Estimation: {estimated_cost:,.0f} €

Connecte-toi à l'admin ZAMI pour traiter ce lead.
""")

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        return True

    except Exception:
        return False
