import os
import smtplib
from email.message import EmailMessage

def send_new_lead_email(name, email, phone, address, estimated_cost, dpe_rating):
    try:
        smtp_host = os.environ.get("SMTP_HOST", "")
        smtp_port = int(os.environ.get("SMTP_PORT", "587"))
        smtp_user = os.environ.get("SMTP_USER", "")
        smtp_password = os.environ.get("SMTP_PASSWORD", "")
        admin_email = os.environ.get("ADMIN_EMAIL", "thezamifrance@gmail.com")

        if not smtp_host or not smtp_user or not smtp_password:
            return False

        msg = EmailMessage()
        msg["Subject"] = f"🔥 Nouveau lead ZAMI - {name}"
        msg["From"] = smtp_user
        msg["To"] = admin_email

        msg.set_content(f"""
NOUVEAU LEAD ZAMI

Nom: {name}
Email: {email}
Téléphone: {phone}
Adresse: {address}

DPE: {dpe_rating}
Estimation: {estimated_cost:,.0f} €

Connectez-vous à l'administration ZAMI pour traiter ce lead.
""")

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        return True

    except Exception as e:
        print("EMAIL ERROR:", e)
        return False
