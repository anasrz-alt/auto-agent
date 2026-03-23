from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage


# ---------------------------
# 1. Model Configuration
# ---------------------------

MODEL = "gpt-4o"

# ---------------------------
# 2. Tool Definitions
# ---------------------------

@tool
def SpeechRecognitionTool(audio_file: str) -> str:
    """Processes audio files for speech recognition."""
    return speechrecognitiontool_func(audio_file)

@tool
def SoundAnalysisTool(audio_file: str) -> str:
    """Analyzes sound characteristics of audio files."""
    return soundanalysistool_func(audio_file)

@tool
def TranscriptionService(audio_file: str) -> str:
    """Transcribes audio files into text."""
    return transcriptionservice_func(audio_file)

@tool
def SearchEngineIntegration(query: str) -> str:
    """Searches the web for information related to the query."""
    return searchengineintegration_func(query)

@tool
def WebBrowser(url: str) -> str:
    """Fetches content from a specified web page."""
    return webbrowser_func(url)

@tool
def NaturalLanguageProcessingTool(text: str) -> str:
    """Processes text for natural language understanding tasks."""
    return naturallanguageprocessingtool_func(text)

@tool
def AudioEditingTool(audio_file: str, action: str) -> str:
    """Edits audio files based on specified actions."""
    return audioeditingtool_func(audio_file, action)

@tool
def DataVisualizationTool(data: List[float]) -> str:
    """Generates visualizations for the provided data."""
    return datavisualizationtool_func(data)

TOOLS = [
    SpeechRecognitionTool,
    SoundAnalysisTool,
    TranscriptionService,
    SearchEngineIntegration,
    WebBrowser,
    NaturalLanguageProcessingTool,
    AudioEditingTool,
    DataVisualizationTool
]

# ---------------------------
# 3. Create Agent
# ---------------------------

agent = create_agent(
    model=MODEL,
    tools=TOOLS,
    system_prompt="You are an autonomous audio processing agent capable of executing tasks using various audio tools."
)

# ---------------------------
# 4. Entry Point Function
# ---------------------------

def run(query: str) -> str:
    """Runs the agent with the provided query."""
    response = agent.invoke(
        {"messages": [HumanMessage(content=query)]}
    )
    return response

# ---------------------------
# 5. Test Agent Execution
# ---------------------------

if __name__ == "__main__":
    print("--- Running Agent: Agent5T (Model: openai/gpt-4o) ---")
    print("Description: An AudioProcessor Agent for speech recognition, sound analysis, and transcription.")
    print("----\n")

    try:
        test_query = "Please transcribe this audio file and analyze its sound characteristics."
        output = run(test_query)
        print("Final Output:\n", output)
    except Exception as e:
        print(f"Agent Execution Failed: {e}")