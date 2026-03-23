from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from agents.generated.tools.calculator import calculator_func
from agents.generated.tools.pdfviewer import pdfviewer_func
from agents.generated.tools.searchengine import searchengine_func
from agents.generated.tools.webbrowser import webbrowser_func
from agents.generated.tools.wikipedia import wikipedia_func

# ---------------------------
# 1. Model Configuration
# ---------------------------

MODEL = "openai/gpt-4o"

# ---------------------------
# 2. Tool Definitions
# ---------------------------

@tool
def Calculator(expression: str) -> str:
    """Perform numerical calculations."""
    return calculator_func(expression)

@tool
def PDFViewer(file_path: str) -> str:
    """Analyze and extract information from a PDF document."""
    return pdfviewer_func(file_path)

@tool
def SearchEngine(query: str) -> str:
    """Search the internet for real-time data."""
    return searchengine_func(query)

@tool
def WebBrowser(url: str) -> str:
    """Browse the web for information."""
    return webbrowser_func(url)

@tool
def Wikipedia(query: str) -> str:
    """Access structured knowledge from Wikipedia."""
    return wikipedia_func(query)

TOOLS = [
    Calculator,
    PDFViewer,
    SearchEngine,
    WebBrowser,
    Wikipedia
]

# ---------------------------
# 3. Create Agent
# ---------------------------

system_prompt = (
    "You are an OmniTool Agent named 'onet'. Your purpose is to autonomously perform tasks "
    "and make decisions by leveraging various tools. You have access to a Calculator for numerical computations, "
    "a PDF Viewer for document analysis, a Search Engine for real-time internet data, "
    "a Web Browser for browsing the web, and Wikipedia for structured knowledge access. "
    "Utilize these tools efficiently to handle complex queries, conduct research, and perform data-driven calculations."
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
    """Run the agent with the provided query."""
    try:
        response = agent.invoke(
            {"messages": [HumanMessage(content=query)]}
        )
        return response['content']
    except Exception as e:
        return f"Agent Execution Failed: {e}"

# ---------------------------
# 5. Test Agent Execution
# ---------------------------

if __name__ == "__main__":
    test_query = "What is the capital of France and calculate 15 * 23?"
    print(f"\n--- Running Agent: onet (Model: {MODEL}) ---")
    print("Description: An OmniTool Agent for autonomous task execution.")
    print("----\n")

    output = run(test_query)
    print("Final Output:\n", output)