import os
import requests

def send_new_lead_email(name, email, phone, address, estimated_cost, dpe_rating):
    try:
        api_key = os.environ.get("RESEND_API_KEY", "")
        admin_email = os.environ.get("ADMIN_EMAIL", "thezamifrance@gmail.com")

        if not api_key:
            return False

        payload = {
            "from": "ZAMI <onboarding@resend.dev>",
            "to": [admin_email],
            "subject": f"🔥 Nouveau lead ZAMI - {name}",
            "text": f"""
NOUVEAU LEAD ZAMI

Nom: {name}
Email: {email}
Téléphone: {phone}
Adresse: {address}

DPE: {dpe_rating}
Estimation: {estimated_cost:,.0f} €

Connectez-vous à l'administration ZAMI pour traiter ce lead.
"""
        }

        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=10
        )

        if response.status_code in [200, 202]:
            return True

        print("RESEND ERROR:", response.status_code, response.text)
        return False

    except Exception as e:
        print("EMAIL ERROR:", e)
        return False
