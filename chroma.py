import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# 1. Load your API Key from .env
load_dotenv()

def ingest_curriculum():
    # Configuration
    DATA_SOURCE = "resources"
    CHROMA_PATH = "chroma_db"
    
    print("--- 📂 Phase 1: Loading Digital Textbooks ---")
    
    documents = []
    
    # Check if the folder exists
    if not os.path.exists(DATA_SOURCE):
        os.makedirs(DATA_SOURCE)
        print(f"Created '{DATA_SOURCE}' folder. Place your digital PDFs here.")
        return

    # Loop through the digital PDFs you created
    for file in os.listdir(DATA_SOURCE):
        if file.endswith(".pdf"):
            path = os.path.join(DATA_SOURCE, file)
            print(f"📖 Reading: {file}...")
            
            try:
                # PyMuPDF is very fast for digital PDFs
                loader = PyMuPDFLoader(path)
                data = loader.load()
                
                # Add metadata so the AI knows which book it's reading
                for page in data:
                    page.metadata["source"] = file
                
                documents.extend(data)
            except Exception as e:
                print(f"❌ Error loading {file}: {e}")

    if not documents:
        print("🛑 No documents found. Please add digital PDFs to the 'resources' folder.")
        return

    print(f"✅ Loaded {len(documents)} pages.")

    # 2. Splitting the text into manageable chunks
    print("\n--- ✂️ Phase 2: Splitting Text into Chunks ---")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150, # Overlap keeps context between chunks
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Created {len(chunks)} text chunks.")

    # 3. Generating Embeddings and Saving to Database
    print("\n--- 🧠 Phase 3: Building the Vector Database ---")
    try:
        # This will create the 'chroma_db' folder automatically
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=OpenAIEmbeddings(),
            persist_directory=CHROMA_PATH
        )
        print(f"🎉 SUCCESS: {len(chunks)} chunks stored in '{CHROMA_PATH}'.")
        print("EduMate AI is now ready to answer questions!")
        
    except Exception as e:
        print(f"❌ ChromaDB Error: {e}")

if __name__ == "__main__":
    ingest_curriculum()