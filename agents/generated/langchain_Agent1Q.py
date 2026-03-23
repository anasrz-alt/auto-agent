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
def searchtool_func(query: str) -> str:
    """Query web sources for targeted extractions."""
    return searchtool_func(query)

@tool
def pdfextractor_func(file_path: str) -> str:
    """Extract targeted information from PDF files."""
    return pdfextractor_func(file_path)

@tool
def excelanalyzer_func(file_path: str) -> str:
    """Analyze Excel files for counts and comparisons."""
    return excelanalyzer_func(file_path)

@tool
def datacomparer_func(data1: List[float], data2: List[float]) -> str:
    """Compare two datasets and return differences."""
    return datacomparer_func(data1, data2)

@tool
def webbrowser_func(url: str) -> str:
    """Browse the web for additional data."""
    return webbrowser_func(url)

@tool
def pythonexecutor_func(code: str) -> str:
    """Execute Python code for calculations."""
    return pythonexecutor_func(code)

@tool
def dataformatter_func(data: str, format_type: str) -> str:
    """Format the data according to specified units and orders."""
    return dataformatter_func(data, format_type)

TOOLS = [
    searchtool_func,
    pdfextractor_func,
    excelanalyzer_func,
    datacomparer_func,
    webbrowser_func,
    pythonexecutor_func,
    dataformatter_func
]

# ---------------------------
# 3. Create Agent
# ---------------------------

agent = create_agent(
    model=MODEL,
    tools=TOOLS,
    system_prompt="You are Agent1Q, a reliable assistant for querying and analyzing data from various sources."
)

# ---------------------------
# 4. Entry Point Function
# ---------------------------

def run(query: str) -> str:
    print(f"Running Agent1Q with query: {query}")
    response = agent.invoke(
        {"messages": [HumanMessage(content=query)]}
    )
    return response

# ---------------------------
# 5. Test Agent Execution
# ---------------------------

if __name__ == "__main__":
    test_query = "Analyze the availability of books and accommodations from the provided sources."
    print("Final Output:\n", run(test_query))