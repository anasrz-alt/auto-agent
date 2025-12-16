from typing import Any, Dict
import os

import requests

def geolocationapi_func(input: str, files: dict | None = None) -> str:
    """Retrieve geographical coordinates of a city based on its name.
    
    Args:
        input (str): The name of the city to retrieve coordinates for.
        files (dict | None): Optional; a dictionary mapping filenames to their content.
    
    Returns:
        str: A formatted string with the city's name and its latitude and longitude, or an error message.
    """
    
    # Step 1: Validate inputs and normalize the query
    if not isinstance(input, str) or not input.strip():
        return "Error: Invalid city name provided."
    
    city_name = input.strip()
    
    # Step 2: Detect user intent (in this case, always to fetch coordinates)
    # No additional intent detection needed as the function is specific to geolocation.
    
    # Step 3: If `files` is provided, check for relevant content (not used in this case)
    if files:
        # For future extensions, we could parse files for city names.
        pass
    
    # Step 4: Prepare to call the geolocation API
    api_url = f"http://api.positionstack.com/v1/forward?access_key=YOUR_ACCESS_KEY&query={city_name}"
    
    try:
        # Step 5: Execute the API call
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses
        
        data = response.json()
        
        # Check if the response contains valid data
        if 'data' in data and data['data']:
            coordinates = data['data'][0]
            latitude = coordinates['latitude']
            longitude = coordinates['longitude']
            return f"{city_name}: Latitude: {latitude}, Longitude: {longitude}"
        else:
            return f"Error: No geographical data found for '{city_name}'."
    
    except requests.RequestException as e:
        return f"Error: Unable to fetch data due to network issues: {str(e)}"
    except Exception as e:
        return f"Error: An unexpected error occurred: {str(e)}"
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "GeolocationAPI",
        "description": "An API that retrieves the geographical coordinates of a city based on its name, enabling accurate time retrieval.",
        "function": geolocationapi_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")