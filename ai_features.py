"""
ai_features.py — ZAMI AI Features (Simplified)
"""

import streamlit as st
import tempfile
import os

# Try to import OpenAI
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Try to import PDF processing
try:
    from pypdf import PdfReader
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


# ============================================
# CONFIGURATION
# ============================================

def get_api_key():
    """Get API key from secrets"""
    try:
        return st.secrets.get("OPENROUTER_API_KEY", "")
    except:
        return ""


# ============================================
# FEATURE 1: AI CHAT AGENT (Without LangChain)
# ============================================

def ai_chat_agent():
    """Simple AI chat agent using direct OpenAI call"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(34,197,94,0.05)); border-radius: 16px; padding: 20px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 15px;">
            <span style="font-size: 32px;">🤖</span>
            <div>
                <strong style="font-size: 18px;">ZAMI AI Assistant</strong>
                <p style="font-size: 13px; color: #94a3b8; margin: 0;">Ask me anything about DPE, subsidies, or renovation</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not OPENAI_AVAILABLE:
        st.error("❌ OpenAI package not installed. Please wait for deployment to complete.")
        return
    
    api_key = get_api_key()
    
    if not api_key:
        st.warning("⚠️ API key not configured.")
        st.info("""
        ### How to set up:
        1. Get a free API key from [OpenRouter](https://openrouter.io/keys)
        2. Go to Streamlit Cloud Settings → Secrets
        3. Add: `OPENROUTER_API_KEY = "your-key-here"`
        """)
        return
    
    # Configure OpenAI client for OpenRouter
    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    # Initialize session state
    if "ai_chat_history" not in st.session_state:
        st.session_state.ai_chat_history = []
    
    # Display chat history
    for msg in st.session_state.ai_chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Chat input
    user_question = st.chat_input("Ask me about your property renovation...")
    
    if user_question:
        # Add user message
        st.session_state.ai_chat_history.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.write(user_question)
        
        # Get AI response
        with st.spinner("🤔 Thinking..."):
            try:
                messages = [
                    {"role": "system", "content": "You are ZAMI AI Assistant, expert in French property energy renovation. Help with DPE, MaPrimeRénov' subsidies, ROI, and RGE contractors. Be concise and helpful. Respond in French if asked in French."},
                ] + st.session_state.ai_chat_history
                
                response = client.chat.completions.create(
                    model="meta-llama/llama-3.2-3b-instruct:free",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500
                )
                
                answer = response.choices[0].message.content
                st.session_state.ai_chat_history.append({"role": "assistant", "content": answer})
                with st.chat_message("assistant"):
                    st.write(answer)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Quick question buttons
    st.markdown("---")
    st.markdown("### 🔍 Quick Questions")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💡 What is DPE?", use_container_width=True):
            st.session_state.ai_chat_history.append({"role": "user", "content": "What is DPE?"})
            st.rerun()
    with col2:
        if st.button("💰 How much subsidy?", use_container_width=True):
            st.session_state.ai_chat_history.append({"role": "user", "content": "How much MaPrimeRénov' subsidy can I get?"})
            st.rerun()
    with col3:
        if st.button("🔧 Find contractor?", use_container_width=True):
            st.session_state.ai_chat_history.append({"role": "user", "content": "How to find certified RGE contractors?"})
            st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.ai_chat_history = []
        st.rerun()


# ============================================
# FEATURE 2: PDF Q&A (Simple Version)
# ============================================

def pdf_qa_chatbot():
    """Simple PDF text extraction and Q&A"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(34,197,94,0.05)); border-radius: 16px; padding: 20px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 15px;">
            <span style="font-size: 32px;">📄</span>
            <div>
                <strong style="font-size: 18px;">DPE Document Analyzer</strong>
                <p style="font-size: 13px; color: #94a3b8; margin: 0;">Upload your DPE certificate and ask questions about it</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not OPENAI_AVAILABLE:
        st.error("❌ OpenAI package not installed.")
        return
    
    api_key = get_api_key()
    
    if not api_key:
        st.warning("⚠️ API key not configured.")
        return
    
    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    # Initialize session state
    if "pdf_text" not in st.session_state:
        st.session_state.pdf_text = ""
    if "pdf_processed" not in st.session_state:
        st.session_state.pdf_processed = False
    if "pdf_chat_history" not in st.session_state:
        st.session_state.pdf_chat_history = []
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your DPE certificate (PDF)", type=["pdf"])
    
    if uploaded_file and not st.session_state.pdf_processed:
        with st.spinner("📖 Reading PDF..."):
            try:
                if PDF_AVAILABLE:
                    reader = PdfReader(uploaded_file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()
                    st.session_state.pdf_text = text[:8000]  # Limit to 8000 chars
                    st.session_state.pdf_processed = True
                    st.success(f"✅ Document loaded! {len(text)} characters extracted.")
                else:
                    st.error("PDF processing not available. Please wait for packages to install.")
            except Exception as e:
                st.error(f"Error reading PDF: {str(e)}")
    
    if st.session_state.pdf_processed and st.session_state.pdf_text:
        st.info(f"📄 Document ready for questions")
        
        if st.button("🔄 Clear Document", use_container_width=True):
            st.session_state.pdf_processed = False
            st.session_state.pdf_text = ""
            st.session_state.pdf_chat_history = []
            st.rerun()
        
        st.markdown("---")
        
        # Display chat history
        for msg in st.session_state.pdf_chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        # Question input
        user_question = st.chat_input("Ask about your DPE document...")
        
        if user_question:
            st.session_state.pdf_chat_history.append({"role": "user", "content": user_question})
            with st.chat_message("user"):
                st.write(user_question)
            
            with st.spinner("🔍 Analyzing..."):
                try:
                    messages = [
                        {"role": "system", "content": f"You are analyzing this DPE document. Answer questions based ONLY on the document content. Document text: {st.session_state.pdf_text[:4000]}"},
                        {"role": "user", "content": user_question}
                    ]
                    
                    response = client.chat.completions.create(
                        model="meta-llama/llama-3.2-3b-instruct:free",
                        messages=messages,
                        temperature=0.3,
                        max_tokens=500
                    )
                    
                    answer = response.choices[0].message.content
                    st.session_state.pdf_chat_history.append({"role": "assistant", "content": answer})
                    with st.chat_message("assistant"):
                        st.write(answer)
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        # Sample questions
        st.markdown("---")
        st.markdown("### 💡 Try asking:")
        sample_qs = [
            "What is the DPE class?",
            "What is the energy consumption?",
            "What renovations are recommended?"
        ]
        
        cols = st.columns(3)
        for i, q in enumerate(sample_qs):
            with cols[i]:
                if st.button(q, use_container_width=True):
                    st.session_state.pdf_chat_history.append({"role": "user", "content": q})
                    st.rerun()
    
    elif not st.session_state.pdf_processed:
        st.info("📤 Upload a DPE PDF document to start asking questions about it.")


# ============================================
# MAIN PAGE
# ============================================

def ai_features_page():
    """Main page for AI features"""
    
    st.markdown("""
    <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 2.5rem; margin-bottom: 1rem;">
        🤖 ZAMI AI Features
    </h1>
    <p style="color: #94a3b8; margin-bottom: 2rem;">
        Powered by AI to help you make better renovation decisions
    </p>
    """, unsafe_allow_html=True)
    
    if not OPENAI_AVAILABLE:
        st.warning("⚠️ AI packages are being installed. Please wait a few minutes and refresh.")
        return
    
    # Tab selection
    tab1, tab2 = st.tabs(["💬 AI Chat Assistant", "📄 DPE Document Analyzer"])
    
    with tab1:
        ai_chat_agent()
    
    with tab2:
        pdf_qa_chatbot()