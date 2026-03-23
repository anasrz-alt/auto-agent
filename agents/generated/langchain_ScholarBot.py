from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from agents.generated.tools.searchtool import searchtool_func
from agents.generated.tools.webbrowser import webbrowser_func
from agents.generated.tools.databasequerytool import databasequerytool_func
from agents.generated.tools.apiclient import apiclient_func

# ---------------------------
# 1. Model Configuration
# ---------------------------

MODEL = "openai/gpt-4o"

# ---------------------------
# 2. Tool Definitions
# ---------------------------

@tool
def searchtool(name: str) -> str:
    """Search for the number of publications for a given professor's name and university."""
    return searchtool_func(name)

@tool
def webbrowser(name: str) -> str:
    """Use the web browser to find the number of publications for a given professor's name and university."""
    return webbrowser_func(name)

@tool
def databasequerytool(name: str) -> str:
    """Query the database for the number of publications for a given professor's name and university."""
    return databasequerytool_func(name)

@tool
def apiclient(name: str) -> str:
    """Use the API client to fetch the number of publications for a given professor's name and university."""
    return apiclient_func(name)

TOOLS = [
    searchtool,
    webbrowser,
    databasequerytool,
    apiclient
]

# ---------------------------
# 3. Create Agent
# ---------------------------

system_prompt = (
    "You are ScholarBot, an AI agent designed to assist users in retrieving the number of publications "
    "for a specified professor and their associated university. You can utilize various tools to gather "
    "this information, including searching the web, querying databases, and using API clients. "
    "Please provide clear and concise answers based on the information you retrieve."
)

agent = create_agent(
    model=MODEL,
    tools=TOOLS,
    system_prompt=system_prompt
)

# ---------------------------
# 4. Entry Point Function
# ---------------------------

def run(query: str) -> str:
    """Run the ScholarBot agent with the provided query."""
    response = agent.invoke(
        {"messages": [HumanMessage(content=query)]}
    )
    return response

# ---------------------------
# 5. Test Agent Execution
# ---------------------------

if __name__ == "__main__":
    print(f"\n--- Running Agent: ScholarBot (Model: {MODEL}) ---")
    print("Description: An AI agent to extract the number of publications for a professor.")
    print("----\n")

    test_query = "How many publications does Professor John Doe from Harvard University have?"
    try:
        final_output = run(test_query)
        print("Final Output:\n", final_output)
    except Exception as e:
        print(f"Agent Execution Failed: {e}")