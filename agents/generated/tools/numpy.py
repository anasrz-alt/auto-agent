from typing import Any, Dict
import os

def numpy_func(query: str, files: dict | None = None) -> str:
    """Processes a user query to answer questions or perform tasks using provided file content. 
    The function accepts a query string and an optional dictionary of files, returning a string 
    that contains the result or an error message if files are required but not provided.

    Args:
        query (str): The user's query regarding the task or information needed.
        files (dict | None): A dictionary mapping filenames to their content as strings or bytes.

    Returns:
        str: The result of processing the query, or an error message if applicable.
    """
    import json
    import csv
    from io import StringIO

    # Step 1: Validate inputs and normalize the query
    query = query.strip().lower()
    if not query:
        return "Error: Query cannot be empty."

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

    # Step 3: Handle missing files if needed
    if intent in ["extract", "transform", "calculate"] and files is None:
        return "Error: No files provided. Please supply files for processing."

    # Step 4: Parse files if provided
    parsed_data = {}
    if files:
        for filename, content in files.items():
            if isinstance(content, bytes):
                content = content.decode('utf-8', errors='ignore')
            if filename.endswith('.json'):
                try:
                    parsed_data[filename] = json.loads(content)
                except json.JSONDecodeError:
                    return f"Error: Invalid JSON in file {filename}."
            elif filename.endswith('.csv'):
                try:
                    parsed_data[filename] = list(csv.reader(StringIO(content)))
                except Exception:
                    return f"Error: Failed to parse CSV in file {filename}."
            elif filename.endswith('.txt') or filename.endswith('.md'):
                parsed_data[filename] = content.splitlines()
            else:
                return f"Error: Unsupported file type for {filename}."

    # Step 5: Execute the strategy based on intent
    result = ""
    if intent == "summarize":
        result = "\n".join(line for data in parsed_data.values() for line in data[:3])  # Simple summary
    elif intent == "extract":
        result = json.dumps({k: v[:3] for k, v in parsed_data.items()})  # Extract first 3 lines/entries
    elif intent == "transform":
        result = "\n".join(data.upper() for data in parsed_data.values() if isinstance(data, list))  # Example transformation
    elif intent == "calculate":
        result = "Calculation results would go here."  # Placeholder for calculations
    elif intent == "search":
        result = "Search results would go here."  # Placeholder for search results

    # Step 6: Produce a clear result string
    return f"Result: {result}\nSTEPS: - Validated input\n- Detected intent: {intent}\n- Parsed files: {list(files.keys())}\n- Executed strategy."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "NumPy",
        "description": "A library for numerical computing in Python, offering support for large, multi-dimensional arrays and matrices.",
        "function": numpy_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")