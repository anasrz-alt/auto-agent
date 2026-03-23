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
from agents.generated.tools.notetakingassistant import notetakingassistant_func

# ---------------------------
# 1. Model Configuration
# ---------------------------

MODEL = "openai/gpt-4o"

# ---------------------------
# 2. Tool Definitions
# ---------------------------

@tool
def fileio(file_path: str) -> str:
    """Access and manipulate files."""
    return fileio_func(file_path)

@tool
def speechtotext(audio_file: str) -> str:
    """Transcribe spoken audio into text."""
    return speechtotext_func(audio_file)

@tool
def textprocessor(text: str) -> str:
    """Process and analyze text data."""
    return textprocessor_func(text)

@tool
def audiofilehandler(audio_file: str) -> str:
    """Handle audio file operations."""
    return audiofilehandler_func(audio_file)

@tool
def dataorganizer(data: List[str]) -> str:
    """Organize and structure data efficiently."""
    return dataorganizer_func(data)

@tool
def voicecommandprocessor(command: str) -> str:
    """Process voice commands for actions."""
    return voicecommandprocessor_func(command)

@tool
def notetakingassistant(notes: str) -> str:
    """Assist in taking and organizing notes."""
    return notetakingassistant_func(notes)

TOOLS = [
    fileio,
    speechtotext,
    textprocessor,
    audiofilehandler,
    dataorganizer,
    voicecommandprocessor,
    notetakingassistant
]

# ---------------------------
# 3. Create Agent
# ---------------------------

system_prompt = (
    "You are an AudioFileSync Agent named 'sixt'. Your primary role is to autonomously "
    "perform tasks related to audio and text data. You can access, read, and manipulate "
    "various file types, transcribe audio into text, and assist with data organization, "
    "note-taking, and voice command processing. Use the tools provided to fulfill user requests."
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
    print(f"\n--- Running Agent: sixt (Model: {MODEL}) ---")
    print("Description: An AudioFileSync Agent that performs tasks related to audio and text data.")
    print("----\n")

    test_prompt = "Please transcribe the audio from the file 'example_audio.mp3' and organize the notes."
    
    try:
        final_output = run(test_prompt)
        print("Final Output:\n", final_output)
    except Exception as e:
        print(f"Agent Execution Failed: {e}")