from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from agents.generated.tools.weatherapi import weatherapi_func
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
def weatherapi(city: str) -> str:
    """Fetch weather information for a specified city using WeatherAPI."""
    return weatherapi_func(city)

@tool
def searchtool(query: str) -> str:
    """Search for information online using the SearchTool."""
    return searchtool_func(query)

@tool
def webbrowser(url: str) -> str:
    """Open a webpage using the WebBrowser tool."""
    return webbrowser_func(url)

TOOLS = [
    weatherapi,
    searchtool,
    webbrowser
]

# ---------------------------
# 3. Create Agent
# ---------------------------

system_prompt = (
    "You are WeatherBot, an AI agent designed to fetch weather information for any city. "
    "You can use the WeatherAPI to get accurate weather data, the SearchTool to find additional "
    "information if needed, and the WebBrowser to access web pages for more details. "
    "Please provide clear and concise weather reports based on user queries."
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
        return response['content']
    except Exception as e:
        return f"Agent Execution Failed: {e}"

# ---------------------------
# 5. Test Agent Execution
# ---------------------------

if __name__ == "__main__":
    print("--- Running WeatherBot (Model: {}) ---".format(MODEL))
    print("Description: A helpful agent to provide weather information.")
    print("----\n")

    test_query = "What is the weather like in New York City?"
    output = run(test_query)
    print("Final Output:\n", output)