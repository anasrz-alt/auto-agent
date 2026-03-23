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
def fileio_func(file_path: str) -> str:
    """Ingests file-based data."""
    return f"Data from {file_path} ingested."

@tool
def webbrowser_func(url: str) -> str:
    """Fetches data from the web."""
    return f"Data fetched from {url}."

@tool
def pythonexecutor_func(code: str) -> str:
    """Executes Python code."""
    return f"Executed code: {code}"

@tool
def speechtotext_func(audio_path: str) -> str:
    """Transcribes audio to text."""
    return f"Transcribed text from {audio_path}."

@tool
def dictionaryvalidator_func(word_list: List[str], dictionary: List[str], exclude_proper_nouns: bool) -> List[str]:
    """Validates words against a dictionary."""
    return [word for word in word_list if word.lower() in dictionary]

TOOLS = [
    fileio_func,
    webbrowser_func,
    pythonexecutor_func,
    speechtotext_func,
    dictionaryvalidator_func
]

# ---------------------------
# 3. Create Agent
# ---------------------------

agent = create_agent(
    model=MODEL,
    tools=TOOLS,
    system_prompt="You are Agent5Q, a versatile agent for processing file-based data and web-sourced dictionaries."
)

# ---------------------------
# 4. Entry Point Function
# ---------------------------

def run(query: str) -> str:
    print(f"\n--- Running Agent: Agent5Q (Model: {MODEL}) ---")
    print("Query:", query)
    print("----\n")

    try:
        response = agent.invoke(
            {"messages": [HumanMessage(content=query)]}
        )
        return response
    except Exception as e:
        return f"Agent Execution Failed: {e}"

if __name__ == "__main__":
    # Example query to test the agent
    test_query = "Ingest the audio file and validate words against the dictionary."
    result = run(test_query)
    print("Final Output:\n", result)