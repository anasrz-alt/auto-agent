from typing import Any, Dict
import os

import requests

def searchtool_func(input: str, files: dict | None = None) -> str:
    """
    A tool that enables the agent to perform web searches to gather supplementary information 
    about weather conditions or related topics. It takes a user query as input and optionally 
    a dictionary of files to search for relevant information. The output is a string containing 
    the search results or information extracted from the files.

    Args:
        input (str): The user's search query.
        files (dict | None): A dictionary mapping filenames to their content (string or bytes).

    Returns:
        str: A string with the search results or extracted information.
    """
    
    # Step 1: Validate inputs and normalize the query
    if not isinstance(input, str) or not input.strip():
        return "Invalid input: Please provide a non-empty search query."
    
    query = input.strip()
    
    # Step 2: Detect user intent (e.g., weather search)
    if "weather" in query.lower():
        return fetch_weather_info(query)
    
    # Step 3: If files are provided, detect and parse file types
    if files:
        for filename, content in files.items():
            if isinstance(content, bytes):
                content = content.decode('utf-8', errors='ignore')
            # Step 4: Search within files for relevant information
            if query.lower() in content.lower():
                return f"Found in {filename}: {content}"
    
    return "No relevant information found."

def fetch_weather_info(query: str) -> str:
    """
    Fetch weather information based on the user's query.

    Args:
        query (str): The user's search query related to weather.

    Returns:
        str: A string containing the weather information or an error message.
    """
    # Example API endpoint (replace with a real weather API)
    api_key = "your_api_key_here"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    # Extract city name from query (simple extraction, can be improved)
    city_name = query.split("weather in")[-1].strip() if "weather in" in query else query
    
    try:
        response = requests.get(base_url, params={"q": city_name, "appid": api_key, "units": "metric"})
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        
        # Extract relevant weather information
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"The current weather in {city_name} is {weather_description} with a temperature of {temperature}°C."
    
    except requests.RequestException as e:
        return f"Error fetching weather data: {str(e)}"
    except KeyError:
        return "Error: Unexpected data format received from the weather API."

# Example runs
print(searchtool_func("What's the weather in New York?"))
print(searchtool_func("Tell me about the weather in London."))

# Unit tests
def test_searchtool_func():
    assert searchtool_func("What's the weather in New York?") == "The current weather in New York is ..."
    assert searchtool_func("weather in London") == "The current weather in London is ..."
    assert searchtool_func("") == "Invalid input: Please provide a non-empty search query."
    assert searchtool_func("Search for something") == "No relevant information found."
    assert searchtool_func("weather in Paris", {"file1.txt": "This is a test file."}) == "No relevant information found."
    
test_searchtool_func()
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "SearchTool",
        "description": "A tool that enables the agent to perform web searches to gather supplementary information about weather conditions or related topics.",
        "function": searchtool_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")