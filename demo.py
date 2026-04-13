import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 1. Load your API Key
load_dotenv()

def test_edumate_answer():
    # Initialize the LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    
    # Sample English Context (usually this comes from your ChromaDB)
    context = "Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods with the help of chlorophyll."
    question = "What is photosynthesis?"

    # 2. Multilingual Prompt Engineering
    # We ask the AI to answer in English AND then translate to Tamil
    prompt = f"""
    You are an expert Science tutor for Sri Lankan students.
    Using the context: {context}
    
    INSTRUCTIONS:
    1. Answer the question clearly in English.
    2. Provide the exact same answer translated into Tamil.
    3. IMPORTANT: Use simple, easy-to-understand language suitable for a 15-year-old (GCE O/L student). 
       Avoid overly complex scientific jargon unless it is necessary for the syllabus.
    
    Question: {question}
    """

    print("--- Requesting Answer from OpenAI ---")
    response = llm.invoke(prompt)
    
    print("\n--- EduMate Response ---")
    print(response.content)

if __name__ == "__main__":
    test_edumate_answer()