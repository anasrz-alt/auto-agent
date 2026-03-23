from typing import Optional, List
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# ---------------------------
# 1. Model Configuration
# ---------------------------

MODEL = "openai/gpt-4o"
model = ChatOpenAI(model=MODEL, temperature=0.2)

# ---------------------------
# 2. Tool Definitions
# ---------------------------

@tool
def pythonexecutor_func(code: str) -> str:
    """Execute arbitrary Python code."""
    return exec(code)

@tool
def pandas_func(data: str) -> str:
    """Manipulate data using Pandas."""
    import pandas as pd
    return pd.read_csv(data).head().to_string()

@tool
def numpy_func(array: List[float]) -> str:
    """Perform operations with NumPy."""
    import numpy as np
    return np.mean(array)

@tool
def matplotlib_func(data: List[float]) -> str:
    """Create a plot using Matplotlib."""
    import matplotlib.pyplot as plt
    plt.plot(data)
    plt.savefig('plot.png')
    return "Plot saved as 'plot.png'."

@tool
def scikit_learn_func(model: str, data: List[float]) -> str:
    """Train a model using Scikit-learn."""
    from sklearn.linear_model import LinearRegression
    import numpy as np
    X = np.array(data).reshape(-1, 1)
    y = np.array([1, 2, 3])  # Dummy target
    reg = LinearRegression().fit(X, y)
    return f"Model trained with coefficients: {reg.coef_}"

@tool
def requests_func(url: str) -> str:
    """Make an HTTP request."""
    import requests
    response = requests.get(url)
    return response.text

@tool
def beautifulsoup_func(html: str) -> str:
    """Parse HTML using BeautifulSoup."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    return soup.title.string

@tool
def selenium_func(url: str) -> str:
    """Automate a web browser using Selenium."""
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.get(url)
    title = driver.title
    driver.quit()
    return title

@tool
def opencv_func(image_path: str) -> str:
    """Process an image using OpenCV."""
    import cv2
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('gray_image.png', gray_image)
    return "Gray image saved as 'gray_image.png'."

@tool
def tensorflow_func(model_path: str) -> str:
    """Load and use a TensorFlow model."""
    import tensorflow as tf
    model = tf.keras.models.load_model(model_path)
    return "TensorFlow model loaded."

@tool
def pytorch_func(model_path: str) -> str:
    """Load and use a PyTorch model."""
    import torch
    model = torch.load(model_path)
    return "PyTorch model loaded."

@tool
def flask_func(app_code: str) -> str:
    """Run a Flask application."""
    from flask import Flask
    app = Flask(__name__)
    exec(app_code)
    return "Flask app running."

@tool
def django_func(project_code: str) -> str:
    """Run a Django application."""
    import django
    exec(project_code)
    return "Django app running."

@tool
def sqlalchemy_func(query: str) -> str:
    """Execute a SQL query using SQLAlchemy."""
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///:memory:')
    with engine.connect() as connection:
        result = connection.execute(query)
        return str(result.fetchall())

@tool
def jupyter_func(code: str) -> str:
    """Execute code in Jupyter."""
    from IPython import get_ipython
    ipython = get_ipython()
    return ipython.run_cell(code).result

@tool
def gitpython_func(repo_path: str) -> str:
    """Interact with a Git repository."""
    import git
    repo = git.Repo(repo_path)
    return f"Current branch: {repo.active_branch.name}"

TOOLS = [
    pythonexecutor_func,
    pandas_func,
    numpy_func,
    matplotlib_func,
    scikit_learn_func,
    requests_func,
    beautifulsoup_func,
    selenium_func,
    opencv_func,
    tensorflow_func,
    pytorch_func,
    flask_func,
    django_func,
    sqlalchemy_func,
    jupyter_func,
    gitpython_func
]

# ---------------------------
# 3. Create Agent
# ---------------------------

agent = create_agent(
    model=model,
    tools=TOOLS,
    system_prompt="You are a helpful and reliable agent."
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
    test_query = "How can I analyze a dataset using Pandas?"
    print(f"Running Agent7T with query: {test_query}")
    output = run(test_query)
    print("Final Output:\n", output)