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
def fileio_tool(file_path: str) -> str:
    """Read the content of a file."""
    return fileio_func(file_path)

@tool
def python_executor_tool(code: str) -> str:
    """Execute Python code and return the output."""
    return pythonexecutor_func(code)

TOOLS = [
    fileio_tool,
    python_executor_tool
]

# ---------------------------
# 3. Create Agent
# ---------------------------

agent = create_agent(
    model=MODEL,
    tools=TOOLS,
    system_prompt="You are a helpful and reliable agent that executes and analyzes Python code."
)

# ---------------------------
# 4. Entry Point Function
# ---------------------------

def run(query: str) -> Optional[str]:
    print(f"Received query: {query}")
    try:
        response = agent.invoke(
            {"messages": [HumanMessage(content=query)]}
        )
        return response['output']  # Assuming the output is in the 'output' key
    except Exception as e:
        return f"Agent Execution Failed: {e}"

# ---------------------------
# 5. Test Agent Execution
# ---------------------------

if __name__ == "__main__":
    print("--- Running Agent: Agent7Q (Model: openai/gpt-4o) ---")
    print("Description: This agent executes and analyzes Python code from a file.")
    print("----\n")

    test_query = "Please read the Python code from the provided file and execute it to return the final numeric output."
    final_output = run(test_query)
    print("Final Output:\n", final_output)