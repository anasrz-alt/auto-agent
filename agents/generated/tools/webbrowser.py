from typing import Any, Dict
import os

import requests

def webbrowser_func(input: str, files: dict | None = None) -> str:
    """
    This function facilitates browsing and downloading web-sourced information based on the user's input.
    It accepts a query string to determine the intent (search, download, etc.) and optionally a dictionary of files.
    The output is a string containing the relevant information or an error message if the process fails.

    Args:
        input (str): The user's query or command for web browsing.
        files (dict | None): A dictionary mapping filenames to their content (string or bytes).

    Returns:
        str: The result of the web browsing operation or an error message.
    """
    
    # Stage 1: Validate inputs and normalize the query
    if not isinstance(input, str) or not input.strip():
        return "Error: Input query must be a non-empty string."
    
    query = input.strip().lower()
    
    # Stage 2: Detect user intent
    if "download" in query:
        return handle_download(query)
    elif "search" in query:
        return handle_search(query)
    else:
        return "Error: Unrecognized command. Please use 'search' or 'download'."

def handle_download(query: str) -> str:
    """Handles download requests based on the user's query."""
    try:
        url = query.split("download")[-1].strip()
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return f"Downloaded content from {url}:\n{response.text[:200]}..."  # Return a snippet of the content
    except requests.RequestException as e:
        return f"Error during download: {str(e)}"

def handle_search(query: str) -> str:
    """Handles search requests based on the user's query."""
    try:
        search_term = query.split("search")[-1].strip()
        # Example API for searching (replace with a real API if needed)
        response = requests.get(f"https://api.example.com/search?q={search_term}")
        response.raise_for_status()
        results = response.json()  # Assuming the response is in JSON format
        return f"Search results for '{search_term}': {results.get('results', 'No results found.')}"
    except requests.RequestException as e:
        return f"Error during search: {str(e)}"

# Unit tests
def test_webbrowser_func():
    assert webbrowser_func("search Python programming") == "Error: Unrecognized command. Please use 'search' or 'download'."
    assert webbrowser_func("download https://www.example.com") == "Downloaded content from https://www.example.com:\n"  # This would depend on the actual content
    assert webbrowser_func("") == "Error: Input query must be a non-empty string."
    assert webbrowser_func("download invalid_url") == "Error during download: Invalid URL 'invalid_url': No schema supplied. Perhaps you meant http://invalid_url?"

# Uncomment to run tests
# test_webbrowser_func()
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "WebBrowser",
        "description": "Facilitates browsing and downloading web-sourced information from various online resources.",
        "function": webbrowser_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")