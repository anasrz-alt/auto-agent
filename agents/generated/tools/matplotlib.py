from typing import Any, Dict
import os

def matplotlib_func(query: str, files: dict | None = None) -> str:
    """A versatile tool for processing user queries related to files, enabling summarization, extraction, transformation, and basic computations. 
    Accepts a user query and optional files, returning a string response with results or error messages.

    Args:
        query (str): The user query specifying the task to perform.
        files (dict | None): A dictionary mapping filenames to their content as strings or bytes.

    Returns:
        str: A response string containing the result of the query or an error message.
    """
    import json
    import re

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: The query must be a non-empty string."
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
    else:
        return "Error: Unable to determine the intent from the query."

    # Step 3: Handle files if provided
    file_contents = {}
    if files:
        for filename, content in files.items():
            if isinstance(content, bytes):
                content = content.decode(errors='ignore')
            file_contents[filename] = content

    # Step 4: Select strategy based on intent and available files
    if intent == "summarize":
        if not file_contents:
            return "Error: No files provided to summarize. Please provide files."
        summaries = {filename: content[:100] + '...' for filename, content in file_contents.items()}  # Simple summary
        return f"Summaries: {json.dumps(summaries)}"

    elif intent == "extract":
        if not file_contents:
            return "Error: No files provided to extract from. Please provide files."
        extracted_data = {}
        for filename, content in file_contents.items():
            matches = re.findall(r'\b\w+\b', content)  # Extract words as a simple example
            extracted_data[filename] = matches
        return f"Extracted Data: {json.dumps(extracted_data)}"

    elif intent == "transform":
        if not file_contents:
            return "Error: No files provided to transform. Please provide files."
        transformed_data = {filename: content.upper() for filename, content in file_contents.items()}  # Simple transformation
        return f"Transformed Data: {json.dumps(transformed_data)}"

    elif intent == "calculate":
        return "Error: Calculation requests are not supported without specific data."

    # Step 5: Handle unexpected cases
    return "Error: The query could not be processed."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "Matplotlib",
        "description": "A plotting library for Python that provides an object-oriented API for embedding plots into applications.",
        "function": matplotlib_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")