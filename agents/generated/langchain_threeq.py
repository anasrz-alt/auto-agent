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
def search_tool(query: str) -> str:
    """Perform a web search for the given query."""
    return searchtool_func(query)

@tool
def web_browser(url: str) -> str:
    """Browse the web page at the given URL and extract relevant information."""
    return webbrowser_func(url)

@tool
def youtube_api(video_id: str) -> str:
    """Get metadata and transcripts for the specified YouTube video."""
    return youtubeapi_func(video_id)

@tool
def wikipedia_api(query: str) -> str:
    """Fetch information from Wikipedia based on the provided query."""
    return wikipediaapi_func(query)

@tool
def text_parser(text: str) -> str:
    """Parse and format text according to specified instructions."""
    return textparser_func(text)

TOOLS = [
    search_tool,
    web_browser,
    youtube_api,
    wikipedia_api,
    text_parser
]

# ---------------------------
# 3. Create Agent
# ---------------------------

system_prompt = (
    "You are a helpful and reliable trivia agent named 'threeq'. "
    "Your task is to resolve multimedia and historical trivia queries by leveraging web searches "
    "and page browsing. You will access film synopses, YouTube video metadata/transcripts, "
    "or Wikipedia archives for precise details. Your outputs must be strictly formatted as per "
    "instructions, prioritizing verified sources from August 2023."
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
    response = agent.invoke(
        {"messages": [HumanMessage(content=query)]}
    )
    return response

# ---------------------------
# 5. Test Agent Execution
# ---------------------------

if __name__ == "__main__":
    test_query = "What are the main colors of the objects in the movie 'Inception'?"
    print(f"\n--- Running Agent: threeq (Model: {MODEL}) ---")
    print("Description: Resolving multimedia and historical trivia queries.")
    print("----\n")

    try:
        final_output = run(test_query)
        print("Final Output:\n", final_output)
    except Exception as e:
        print(f"Agent Execution Failed: {e}")