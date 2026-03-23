from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from agents.generated.tools.fileio import fileio_func
from agents.generated.tools.pythonexecutor import pythonexecutor_func

# ---------------------------
# 1. Model Configuration
# ---------------------------

MODEL = "openai/gpt-4o"

# ---------------------------
# 2. Tool Definitions
# ---------------------------

@tool
def fileio_func(file_path: str) -> str:
    """Read the content of a file at the given path."""
    return fileio_func(file_path)

@tool
def pythonexecutor_func(code: str) -> str:
    """Execute the provided Python code in a secure environment."""
    return pythonexecutor_func(code)

TOOLS = [
    fileio_func,
    pythonexecutor_func
]

# ---------------------------
# 3. Create Agent
# ---------------------------

system_prompt = (
    "You are a Python code execution agent named 'sevenq'. Your task is to execute and analyze "
    "Python code provided in an attached file. You will run the code in a secure environment, "
    "determine the final numeric output, and return it exactly as produced. You must handle any "
    "potential dependencies and parse the code to extract the last computed or printed numerical value. "
    "You have access to the following tools: FileIO for reading files and PythonExecutor for executing Python code."
)

agent = create_agent(
    model=MODEL,
    tools=TOOLS,
    system_prompt=system_prompt
)

# ---------------------------
# 4. Entry Point Function
# ---------------------------

def run(query: str) -> Optional[str]:
    print(f"\n--- Running Agent: sevenq (Model: {MODEL}) ---")
    print("Description: Executes and analyzes Python code from a file.")
    print("----\n")

    try:
        response = agent.invoke(
            {"messages": [HumanMessage(content=query)]}
        )
        return response['content']  # Assuming the response contains a 'content' field
    except Exception as e:
        print(f"Agent Execution Failed: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    result = run("Please execute the Python code in 'path/to/your/file.py' and return the final output.")
    print("Final Output:\n", result)