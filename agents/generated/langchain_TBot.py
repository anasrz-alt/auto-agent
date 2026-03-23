from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from agents.generated.tools.timezoneapi import timezoneapi_func
from agents.generated.tools.searchtool import searchtool_func
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
    """Check the current time in a specified city using the TimeZoneAPI."""
    return timezoneapi_func(city)

@tool
def searchtool_func(query: str) -> str:
    """Search for information related to the query."""
    return searchtool_func(query)

@tool
def webbrowser_func(url: str) -> str:
    """Open a URL in a web browser."""
    return webbrowser_func(url)

TOOLS = [
    timezoneapi_func,
    searchtool_func,
    webbrowser_func
]

# ---------------------------
# 3. Create Agent
# ---------------------------

system_prompt = (
    "You are TBot, a helpful agent designed to check the current time in cities around the world. "
    "You can utilize the following tools: "
    "1. TimeZoneAPI - to get the current time in a specified city. "
    "2. SearchTool - to find additional information if needed. "
    "3. WebBrowser - to open relevant URLs for further exploration."
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
    print("--- Running Agent: TBot (Model: {}) ---".format(MODEL))
    print("Description: A helpful agent to check time in cities worldwide.")
    print("----\n")

    test_query = "What is the current time in Tokyo?"
    result = run(test_query)
    print("Final Output:\n", result)