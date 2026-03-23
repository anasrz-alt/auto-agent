from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from agents.generated.tools.speechrecognitiontool import speechrecognitiontool_func
from agents.generated.tools.soundanalysistool import soundanalysistool_func
from agents.generated.tools.transcriptionservice import transcriptionservice_func
from agents.generated.tools.searchengineapi import searchengineapi_func
from agents.generated.tools.webbrowser import webbrowser_func
from agents.generated.tools.naturallanguageprocessingtool import naturallanguageprocessingtool_func
from agents.generated.tools.audioplaybacktool import audioplaybacktool_func
from agents.generated.tools.fileio import fileio_func
from agents.generated.tools.datavisualizationtool import datavisualizationtool_func

# ---------------------------
# 1. Model Configuration
# ---------------------------

MODEL = "openai/gpt-4o"

# ---------------------------
# 2. Tool Definitions
# ---------------------------

@tool
def speechrecognitiontool(audio_file: str) -> str:
    """Process an audio file for speech recognition."""
    return speechrecognitiontool_func(audio_file)

@tool
def soundanalysistool(audio_file: str) -> str:
    """Analyze sound characteristics from an audio file."""
    return soundanalysistool_func(audio_file)

@tool
def transcriptionservice(audio_file: str) -> str:
    """Transcribe audio content to text."""
    return transcriptionservice_func(audio_file)

@tool
def searchengineapi(query: str) -> str:
    """Search the web for relevant information based on a query."""
    return searchengineapi_func(query)

@tool
def webbrowser(url: str) -> str:
    """Open a web page and return its content."""
    return webbrowser_func(url)

@tool
def naturallanguageprocessingtool(text: str) -> str:
    """Process text for natural language understanding and insights."""
    return naturallanguageprocessingtool_func(text)

@tool
def audioplaybacktool(audio_file: str) -> str:
    """Play an audio file."""
    return audioplaybacktool_func(audio_file)

@tool
def fileio(file_path: str, mode: str) -> str:
    """Read or write to a file."""
    return fileio_func(file_path, mode)

@tool
def datavisualizationtool(data: List[float]) -> str:
    """Visualize data in a graphical format."""
    return datavisualizationtool_func(data)

TOOLS = [
    speechrecognitiontool,
    soundanalysistool,
    transcriptionservice,
    searchengineapi,
    webbrowser,
    naturallanguageprocessingtool,
    audioplaybacktool,
    fileio,
    datavisualizationtool
]

# ---------------------------
# 3. Create Agent
# ---------------------------

system_prompt = (
    "You are an AudioProcessor Agent named 'fivet'. Your purpose is to autonomously execute tasks "
    "related to audio processing, including speech recognition, sound analysis, and transcription. "
    "You can utilize various tools to enhance your capabilities, including searching online for "
    "contextual information and providing insights based on audio data. The available tools are: "
    "SpeechRecognitionTool, SoundAnalysisTool, TranscriptionService, SearchEngineAPI, WebBrowser, "
    "NaturalLanguageProcessingTool, AudioPlaybackTool, FileIO, and DataVisualizationTool."
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
    print("--- Running Agent: fivet (Model: openai/gpt-4o) ---")
    print("Description: An AudioProcessor Agent for speech recognition and sound analysis.")
    test_query = "Please transcribe the audio file located at 'audio/sample.wav'."
    output = run(test_query)
    print("Final Output:\n", output)