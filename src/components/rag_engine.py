from typing import List, Dict
from dotenv import load_dotenv
import logging

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.schema import Document

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGEngine:
    """RAG system using Ollama + HuggingFace embeddings"""
    
    def __init__(self):
        """Initialize RAG components"""
        logger.info("🚀 Initializing RAG Engine...")
        
        # Initialize embeddings
        logger.info("📥 Loading embedding model (first time takes ~1 min)...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        logger.info("✅ Embeddings loaded!")
        
        # FREE LLM via Ollama
        logger.info("🦙 Connecting to Ollama (Llama 2)...")
        self.llm = Ollama(
            model="llama2:7b-chat-q4_0",
            temperature=0.7
        )
        logger.info("✅ Ollama connected!")
        
        # Text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        self.vectorstore = None
        self.qa_chain = None
        
        logger.info("✅ RAG Engine initialized!")
    
    def process_documents(self, documents: List[Dict[str, str]]):
        """Process documents and create vector store"""
        logger.info(f"📄 Processing {len(documents)} documents...")
        
        # Convert to LangChain Document format
        langchain_docs = []
        for doc in documents:
            chunks = self.text_splitter.split_text(doc['content'])
            
            for i, chunk in enumerate(chunks):
                langchain_docs.append(
                    Document(
                        page_content=chunk,
                        metadata={
                            'source': doc['filename'],
                            'chunk': i
                        }
                    )
                )
        
        logger.info(f"   Created {len(langchain_docs)} chunks")
        
        # Create vector store with embeddings
        logger.info("🔢 Creating vector store...")
        logger.info("   (This may take 1-2 minutes...)")
        
        self.vectorstore = Chroma.from_documents(
            documents=langchain_docs,
            embedding=self.embeddings,
            persist_directory="./data/chroma_db"
        )
        
        logger.info("✅ Vector store created!")
        
        # Create QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 3}
            ),
            return_source_documents=True
        )
        
        logger.info("✅ Documents indexed!")
    
    def ask(self, question: str) -> Dict:
        """Ask a question about the documents"""
        if not self.qa_chain:
            raise ValueError("❌ No documents loaded!")
        
        logger.info(f"❓ Question: {question}")
        logger.info("   ⏳ Generating answer (10-30 seconds)...")
        
        result = self.qa_chain({"query": question})
        
        answer = result['result']
        sources = result['source_documents']
        
        logger.info(f"✅ Answer generated!")
        
        return {
            'answer': answer,
            'sources': [
                {
                    'filename': doc.metadata['source'],
                    'chunk': doc.metadata['chunk'],
                    'content': doc.page_content[:200] + "..."
                }
                for doc in sources
            ]

        }
