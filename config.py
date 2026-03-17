# config.py
from agno.models.google import Gemini
from agno.vectordb.lancedb import LanceDb
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.knowledge import Knowledge

# 1. Setup Model & Embedder
model = Gemini(id="gemini-2.5-flash")
embedder = GeminiEmbedder()

# 2. Setup Vector DB
# Both scripts must point to this same URI
db_uri = "./paper_db"
vector_db = LanceDb(
    uri=db_uri,
    table_name="research_papers",
    embedder=embedder
)

# 3. Setup Knowledge Base
knowledge_base = Knowledge(
    vector_db=vector_db
)