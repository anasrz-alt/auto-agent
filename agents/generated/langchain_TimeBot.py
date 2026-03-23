from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from agents.generated.tools.worldtimeapi import worldtimeapi_func
from agents.generated.tools.timezonedatabaseapi import timezonedatabaseapi_func
from agents.generated.tools.geolocationapi import geolocationapi_func
from agents.generated.tools.searchtool import searchtool_func

# ---------------------------
# 1. Model Configuration
# ---------------------------

MODEL = "openai/gpt-4o"

# ---------------------------
# 2. Tool Definitions
# ---------------------------

@tool
def worldtimeapi(city: str) -> str:
    """Get the current time in a specified city using WorldTimeAPI."""
    return worldtimeapi_func(city)

@tool
def timezonedatabase(city: str) -> str:
    """Get the timezone information for a specified city using TimezoneDatabaseAPI."""
    return timezonedatabaseapi_func(city)

@tool
def geolocation(city: str) -> str:
    """Get geolocation data for a specified city using GeolocationAPI."""
    return geolocationapi_func(city)

@tool
def search_tool(query: str) -> str:
    """Search for information related to a query using the SearchTool."""
    return searchtool_func(query)

TOOLS = [
    worldtimeapi,
    timezonedatabase,
    geolocation,
    search_tool
]

# ---------------------------
# 3. Create Agent
# ---------------------------

system_prompt = (
    "You are TimeBot, a helpful agent that provides the current time in any city around the world. "
    "You have access to the following tools: "
    "1. WorldTimeAPI - to get the current time in a specified city. "
    "2. TimezoneDatabaseAPI - to retrieve timezone information for a city. "
    "3. GeolocationAPI - to fetch geolocation data for a city. "
    "4. SearchTool - to find additional information related to cities and time. "
    "Your task is to assist users in finding the current local time based on their queries."
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
    """Run the agent with a given query."""
    response = agent.invoke(
        {"messages": [HumanMessage(content=query)]}
    )
    return response

# ---------------------------
# 5. Test Agent Execution
# ---------------------------

if __name__ == "__main__":
    print(f"\n--- Running Agent: TimeBot (Model: {MODEL}) ---")
    print("Description: An agent that tells time in any city of the world.")
    print("----\n")

    try:
        test_query = "What time is it in New York?"
        response = run(test_query)
        print("Final Output:\n", response)
    except Exception as e:
        print(f"Agent Execution Failed: {e}")