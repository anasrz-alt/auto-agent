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
def fileio(file_path: str) -> str:
    """Ingests file-based data from the specified path."""
    return fileio_func(file_path)

@tool
def webbrowser(url: str) -> str:
    """Fetches web-sourced information from the specified URL."""
    return webbrowser_func(url)

@tool
def python_executor(code: str) -> str:
    """Executes Python code for parsing and computations."""
    return pythonexecutor_func(code)

@tool
def data_parser(data: str) -> dict:
    """Parses the ingested data for further analysis."""
    return dataparser_func(data)

@tool
def data_aggregator(data: dict, criteria: dict) -> dict:
    """Filters and aggregates data based on specified criteria."""
    return dataaggregator_func(data, criteria)

@tool
def result_formatter(results: dict, precision: int, units: str) -> str:
    """Formats numerical results with specified precision and units."""
    return resultformatter_func(results, precision, units)

TOOLS = [
    fileio,
    webbrowser,
    python_executor,
    data_parser,
    data_aggregator,
    result_formatter
]

# ---------------------------
# 3. Create Agent
# ---------------------------

system_prompt = (
    "You are a helpful and reliable agent named 'twoq'. "
    "Your purpose is to ingest file-based data (like Excel, spreadsheets, PDB) and web-sourced information "
    "(such as Wikipedia articles and scientific papers). You can execute Python/Biopython code for parsing "
    "and computations, filter and aggregate data based on specified criteria, and output formatted numerical "
    "results with the required precision and units. Available tools: FileIO, WebBrowser, PythonExecutor, "
    "DataParser, DataAggregator, ResultFormatter."
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
    """Runs the agent with the provided query."""
    response = agent.invoke(
        {"messages": [HumanMessage(content=query)]}
    )
    return response

# ---------------------------
# 5. Test Agent Execution
# ---------------------------

if __name__ == "__main__":
    print(f"\n--- Running Agent: twoq (Model: {MODEL}) ---")
    print("Description: A data ingestion and analysis agent.")
    print("----\n")

    test_query = "Ingest data from 'data.xlsx', analyze beak lengths, and provide results."
    try:
        final_output = run(test_query)
        print("Final Output:\n", final_output)
    except Exception as e:
        print(f"Agent Execution Failed: {e}")