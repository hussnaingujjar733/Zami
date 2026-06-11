"""
Stripe Payment Integration for ZAMI
Real payment processing with escrow
"""

import streamlit as st
import stripe
from datetime import datetime

# Initialize Stripe with real keys
def init_stripe():
    """Initialize Stripe with API keys from secrets"""
    stripe.api_key = st.secrets.get("STRIPE_SECRET_KEY", "")
    return stripe.api_key != ""

def create_payment_intent(amount_euros, project_id, homeowner_email, description=""):
    """
    Create a payment intent for homeowner to pay
    Money is held by Stripe until captured
    """
    
    if not init_stripe():
        st.error("❌ Stripe not configured. Please add API keys.")
        return None
    
    try:
        amount_cents = int(amount_euros * 100)
        
        payment_intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency='eur',
            payment_method_types=['card'],
            receipt_email=homeowner_email,
            description=f"ZAMI Renovation - Project #{project_id} - {description[:100]}",
            metadata={
                'project_id': str(project_id),
                'type': 'renovation_payment',
                'platform': 'zami'
            },
            statement_descriptor='ZAMI RENOVATION',
            statement_descriptor_suffix=f'PROJ{project_id}',
        )
        
        # Save payment record
        with utils_db_marketplace.get_db() as conn:
            conn.execute(
                """INSERT INTO payments 
                   (project_id, amount, stripe_intent_id, status, created_at) 
                   VALUES (?, ?, ?, ?, ?)""",
                (project_id, amount_euros, payment_intent.id, 'requires_confirmation', datetime.now().isoformat())
            )
            conn.commit()
        
        return payment_intent
        
    except stripe.error.CardError as e:
        st.error(f"Card error: {e.error.message}")
        return None
    except Exception as e:
        st.error(f"Payment error: {str(e)}")
        return None


def confirm_payment(payment_intent_id):
    """Confirm/capture the payment"""
    
    if not init_stripe():
        return False
    
    try:
        payment_intent = stripe.PaymentIntent.capture(payment_intent_id)
        
        with utils_db_marketplace.get_db() as conn:
            conn.execute(
                "UPDATE payments SET status = 'captured' WHERE stripe_intent_id = ?",
                (payment_intent_id,)
            )
            conn.commit()
        
        return payment_intent.status == 'succeeded'
    except Exception as e:
        st.error(f"Confirmation error: {e}")
        return False


def release_to_contractor(project_id, payment_intent_id, contractor_stripe_account_id, amount_euros):
    """
    Release payment to contractor after work verification
    Requires Stripe Connect account for contractor
    """
    
    if not init_stripe():
        return False
    
    try:
        amount_cents = int(amount_euros * 100)
        
        # Create transfer to contractor's connected account
        transfer = stripe.Transfer.create(
            amount=amount_cents,
            currency='eur',
            destination=contractor_stripe_account_id,
            transfer_group=f'project_{project_id}',
            metadata={
                'project_id': str(project_id),
                'type': 'contractor_payout'
            }
        )
        
        with utils_db_marketplace.get_db() as conn:
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
        st.error(f"Transfer error: {e}")
        return False


def refund_payment(payment_intent_id):
    """Refund payment to homeowner"""
    
    if not init_stripe():
        return False
    
    try:
        refund = stripe.Refund.create(
            payment_intent=payment_intent_id,
        )
        
        with utils_db_marketplace.get_db() as conn:
            conn.execute(
                "UPDATE payments SET status = 'refunded' WHERE stripe_intent_id = ?",
                (payment_intent_id,)
            )
            conn.commit()
        
        return True
    except Exception as e:
        st.error(f"Refund error: {e}")
        return False


def get_payment_status(payment_intent_id):
    """Get payment status from Stripe"""
    
    if not init_stripe():
        return None
    
    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return {
            'status': payment_intent.status,
            'amount': payment_intent.amount / 100,
            'currency': payment_intent.currency
        }
    except Exception as e:
        return {'error': str(e)}


