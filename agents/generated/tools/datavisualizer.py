from typing import Any, Dict
import os

def datavisualizer_func(query: str, files: dict | None = None) -> str:
    """A tool that analyzes user queries and reads provided files to answer questions, extract data, or perform tasks. 
    It accepts a query string and an optional dictionary of files, returning a string with the result or an error message.

    Args:
        query (str): The user's request or question regarding data or files.
        files (dict | None): A dictionary mapping filenames to their content as strings or bytes.

    Returns:
        str: A response string containing the answer, extracted data, or an error message.
    """
    import json
    import csv
    from io import StringIO

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: Query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize query for easier processing

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
        parsed_data = {}
        for filename, content in files.items():
            if isinstance(content, bytes):
                content = content.decode('utf-8', errors='ignore')  # Decode bytes safely
            if filename.endswith('.json'):
                try:
                    parsed_data[filename] = json.loads(content)
                except json.JSONDecodeError:
                    return f"Error: Invalid JSON in file '{filename}'."
            elif filename.endswith('.csv'):
                try:
                    parsed_data[filename] = list(csv.reader(StringIO(content)))
                except Exception:
                    return f"Error: Invalid CSV in file '{filename}'."
            elif filename.endswith('.txt') or filename.endswith('.md'):
                parsed_data[filename] = content.splitlines()
            else:
                return f"Error: Unsupported file type for '{filename}'."

    # Step 4: Select strategy based on intent and available files
    if intent == "summarize" and parsed_data:
        summary = {filename: data[:2] for filename, data in parsed_data.items()}  # Simple summary
        result = f"Summary of files: {json.dumps(summary)}"
    elif intent == "extract" and parsed_data:
        extracted = {filename: data for filename, data in parsed_data.items() if isinstance(data, list) and data}
        result = f"Extracted data: {json.dumps(extracted)}"
    elif intent == "calculate":
        result = "Error: Calculation requires specific data context."
    elif intent == "transform":
        result = "Error: Transformation requires specific data context."
    elif intent == "search":
        result = "Error: Searching requires specific data context."
    else:
        # Step 5: Handle missing files case
        if not files:
            return "Error: No files provided. Please supply files to analyze."
        result = "Error: Unable to determine intent or process files."

    # Step 6: Produce a clear result string
    return f"{result}\nSTEPS: - Validated input\n - Detected intent\n - Processed files\n - Generated result"
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "DataVisualizer",
        "description": "A tool that creates visual representations of data, helping the agent to present insights and findings in an understandable format.",
        "function": datavisualizer_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")