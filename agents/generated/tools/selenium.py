from typing import Any, Dict
import os

def selenium_func(query: str, files: dict | None = None) -> str:
    """A tool for processing user queries and reading provided files to answer questions or perform tasks. 
    It accepts a query string and an optional dictionary of files, returning a string with the result or an error message.

    Args:
        query (str): The user's query or request.
        files (dict | None): A dictionary mapping filenames to their content as strings or bytes.

    Returns:
        str: The result of processing the query, or an error message if applicable.
    """
    import json

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: The query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize the query

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
    file_contents = {}
    if files:
        for filename, content in files.items():
            if isinstance(content, bytes):
                try:
                    file_contents[filename] = content.decode('utf-8')
                except UnicodeDecodeError:
                    return f"Error: The file '{filename}' could not be decoded."
            elif isinstance(content, str):
                file_contents[filename] = content
            else:
                return f"Error: Unsupported content type for file '{filename}'."

    # Step 4: Select strategy based on intent and available files
    if intent in ["summarize", "extract"] and not file_contents:
        return "Error: No files provided to summarize or extract from. Please provide files."

    result = ""
    if intent == "summarize" and file_contents:
        # Simple summarization by returning the first 100 characters of each file
        summaries = {filename: content[:100] + "..." for filename, content in file_contents.items()}
        result = f"Summaries: {json.dumps(summaries)}"
    elif intent == "extract" and file_contents:
        # Example extraction: return the first line of each file
        extractions = {filename: content.splitlines()[0] for filename, content in file_contents.items() if content}
        result = f"Extractions: {json.dumps(extractions)}"
    elif intent == "transform":
        result = "Transformation not implemented yet."
    elif intent == "calculate":
        result = "Calculation not implemented yet."
    elif intent == "search" and file_contents:
        result = "Search functionality not implemented yet."
    else:
        result = "Error: Unrecognized intent or no files provided."

    # Step 5: Produce a clear result string
    return result + "\nSTEPS: " + ", ".join([
        "Validated input",
        "Detected intent",
        "Processed files",
        "Executed strategy",
        "Generated result"
    ])
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "Selenium",
        "description": "A tool for automating web applications for testing purposes, allowing for browser control.",
        "function": selenium_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")