def display_payment_element(payment_intent_client_secret):
    """
    Display Stripe Payment Element in Streamlit
    Uses custom component
    """
    
    # Stripe Payment Element HTML/JS
    payment_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://js.stripe.com/v3/"></script>
        <style>
            .stripe-form {{
                padding: 20px;
                background: #1e293b;
                border-radius: 12px;
                border: 1px solid #34d399;
            }}
            .stripe-button {{
                background: linear-gradient(135deg, #2E7D32, #1B5E20);
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                width: 100%;
                font-size: 16px;
                cursor: pointer;
                margin-top: 20px;
            }}
            .stripe-button:hover {{
                background: linear-gradient(135deg, #1B5E20, #0D3B0F);
            }}
        </style>
    </head>
    <body>
        <div class="stripe-form">
            <div id="payment-element"></div>
            <button id="submit" class="stripe-button">💳 Payer maintenant</button>
            <div id="error-message" style="color: red; margin-top: 10px;"></div>
        </div>
        
        <script>
            const stripe = Stripe('{st.secrets.get("STRIPE_PUBLISHABLE_KEY", "")}');
            
            const elements = stripe.elements({{
                clientSecret: '{payment_intent_client_secret}',
            }});
            
            const paymentElement = elements.create('payment');
            paymentElement.mount('#payment-element');
            
            const form = document.getElementById('payment-form');
            const submitBtn = document.getElementById('submit');
            
            submitBtn.addEventListener('click', async (e) => {{
                e.preventDefault();
                submitBtn.disabled = true;
                submitBtn.textContent = 'Traitement...';
                
                const {{ error }} = await stripe.confirmPayment({{
                    elements,
                    confirmParams: {{
                        return_url: window.location.origin + '/?payment_success=true',
                    }},
                }});
                
                if (error) {{
                    const errorDiv = document.getElementById('error-message');
                    errorDiv.textContent = error.message;
                    submitBtn.disabled = false;
                    submitBtn.textContent = '💳 Payer maintenant';
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    return payment_html


def homeowner_payment_modal(amount, project_id, address, homeowner_email):
    """Display payment modal for homeowner"""
    
    st.markdown("---")
    st.subheader("💳 Paiement sécurisé")
    
    # Create payment intent
    payment_intent = create_payment_intent(amount, project_id, homeowner_email, address)
    
    if payment_intent:
        st.info(f"💰 Montant à payer: **{amount:,.0f} €**")
        
        # Display Stripe Payment Element
        from streamlit.components.v1 import html
        html(display_payment_element(payment_intent.client_secret), height=400)
        
        # Check for payment success
        if st.query_params.get('payment_success') == 'true':
            if confirm_payment(payment_intent.id):
                with utils_db_marketplace.get_db() as conn:
                    conn.execute(
                        "UPDATE projects SET status = 'paid_by_homeowner' WHERE id = ?",
                        (project_id,)
                    )
                    conn.commit()
                st.success("✅ Paiement confirmé! Merci.")
                st.balloons()
                st.rerun()
    else:
        st.error("Erreur de création du paiement")


def simple_payment_button(amount, project_id, homeowner_email):
    """Simple payment button that redirects to Stripe Checkout"""
    
    if not init_stripe():
        st.error("Payment system not configured")
        return
    
    try:
        amount_cents = int(amount * 100)
        
        # Create checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': f'ZAMI - Projet de rénovation #{project_id}',
                        'description': 'Paiement pour les travaux de rénovation énergétique',
                    },
                    'unit_amount': amount_cents,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://zami.streamlit.app/?payment_success=true&project_id={}'.format(project_id),
            cancel_url='https://zami.streamlit.app/?payment_cancel=true',
            customer_email=homeowner_email,
            metadata={
                'project_id': str(project_id),
                'type': 'renovation_payment'
            }
        )
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown(f'<a href="{session.url}" target="_blank"><button style="background: linear-gradient(135deg, #2E7D32, #1B5E20); color: white; padding: 12px 24px; border: none; border-radius: 12px; width: 100%; font-size: 1rem; font-weight: bold; cursor: pointer;">💳 Payer {amount:,.0f} €</button></a>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error: {str(e)}")


# Import database utils
from utils import utils_db_marketplace

# Test function
if __name__ == "__main__":
    print("Testing Stripe module...")
    if init_stripe():
        print("✅ Stripe configured with real keys!")
    else:
        print("❌ Stripe not configured")
