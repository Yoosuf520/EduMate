import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

app = FastAPI()

# 2. Enable CORS (Prevents browser blocks when calling the API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Mount Templates (for CSS/JS access)
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
templates = Jinja2Templates(directory="templates")

# 4. Initialize Vector DB
# Ensure you have run chroma.py first to create the ./chroma_db folder
embeddings = OpenAIEmbeddings()
vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# 5. Updated Data Model to include 'lang'
class Query(BaseModel):
    text: str
    lang: str

@app.get("/")
async def read_root(request: Request):
    # Explicitly use context= to avoid the hashing error
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={} 
    )
@app.post("/ask")
async def ask_edu_mate(query: Query):
    # A. Search for relevant Science context from your PDFs
    docs = vector_db.similarity_search(query.text, k=3)
    context = "\n".join([d.page_content for d in docs])

    # B. Call OpenAI with specialized Multilingual Instructions
    llm = ChatOpenAI(model="gpt-4o", temperature=0.3)
    
    system_instruction = f"""
You are EduMate AI, an expert Science tutor for Sri Lankan O/L and A/L students.

TASK:
1. Use the provided context: {context}
2. Answer accurately based on the Sri Lankan syllabus.
3. The student wants the answer in: {query.lang}.

STYLE RULES:
- Use simple, clear language suitable for a 15-year-old student.
- If the language is Tamil or Sinhala, provide the explanation in that language, 
  but ALWAYS include the English scientific terms in brackets [like this].
  Example: "ஒளிச்சேர்க்கை [Photosynthesis] என்பது..."
"""
    response = llm.invoke([
        ("system", system_instruction),
        ("human", query.text)
    ])

    return {"answer": response.content}