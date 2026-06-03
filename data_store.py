# data_store.py
import json
import os
import hashlib
import time

DATA_FILE = "agencies.json"
LEADS_FILE = "leads.json"
MESSAGES_FILE = "messages.json"
QUOTES_FILE = "quotes.json"


def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()


# ─────────────────────────────────────────────
# AGENCY FUNCTIONS
# ─────────────────────────────────────────────

def load_agencies():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_agencies(agencies):
    with open(DATA_FILE, "w") as f:
        json.dump(agencies, f, indent=2)


def register_agency(company_name, email, phone, siret, address, password):
    agencies = load_agencies()
    if email in agencies:
        return False
    agencies[email] = {
        "id": len(agencies) + 1,
        "company_name": company_name,
        "email": email,
        "phone": phone,
        "siret": siret,
        "address": address,
        "password_hash": hash_password(password),
        "created_at": str(time.time())
    }
    save_agencies(agencies)
    return True


def authenticate_agency(email, password):
    agencies = load_agencies()
    if email in agencies:
        if agencies[email]["password_hash"] == hash_password(password):
            return (agencies[email]["id"], agencies[email]["company_name"])
    return None


def get_all_agencies():
    agencies = load_agencies()
    return [(v["id"], v["company_name"], v["email"], v.get("phone", "")) for v in agencies.values()]


def get_agency_by_id(agency_id):
    agencies = load_agencies()
    for email, data in agencies.items():
        if data["id"] == agency_id:
            return data
    return None


# ─────────────────────────────────────────────
# LEAD FUNCTIONS
# ─────────────────────────────────────────────

def load_leads():
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "r") as f:
            return json.load(f)
    return []


def save_leads(leads):
    with open(LEADS_FILE, "w") as f:
        json.dump(leads, f, indent=2)


def assign_lead_to_agency(agency_id, lead_data):
    leads = load_leads()
    new_lead = {
        "id": len(leads) + 1,
        "agency_id": agency_id,
        "property_address": lead_data.get("address"),
        "property_dpe": lead_data.get("dpe"),
        "property_surface": lead_data.get("surface"),
        "estimated_budget": lead_data.get("budget"),
        "customer_name": lead_data.get("customer_name"),
        "customer_phone": lead_data.get("customer_phone"),
        "customer_email": lead_data.get("customer_email"),
        "status": "pending",
        "assigned_at": str(time.time()),
        "accepted_at": None,
        "rejected_at": None
    }
    leads.append(new_lead)
    save_leads(leads)
    return new_lead["id"]


def get_agency_leads(agency_id):
    leads = load_leads()
    return [tuple(l.values()) for l in leads if l["agency_id"] == agency_id]


def update_lead_status(lead_id, status):
    leads = load_leads()
    for lead in leads:
        if lead["id"] == lead_id:
            lead["status"] = status
            if status == "accepted":
                lead["accepted_at"] = str(time.time())
            else:
                lead["rejected_at"] = str(time.time())
            break
    save_leads(leads)


def get_lead_by_id(lead_id):
    leads = load_leads()
    for lead in leads:
        if lead["id"] == lead_id:
            return lead
    return None


# ─────────────────────────────────────────────
# MESSAGES FUNCTIONS
# ─────────────────────────────────────────────

def load_messages():
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, "r") as f:
            return json.load(f)
    return []


def save_messages(messages):
    with open(MESSAGES_FILE, "w") as f:
        json.dump(messages, f, indent=2)


def add_message(lead_id, sender_type, sender_id, message):
    messages = load_messages()
    new_msg = {
        "id": len(messages) + 1,
        "lead_id": lead_id,
        "sender_type": sender_type,
        "sender_id": sender_id,
        "message": message,
        "sent_at": str(time.time())
    }
    messages.append(new_msg)
    save_messages(messages)


def get_messages(lead_id):
    messages = load_messages()
    return [tuple(m.values()) for m in messages if m["lead_id"] == lead_id]


# ─────────────────────────────────────────────
# QUOTES FUNCTIONS
# ─────────────────────────────────────────────

def load_quotes():
    if os.path.exists(QUOTES_FILE):
        with open(QUOTES_FILE, "r") as f:
            return json.load(f)
    return []


def save_quotes(quotes):
    with open(QUOTES_FILE, "w") as f:
        json.dump(quotes, f, indent=2)


def add_quote(lead_id, agency_id, amount, details):
    quotes = load_quotes()
    new_quote = {
        "id": len(quotes) + 1,
        "lead_id": lead_id,
        "agency_id": agency_id,
        "quote_amount": amount,
        "quote_details": details,
        "status": "pending",
        "created_at": str(time.time())
    }
    quotes.append(new_quote)
    save_quotes(quotes)


def get_quotes_for_lead(lead_id):
    quotes = load_quotes()
    return [tuple(q.values()) for q in quotes if q["lead_id"] == lead_id]