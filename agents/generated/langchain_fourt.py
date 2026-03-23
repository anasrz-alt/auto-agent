from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from agents.generated.tools.videorecognitionapi import videorecognitionapi_func
from agents.generated.tools.objectdetectionmodel import objectdetectionmodel_func
from agents.generated.tools.actionrecognitionmodel import actionrecognitionmodel_func
from agents.generated.tools.webbrowser import webbrowser_func
from agents.generated.tools.datastorage import datastorage_func
from agents.generated.tools.realtimestreamingapi import realtimestreamingapi_func
from agents.generated.tools.contentmoderationtool import contentmoderationtool_func
from agents.generated.tools.automatedtaggingsystem import automatedtaggingsystem_func
from agents.generated.tools.insightextractiontool import insightextractiontool_func
from agents.generated.tools.correlationengine import correlationengine_func

# ---------------------------
# 1. Model Configuration
# ---------------------------

MODEL = "openai/gpt-4o"

# ---------------------------
# 2. Tool Definitions
# ---------------------------

@tool
def videorecognitionapi(video_path: str) -> str:
    """Analyze video content for objects and actions."""
    return videorecognitionapi_func(video_path)

@tool
def objectdetectionmodel(frame: bytes) -> List[str]:
    """Detect objects in a video frame."""
    return objectdetectionmodel_func(frame)

@tool
def actionrecognitionmodel(frame: bytes) -> List[str]:
    """Recognize actions in a video frame."""
    return actionrecognitionmodel_func(frame)

@tool
def webbrowser(query: str) -> str:
    """Retrieve information from the internet based on a query."""
    return webbrowser_func(query)

@tool
def datastorage(data: dict) -> str:
    """Store data for future reference."""
    return datastorage_func(data)

@tool
def realtimestreamingapi(stream_url: str) -> str:
    """Process real-time video streams."""
    return realtimestreamingapi_func(stream_url)

@tool
def contentmoderationtool(content: str) -> str:
    """Moderate content for appropriateness."""
    return contentmoderationtool_func(content)

@tool
def automatedtaggingsystem(content: str) -> List[str]:
    """Automatically tag content based on analysis."""
    return automatedtaggingsystem_func(content)

@tool
def insightextractiontool(data: str) -> str:
    """Extract insights from provided data."""
    return insightextractiontool_func(data)

@tool
def correlationengine(data1: str, data2: str) -> str:
    """Correlate two sets of data."""
    return correlationengine_func(data1, data2)

TOOLS = [
    videorecognitionapi,
    objectdetectionmodel,
    actionrecognitionmodel,
    webbrowser,
    datastorage,
    realtimestreamingapi,
    contentmoderationtool,
    automatedtaggingsystem,
    insightextractiontool,
    correlationengine
]

# ---------------------------
# 3. Create Agent
# ---------------------------

system_prompt = (
    "You are the VideoAnalyzer Agent named 'fourt'. Your purpose is to autonomously "
    "process video data and act on it using various tools for video recognition, "
    "content moderation, automated tagging, and real-time internet retrieval. "
    "You have access to the following tools: VideoRecognitionAPI, ObjectDetectionModel, "
    "ActionRecognitionModel, WebBrowser, DataStorage, RealTimeStreamingAPI, "
    "ContentModerationTool, AutomatedTaggingSystem, InsightExtractionTool, "
    "and CorrelationEngine. Use these tools to interpret content, identify objects, "
    "actions, and patterns, and provide insights based on real-time data."
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
    test_query = "Analyze the video from the provided URL and identify any suspicious actions."
    print(f"\n--- Running Agent: fourt (Model: {MODEL}) ---")
    print("Description: A VideoAnalyzer Agent for processing and analyzing video content.")
    print("----\n")

    try:
        final_output = run(test_query)
        print("Final Output:\n", final_output)
    except Exception as e:
        print(f"Agent Execution Failed: {e}")