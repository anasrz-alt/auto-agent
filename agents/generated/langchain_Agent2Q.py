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
    """Ingests file-based data from the specified file path."""
    return f"Data ingested from {file_path}."

@tool
def webbrowser_func(url: str) -> str:
    """Fetches information from the specified web URL."""
    return f"Data fetched from {url}."

@tool
def pythonexecutor_func(code: str) -> str:
    """Executes the provided Python code and returns the result."""
    return eval(code)

@tool
def dataparser_func(data: str, format: str) -> str:
    """Parses the provided data based on the specified format (e.g., Excel, CSV)."""
    return f"Data parsed in {format} format."

@tool
def dataaggregator_func(data: List[float], criteria: str) -> float:
    """Aggregates the provided data based on the specified criteria."""
    return sum(data) / len(data)  # Example aggregation: average

@tool
def resultformatter_func(value: float, precision: int, unit: str) -> str:
    """Formats the numerical result with the specified precision and unit."""
    return f"{value:.{precision}f} {unit}"

TOOLS = [
    fileio_func,
    webbrowser_func,
    pythonexecutor_func,
    dataparser_func,
    dataaggregator_func,
    resultformatter_func
]

# ---------------------------
# 3. Create Agent
# ---------------------------

agent = create_agent(
    model=MODEL,
    tools=TOOLS,
    system_prompt="You are a helpful and reliable agent."
)

# ---------------------------
# 4. Entry Point Function
# ---------------------------

def run(query: str) -> str:
    print(f"Running query: {query}")
    response = agent.invoke(
        {"messages": [HumanMessage(content=query)]}
    )
    return response

# ---------------------------
# 5. Test Agent Execution
# ---------------------------

if __name__ == "__main__":
    print(f"\n--- Running Agent: Agent2Q (Model: {MODEL}) ---")
    print("Description: This agent ingests file-based and web-sourced data, performs computations, and formats results.")
    print("----\n")

    test_query = "Ingest data from 'data.xlsx' and calculate the average beak length."
    try:
        final_output = run(test_query)
        print("Final Output:\n", final_output)
    except Exception as e:
        print(f"Agent Execution Failed: {e}")