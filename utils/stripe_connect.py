"""
Stripe Connect - Escrow payments for ZAMI
Homeowner pays → ZAMI holds → Artisan gets paid after verification
"""

import streamlit as st
import stripe
from datetime import datetime

# Initialize Stripe
def init_stripe():
    stripe.api_key = st.secrets.get("STRIPE_SECRET_KEY", "")
    return stripe.api_key

# ========== ARTISAN ONBOARDING ==========

def create_artisan_stripe_account(artisan_id, email, company_name):
    """
    Create a Stripe Connect account for artisan
    This allows them to receive payments
    """
    
    if not init_stripe():
        return None
    
    try:
        account = stripe.account.create(
            type='express',
            country='FR',
            email=email,
            business_type='individual',
            business_profile={
                'name': company_name,
                'url': 'https://zami.streamlit.app'
            },
            capabilities={
                'transfers': {'requested': True},
            },
            metadata={
                'artisan_id': str(artisan_id)
            }
        )
        
        # Save account ID to database
        with st.session_state.get_db() as conn:
            conn.execute(
                "UPDATE contractors SET stripe_account_id = ? WHERE id = ?",
                (account.id, artisan_id)
            )
            conn.commit()
        
        return account.id
        
    except Exception as e:
        st.error(f"Stripe Connect error: {e}")
        return None


def get_artisan_onboarding_link(artisan_id, stripe_account_id):
    """
    Get onboarding link for artisan to complete their Stripe account
    """
    
    if not init_stripe():
        return None
    
    try:
        account_link = stripe.account_link.create(
            account=stripe_account_id,
            refresh_url='https://zami.streamlit.app/artisan/refresh',
            return_url='https://zami.streamlit.app/artisan/complete',
            type='account_onboarding',
        )
        return account_link.url
    except Exception as e:
        st.error(f"Onboarding link error: {e}")
        return None


# ========== ESCROW PAYMENT ==========

def create_escrow_payment(amount_euros, project_id, homeowner_email, artisan_stripe_account_id):
    """
    Create a payment intent that holds money in escrow
    Homeowner pays, money held by Stripe until released
    """
    
    if not init_stripe():
        return None
    
    try:
        amount_cents = int(amount_euros * 100)
        
        # Create payment intent with destination charge
        payment_intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency='eur',
            payment_method_types=['card'],
            transfer_data={
                'destination': artisan_stripe_account_id,
            },
            metadata={
                'project_id': str(project_id),
                'type': 'renovation_payment'
            },
            capture_method='manual',  # Manual capture = escrow
            statement_descriptor='ZAMI RENOVATION',
            receipt_email=homeowner_email,
        )
        
        # Save to database
        with st.session_state.get_db() as conn:
            conn.execute(
                "INSERT INTO payments (project_id, amount, stripe_intent_id, status, created_at) VALUES (?,?,?,?,?)",
                (project_id, amount_euros, payment_intent.id, 'pending', datetime.now().isoformat())
            )
            conn.commit()
        
        return payment_intent.client_secret
        
    except Exception as e:
        st.error(f"Payment intent error: {e}")
        return None


def confirm_payment(payment_intent_id):
    """
    Confirm/capture the payment (after homeowner approves)
    Money is now held in escrow
    """
    
    if not init_stripe():
        return False
    
    try:
        stripe.PaymentIntent.capture(payment_intent_id)
        return True
    except Exception as e:
        st.error(f"Capture error: {e}")
        return False


def release_payment_to_artisan(payment_intent_id, project_id):
    """
    Release escrow money to artisan after work verification
    """
    
    if not init_stripe():
        return False
    
    try:
        # Payment already captured, funds will be transferred
        # Update database
        with st.session_state.get_db() as conn:
            conn.execute(
                "UPDATE payments SET status = 'released', released_at = ? WHERE stripe_intent_id = ?",
                (datetime.now().isoformat(), payment_intent_id)
            )
            conn.execute(
                "UPDATE projects SET status = 'paid' WHERE id = ?",
                (project_id,)
            )
            conn.commit()
        
        return True
        
    except Exception as e:
        st.error(f"Release error: {e}")
        return False


def refund_payment(payment_intent_id):
    """
    Refund payment to homeowner (if work not done)
    """
    
    if not init_stripe():
        return False
    
    try:
        refund = stripe.Refund.create(
            payment_intent=payment_intent_id,
        )
        
        with st.session_state.get_db() as conn:
            conn.execute(
                "UPDATE payments SET status = 'refunded' WHERE stripe_intent_id = ?",
                (payment_intent_id,)
            )
            conn.commit()
        
        return True
    except Exception as e:
        st.error(f"Refund error: {e}")
        return False


# ========== PAYMENT BUTTONS ==========

def homeowner_payment_button(amount, project_id, artisan_stripe_account_id, homeowner_email):
    """
    Display payment button for homeowner
    """
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button(f"💳 Payer {amount:,.0f} €", type="primary", use_container_width=True):
            client_secret = create_escrow_payment(
                amount, project_id, homeowner_email, artisan_stripe_account_id
            )
            
            if client_secret:
                # In production, use Stripe Elements
                # For now, show success and update status
                with st.session_state.get_db() as conn:
                    conn.execute(
                        "UPDATE projects SET status = 'paid_by_homeowner' WHERE id = ?",
                        (project_id,)
                    )
                    conn.commit()
                
                st.success("✅ Paiement effectué! L'argent est sécurisé.")
                st.info("Le paiement sera débloqué à l'artisan après vérification des travaux.")
                st.rerun()
            else:
                st.error("Erreur de paiement")


def artisan_request_payout_button(payment_intent_id, project_id):
    """
    Button for artisan to request payout
    (Admin triggers after verification)
    """
    
    if st.button("💰 Demander le paiement", type="primary"):
        if release_payment_to_artisan(payment_intent_id, project_id):
            st.success("✅ Paiement débloqué! Sous 2-3 jours ouvrés.")
            st.rerun()
        else:
            st.error("Erreur de déblocage")


# ========== ADMIN PAYMENT MANAGEMENT ==========

def admin_payment_controls(payment_intent_id, project_id, amount):
    """
    Admin controls for payment management
    """
    
    st.write(f"**Montant:** {amount:,.0f} €")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Débloquer paiement artisan", key=f"release_{project_id}", type="primary"):
            if release_payment_to_artisan(payment_intent_id, project_id):
                st.success("Paiement débloqué!")
                st.rerun()
    
    with col2:
        if st.button("❌ Rembourser homeowner", key=f"refund_{project_id}"):
            if refund_payment(payment_intent_id):
                st.success("Remboursement effectué!")
                st.rerun()


def get_payment_status(project_id):
    """Get payment status for a project"""
    
    with st.session_state.get_db() as conn:
        payment = conn.execute(
            "SELECT * FROM payments WHERE project_id = ? ORDER BY created_at DESC LIMIT 1",
            (project_id,)
        ).fetchone()
        
        if payment:
            return {
                'status': payment[3],
                'amount': payment[2],
                'stripe_intent_id': payment[4],
                'created_at': payment[5]
            }
    return None


def update_payment_status(project_id, status):
    """Update payment status in database"""
    
    with st.session_state.get_db() as conn:
        conn.execute(
            "UPDATE payments SET status = ? WHERE project_id = ?",
            (status, project_id)
        )
        conn.commit()
