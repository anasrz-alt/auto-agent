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
def calculator_func(expression: str) -> str:
    """Perform numerical calculations based on the provided expression."""
    # Implement the calculator logic here
    return f"Calculated result for {expression}"

@tool
def pdfviewer_func(file_path: str) -> str:
    """Analyze the PDF document at the specified file path."""
    # Implement the PDF viewer logic here
    return f"Analyzed PDF document at {file_path}"

@tool
def searchengine_func(query: str) -> str:
    """Search the internet for the given query."""
    # Implement the search engine logic here
    return f"Search results for: {query}"

@tool
def webbrowser_func(url: str) -> str:
    """Browse the web at the specified URL."""
    # Implement the web browser logic here
    return f"Browsed to: {url}"

@tool
def wikipedia_func(query: str) -> str:
    """Fetch information from Wikipedia based on the query."""
    # Implement the Wikipedia logic here
    return f"Wikipedia entry for: {query}"

TOOLS = [
    calculator_func,
    pdfviewer_func,
    searchengine_func,
    webbrowser_func,
    wikipedia_func
]

# ---------------------------
# 3. Create Agent
# ---------------------------

agent = create_agent(
    model=ChatOpenAI(model=MODEL),
    tools=TOOLS,
    system_prompt="You are a helpful and reliable agent."
)

# ---------------------------
# 4. Run Function
# ---------------------------

def run(query: str) -> str:
    """Run the agent with the provided query."""
    response = agent.invoke(
        {"messages": [HumanMessage(content=query)]}
    )
    return response

# ---------------------------
# 5. Test Agent Execution
# ---------------------------

if __name__ == "__main__":
    test_query = "What is the capital of France and how do I calculate 5 + 7?"
    print(f"\n--- Running Agent: Agent1T (Model: {MODEL}) ---")
    print("Description: An OmniTool Agent for autonomous tasks.")
    print("----\n")

    try:
        final_output = run(test_query)
        print("Final Output:\n", final_output)
    except Exception as e:
        print(f"Agent Execution Failed: {e}")