"""
ai_features.py — ZAMI AI Features
Contains: AI Chat Agent + PDF Q&A Chatbot
"""

import streamlit as st
import tempfile
import os

# Optional imports with try-except for graceful fallback
try:
    from langchain_openai import ChatOpenAI
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_community.vectorstores import Chroma
    from langchain_openai import OpenAIEmbeddings
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.memory import ConversationBufferMemory
    from langchain.chains import RetrievalQA
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    LANGCHAIN_AVAILABLE = False
    print(f"LangChain import error: {e}")


# ============================================
# CONFIGURATION
# ============================================

def get_llm():
    """Get LLM instance from secrets"""
    
    if not LANGCHAIN_AVAILABLE:
        return None
    
    # Try to get API key from Streamlit secrets
    try:
        openrouter_key = st.secrets.get("OPENROUTER_API_KEY", "")
        openai_key = st.secrets.get("OPENAI_API_KEY", "")
    except:
        openrouter_key = ""
        openai_key = ""
    
    # Use OpenAI if available
    if openai_key:
        try:
            return ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7,
                api_key=openai_key
            )
        except Exception:
            pass
    
    # Use OpenRouter as fallback (free)
    if openrouter_key:
        try:
            return ChatOpenAI(
                model="meta-llama/llama-3.2-3b-instruct:free",
                temperature=0.7,
                api_key=openrouter_key,
                base_url="https://openrouter.ai/api/v1"
            )
        except Exception:
            pass
    
    return None


# ============================================
# FEATURE 1: AI CHAT AGENT
# ============================================

