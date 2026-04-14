EduMate: AI-Powered Syllabus Assistant
EduMate is a specialized RAG (Retrieval-Augmented Generation) system built to provide accurate, syllabus-aligned educational support for Sri Lankan GCE O/L and A/L students.

🌟 Key Features (Current Demo)
Local RAG Architecture: Utilizes LangChain and ChromaDB to ground AI responses exclusively in official National Institute of Education (NIE) textbooks, eliminating LLM hallucinations.

Advanced OCR Pipeline: A custom ingestion engine using PyMuPDF and Tesseract OCR to transform low-resolution, scanned local PDFs into high-dimensional vector embeddings.

Contextual Embedding Strategy: Employs OpenAI text-embedding-3-small models with a recursive character splitting strategy (1000 chunk size, 150 overlap) to preserve scientific context.

Bilingual Support: Specifically tuned to handle the transition between Sinhala/Tamil mediums and English by providing dual-language technical terminology.

🛠️ Tech Stack
Language: Python 3.10+

Framework: FastAPI

LLM Orchestration: LangChain

Vector Database: ChromaDB

OCR Engines: Tesseract, PyMuPDF (fitz)

Frontend: Jinja2 Templates, HTML5/CSS3

🚀 Future Roadmap & Feature Improvements
To scale EduMate into a nationwide tool, the following features are in active development:

Multimodal Diagram Analysis: Integrating Vision Transformers (ViT) or GPT-4o-vision to interpret biological diagrams, circuit maps, and chemical structures directly from textbooks.

National Exam Logic: Fine-tuning the retriever to include 10+ years of Department of Examinations past papers and official marking schemes for automated scoring and guidance.

Voice-Interactive Learning: Implementing OpenAI Whisper for speech-to-text queries, allowing students to interact with the tutor hands-free.

Offline Edge Deployment: Researching the use of Ollama or LlamaCpp to run the entire system offline on low-spec hardware, ensuring accessibility in rural areas with limited internet.

Teacher Analytics: A dashboard for educators to visualize "Knowledge Gaps" based on the most frequent student queries.


Install OCR Engines: Install Tesseract OCR and Poppler.

Environment Variables: Create a .env file with your OPENAI_API_KEY.

Data Ingestion: Place PDFs in /resources and run python chroma.py.

Launch: Run fastapi dev to start the local server.
