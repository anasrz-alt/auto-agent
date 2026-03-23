from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from agents.generated.tools.timezoneapi import timezoneapi_func
from agents.generated.tools.geolocationapi import geolocationapi_func
from agents.generated.tools.webbrowser import webbrowser_func

# ---------------------------
# 1. Model Configuration
# ---------------------------

MODEL = "openai/gpt-4o"

# ---------------------------
# 2. Tool Definitions
# ---------------------------

@tool
def timezoneapi_func(city: str) -> str:
    """Get the current time in a specified city using the TimeZoneAPI."""
    return timezoneapi_func(city)

@tool
def geolocationapi_func(city: str) -> str:
    """Get the geographical coordinates of a specified city using the GeolocationAPI."""
    return geolocationapi_func(city)

@tool
def webbrowser_func(url: str) -> str:
    """Open a URL in the web browser."""
    return webbrowser_func(url)

TOOLS = [
    timezoneapi_func,
    geolocationapi_func,
    webbrowser_func
]

# ---------------------------
# 3. Create Agent
# ---------------------------

system_prompt = (
    "You are TimerBot, a helpful agent that provides the current time in any city around the world. "
    "You can use the following tools: "
    "1. TimeZoneAPI to get the current time based on the city name. "
    "2. GeolocationAPI to find geographical coordinates of cities if needed. "
    "3. WebBrowser to open relevant links for further information."
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
    """Run the agent with the provided query."""
    try:
        response = agent.invoke(
            {"messages": [HumanMessage(content=query)]}
        )
        return response
    except Exception as e:
        return f"Agent Execution Failed: {e}"

# ---------------------------
# 5. Test Agent Execution
# ---------------------------

if __name__ == "__main__":
    print("--- Running Agent: TimerBot (Model: {}) ---".format(MODEL))
    print("Description: An agent that tells the current time in any city of the world.")
    print("----\n")

    test_prompt = "What time is it in New York?"
    final_output = run(test_prompt)
    print("Final Output:\n", final_output)