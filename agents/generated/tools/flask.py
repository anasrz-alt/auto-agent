from typing import Any, Dict
import os

def flask_func(query: str, files: dict | None = None) -> str:
    """Processes a user query to answer questions or perform tasks based on provided files. 
    Accepts a query string and an optional dictionary of files (filename -> content). 
    Returns a string with the result or an error message if files are needed but not provided."""
    
    import json
    
    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: Query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize query
    
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
    if files is not None:
        file_contents = {}
        for filename, content in files.items():
            if isinstance(content, bytes):
                file_contents[filename] = content.decode('utf-8', errors='ignore')
            else:
                file_contents[filename] = content
        
        # Example: Simple parsing for common file types
        parsed_data = {}
        for filename, content in file_contents.items():
            if filename.endswith('.json'):
                try:
                    parsed_data[filename] = json.loads(content)
                except json.JSONDecodeError:
                    return f"Error: Invalid JSON in file {filename}."
            elif filename.endswith('.csv'):
                parsed_data[filename] = [line.split(',') for line in content.splitlines()]
            elif filename.endswith('.md') or filename.endswith('.txt'):
                parsed_data[filename] = content.splitlines()
    
    # Step 4: Select a strategy based on intent and available files
    if intent == "summarize" and files:
        summary = "\n".join(content[:3] for content in parsed_data.values() if isinstance(content, list))
        result = f"Summary:\n{summary}"
    elif intent == "extract" and files:
        extracted_data = {filename: content for filename, content in parsed_data.items() if isinstance(content, list)}
        result = f"Extracted Data (JSON): {json.dumps(extracted_data)}"
    elif intent == "calculate":
        # Placeholder for calculation logic
        result = "Calculation results are not implemented."
    else:
        if files is None:
            return "Error: No files provided for processing. Please supply files as a dictionary."
        result = "Error: Unrecognized intent or insufficient data."
    
    # Step 5: Produce a clear result string
    return f"{result}\n\nSTEPS:\n- Validated input query.\n- Detected intent: {intent}.\n- Processed files: {list(files.keys()) if files else 'None'}.\n- Generated result."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "Flask",
        "description": "A lightweight WSGI web application framework in Python for building web applications quickly.",
        "function": flask_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")