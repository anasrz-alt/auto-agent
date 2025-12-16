from typing import Any, Dict
import os

def pandas_func(query: str, files: dict | None = None) -> str:
    """Processes a user query to extract information or perform tasks based on provided files. 
    The function accepts a query string and an optional dictionary of files, returning a string 
    with the result or an error message if files are required but not provided.

    Args:
        query (str): The user query specifying the task to perform.
        files (dict | None): A dictionary mapping filenames to their content as strings or bytes.

    Returns:
        str: The result of processing the query, or an error message if applicable.
    """
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
        return "Error: No files provided. Please supply a dictionary of files."

    parsed_data = {}
    for filename, content in files.items():
        if isinstance(content, bytes):
            content = content.decode('utf-8', errors='ignore')  # Safely decode bytes
        if filename.endswith('.json'):
            try:
                parsed_data[filename] = json.loads(content)
            except json.JSONDecodeError:
                return f"Error: Failed to parse JSON from {filename}."
        elif filename.endswith('.csv'):
            try:
                parsed_data[filename] = list(csv.reader(StringIO(content)))
            except Exception:
                return f"Error: Failed to parse CSV from {filename}."
        elif filename.endswith('.txt') or filename.endswith('.md'):
            parsed_data[filename] = content.splitlines()
        else:
            return f"Error: Unsupported file type for {filename}."

    # Step 4: Select strategy based on intent and available files
    if intent == "summarize":
        summaries = {filename: "\n".join(content[:3]) + '...' for filename, content in parsed_data.items()}
        result = json.dumps(summaries)
        return f"Summarized content:\n{result}\nSTEPS: [Parsed files, Summarized content]"

    elif intent == "extract":
        # Example extraction logic (could be enhanced)
        extracted = {filename: content for filename, content in parsed_data.items() if isinstance(content, list)}
        result = json.dumps(extracted)
        return f"Extracted data:\n{result}\nSTEPS: [Parsed files, Extracted data]"

    elif intent == "transform":
        # Example transformation logic (could be enhanced)
        transformed = {filename: [line.upper() for line in content] for filename, content in parsed_data.items()}
        result = json.dumps(transformed)
        return f"Transformed data:\n{result}\nSTEPS: [Parsed files, Transformed data]"

    elif intent == "calculate":
        # Example calculation logic (could be enhanced)
        calculations = {filename: len(content) for filename, content in parsed_data.items()}
        result = json.dumps(calculations)
        return f"Calculated lengths:\n{result}\nSTEPS: [Parsed files, Calculated lengths]"

    elif intent == "search":
        # Example search logic (could be enhanced)
        search_results = {filename: [line for line in content if query in line] for filename, content in parsed_data.items()}
        result = json.dumps(search_results)
        return f"Search results:\n{result}\nSTEPS: [Parsed files, Searched content]"

    return "Error: No valid intent detected from the query."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "Pandas",
        "description": "A library for data manipulation and analysis, providing data structures like DataFrames.",
        "function": pandas_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")