def ai_chat_agent():
    """Simple AI chat agent for property renovation questions"""
    
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
    
    if not LANGCHAIN_AVAILABLE:
        st.error("❌ AI features not available. Packages are being installed.")
        st.info("Please wait 2-3 minutes and refresh the page. If issue persists, contact support.")
        return
    
    llm = get_llm()
    
    if not llm:
        st.warning("⚠️ AI features require API key configuration.")
        st.info("""
        ### How to set up AI features:
        1. Get a free API key from [OpenRouter](https://openrouter.io/keys)
        2. Add it to Streamlit Cloud Secrets:
           - Go to your app settings
           - Add `OPENROUTER_API_KEY` = "your-key-here"
        """)
        return
    
    # Initialize session state for chat history
    if "ai_chat_history" not in st.session_state:
        st.session_state.ai_chat_history = []
    
    # Display chat history
    for msg in st.session_state.ai_chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 12px;">
                <div style="background: linear-gradient(135deg, #22c55e, #16a34a); border-radius: 18px; padding: 10px 16px; max-width: 80%;">
                    <span style="color: white;">{msg['content']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin-bottom: 12px;">
                <div style="background: rgba(34,197,94,0.1); border: 1px solid rgba(34,197,94,0.3); border-radius: 18px; padding: 10px 16px; max-width: 80%;">
                    <span style="color: #e2e8f0;">🤖 {msg['content']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    user_question = st.chat_input("Ask me about your property renovation...")
    
    if user_question:
        # Add user message
        st.session_state.ai_chat_history.append({"role": "user", "content": user_question})
        
        # Get AI response
        with st.spinner("🤔 Thinking..."):
            try:
                system_prompt = """You are ZAMI AI Assistant, an expert in French property energy renovation.
                You help property owners with:
                - DPE (Diagnostic de Performance Énergétique) - classes A to G
                - MaPrimeRénov' subsidies and eligibility
                - Renovation cost estimates and ROI
                - Finding RGE certified contractors
                - Energy efficiency improvements
                
                Be helpful, concise, and professional. Respond in French unless asked otherwise.
                """
                
                messages = [
                    {"role": "system", "content": system_prompt}
                ] + [
                    {"role": m["role"], "content": m["content"]} 
                    for m in st.session_state.ai_chat_history
                ]
                
                response = llm.invoke(messages)
                answer = response.content
                
                st.session_state.ai_chat_history.append({"role": "assistant", "content": answer})
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.session_state.ai_chat_history.pop()
    
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
# FEATURE 2: PDF Q&A CHATBOT
# ============================================

def pdf_qa_chatbot():
    """Chat with your DPE PDF documents"""
    
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
    
    if not LANGCHAIN_AVAILABLE:
        st.error("❌ AI features not available. Packages are being installed.")
        return
    
    llm = get_llm()
    
    if not llm:
        st.warning("⚠️ AI features require API key configuration.")
        st.info("Get a free API key from [OpenRouter](https://openrouter.io/keys) and add to Streamlit secrets.")
        return
    
    # Initialize session state for PDF chat
    if "pdf_chat_history" not in st.session_state:
        st.session_state.pdf_chat_history = []
    if "pdf_vectorstore" not in st.session_state:
        st.session_state.pdf_vectorstore = None
    if "pdf_processed" not in st.session_state:
        st.session_state.pdf_processed = False
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your DPE certificate (PDF)", type=["pdf"])
    
    if uploaded_file and not st.session_state.pdf_processed:
        with st.spinner("📖 Analyzing your DPE document..."):
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    tmp_path = tmp_file.name
                
                # Load PDF
                loader = PyPDFLoader(tmp_path)
                documents = loader.load()
                
                # Split text into chunks
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    separators=["\n\n", "\n", " ", ""]
                )
                chunks = text_splitter.split_documents(documents)
                
                # Get embedding API key
                try:
                    openai_key = st.secrets.get("OPENAI_API_KEY", "")
                    openrouter_key = st.secrets.get("OPENROUTER_API_KEY", "")
                except:
                    openai_key = ""
                    openrouter_key = ""
                
                # Use OpenAI embeddings if API key available
                if openai_key:
                    embeddings = OpenAIEmbeddings(
                        model="text-embedding-3-small",
                        openai_api_key=openai_key
                    )
                else:
                    # Use a free embedding model via HuggingFace
                    from langchain_community.embeddings import HuggingFaceEmbeddings
                    embeddings = HuggingFaceEmbeddings(
                        model_name="sentence-transformers/all-MiniLM-L6-v2"
                    )
                
                # Create vector store
                vectorstore = Chroma.from_documents(
                    documents=chunks,
                    embedding=embeddings,
                    persist_directory="./dpe_chroma_db"
                )
                
                st.session_state.pdf_vectorstore = vectorstore
                st.session_state.pdf_processed = True
                
                # Clean up temp file
                os.unlink(tmp_path)
                
                st.success(f"✅ Document processed! {len(chunks)} sections created. You can now ask questions.")
                
            except Exception as e:
                st.error(f"Error processing PDF: {str(e)}")
    
    if st.session_state.pdf_processed and st.session_state.pdf_vectorstore:
        st.info(f"📄 Active document ready for questions")
        
        if st.button("🔄 Clear document", use_container_width=True):
            st.session_state.pdf_processed = False
            st.session_state.pdf_vectorstore = None
            st.session_state.pdf_chat_history = []
            st.rerun()
        
        st.markdown("---")
        
        # Display chat history
        for msg in st.session_state.pdf_chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 12px;">
                    <div style="background: linear-gradient(135deg, #22c55e, #16a34a); border-radius: 18px; padding: 10px 16px; max-width: 80%;">
                        <span style="color: white;">{msg['content']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin-bottom: 12px;">
                    <div style="background: rgba(34,197,94,0.1); border: 1px solid rgba(34,197,94,0.3); border-radius: 18px; padding: 10px 16px; max-width: 80%;">
                        <span style="color: #e2e8f0;">📄 {msg['content']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Question input
        user_question = st.chat_input("Ask about your DPE document...")
        
        if user_question:
            st.session_state.pdf_chat_history.append({"role": "user", "content": user_question})
            
            with st.spinner("🔍 Searching document..."):
                try:
                    # Create QA chain
                    qa_chain = RetrievalQA.from_chain_type(
                        llm=llm,
                        retriever=st.session_state.pdf_vectorstore.as_retriever(
                            search_kwargs={"k": 4}
                        ),
                        return_source_documents=True
                    )
                    
                    result = qa_chain.invoke({"query": user_question})
                    answer = result['result']
                    
                    st.session_state.pdf_chat_history.append({"role": "assistant", "content": answer})
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.session_state.pdf_chat_history.pop()
        
        # Sample questions
        st.markdown("---")
        st.markdown("### 💡 Try asking:")
        sample_qs = [
            "What is my current DPE class?",
            "How much subsidy can I get?",
            "What renovations are recommended?",
            "What is my energy consumption?"
        ]
        
        cols = st.columns(2)
        for i, q in enumerate(sample_qs):
            with cols[i % 2]:
                if st.button(q, use_container_width=True):
                    st.session_state.pdf_chat_history.append({"role": "user", "content": q})
                    st.rerun()
    
    elif not st.session_state.pdf_processed:
        st.info("📤 Upload a DPE PDF document to start asking questions about it.")


# ============================================
# MAIN AI FEATURES PAGE
# ============================================

def ai_features_page():
    """Main page for AI features"""
    
    st.markdown("""
    <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 2.5rem; margin-bottom: 1rem;">
        🤖 ZAMI AI Features
    </h1>
    <p style="color: #94a3b8; margin-bottom: 2rem;">
        Powered by advanced AI to help you make better renovation decisions
    </p>
    """, unsafe_allow_html=True)
    
    if not LANGCHAIN_AVAILABLE:
        st.warning("⚠️ AI packages are being installed. Please wait a few minutes and refresh the page.")
        st.info("This happens only once during initial deployment.")
        return
    
    # Tab selection
    tab1, tab2 = st.tabs(["💬 AI Chat Assistant", "📄 DPE Document Analyzer"])
    
    with tab1:
        ai_chat_agent()
    
    with tab2:
        pdf_qa_chatbot()