from typing import Any, Dict
import os

def datastorage_func(query: str, files: dict | None = None) -> str:
    """Processes user queries to extract information from provided files or perform tasks. 
    Accepts a query string and an optional dictionary of files (filename -> content). 
    Returns a string with the result or an error message if files are required but not provided."""
    
    import json
    import csv
    from io import StringIO

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: Query must be a non-empty string."
    
    query = query.strip().lower()

    # Step 2: Detect user intent
    intent = None
    if "summarize" in query:
        intent = "summarize"
    elif "extract" in query:
        intent = "extract"
    elif "transform" in query:
        intent = "transform"
    elif "calculate" in query:
        intent = "calculate"
    elif "search" in query:
        intent = "search"
    
    # Step 3: Handle files if provided
    if files is None:
        return "Error: No files provided. Please supply a dictionary of files (filename -> content)."

    # Step 4: Parse files
    parsed_data = {}
    for filename, content in files.items():
        try:
            if filename.endswith('.json'):
                parsed_data[filename] = json.loads(content)
            elif filename.endswith('.csv'):
                parsed_data[filename] = list(csv.reader(StringIO(content)))
            elif filename.endswith('.md') or filename.endswith('.txt'):
                parsed_data[filename] = content.splitlines()
            else:
                parsed_data[filename] = content  # Treat as plain text
        except Exception as e:
            return f"Error parsing file {filename}: {str(e)}"

    # Step 5: Execute the strategy based on intent
    if intent == "summarize":
        summaries = {filename: "\n".join(data[:3]) + "..." for filename, data in parsed_data.items()}
        result = f"Summaries: {summaries}"
    elif intent == "extract":
        extracted = {filename: data for filename, data in parsed_data.items() if isinstance(data, list) and data}
        result = f"Extracted Data: {json.dumps(extracted)}"
    elif intent == "transform":
        transformed = {filename: [line.upper() for line in data] for filename, data in parsed_data.items()}
        result = f"Transformed Data: {json.dumps(transformed)}"
    elif intent == "calculate":
        # Placeholder for calculation logic
        result = "Calculation feature is not implemented yet."
    elif intent == "search":
        result = "Search feature is not implemented yet."
    else:
        return "Error: Unrecognized intent. Please specify a clear action."

    # Step 6: Produce a clear result string
    return f"Result: {result}\nSTEPS: [Validated input, Detected intent, Parsed files, Executed strategy]"
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "DataStorage",
        "description": "A system for storing processed data, insights, and metadata for future reference.",
        "function": datastorage_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")