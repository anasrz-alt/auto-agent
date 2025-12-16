from typing import Any, Dict
import os

import json
import pandas as pd
from typing import Dict, Union

def dataparser_func(input: str, files: Dict[str, Union[str, bytes]] = None) -> str:
    """
    Parses and structures data from various formats for further analysis. 
    The function accepts a user query and optional files, detects the intent, 
    and returns a structured response based on the input and file contents.

    Args:
        input (str): User input query describing the desired operation.
        files (dict | None): Optional dictionary mapping filenames to their contents.

    Returns:
        str: A structured response based on the input and any provided files.
    """
    
    # Step 1: Validate inputs and normalize the query
    if not isinstance(input, str) or not input.strip():
        return "Invalid input: Please provide a non-empty string query."
    
    query = input.strip().lower()
    
    # Step 2: Detect user intent
    if "summarize" in query:
        intent = "summarize"
    elif "extract" in query:
        intent = "extract"
    elif "transform" in query:
        intent = "transform"
    else:
        intent = "unknown"
    
    # Step 3: If files are provided, detect and parse file types
    data_frames = {}
    if files:
        for filename, content in files.items():
            try:
                if filename.endswith('.json'):
                    data_frames[filename] = pd.json_normalize(json.loads(content))
                elif filename.endswith('.csv'):
                    data_frames[filename] = pd.read_csv(pd.compat.StringIO(content.decode('utf-8')))
                else:
                    return f"Unsupported file type for {filename}."
            except Exception as e:
                return f"Error parsing {filename}: {str(e)}"
    
    # Step 4: Select a strategy based on intent and available files
    if intent == "summarize":
        if data_frames:
            summary = {filename: df.describe().to_dict() for filename, df in data_frames.items()}
            return json.dumps(summary, indent=2)
        else:
            return "No files provided to summarize."
    
    elif intent == "extract":
        if data_frames:
            extracted_data = {filename: df.head().to_dict() for filename, df in data_frames.items()}
            return json.dumps(extracted_data, indent=2)
        else:
            return "No files provided to extract data from."
    
    elif intent == "transform":
        return "Transformation intent detected, but no specific transformation defined."
    
    else:
        return "Unknown intent. Please specify a valid operation (summarize, extract, transform)."

# Unit tests
def test_dataparser_func():
    # Test case 1: Summarize JSON data
    json_data = '{"name": ["Alice", "Bob"], "age": [25, 30]}'
    result = dataparser_func("summarize the data", {"data.json": json_data})
    assert "count" in result, "Test case 1 failed."

    # Test case 2: Extract CSV data
    csv_data = "name,age\nAlice,25\nBob,30"
    result = dataparser_func("extract data", {"data.csv": csv_data.encode('utf-8')})
    assert "Alice" in result, "Test case 2 failed."

    # Test case 3: Invalid input
    result = dataparser_func("", None)
    assert result == "Invalid input: Please provide a non-empty string query.", "Test case 3 failed."

    # Test case 4: Unsupported file type
    result = dataparser_func("summarize", {"data.txt": "some text"})
    assert result == "Unsupported file type for data.txt.", "Test case 4 failed."

    # Test case 5: Unknown intent
    result = dataparser_func("do something", None)
    assert result == "Unknown intent. Please specify a valid operation (summarize, extract, transform).", "Test case 5 failed."

    print("All test cases passed.")

# Uncomment to run tests
# test_dataparser_func()
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "DataParser",
        "description": "Parses and structures data from various formats for further analysis.",
        "function": dataparser_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")