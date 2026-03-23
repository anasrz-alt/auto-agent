from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from agents.generated.tools.searchtool import searchtool_func
from agents.generated.tools.webbrowser import webbrowser_func
from agents.generated.tools.youtubeapi import youtubeapi_func
from agents.generated.tools.wikipediaapi import wikipediaapi_func
from agents.generated.tools.textparser import textparser_func

# ---------------------------
# 1. Model Configuration
# ---------------------------

MODEL = "openai/gpt-4o"


# ---------------------------
# 2. Tool Definitions
# ---------------------------

@tool
def SearchTool(query: str) -> str:
    """Perform a web search for the given query."""
    return searchtool_func(query)

@tool
def WebBrowser(url: str) -> str:
    """Browse the specified web page and return its content."""
    return webbrowser_func(url)

@tool
def YouTubeAPI(video_id: str) -> str:
    """Fetch metadata and transcripts for the specified YouTube video."""
    return youtubeapi_func(video_id)

@tool
def WikipediaAPI(query: str) -> str:
    """Retrieve information from Wikipedia for the given query."""
    return wikipediaapi_func(query)

@tool
def TextParser(text: str) -> str:
    """Parse the provided text for structured information."""
    return textparser_func(text)

TOOLS = [
    SearchTool,
    WebBrowser,
    YouTubeAPI,
    WikipediaAPI,
    TextParser
]


# ---------------------------
# 3. Create Agent
# ---------------------------

agent = create_agent(
    model=MODEL,
    tools=TOOLS,
    system_prompt="You are Agent3Q, a helpful assistant for resolving multimedia and historical trivia queries."
)


# ---------------------------
# 4. Entry Point Function
# ---------------------------

def run(query: str) -> str:
    response = agent.invoke(
        {"messages": [HumanMessage(content=query)]}
    )
    return response


# ---------------------------
# 5. Test Agent Execution
# ---------------------------

if __name__ == "__main__":
    print(f"\n--- Running Agent: Agent3Q (Model: {MODEL}) ---")
    print("Description: Resolving multimedia and historical trivia queries.")
    print("----\n")

    test_query = "What colors are associated with the main characters in the movie 'The Grand Budapest Hotel'?"
    try:
        final_output = run(test_query)
        print("Final Output:\n", final_output)
    except Exception as e:
        print(f"Agent Execution Failed: {e}")