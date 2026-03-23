from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from agents.generated.tools.fileio import fileio_func
from agents.generated.tools.speechtotext import speechtotext_func
from agents.generated.tools.textprocessor import textprocessor_func
from agents.generated.tools.audiofilehandler import audiofilehandler_func
from agents.generated.tools.dataorganizer import dataorganizer_func
from agents.generated.tools.voicecommandprocessor import voicecommandprocessor_func
from agents.generated.tools.notetaker import notetaker_func
from agents.generated.tools.pythonexecutor import pythonexecutor_func

# ---------------------------
# 1. Model Configuration
# ---------------------------

MODEL = "openai/gpt-4o"

# ---------------------------
# 2. Tool Definitions
# ---------------------------

@tool
def FileIO(file_path: str) -> str:
    """Access, read, and manipulate various file types."""
    return fileio_func(file_path)

@tool
def SpeechToText(audio_file: str) -> str:
    """Transcribe spoken audio into text."""
    return speechtotext_func(audio_file)

@tool
def TextProcessor(text: str) -> str:
    """Process and analyze text data."""
    return textprocessor_func(text)

@tool
def AudioFileHandler(audio_file: str) -> str:
    """Handle audio file operations."""
    return audiofilehandler_func(audio_file)

@tool
def DataOrganizer(data: List[str]) -> str:
    """Organize and structure data efficiently."""
    return dataorganizer_func(data)

@tool
def VoiceCommandProcessor(command: str) -> str:
    """Process voice commands for various tasks."""
    return voicecommandprocessor_func(command)

@tool
def NoteTaker(notes: str) -> str:
    """Automate note-taking from audio or text."""
    return notetaker_func(notes)

@tool
def PythonExecutor(code: str) -> str:
    """Execute Python code dynamically."""
    return pythonexecutor_func(code)

TOOLS = [
    FileIO,
    SpeechToText,
    TextProcessor,
    AudioFileHandler,
    DataOrganizer,
    VoiceCommandProcessor,
    NoteTaker,
    PythonExecutor
]

# ---------------------------
# 3. Create Agent
# ---------------------------

agent = create_agent(
    model=MODEL,
    tools=TOOLS,
    system_prompt="You are an AudioFileSync Agent that autonomously performs tasks using audio and text data."
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
    print("--- Running Agent: Agent6T (Model: openai/gpt-4o) ---")
    print("Description: An AudioFileSync Agent for efficient data handling.")
    print("----\n")

    test_query = "Transcribe the audio file located at 'path/to/audiofile.wav' and organize the notes."
    try:
        final_output = run(test_query)
        print("Final Output:\n", final_output)
    except Exception as e:
        print(f"Agent Execution Failed: {e}")