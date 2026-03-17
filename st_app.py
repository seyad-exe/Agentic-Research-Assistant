import streamlit as st
from agno.agent import Agent
from agno.team import Team
from config import model, knowledge_base

# --- Page Config ---
st.set_page_config(
    page_title="Research Agent Team",
    page_icon="🎓",
    layout="wide"
)

# --- Title & Sidebar ---
st.title("🎓 Research Paper Assistant")
st.markdown("Ask questions about the papers stored in your **LanceDB** knowledge base.")

with st.sidebar:
    st.header("Team Roles")
    st.info("""
    - **🕵️ Searcher:** Finds relevant papers.
    - **📝 Summarizer:** Extracts equations & data.
    - **💬 Copilot:** Answers your specific questions.
    """)
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- Initialize Team (Cached) ---
# We cache the team creation so it doesn't reload on every interaction
@st.cache_resource
def get_team():

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

    return Team(
        name="ResearchPaperTeam",
        members=[search_agent, summarizer_agent, chat_agent],
        model=model,
        # This allows the team to remember the conversation context 
        instructions="""
    Coordinate the workflow:
    1. Use PaperSearcher to find relevant information in the loaded papers.
    2. Use PaperSummarizer to analyze specific technical details.
    3. Use LiteratureCopilot to synthesize the final answer for the user.
    """
    )

paper_team = get_team()

# --- Chat Logic ---

# 1. Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Display existing chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Handle user input
if prompt := st.chat_input("Ask about machine learning, equations, or specific papers..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        # Create a placeholder for the streaming response
        response_placeholder = st.empty()
        full_response = ""
        
        # Run the team with streaming enabled
        # stream=True returns a generator we can iterate over
        response_stream = paper_team.run(prompt, stream=True)
        
        try:
            for chunk in response_stream:
                # Agno streams chunks; we append them to build the full text
                # Note: Depending on the version, chunk might be a string or object.
                # If chunk is an object with .content, use chunk.content
                content = getattr(chunk, "content", str(chunk))
                if content:
                    full_response += content
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})