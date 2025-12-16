from typing import Any, Dict
import os

import requests

def timezonedatabaseapi_func(input: str, files: dict | None = None) -> str:
    """Fetches timezone information based on user input, allowing conversion between local time and UTC.
    
    Args:
        input (str): A string containing the timezone query or local time to convert.
        files (dict | None): Optional dictionary mapping filename to file content for additional context.
    
    Returns:
        str: A human-readable string with the timezone information or conversion result.
    """
    
    # Step 1: Validate inputs and normalize the query
    input = input.strip()
    if not input:
        return "Error: Input cannot be empty."

    # Step 2: Detect user intent
    if "convert" in input.lower():
        intent = "convert"
    elif "timezone" in input.lower():
        intent = "fetch_timezone"
    else:
        return "Error: Unrecognized query. Please specify 'convert' or 'timezone'."

    # Step 3: If files are provided, parse file types (currently not implemented)
    if files:
        # Placeholder for future file processing
        pass

    # Step 4: Execute based on detected intent
    try:
        if intent == "convert":
            # Extract local time and timezone from the input
            parts = input.split(" ")
            local_time = parts[1]  # Assuming the format "convert <time> <timezone>"
            timezone = parts[2]
            return convert_time_to_utc(local_time, timezone)
        elif intent == "fetch_timezone":
            return fetch_timezone_info(input)
    except Exception as e:
        return f"Error: {str(e)}"

def convert_time_to_utc(local_time: str, timezone: str) -> str:
    """Converts local time to UTC based on the provided timezone."""
    try:
        url = f"http://api.timezonedb.com/v2.1/get-time-zone?key=YOUR_API_KEY&format=json&by=zone&zone={timezone}"
        response = requests.get(url)
        data = response.json()
        
        if data.get("status") != "OK":
            return f"Error: {data.get('message', 'Unable to fetch timezone data.')}"
        
        # Here you would convert the local_time to UTC based on the timezone offset
        # This is a placeholder for actual conversion logic
        utc_time = f"Converted {local_time} in {timezone} to UTC (placeholder)"
        return utc_time
    except requests.RequestException:
        return "Error: Failed to connect to the timezone database API."

def fetch_timezone_info(query: str) -> str:
    """Fetches timezone information based on the query."""
    try:
        url = f"http://api.timezonedb.com/v2.1/get-time-zone?key=YOUR_API_KEY&format=json&by=zone&zone={query}"
        response = requests.get(url)
        data = response.json()
        
        if data.get("status") != "OK":
            return f"Error: {data.get('message', 'Unable to fetch timezone data.')}"
        
        return f"Timezone: {data['zoneName']}, GMT Offset: {data['gmtOffset']}, Current Time: {data['formatted']}"
    except requests.RequestException:
        return "Error: Failed to connect to the timezone database API."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "TimezoneDatabaseAPI",
        "description": "An API that offers timezone information, allowing the agent to convert local times to UTC and vice versa.",
        "function": timezonedatabaseapi_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")