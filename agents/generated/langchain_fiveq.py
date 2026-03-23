from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from agents.generated.tools.fileio import fileio_func
from agents.generated.tools.webbrowser import webbrowser_func
from agents.generated.tools.pythonexecutor import pythonexecutor_func
from agents.generated.tools.audioprocessor import audioprocessor_func
from agents.generated.tools.dictionaryvalidator import dictionaryvalidator_func

# ---------------------------
# 1. Model Configuration
# ---------------------------

MODEL = "openai/gpt-4o"

# ---------------------------
# 2. Tool Definitions
# ---------------------------

@tool
def fileio_func(file_path: str) -> str:
    """Ingest file-based data from the specified file path."""
    return fileio_func(file_path)

@tool
def webbrowser_func(url: str) -> str:
    """Browse the web to fetch data from the specified URL."""
    return webbrowser_func(url)

@tool
def pythonexecutor_func(code: str) -> str:
    """Execute the provided Python code and return the result."""
    return pythonexecutor_func(code)

@tool
def audioprocessor_func(file_path: str) -> str:
    """Process audio files for transcription or extraction."""
    return audioprocessor_func(file_path)

@tool
def dictionaryvalidator_func(words: List[str], dictionary: List[str], exclude_proper_nouns: bool = False) -> List[str]:
    """Validate words against the provided dictionary, considering case insensitivity and proper nouns."""
    return dictionaryvalidator_func(words, dictionary, exclude_proper_nouns)

TOOLS = [
    fileio_func,
    webbrowser_func,
    pythonexecutor_func,
    audioprocessor_func,
    dictionaryvalidator_func
]

# ---------------------------
# 3. Create Agent
# ---------------------------

system_prompt = (
    "You are fiveq, an AI agent designed to process various types of data including "
    "file-based inputs like audio and text files, as well as web-sourced dictionaries. "
    "You can execute Python code for tasks such as puzzle solving and audio processing. "
    "Your capabilities include validating words against dictionaries and outputting results "
    "in a strictly formatted manner. Available tools are: FileIO, WebBrowser, PythonExecutor, "
    "AudioProcessor, and DictionaryValidator."
)

agent = create_agent(
    model=MODEL,
    tools=TOOLS,
    system_prompt=system_prompt
)

# ---------------------------
# 4. Run Agent Execution
# ---------------------------

def run(query: str):
    print(f"\n--- Running Agent: fiveq (Model: {MODEL}) ---")
    print("Description: An AI agent for data processing and validation.")
    print("----\n")

    try:
        response = agent.invoke(
            {"messages": [HumanMessage(content=query)]}
        )
        return response
    except Exception as e:
        return f"Agent Execution Failed: {e}"

if __name__ == "__main__":
    # Example usage
    result = run("Please transcribe the audio file at path 'audio.mp3' and validate the words against the dictionary from 'https://raw.githubusercontent.com/example/dictionary.txt'.")
    print("Final Output:\n", result)