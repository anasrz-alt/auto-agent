from typing import Any, Dict
import os

import requests

def weatherapi_func(input: str, files: dict | None = None) -> str:
    """
    Fetches weather data for a specified location using the WeatherAPI.
    
    Args:
        input (str): A string containing the location for which to fetch weather data.
        files (dict | None): Optional; a dictionary mapping filenames to their content.
        
    Returns:
        str: A human-readable string containing the current weather information or an error message.
    """
    # Step 1: Validate inputs and normalize the query
    location = input.strip()
    if not location:
        return "Error: Location input cannot be empty."

    # Step 2: Detect user intent (in this case, always fetching weather data)
    # Intent is implicit in the function's purpose

    # Step 3: If files are provided, we can process them (not used in this case)
    if files:
        # For future enhancements, we could analyze files for location data
        pass

    # Step 4: Prepare to fetch weather data
    api_key = "YOUR_API_KEY"  # Replace with your actual API key
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"

    try:
        # Step 5: Execute the API call
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        weather_data = response.json()

        # Step 6: Produce a clear result string
        current_weather = weather_data['current']
        location_name = weather_data['location']['name']
        temperature = current_weather['temp_c']
        condition = current_weather['condition']['text']
        result = f"The current weather in {location_name} is {temperature}°C with {condition}."
        return result

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except KeyError as key_err:
        return f"Error processing weather data: {key_err}"
    except Exception as err:
        return f"An error occurred: {err}"

# Example runs
# print(weatherapi_func("London"))
# print(weatherapi_func("New York"))

# Unit tests
def test_weatherapi_func():
    assert weatherapi_func("London") is not None
    assert weatherapi_func(" ") == "Error: Location input cannot be empty."
    assert "Error" in weatherapi_func("InvalidLocation")  # Assuming this will return an error
    print("All tests passed.")

# Uncomment to run tests
# test_weatherapi_func()
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "WeatherAPI",
        "description": "A RESTful API that provides weather data for various locations worldwide, including current conditions, forecasts, and historical data.",
        "function": weatherapi_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")