from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from agents.generated.tools.imagerecognitiontool import imagerecognitiontool_func
from agents.generated.tools.ocrtool import ocrtool_func
from agents.generated.tools.webbrowser import webbrowser_func
from agents.generated.tools.searchengine import searchengine_func
from agents.generated.tools.dataanalysistool import dataanalysistool_func
from agents.generated.tools.automatedtaggingtool import automatedtaggingtool_func

# ---------------------------
# 1. Model Configuration
# ---------------------------

MODEL = "openai/gpt-4o"

# ---------------------------
# 2. Tool Definitions
# ---------------------------

@tool
def ImageRecognitionTool(image_path: str) -> str:
    """Identify objects, patterns, or text in the provided image."""
    return imagerecognitiontool_func(image_path)

@tool
def OCRTool(image_path: str) -> str:
    """Extract text from the provided image or document."""
    return ocrtool_func(image_path)

@tool
def WebBrowser(query: str) -> str:
    """Browse the web to gather real-time information based on the query."""
    return webbrowser_func(query)

@tool
def SearchEngine(query: str) -> str:
    """Perform a search to find relevant information online."""
    return searchengine_func(query)

@tool
def DataAnalysisTool(data: str) -> str:
    """Analyze the provided data for insights and patterns."""
    return dataanalysistool_func(data)

@tool
def AutomatedTaggingTool(content: str) -> str:
    """Automatically tag the content based on its analysis."""
    return automatedtaggingtool_func(content)

TOOLS = [
    ImageRecognitionTool,
    OCRTool,
    WebBrowser,
    SearchEngine,
    DataAnalysisTool,
    AutomatedTaggingTool
]

# ---------------------------
# 3. Create Agent
# ---------------------------

system_prompt = (
    "You are a VisionSearch Agent named 'threet'. Your purpose is to autonomously perform tasks "
    "by processing diverse data using image recognition tools to identify objects, patterns, or text. "
    "You can extract text from images or documents using OCR, and gather real-time online information "
    "through search engines and web browsers. Your capabilities include visual search, automated tagging, "
    "content analysis, and comprehensive research with accurate results. You have access to the following tools: "
    "ImageRecognitionTool, OCRTool, WebBrowser, SearchEngine, DataAnalysisTool, AutomatedTaggingTool."
)

agent = create_agent(
    model=MODEL,
    tools=TOOLS,
    system_prompt=system_prompt
)

# ---------------------------
# 4. Test Agent Execution
# ---------------------------

def run(query: str) -> str:
    """Run the agent with the provided query."""
    print(f"\n--- Running Agent: threet (Model: {MODEL}) ---")
    try:
        response = agent.invoke(
            {"messages": [HumanMessage(content=query)]}
        )
        return response
    except Exception as e:
        return f"Agent Execution Failed: {e}"

if __name__ == "__main__":
    test_query = "Analyze the image at 'path/to/image.jpg' and extract any text."
    output = run(test_query)
    print("Final Output:\n", output)