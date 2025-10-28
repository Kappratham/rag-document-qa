# 🤖 DocsDoctor - AI-Powered Document Q&A System

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.0-green.svg)](https://langchain.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Chat with your PDF documents using AI. Upload research papers, textbooks, or reports and ask questions in natural language. Get accurate answers with source citations - all running 100% locally on your computer.

---

## 📋 Table of Contents
- [What is This?](#what-is-this)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Usage Guide](#usage-guide)
- [Troubleshooting](#troubleshooting)
- [Tech Stack](#tech-stack)
- [Examples](#examples)
- [Project Structure](#project-structure)
- [Limitations](#limitations)
- [Contributing](#contributing)

---

## 🎯 What is This?

**DocsDoctor** transforms your PDF documents into an AI-powered question-answering system using RAG (Retrieval-Augmented Generation). Instead of manually searching through hundreds of pages, simply ask questions and get instant answers with exact source citations.

### The Problem
- ❌ Spending hours reading long documents
- ❌ Using Ctrl+F which only finds exact matches
- ❌ AI chatbots that hallucinate or can't access your private files

### The Solution
- ✅ Upload any PDF document
- ✅ Ask questions in plain English
- ✅ Get accurate answers citing exact page locations
- ✅ 100% private - runs on your computer
- ✅ Zero cost - no API fees

---

## ✨ Features

- 🤖 **Local AI Model** - Powered by Llama 2 (7B quantized), runs entirely offline
- 📚 **Multiple PDFs** - Upload and search across many documents simultaneously
- 🎯 **Source Citations** - Every answer shows exact document location
- 💬 **Conversational** - Ask follow-up questions with context awareness
- 🔒 **100% Private** - Your data never leaves your computer
- 💰 **Zero Cost** - No API fees, completely free forever
- ⚡ **Fast** - 10-20 second response times
- 🎨 **Beautiful UI** - Clean Streamlit web interface

---

## 🚀 Quick Start

**TL;DR - Get it running in 5 steps:**

```bash
# 1. Clone repository
git clone https://github.com/kappratham/rag-document-qa.git
cd rag-document-qa

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install Python packages
pip install -r requirements.txt

# 4. Install Ollama and download model
# Download from: https://ollama.com/download
ollama pull llama2:7b-chat-q4_0

# 5. Run the app
streamlit run app.py


⚠️ Limitations
Current Limitations
Document Support:

✅ Text-based PDFs only
❌ Scanned PDFs (no OCR)
❌ Images/diagrams not processed
❌ Complex tables may lose formatting
Language:

✅ English (optimized)
⚠️ Other languages (may work but not tested)
Performance:

Response time: 10-20 seconds (local LLM tradeoff)
RAM requirement: 8GB minimum
Very large PDFs (1000+ pages): 3-5 min processing
Accuracy:

~90% factual accuracy (based on informal testing)
May occasionally refuse unclear questions
Context limited to retrieved chunks (not entire document)
🚀 Future Enhancements
Planned Features:

 Support for Word docs, PowerPoints
 OCR for scanned PDFs
 Export chat history
 Batch upload (drag folder)
 Advanced search filters
 Model switching (speed vs quality)
 Streaming responses
 Dark mode UI
🤝 Contributing
Contributions welcome! Please:

Fork the repository
Create a feature branch (git checkout -b feature/AmazingFeature)
Commit changes (git commit -m 'Add AmazingFeature')
Push to branch (git push origin feature/AmazingFeature)
Open a Pull Request
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Meta AI - Llama 2 open-source model
LangChain - RAG framework
Ollama - Local LLM deployment
HuggingFace - Embedding models
Streamlit - Web framework
📧 Contact
Pratham Kapure

GitHub: @kappratham
LinkedIn: linkedin.com/in/prathamkapure
Email: prathamrkapure@gmail.com
⭐ Support
If you found this helpful, please give it a star! ⭐

Built with ❤️ using LangChain, Llama 2, and Streamlit

🎓 Learning Resources
Want to understand how this works?

LangChain RAG Tutorial
Llama 2 Paper
Vector Databases Explained
Streamlit Documentation