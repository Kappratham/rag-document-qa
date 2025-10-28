from src.utils.pdf_loader import load_multiple_pdfs
from src.components.rag_engine import RAGEngine


def main():
    print("="*60)
    print("🆓 FREE RAG SYSTEM TEST (Ollama + Llama 2)")
    print("="*60)
    
    # 1. Load PDF
    print("\n📄 Step 1: Loading PDF...")
    documents = load_multiple_pdfs(['data/test_paper.pdf'])
    
    if not documents:
        print("❌ No documents loaded!")
        print("💡 Make sure you have a PDF in data/ folder")
        print("   Download one from: https://arxiv.org/abs/1706.03762")
        return
    
    # 2. Initialize RAG
    print("\n🔧 Step 2: Initializing FREE RAG Engine...")
    rag = RAGEngine()
    
    # 3. Process documents
    print("\n⚙️  Step 3: Processing documents...")
    print("   (First time: ~1-2 min for embeddings)")
    rag.process_documents(documents)
    
    # 4. Ask questions
    print("\n" + "="*60)
    print("💬 QUESTION & ANSWER")
    print("="*60)
    
    questions = [
        "What is this paper about?",
        "What are the main findings?",
    ]
    
    for question in questions:
        print(f"\n❓ Q: {question}")
        result = rag.ask(question)
        print(f"✅ A: {result['answer']}")
        print(f"\n📚 Sources:")
        for source in result['sources']:
            print(f"   - {source['filename']} (chunk {source['chunk']})")
    
    # 5. Interactive mode
    print("\n" + "="*60)
    print("🎮 INTERACTIVE MODE")
    print("="*60)
    print("Type your questions (or 'quit' to exit)")
    print("⚠️  Note: Answers take 5-15 seconds with Ollama\n")
    
    while True:
        question = input("❓ Your question: ")
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not question.strip():
            continue
        
        try:
            result = rag.ask(question)
            print(f"\n✅ Answer:\n{result['answer']}\n")
            print(f"📚 Sources: {', '.join([s['filename'] for s in result['sources']])}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    main()