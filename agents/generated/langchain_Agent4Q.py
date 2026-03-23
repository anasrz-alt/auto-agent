from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# ---------------------------
# 1. Model Configuration
# ---------------------------

MODEL = "gpt-4o"

# ---------------------------
# 2. Tool Definitions
# ---------------------------

@tool
def videoanalysistool_func(video_url: str) -> str:
    """Analyze video for frame data."""
    return videoanalysistool_func(video_url)

@tool
def subtitleextractor_func(video_url: str) -> str:
    """Extract subtitles from video."""
    return subtitleextractor_func(video_url)

@tool
def imagerecognitionapi_func(image_data: str) -> str:
    """Recognize objects in images."""
    return imagerecognitionapi_func(image_data)

@tool
def websearchtool_func(query: str) -> str:
    """Perform a web search for contextual information."""
    return websearchtool_func(query)

@tool
def dataformatter_func(data: List[str]) -> str:
    """Format data into a string."""
    return dataformatter_func(data)

TOOLS = [
    videoanalysistool_func,
    subtitleextractor_func,
    imagerecognitionapi_func,
    websearchtool_func,
    dataformatter_func
]

# ---------------------------
# 3. Create Agent
# ---------------------------

agent = create_agent(
    model=MODEL,
    tools=TOOLS,
    system_prompt="You are Agent4Q, an AI agent that analyzes video data and retrieves contextual information."
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
    print("--- Running Agent: Agent4Q (Model: openai/gpt-4o) ---")
    test_query = "Analyze the video at this URL for maximum simultaneous species and extract relevant subtitles."
    result = run(test_query)
    print("Final Output:\n", result)