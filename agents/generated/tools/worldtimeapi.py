from typing import Any, Dict
import os

def worldtimeapi_func(input: str, files: dict | None = None) -> str:
    """Fetches the current time for a specified city using the WorldTimeAPI. 
    The input should be the name of the city or a geographical location. 
    If files are provided, they can contain additional context or location information. 
    Returns the current time in the specified city or an error message if the city is not found."""
    
    import requests

    # Step 1: Validate inputs and normalize the query
    city = input.strip()
    if not city:
        return "Error: No city name provided."

    # Step 2: Detect user intent (in this case, always fetching time)
    # Intent is clear: we want to get the current time for the provided city.

    # Step 3: If `files` is provided, detect and parse file types (not implemented in this case)
    # For simplicity, we will not process files in this implementation.

    # Step 4: Construct the API URL based on the city name
    api_url = f"http://worldtimeapi.org/api/timezone/{city}"
    
    try:
        # Step 5: Execute the API call
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses

        # Step 6: Process the response
        data = response.json()
        current_time = data['datetime']  # Extract the current time from the response
        return f"The current time in {city} is {current_time}."

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"  # Handle HTTP errors
    except requests.exceptions.RequestException as req_err:
        return f"Error occurred while making the request: {req_err}"  # Handle other request errors
    except KeyError:
        return "Error: Could not find the specified city. Please check the city name."  # Handle missing data
    except Exception as e:
        return f"An unexpected error occurred: {e}"  # Handle any other exceptions

# Example runs (not included in the function):
# print(worldtimeapi_func("Europe/London"))
# print(worldtimeapi_func("America/New_York"))
# print(worldtimeapi_func("Invalid/City"))

# Unit tests (not included in the function):
# assert worldtimeapi_func("Europe/London").startswith("The current time in Europe/London is")
# assert "Error: No city name provided." == worldtimeapi_func("")
# assert "Error: Could not find the specified city." in worldtimeapi_func("Invalid/City")
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "WorldTimeAPI",
        "description": "An API that provides current time information for cities around the world based on their geographical location.",
        "function": worldtimeapi_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")