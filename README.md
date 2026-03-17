# 🎓 AI Research Paper Copilot

An intelligent AI assistant built with Agno (https://github.com/agno-agi/agno) that downloads, reads, and helps you chat with academic papers from arXiv. Instead of manually reading through dozens of PDFs, you can use this copilot to instantly extract key equations, datasets, baselines, and main contributions using Retrieval-Augmented Generation (RAG).

## ✨ Features

- Automated Ingestion: Fetch and parse the latest research papers directly from arXiv based on your specific topics.
- Local Vector Database: Uses LanceDB to store document embeddings locally, ensuring fast retrieval without recurring database costs.
- Single Super-Agent Architecture: Powered by Google's gemini-2.5-flash, the agent is optimized to search the knowledge base and synthesize answers in a single, rate-limit-friendly pass.
- Technical Extraction: Specifically prompted to format mathematical equations in LaTeX and clearly cite paper titles.
- Streamlit Chat UI: A clean, conversational, and streaming web interface to interact with your personal research library.

## 🛠️ Tech Stack

- Framework: Agno (https://github.com/agno-agi/agno) (Agentic Workflow & RAG)
- LLM & Embeddings: Google Gemini (gemini-2.5-flash) & GeminiEmbedder
- Vector Database: LanceDB (Local)
- Knowledge Reader: ArxivReader
- Frontend: Streamlit
- Backend API (Optional): FastAPI & Uvicorn

## 📂 Project Structure

├── config.py            # Shared setup for LLM, Embedder, and LanceDB
├── ingest.py            # Script to download papers from arXiv and embed them
├── streamlit_app.py     # Main Streamlit Chat UI with the Research Super-Agent
├── app.py               # (Optional) FastAPI server for API-based interaction
├── paper_db/            # Auto-generated local LanceDB storage (created on run)
└── README.md            # Project documentation

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.9+
- A Google Gemini API Key (from Google AI Studio)

### 2. Installation

Clone the repository and set up a virtual environment:

git clone https://github.com/yourusername/research-copilot.git  
cd research-copilot  
python -m venv venv  

# Activate the virtual environment  
# On Windows:  
venv\Scripts\activate  

# On Mac/Linux:  
source venv/bin/activate  

Install the required dependencies:

pip install agno streamlit lancedb fastapi uvicorn pydantic  

### 3. Environment Variables

Set your Google API key as an environment variable.

On Windows (PowerShell):

$env:GOOGLE_API_KEY="your_api_key_here"

On Mac/Linux:

export GOOGLE_API_KEY="your_api_key_here"

## 🧠 Usage Workflow

### Step 1: Ingest Data

Before chatting, populate your local database with papers. Open ingest.py and modify the topics list (e.g., ["Large Language Models", "Quantum Computing"]). Then run:

python ingest.py

Note: You can run this script anytime to append new papers.

### Step 2: Chat with the Copilot

Start the Streamlit UI:

streamlit run streamlit_app.py

This opens a browser where you can ask:

- "What are the main contributions of the papers on Generative AI?"
- "Show me the key equations used in the provided papers."
- "What datasets were used for training in the Machine Learning papers?"

(Optional) Run the FastAPI backend:

python app.py

## ⚠️ Notes on Rate Limits

This project uses a Single Agent architecture in streamlit_app.py designed to minimize API calls and avoid free-tier rate limits from LLM providers, making it efficient for continuous chatting.
