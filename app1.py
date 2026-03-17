from agno.agent import Agent
from agno.models.google import Gemini
from fastapi import FastAPI
from pydantic import BaseModel

# Your working Gemini model
model = Gemini(id="gemini-2.5-flash")

# Research copilot - only valid parameters
research_copilot = Agent(
    name="ResearchPaperCopilot",
    model=model,
    instructions="""
    You are a research paper workflow assistant. Capabilities:
    
    1. SEARCH: Find recent arXiv papers (2024-2026) on ML/AI topics
       Use URLs like arxiv.org/abs/2501.xxxxx for NeurIPS/ICML/ICLR
    2. SUMMARIZE: Structure as ## Title ## Abstract ## Methods ## Results
    3. EXTRACTION: Key equations (LaTeX), datasets, baselines, contributions  
    4. COMPARE: Analyze multiple papers/datasets/baselines
    
    Always format in clean markdown with citations.
    """,
    markdown=True  # Only confirmed parameter
)

# FastAPI UI
app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/chat")
async def chat(query: Query):
    response = await research_copilot.arun(query.question)
    return {"response": response.content if response else "No response"}

if __name__ == "__main__":
    print("🚀 Research Paper Copilot - Ready!")
    print("🌐 FastAPI UI: http://localhost:8000/docs") 
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
