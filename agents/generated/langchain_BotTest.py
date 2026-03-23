from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from agents.generated.tools.fileio import fileio_func
from agents.generated.tools.webbrowser import webbrowser_func
from agents.generated.tools.pythonexecutor import pythonexecutor_func
from agents.generated.tools.dataparser import dataparser_func
from agents.generated.tools.dataaggregator import dataaggregator_func
from agents.generated.tools.resultformatter import resultformatter_func

# ---------------------------
# 1. Model Configuration
# ---------------------------

MODEL = "openai/gpt-4o"

# ---------------------------
# 2. Tool Definitions
# ---------------------------

@tool
def fileio_tool(file_path: str) -> str:
    """Ingests file-based data from the specified file path."""
    return fileio_func(file_path)

@tool
def webbrowser_tool(url: str) -> str:
    """Fetches data from the specified web URL."""
    return webbrowser_func(url)

@tool
def python_executor_tool(code: str) -> str:
    """Executes the provided Python code and returns the result."""
    return pythonexecutor_func(code)

@tool
def data_parser_tool(data: str) -> dict:
    """Parses the provided data and returns structured information."""
    return dataparser_func(data)

@tool
def data_aggregator_tool(data: List[dict], criteria: dict) -> dict:
    """Aggregates the provided data based on the specified criteria."""
    return dataaggregator_func(data, criteria)

@tool
def result_formatter_tool(results: dict, precision: int, unit: str) -> str:
    """Formats the results with the specified precision and units."""
    return resultformatter_func(results, precision, unit)

TOOLS = [
    fileio_tool,
    webbrowser_tool,
    python_executor_tool,
    data_parser_tool,
    data_aggregator_tool,
    result_formatter_tool
]

# ---------------------------
# 3. Create Agent
# ---------------------------

system_prompt = (
    "You are BotTest, a versatile data processing agent. "
    "You can ingest file-based data (like Excel or PDB files) and web-sourced information "
    "from URLs. You have the ability to execute Python and Biopython code for parsing "
    "and computations such as distances, velocities, and percentages. "
    "You can filter and aggregate data based on specific criteria, "
    "and output formatted numerical results with required precision and units. "
    "Available tools: FileIO, WebBrowser, PythonExecutor, DataParser, DataAggregator, ResultFormatter."
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
    """Executes the agent with the provided query."""
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
    test_query = "Ingest the data from the provided Excel file and calculate the average beak length."
    print(f"\n--- Running Agent: BotTest (Model: {MODEL}) ---")
    print("Description: A versatile data processing agent.")
    print("----\n")
    output = run(test_query)
    print("Final Output:\n", output)