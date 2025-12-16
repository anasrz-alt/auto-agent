from typing import Any, Dict
import os

def opencv_func(query: str, files: dict | None = None) -> str:
    """Processes user queries related to image processing tasks, utilizing provided file contents if available. 
    Accepts a query string and an optional dictionary of files, returning a string response with the result or an error message.
    
    Args:
        query (str): The user query describing the task to perform.
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
    elif "search" in query:
        intent = "search"
    else:
        return "Error: Unable to determine the intent from the query."

    # Step 3: Handle files if provided
    file_contents = {}
    if files:
        for filename, content in files.items():
            if isinstance(content, bytes):
                try:
                    content = content.decode('utf-8')
                except Exception:
                    return f"Error: Unable to decode file '{filename}'."
            file_contents[filename] = content

    # Step 4: Select strategy based on intent and available files
    if intent == "summarize" and file_contents:
        summaries = {filename: content[:100] + '...' for filename, content in file_contents.items()}
        result = json.dumps(summaries)
        return f"Summaries: {result}\nSTEPS: - Summarized content from provided files."

    elif intent == "extract" and file_contents:
        extracted_data = {}
        for filename, content in file_contents.items():
            matches = re.findall(r'\b\w+\b', content)
            extracted_data[filename] = matches
        result = json.dumps(extracted_data)
        return f"Extracted Data: {result}\nSTEPS: - Extracted words from provided files."

    elif intent == "transform" and file_contents:
        transformed_data = {filename: content.upper() for filename, content in file_contents.items()}
        result = json.dumps(transformed_data)
        return f"Transformed Data: {result}\nSTEPS: - Transformed content to uppercase."

    elif intent == "calculate":
        return "Error: Calculation requires specific data or context not provided."

    elif intent == "search":
        return "Error: Searching requires specific terms or context not provided."

    # Step 5: Handle case where files are required but not provided
    return "Error: No files provided. Please supply files as a dictionary mapping filename to content."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "OpenCV",
        "description": "An open-source computer vision and machine learning software library for image processing.",
        "function": opencv_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")