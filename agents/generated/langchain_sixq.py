from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from agents.generated.tools.searchtool import searchtool_func
from agents.generated.tools.pdfextractor import pdfextractor_func
from agents.generated.tools.excelanalyzer import excelanalyzer_func
from agents.generated.tools.datacomparer import datacomparer_func
from agents.generated.tools.webbrowser import webbrowser_func
from agents.generated.tools.pythonexecutor import pythonexecutor_func
from agents.generated.tools.textanalyzer import textanalyzer_func

# ---------------------------
# 1. Model Configuration
# ---------------------------

MODEL = "openai/gpt-4o"

# ---------------------------
# 2. Tool Definitions
# ---------------------------

@tool
def searchtool(query: str) -> str:
    """Queries web sources for targeted extractions."""
    return searchtool_func(query)

@tool
def pdfextractor(pdf_path: str) -> str:
    """Extracts targeted information from PDF files."""
    return pdfextractor_func(pdf_path)

@tool
def excelanalyzer(file_path: str) -> str:
    """Analyzes Excel files for counts and comparisons."""
    return excelanalyzer_func(file_path)

@tool
def datacomparer(data1: List[float], data2: List[float]) -> str:
    """Compares two datasets and returns differences."""
    return datacomparer_func(data1, data2)

@tool
def webbrowser(url: str) -> str:
    """Browses the web for additional information."""
    return webbrowser_func(url)

@tool
def pythonexecutor(code: str) -> str:
    """Executes Python code for calculations and data processing."""
    return pythonexecutor_func(code)

@tool
def textanalyzer(text: str) -> str:
    """Analyzes text for specific mentions and settings."""
    return textanalyzer_func(text)

TOOLS = [
    searchtool,
    pdfextractor,
    excelanalyzer,
    datacomparer,
    webbrowser,
    pythonexecutor,
    textanalyzer
]

# ---------------------------
# 3. Create Agent
# ---------------------------

system_prompt = (
    "You are an intelligent agent named 'sixq'. Your purpose is to assist users in querying "
    "web and PDF sources for targeted extractions, analyzing Excel files for counts and comparisons, "
    "cross-verifying multi-paper overlaps or census splits, and delivering formatted results. "
    "You have access to the following tools: SearchTool, PDFExtractor, ExcelAnalyzer, DataComparer, "
    "WebBrowser, PythonExecutor, and TextAnalyzer. Please adhere to specified units, orders, and exclusions in your responses."
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
    print(f"\n--- Running Agent: sixq (Model: {MODEL}) ---")
    print("Description: An intelligent agent for targeted data extraction and analysis.")
    print("----\n")

    test_query = "Please analyze the attached Excel file for book availability and provide the results."
    try:
        final_output = run(test_query)
        print("Final Output:\n", final_output)
    except Exception as e:
        print(f"Agent Execution Failed: {e}")