from typing import Any, Dict
import os

import requests
from datetime import datetime
from typing import Dict, Optional

def timezoneapi_func(input: str, files: Optional[Dict[str, str]] = None) -> str:
    """
    This function retrieves the current time and timezone information for a specified city.
    It accepts a city name as input and optionally a dictionary of files. The output is a 
    string containing the city's timezone and current time or an error message if the city 
    is not found or if there are issues with the API call.
    
    :param input: The name of the city for which to retrieve timezone information.
    :param files: Optional dictionary mapping filename to file content (not used in this implementation).
    :return: A string with the current time and timezone information or an error message.
    """
    
    # Step 1: Validate input and normalize the query
    city = input.strip()
    if not city:
        return "Error: No city name provided."
    
    # Step 2: Define the API endpoint and parameters
    api_url = "http://worldtimeapi.org/api/timezone"
    
    # Step 3: Detect user intent (in this case, always fetching timezone info)
    try:
        # Step 4: Make the API call to fetch timezone data
        response = requests.get(f"{api_url}/{city}")
        response.raise_for_status()  # Raise an error for bad responses
        
        # Step 5: Process the response
        data = response.json()
        timezone = data['timezone']
        current_time = datetime.fromisoformat(data['datetime'][:-1])  # Remove 'Z' and convert
        
        # Step 6: Format the result
        result = f"The current time in {city} is {current_time.strftime('%Y-%m-%d %H:%M:%S')} in the timezone {timezone}."
        return result
    
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except KeyError:
        return "Error: Could not retrieve timezone information for the specified city."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Example runs
print(timezoneapi_func("America/New_York"))
print(timezoneapi_func("Europe/London"))
print(timezoneapi_func("Invalid/City"))

# Unit tests
def test_timezoneapi_func():
    assert "The current time in America/New_York" in timezoneapi_func("America/New_York")
    assert "The current time in Europe/London" in timezoneapi_func("Europe/London")
    assert timezoneapi_func("") == "Error: No city name provided."
    assert "Error: Could not retrieve timezone information" in timezoneapi_func("Invalid/City")

test_timezoneapi_func()
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "TimeZoneAPI",
        "description": "A tool that provides current time and timezone information for cities around the world.",
        "function": timezoneapi_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")