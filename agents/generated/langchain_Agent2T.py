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
def exceltool_func(data: str) -> str:
    """Manipulate and analyze data using Excel."""
    return f"Processed data in Excel: {data}"

@tool
def calculatortool_func(expression: str) -> str:
    """Perform precise calculations."""
    return f"Calculated result for {expression}"

@tool
def pdfextractortool_func(file_path: str) -> str:
    """Extract information from PDF documents."""
    return f"Extracted data from PDF: {file_path}"

@tool
def datavisualizationtool_func(data: str) -> str:
    """Create visualizations from data."""
    return f"Generated visualization for data: {data}"

@tool
def dataanalysistool_func(data: str) -> str:
    """Analyze data for insights."""
    return f"Analyzed data: {data}"

@tool
def financialmodelingtool_func(model_data: str) -> str:
    """Create financial models based on input data."""
    return f"Created financial model with data: {model_data}"

@tool
def dataorganizationtool_func(data: str) -> str:
    """Organize data for better accessibility."""
    return f"Organized data: {data}"

TOOLS = [
    exceltool_func,
    calculatortool_func,
    pdfextractortool_func,
    datavisualizationtool_func,
    dataanalysistool_func,
    financialmodelingtool_func,
    dataorganizationtool_func
]

# ---------------------------
# 3. Create Agent
# ---------------------------

agent = create_agent(
    model=ChatOpenAI(model=MODEL, temperature=0.2),
    tools=TOOLS,
    system_prompt="You are a helpful and reliable DataInsight Agent."
)

# ---------------------------
# 4. Entry Point Function
# ---------------------------

def run(query: str) -> str:
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
    print("--- Running Agent: Agent2T (Model: openai/gpt-4o) ---")
    print("Description: A DataInsight Agent for advanced data manipulation and analysis.")
    print("----\n")

    test_query = "How can I analyze the sales data from last quarter?"
    output = run(test_query)
    print("Final Output:\n", output)