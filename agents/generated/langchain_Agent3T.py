from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# ---------------------------
# 1. Model Configuration
# ---------------------------

MODEL = "openai/gpt-4o"

# ---------------------------
# 2. Tool Definitions
# ---------------------------

@tool
def imagerecognitiontool_func(image_path: str) -> str:
    """Identify objects, patterns, or text in the image."""
    return imagerecognitiontool_func(image_path)

@tool
def ocrtool_func(image_path: str) -> str:
    """Extract text from images or documents using OCR."""
    return ocrtool_func(image_path)

@tool
def webbrowser_func(url: str) -> str:
    """Browse the web to gather real-time information."""
    return webbrowser_func(url)

@tool
def searchengine_func(query: str) -> str:
    """Perform a search query to find relevant online information."""
    return searchengine_func(query)

@tool
def dataanalysistool_func(data: List[str]) -> str:
    """Analyze data for patterns and insights."""
    return dataanalysistool_func(data)

@tool
def automatedtaggingtool_func(content: str) -> List[str]:
    """Automatically tag content based on its analysis."""
    return automatedtaggingtool_func(content)

TOOLS = [
    imagerecognitiontool_func,
    ocrtool_func,
    webbrowser_func,
    searchengine_func,
    dataanalysistool_func,
    automatedtaggingtool_func
]

# ---------------------------
# 3. Create Agent
# ---------------------------

agent = create_agent(
    model=MODEL,
    tools=TOOLS,
    system_prompt="You are Agent3T, a VisionSearch Agent that autonomously performs tasks using image recognition, OCR, and web browsing."
)

# ---------------------------
# 4. Entry Point Function
# ---------------------------

def run(query: str) -> str:
    print(f"Running Agent3T with query: {query}")
    response = agent.invoke(
        {"messages": [HumanMessage(content=query)]}
    )
    return response

# ---------------------------
# 5. Test Agent Execution
# ---------------------------

if __name__ == "__main__":
    test_query = "Analyze this image and extract any text from it."
    final_output = run(test_query)
    print("Final Output:\n", final_output)