# app.py
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from agno.agent import Agent
from agno.team import Team

# Import shared config
from config import model, knowledge_base
# --- Agents ---

# Agent A: Search & Retrieval Specialist
# Uses the knowledge base to find relevant context
search_agent = Agent(
    name="PaperSearcher",
    model=model,
    knowledge=knowledge_base,
    search_knowledge=True, # Enable searching the vector DB
    instructions="""
    You are a researcher. Search the knowledge base for relevant papers.
    When asked about a topic, identify the most relevant papers from the database
    and list their titles and publication years.
    """,
    markdown=True
)

# Agent B: Summarizer
summarizer_agent = Agent(
    name="PaperSummarizer",
    model=model,
    knowledge=knowledge_base,
    instructions="""
    You are a technical summarizer. When given paper content or context:
    1. Extract key equations (use LaTeX format).
    2. Identify datasets used.
    3. Note baselines and performance metrics.
    4. Summarize main contributions.
    """,
    markdown=True
)

# Agent C: Literature Review Copilot
chat_agent = Agent(
    name="LiteratureCopilot", 
    model=model,
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions="Answer questions about the literature review using ONLY stored papers. Cite paper titles explicitly.",
    markdown=True
)

# --- Team ---
paper_team = Team(
    name="ResearchPaperTeam",
    members=[search_agent, summarizer_agent, chat_agent],
    instructions="""
    Coordinate the workflow:
    1. Use PaperSearcher to find relevant information in the loaded papers.
    2. Use PaperSummarizer to analyze specific technical details.
    3. Use LiteratureCopilot to synthesize the final answer for the user.
    """,
    model=model
)

# --- FastAPI App ---
app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/chat")
async def chat(query: Query):
    run_response = paper_team.run(query.question, stream=False)
    return {"response": run_response.content}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)