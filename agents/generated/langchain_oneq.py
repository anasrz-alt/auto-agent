from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from agents.generated.tools.searchtool import searchtool_func
from agents.generated.tools.pdfextractor import pdfextractor_func
from agents.generated.tools.excelanalyzer import excelanalyzer_func
from agents.generated.tools.datacomparator import datacomparator_func
from agents.generated.tools.webbrowser import webbrowser_func
from agents.generated.tools.pythonexecutor import pythonexecutor_func

# ---------------------------
# 1. Model Configuration
# ---------------------------

MODEL = "openai/gpt-4o"

# ---------------------------
# 2. Tool Definitions
# ---------------------------

@tool
def searchtool(query: str) -> str:
    """Query web sources for information."""
    return searchtool_func(query)

@tool
def pdfextractor(file_path: str) -> str:
    """Extract text and data from a PDF file."""
    return pdfextractor_func(file_path)

@tool
def excelanalyzer(file_path: str) -> str:
    """Analyze Excel files for counts and comparisons."""
    return excelanalyzer_func(file_path)

@tool
def datacomparator(data1: List[float], data2: List[float]) -> str:
    """Compare two datasets and return differences."""
    return datacomparator_func(data1, data2)

@tool
def webbrowser(url: str) -> str:
    """Browse the web for information."""
    return webbrowser_func(url)

@tool
def pythonexecutor(code: str) -> str:
    """Execute Python code and return the result."""
    return pythonexecutor_func(code)

TOOLS = [
    searchtool,
    pdfextractor,
    excelanalyzer,
    datacomparator,
    webbrowser,
    pythonexecutor
]

# ---------------------------
# 3. Create Agent
# ---------------------------

system_prompt = (
    "You are 'oneq', an AI agent designed to assist users with targeted data extractions and analyses. "
    "You can query web and PDF sources for specific information, analyze Excel files for counts and comparisons, "
    "and cross-verify data for overlaps or splits. Your tools include:\n"
    "- SearchTool: To query web sources.\n"
    "- PDFExtractor: To extract data from PDFs.\n"
    "- ExcelAnalyzer: To analyze Excel files.\n"
    "- DataComparator: To compare datasets.\n"
    "- WebBrowser: To browse the web for information.\n"
    "- PythonExecutor: To execute Python code for calculations.\n"
    "Please provide formatted results adhering to specified units, orders, and exclusions."
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
    """Run the agent with the given query."""
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
    test_query = "Please analyze the attached Excel file for book availability and compare it with the census data."
    print(f"\n--- Running Agent: oneq (Model: {MODEL}) ---")
    print("Description: An AI agent for targeted data extractions and analyses.")
    print("----\n")
    final_output = run(test_query)
    print("Final Output:\n", final_output)