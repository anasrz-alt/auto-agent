from typing import Any, Dict
import os

def datavisualizationtool_func(query: str, files: dict | None = None) -> str:
    """A tool for creating visual representations of data to facilitate understanding and insights. 
    It accepts a user query and optional files, processes the query to determine intent, and 
    returns a response based on the content of the files or the query itself.

    Args:
        query (str): The user query describing the desired action or information.
        files (dict | None): A dictionary mapping filenames to their content as strings or bytes.

    Returns:
        str: A response string containing the result of the query processing.
    """
    import json

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: Query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize query to lowercase

    # Step 2: Detect user intent
    intent = None
    if "summarize" in query:
        intent = "summarize"
    elif "extract" in query:
        intent = "extract"
    elif "transform" in query:
        intent = "transform"
    elif "generate" in query:
        intent = "generate"
    elif "search" in query:
        intent = "search"
    elif "calculate" in query:
        intent = "calculate"
    else:
        return "Error: Unable to determine intent from query."

    # Step 3: Handle files if provided
    if files is None or not files:
        return "Error: No files provided. Please supply a dictionary of files."

    parsed_data = {}
    for filename, content in files.items():
        try:
            if filename.endswith('.json'):
                parsed_data[filename] = json.loads(content)
            elif filename.endswith('.csv'):
                parsed_data[filename] = [line.split(',') for line in content.decode().splitlines()]
            elif filename.endswith('.md') or filename.endswith('.txt'):
                parsed_data[filename] = content.decode().splitlines()
            else:
                return f"Error: Unsupported file type for {filename}."
        except Exception as e:
            return f"Error: Failed to parse {filename}. Reason: {str(e)}"

    # Step 4: Select strategy based on intent and available files
    if intent == "summarize":
        summaries = {filename: data[:3] for filename, data in parsed_data.items()}  # Example: first 3 lines
        result = json.dumps(summaries)
    elif intent == "extract":
        result = json.dumps({filename: data for filename, data in parsed_data.items()})
    elif intent == "transform":
        result = "Transformation not implemented yet."
    elif intent == "generate":
        result = "Generation not implemented yet."
    elif intent == "search":
        result = "Search functionality not implemented yet."
    elif intent == "calculate":
        result = "Calculation functionality not implemented yet."
    else:
        return "Error: Unsupported intent."

    # Step 5: Produce a clear result string
    response = f"Result: {result}\nSTEPS:\n- Validated input\n- Determined intent\n- Parsed files\n- Executed strategy"
    return response
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "DataVisualizationTool",
        "description": "A tool for creating visual representations of data to facilitate understanding and insights.",
        "function": datavisualizationtool_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")