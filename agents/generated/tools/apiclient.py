from typing import Any, Dict
import os

import requests

def apiclient_func(input: str, files: dict | None = None) -> str:
    """
    Fetches publication data and statistics for a specified professor from an external API.
    
    Args:
        input (str): The name of the professor whose publication data is requested.
        files (dict | None): Optional dictionary mapping filenames to file content, not used in this implementation.
        
    Returns:
        str: A summary of the professor's publication data or an error message if the request fails.
    """
    
    # Step 1: Validate inputs and normalize the query
    if not isinstance(input, str) or not input.strip():
        return "Error: Invalid input. Please provide a valid professor's name."
    
    professor_name = input.strip()
    
    # Step 2: Detect user intent (for this tool, it's always to fetch data)
    # No additional intent detection needed as this tool's purpose is clear.
    
    # Step 3: If `files` is provided, we would parse them, but we won't use them here.
    
    # Step 4: Construct API request
    api_url = f"https://api.example.com/publications?professor={professor_name}"
    
    try:
        # Step 5: Execute the API request
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Step 6: Process the response
        data = response.json()
        if 'publications' not in data:
            return "Error: No publication data found for the specified professor."
        
        # Format the output
        publications = data['publications']
        output = f"Publications for {professor_name}:\n"
        for pub in publications:
            output += f"- {pub['title']} ({pub['year']})\n"
        
        return output.strip()  # Return the formatted string
    
    except requests.exceptions.RequestException as e:
        return f"Error: Unable to fetch data. {str(e)}"
    except Exception as e:
        return f"Error: An unexpected error occurred. {str(e)}"

# Example runs
print(apiclient_func("John Doe"))
print(apiclient_func(""))

# Unit tests
def test_apiclient_func():
    assert apiclient_func("John Doe") == "Publications for John Doe:\n- Example Title (2023)\n"
    assert apiclient_func("") == "Error: Invalid input. Please provide a valid professor's name."
    assert apiclient_func("Nonexistent Professor") == "Error: No publication data found for the specified professor."
    
# Uncomment to run tests
# test_apiclient_func()
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "APIClient",
        "description": "A tool that interacts with external APIs to fetch publication data and statistics for the specified professor.",
        "function": apiclient_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")