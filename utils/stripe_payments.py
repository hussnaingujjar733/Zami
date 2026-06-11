"""
Stripe Payment Integration for ZAMI
Optional module - app works without Stripe
"""

import streamlit as st

# Try to import stripe, but don't fail if not installed
try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False
    stripe = None

def init_stripe():
    """Initialize Stripe with API keys"""
    if not STRIPE_AVAILABLE:
        return False
    stripe.api_key = st.secrets.get("STRIPE_SECRET_KEY", "")
    return stripe.api_key != ""

def create_payment_intent(amount_euros, project_id, homeowner_email, description=""):
    """Create a payment intent for homeowner to pay"""
    
    if not STRIPE_AVAILABLE or not init_stripe():
        st.warning("⚠️ Payment system not configured. Contact support to complete payment.")
        return None
    
    try:
        amount_cents = int(amount_euros * 100)
        payment_intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency='eur',
            payment_method_types=['card'],
            receipt_email=homeowner_email,
            description=f"ZAMI Renovation - Project #{project_id}",
            metadata={'project_id': str(project_id)}
        )
        return payment_intent
    except Exception as e:
        st.error(f"Payment error: {str(e)}")
        return None

def simple_payment_button(amount, project_id, homeowner_email):
    """Display a simple payment button"""
    
    if not STRIPE_AVAILABLE:
        st.info(f"💰 Pour finaliser le paiement de {amount:,.0f} €, veuillez contacter l'administrateur.")
        return
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button(f"💳 Payer {amount:,.0f} €", type="primary", use_container_width=True):
            st.info("🔗 Redirection vers la page de paiement sécurisé...")
            st.warning("Intégration Stripe en cours de finalisation. Pour le moment, veuillez contacter l'administrateur.")

def confirm_payment(payment_intent_id):
    """Confirm payment (mock for now)"""
    st.success("✅ Paiement simulé avec succès!")
    return True

# For testing
if __name__ == "__main__":
    print(f"Stripe available: {STRIPE_AVAILABLE}")
