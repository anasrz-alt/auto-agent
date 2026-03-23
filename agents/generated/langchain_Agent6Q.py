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
    """Query web sources for targeted extractions."""
    return searchtool_func(query)

@tool
def pdfextractor(file_path: str) -> str:
    """Extract information from PDF files."""
    return pdfextractor_func(file_path)

@tool
def excelanalyzer(file_path: str) -> str:
    """Analyze Excel files for counts and comparisons."""
    return excelanalyzer_func(file_path)

@tool
def datacomparer(data1: List[float], data2: List[float]) -> str:
    """Cross-verify multi-paper overlaps or census splits with calculations."""
    return datacomparer_func(data1, data2)

@tool
def webbrowser(url: str) -> str:
    """Browse web pages for information."""
    return webbrowser_func(url)

@tool
def pythonexecutor(code: str) -> str:
    """Execute Python code for calculations."""
    return pythonexecutor_func(code)

@tool
def textanalyzer(text: str) -> str:
    """Analyze text for specific mentions and settings."""
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

agent = create_agent(
    model=MODEL,
    tools=TOOLS,
    system_prompt="You are Agent6Q, a helpful and reliable agent designed for targeted extractions and analysis."
)

# ---------------------------
# 4. Entry Point Function
# ---------------------------

def run(query: str) -> str:
    """Run the agent with the provided query."""
    print(f"Running Agent6Q with query: {query}")
    response = agent.invoke(
        {"messages": [HumanMessage(content=query)]}
    )
    return response

# ---------------------------
# 5. Test Agent Execution
# ---------------------------

if __name__ == "__main__":
    test_query = "Analyze the availability of books and accommodations in the attached Excel file."
    final_output = run(test_query)
    print("Final Output:\n", final_output)