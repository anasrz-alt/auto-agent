from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from agents.generated.tools.exceltool import exceltool_func
from agents.generated.tools.calculatortool import calculatortool_func
from agents.generated.tools.pdfextractortool import pdfextractortool_func
from agents.generated.tools.datavisualizationtool import datavisualizationtool_func
from agents.generated.tools.dataanalysistool import dataanalysistool_func
from agents.generated.tools.financialmodelingtool import financialmodelingtool_func
from agents.generated.tools.dataorganizationtool import dataorganizationtool_func

# ---------------------------
# 1. Model Configuration
# ---------------------------

MODEL = "openai/gpt-4o"

# ---------------------------
# 2. Tool Definitions
# ---------------------------

@tool
def exceltool(data: str) -> str:
    """Manipulate and analyze data using Excel tools."""
    return exceltool_func(data)

@tool
def calculatortool(expression: str) -> str:
    """Perform precise calculations based on the given expression."""
    return calculatortool_func(expression)

@tool
def pdfextractortool(pdf_path: str) -> str:
    """Extract text and data from a PDF document."""
    return pdfextractortool_func(pdf_path)

@tool
def datavisualizationtool(data: str) -> str:
    """Create visual representations of data for better insights."""
    return datavisualizationtool_func(data)

@tool
def dataanalysistool(data: str) -> str:
    """Analyze data to derive meaningful insights and trends."""
    return dataanalysistool_func(data)

@tool
def financialmodelingtool(data: str) -> str:
    """Build financial models based on provided data."""
    return financialmodelingtool_func(data)

@tool
def dataorganizationtool(data: str) -> str:
    """Organize and structure data for better accessibility."""
    return dataorganizationtool_func(data)

TOOLS = [
    exceltool,
    calculatortool,
    pdfextractortool,
    datavisualizationtool,
    dataanalysistool,
    financialmodelingtool,
    dataorganizationtool
]

# ---------------------------
# 3. Create Agent
# ---------------------------

system_prompt = (
    "You are a DataInsight Agent named 'twot'. Your purpose is to autonomously execute tasks "
    "and process information using various tools for advanced data manipulation, analysis, and visualization. "
    "You have access to the following tools: ExcelTool for data manipulation, CalculatorTool for precise computations, "
    "PDFExtractorTool for document extraction, DataVisualizationTool for creating visual data representations, "
    "DataAnalysisTool for analyzing data, FinancialModelingTool for building financial models, and "
    "DataOrganizationTool for organizing data. Provide actionable insights across diverse applications."
)

agent = create_agent(
    model=MODEL,
    tools=TOOLS,
    system_prompt=system_prompt
)

# ---------------------------
# 4. Run Agent Execution
# ---------------------------

def run(query: str) -> str:
    response = agent.invoke(
        {"messages": [HumanMessage(content=query)]}
    )
    return response

if __name__ == "__main__":
    print(f"\n--- Running Agent: twot (Model: {MODEL}) ---")
    print("Description: A DataInsight Agent for advanced data manipulation and analysis.")
    print("----\n")

    test_prompt = "Analyze the financial data from the last quarter and provide insights."
    
    try:
        final_output = run(test_prompt)
        print("Final Output:\n", final_output)
    except Exception as e:
        print(f"Agent Execution Failed: {e}")