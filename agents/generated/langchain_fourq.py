from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from agents.generated.tools.videoanalysistool import videoanalysistool_func
from agents.generated.tools.subtitleextractor import subtitleextractor_func
from agents.generated.tools.imagerecognitionapi import imagerecognitionapi_func
from agents.generated.tools.naturallanguageprocessingapi import naturallanguageprocessingapi_func
from agents.generated.tools.websearchtool import websearchtool_func
from agents.generated.tools.dataformatter import dataformatter_func

# ---------------------------
# 1. Model Configuration
# ---------------------------

MODEL = "openai/gpt-4o"

# ---------------------------
# 2. Tool Definitions
# ---------------------------

@tool
def video_analysis(url: str) -> str:
    """Analyze video for frame and visual data."""
    return videoanalysistool_func(url)

@tool
def extract_subtitles(url: str) -> str:
    """Extract subtitles from a video URL."""
    return subtitleextractor_func(url)

@tool
def recognize_images(image_data: str) -> str:
    """Recognize and analyze visual content in images."""
    return imagerecognitionapi_func(image_data)

@tool
def process_nlp(text: str) -> str:
    """Perform natural language processing on the provided text."""
    return naturallanguageprocessingapi_func(text)

@tool
def web_search(query: str) -> str:
    """Conduct a web search for contextual information."""
    return websearchtool_func(query)

@tool
def format_data(data: str) -> str:
    """Format the data into a structured output."""
    return dataformatter_func(data)

TOOLS = [
    video_analysis,
    extract_subtitles,
    recognize_images,
    process_nlp,
    web_search,
    format_data
]

# ---------------------------
# 3. Create Agent
# ---------------------------

system_prompt = (
    "You are an AI agent named 'fourq' designed to analyze video URLs for frame and subtitle data, "
    "count visual elements such as maximum simultaneous species, and predict contextual information "
    "like named scientists based on inferred years. You have access to the following tools: "
    "- VideoAnalysisTool: for analyzing video content. "
    "- SubtitleExtractor: for extracting subtitles from videos. "
    "- ImageRecognitionAPI: for recognizing images and visual content. "
    "- NaturalLanguageProcessingAPI: for analyzing narratives in text. "
    "- WebSearchTool: for conducting targeted web searches for contextual dates. "
    "- DataFormatter: for formatting results into structured outputs."
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
    print(f"\n--- Running Agent: fourq (Model: {MODEL}) ---")
    print("Description: Analyzes video URLs for visual and narrative data.")
    print("----\n")

    test_query = "Analyze the video at this URL: [VIDEO_URL] for simultaneous species counts and subtitle extraction."
    try:
        final_output = run(test_query)
        print("Final Output:\n", final_output)
    except Exception as e:
        print(f"Agent Execution Failed: {e}")