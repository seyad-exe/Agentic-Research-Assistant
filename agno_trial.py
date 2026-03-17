from agno.agent import Agent
from agno.models.google import Gemini

# Create a minimal agent with Gemini (no DB, no tools)
agent = Agent(
    model=Gemini(id="gemini-2.5-flash"),
    markdown=True
)

# Pass a query and print the result
query = "5 facts about the Sun"
agent.print_response(query)
