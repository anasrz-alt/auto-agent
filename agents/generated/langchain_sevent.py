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
def pythonexecutor_func(code: str) -> str:
    """Executes a given Python code snippet."""
    return pythonexecutor_func(code)

@tool
def pandas_func(data: str) -> str:
    """Manipulates data using Pandas."""
    return pandas_func(data)

@tool
def numpy_func(array: List[float]) -> str:
    """Performs numerical operations using NumPy."""
    return numpy_func(array)

@tool
def scikit_learn_func(model: str, data: List[float]) -> str:
    """Applies machine learning algorithms using Scikit-learn."""
    return scikit_learn_func(model, data)

@tool
def matplotlib_func(data: List[float]) -> str:
    """Generates plots using Matplotlib."""
    return matplotlib_func(data)

@tool
def requests_func(url: str) -> str:
    """Makes HTTP requests."""
    return requests_func(url)

@tool
def beautifulsoup_func(html: str) -> str:
    """Parses HTML content using BeautifulSoup."""
    return beautifulsoup_func(html)

@tool
def selenium_func(url: str) -> str:
    """Automates web browsing using Selenium."""
    return selenium_func(url)

@tool
def opencv_func(image_path: str) -> str:
    """Processes images using OpenCV."""
    return opencv_func(image_path)

@tool
def tensorflow_func(model: str, data: List[float]) -> str:
    """Runs TensorFlow models."""
    return tensorflow_func(model, data)

@tool
def flask_func(app_code: str) -> str:
    """Runs a Flask application."""
    return flask_func(app_code)

@tool
def django_func(project_code: str) -> str:
    """Runs a Django application."""
    return django_func(project_code)

@tool
def jupyter_func(notebook_code: str) -> str:
    """Executes Jupyter notebook code."""
    return jupyter_func(notebook_code)

@tool
def sqlalchemy_func(query: str) -> str:
    """Executes SQL queries using SQLAlchemy."""
    return sqlalchemy_func(query)

TOOLS = [
    pythonexecutor_func,
    pandas_func,
    numpy_func,
    scikit_learn_func,
    matplotlib_func,
    requests_func,
    beautifulsoup_func,
    selenium_func,
    opencv_func,
    tensorflow_func,
    flask_func,
    django_func,
    jupyter_func,
    sqlalchemy_func
]

# ---------------------------
# 3. Create Agent
# ---------------------------

system_prompt = (
    "You are Sevent, a PythonAutomator Agent designed to autonomously execute tasks "
    "by integrating Python for custom scripts, complex computations, data manipulation, "
    "and automation. You have access to various tools including Pandas, NumPy, Scikit-learn, "
    "Matplotlib, Requests, BeautifulSoup, Selenium, OpenCV, TensorFlow, Flask, Django, Jupyter, "
    "and SQLAlchemy. Your goal is to provide flexible and tailored solutions for data analysis, "
    "machine learning deployment, task automation, and technical challenges."
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
    response = agent.invoke(
        {"messages": [HumanMessage(content=query)]}
    )
    return response

# ---------------------------
# 5. Test Agent Execution
# ---------------------------

if __name__ == "__main__":
    print(f"\n--- Running Agent: Sevent (Model: {MODEL}) ---")
    print("Description: A PythonAutomator Agent for executing tasks.")
    print("----\n")

    test_query = "Analyze the following dataset and provide insights."
    try:
        output = run(test_query)
        print("Final Output:\n", output)
    except Exception as e:
        print(f"Agent Execution Failed: {e}")