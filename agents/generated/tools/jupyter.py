from typing import Any, Dict
import os

def jupyter_func(query: str, files: dict | None = None) -> str:
    """Processes a user query to extract information or perform tasks based on provided files. 
    Accepts a query string and an optional dictionary of files (filename -> content). 
    Returns a string containing the result or an error message if files are required but not provided."""
    
    import json
    
    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: The query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize query to lowercase
    
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
        intent = "general"
    
    # Step 3: Handle file input
    if files is None:
        return "Error: No files provided. Please supply a dictionary of files (filename -> content)."
    
    # Step 4: Parse files based on their types
    file_contents = {}
    for filename, content in files.items():
        if isinstance(content, bytes):
            content = content.decode(errors='ignore')  # Safely decode bytes
        file_contents[filename] = content
    
    # Step 5: Select strategy based on intent and available files
    results = []
    if intent == "summarize":
        for content in file_contents.values():
            results.append(content[:100])  # Simple summary by taking the first 100 characters
    elif intent == "extract":
        for content in file_contents.values():
            results.append(content.splitlines())  # Extract lines as structured data
    elif intent == "transform":
        for content in file_contents.values():
            results.append(content.upper())  # Transform to uppercase as an example
    elif intent == "calculate":
        # Placeholder for calculation logic
        results.append("Calculation functionality not implemented.")
    elif intent == "search":
        results.append("Search functionality not implemented.")
    else:
        results.append("General query processing not implemented.")
    
    # Step 6: Produce a clear result string
    if results:
        result_json = json.dumps(results)
        return f"Results: {result_json}\nSTEPS:\n- Validated query\n- Detected intent\n- Processed files\n- Generated results"
    else:
        return "No results found."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "Jupyter",
        "description": "An open-source web application that allows you to create and share documents that contain live code, equations, visualizations, and narrative text.",
        "function": jupyter_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")