"""
DocsDoctor - RAG-Powered Document Q&A System
Streamlit Web Interface with Fixed Text Colors
"""

import streamlit as st
import os
from pathlib import Path
from src.utils.pdf_loader import load_multiple_pdfs
from src.components.rag_engine import RAGEngine

# Page config
st.set_page_config(
    page_title="DocsDoctor - AI Document Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with FIXED COLORS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextInput > div > div > input {
        font-size: 16px;
        color: #000000 !important;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
    }
    .user-message strong {
        color: #1565c0;
        font-size: 16px;
    }
    .user-message span {
        color: #000000 !important;
        font-size: 16px;
    }
    .assistant-message {
        background-color: #f1f8e9;
        border-left: 5px solid #4caf50;
    }
    .assistant-message strong {
        color: #2e7d32;
        font-size: 16px;
    }
    .assistant-message span {
        color: #000000 !important;
        font-size: 16px;
        white-space: pre-wrap;
        line-height: 1.6;
    }
    .source-box {
        background-color: #fff3cd;
        border-left: 3px solid #ffc107;
        padding: 1rem;
        margin-top: 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.9rem;
    }
    .source-box strong {
        color: #f57c00;
    }
    .source-box em {
        color: #424242;
        display: block;
        margin-top: 0.5rem;
    }
    /* Force dark text everywhere */
    p, span, div, li {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("📚 DocsDoctor - AI Document Assistant")
st.markdown("**Upload PDFs and ask questions. Powered by local Llama 2 + RAG**")

# Sidebar for file upload
st.sidebar.header("📁 Upload Documents")
st.sidebar.markdown("**Upload PDF files to chat with them!**")

uploaded_files = st.sidebar.file_uploader(
    "Choose PDF files",
    type=['pdf'],
    accept_multiple_files=True,
    help="Upload one or more PDF documents"
)

# Initialize session state
if 'rag_engine' not in st.session_state:
    st.session_state.rag_engine = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'documents_processed' not in st.session_state:
    st.session_state.documents_processed = False

# Process uploaded files
if uploaded_files and not st.session_state.documents_processed:
    with st.spinner("🔄 Processing documents... This may take 1-2 minutes..."):
        # Save uploaded files temporarily
        temp_dir = Path("data/temp")
        temp_dir.mkdir(exist_ok=True, parents=True)
        
        file_paths = []
        for uploaded_file in uploaded_files:
            file_path = temp_dir / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            file_paths.append(str(file_path))
        
        # Load and process documents
        try:
            documents = load_multiple_pdfs(file_paths)
            
            # Initialize RAG engine
            st.session_state.rag_engine = RAGEngine()
            st.session_state.rag_engine.process_documents(documents)
            
            st.session_state.documents_processed = True
            st.sidebar.success(f"✅ Processed {len(documents)} documents!")
            
        except Exception as e:
            st.sidebar.error(f"❌ Error processing documents: {e}")

# Show uploaded documents
if uploaded_files:
    st.sidebar.markdown("### 📄 Loaded Documents:")
    for file in uploaded_files:
        st.sidebar.markdown(f"**• {file.name}**")

# Main chat interface
if st.session_state.documents_processed:
    st.markdown("### 💬 Chat with Your Documents")
    
    # Display chat history with FIXED COLORS
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 You:</strong><br>
                    <span style="color: #000000 !important; font-size: 16px;">{message['content']}</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 AI Assistant:</strong><br>
                    <span style="color: #000000 !important; font-size: 16px; white-space: pre-wrap; line-height: 1.6;">{message['content']}</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Show sources if available
            if 'sources' in message:
                with st.expander("📚 View Sources", expanded=False):
                    for i, source in enumerate(message['sources'], 1):
                        st.markdown(f"""
                            <div class="source-box">
                                <strong style="color: #f57c00;">Source {i}:</strong> 
                                <span style="color: #000000 !important;">{source['filename']} (chunk {source['chunk']})</span><br>
                                <em style="color: #424242 !important;">{source['content']}</em>
                            </div>
                        """, unsafe_allow_html=True)
    
    # Question input
    st.markdown("---")
    question = st.text_input(
        "**Ask a question about your documents:**",
        placeholder="e.g., What is this document about?",
        key="question_input"
    )
    
    col1, col2 = st.columns([1, 5])
    
    with col1:
        ask_button = st.button("🚀 Ask", type="primary", use_container_width=True)
    
    with col2:
        clear_button = st.button("🗑️ Clear Chat", use_container_width=True)
    
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()
    
    # Process question
    if ask_button and question:
        # Add user message to chat
        st.session_state.chat_history.append({
            'role': 'user',
            'content': question
        })
        
        # Get answer from RAG
        with st.spinner("🤔 Thinking... (this may take 10-20 seconds)"):
            try:
                result = st.session_state.rag_engine.ask(question)
                
                # Add assistant message to chat
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': result['answer'],
                    'sources': result['sources']
                })
                
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    # Example questions
    st.markdown("---")
    with st.expander("💡 Example Questions You Can Ask"):
        st.markdown("""
        **About Content:**
        - What is this document about?
        - Summarize the key findings
        - What are the main contributions?
        
        **Specific Information:**
        - What methodology was used?
        - What are the results?
        - What are the conclusions?
        
        **Analysis:**
        - What are the limitations?
        - What future work is suggested?
        - How does this compare to previous work?
        """)

else:
    # Instructions when no documents loaded
    st.info("👈 **Upload PDF documents in the sidebar to get started!**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📖 How to use:
        1. **Upload PDFs** using the sidebar file uploader
        2. **Wait** for processing (1-2 minutes first time)
        3. **Ask questions** about your documents in plain English
        4. **Get answers** with source citations showing exact locations!
        5. **Ask follow-ups** for deeper understanding
        """)
    
    with col2:
        st.markdown("""
        ### ✨ Features:
        - 🤖 **Powered by Llama 2** (local AI model)
        - 🔒 **100% private** (runs entirely on your computer)
        - 📚 **Multiple documents** (upload as many as you want)
        - 🎯 **Source citations** for every answer
        - 💬 **Conversational** interface with chat history
        - ⚡ **Fast responses** (10-20 seconds per answer)
        """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 🎯 What Can You Do With This?
    
    **For Students:**
    - 📄 Upload textbooks and ask study questions
    - 📚 Research papers: get quick summaries and insights
    - 📝 Notes: make them searchable and interactive
    
    **For Professionals:**
    - 📊 Reports: extract key information quickly
    - 📋 Documentation: instant answers without scrolling
    - 📑 Contracts: find specific clauses and terms
    
    **For Researchers:**
    - 🔬 Literature review: query across multiple papers
    - 📈 Compare findings from different sources
    - 🎓 Citation tracking: see exact source locations
    """)

# Footer in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("""
    ### ⚙️ System Info
    - **LLM Model:** Llama 2 (7B-Q4)
    - **Embeddings:** MiniLM-L6-v2
    - **Vector DB:** ChromaDB
    - **Framework:** LangChain
    - **Cost:** $0 (100% free!)
    - **Privacy:** 100% local
    
    ---
    
    <div style='text-align: center'>
        <p style='font-size: 0.9rem; color: #666;'>
            Built with 🤖 LangChain + Llama 2<br>
            <strong>100% Free & Private</strong>
        </p>
    </div>
""", unsafe_allow_html=True)