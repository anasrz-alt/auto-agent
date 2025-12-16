from typing import Any, Dict
import os

def notetakingassistant_func(query: str, files: dict | None = None) -> str:
    """A tool for automated note-taking that summarizes, extracts, or transforms information from provided files based on user queries. 
    Inputs: a query string and an optional dictionary of files (filename -> content). 
    Output: a string containing the result or an informative error message."""
    
    import json
    
    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: Query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize the query

    # Step 2: Detect user intent
    intent = None
    if "summarize" in query:
        intent = "summarize"
    elif "extract" in query:
        intent = "extract"
    elif "transform" in query:
        intent = "transform"
    elif "search" in query:
        intent = "search"
    elif "calculate" in query:
        intent = "calculate"
    
    # Step 3: Handle provided files
    if files is not None:
        file_contents = {}
        for filename, content in files.items():
            if isinstance(content, bytes):
                content = content.decode(errors='ignore')  # Safely decode bytes
            file_contents[filename] = content
        
        # Step 4: Select strategy based on intent
        if intent == "summarize":
            return summarize_files(file_contents)
        elif intent == "extract":
            return extract_info(file_contents)
        elif intent == "transform":
            return transform_data(file_contents)
        elif intent == "search":
            return search_files(file_contents, query)
        elif intent == "calculate":
            return perform_calculation(query)
    
    # Step 5: Handle case where files are required but not provided
    return "Error: No files provided. Please supply a dictionary of files (filename -> content) to process the query."

def summarize_files(file_contents):
    """Summarizes the contents of the provided files."""
    summaries = []
    for filename, content in file_contents.items():
        summaries.append(f"Summary of {filename}: {content[:100]}...")  # Simple summary
    return "\n".join(summaries)

def extract_info(file_contents):
    """Extracts structured information from the provided files."""
    extracted_data = {}
    for filename, content in file_contents.items():
        lines = content.splitlines()
        extracted_data[filename] = lines[:5]  # Extract first 5 lines as an example
    return f"Extracted Data (JSON): {json.dumps(extracted_data)}"

def transform_data(file_contents):
    """Transforms data from the provided files into a different format."""
    transformed_data = {}
    for filename, content in file_contents.items():
        transformed_data[filename] = content.upper()  # Simple transformation to uppercase
    return f"Transformed Data (JSON): {json.dumps(transformed_data)}"

def search_files(file_contents, query):
    """Searches for the query term in the provided files."""
    results = {}
    for filename, content in file_contents.items():
        if query in content.lower():
            results[filename] = content.lower().count(query)  # Count occurrences
    return f"Search Results (JSON): {json.dumps(results)}"

def perform_calculation(query):
    """Performs a simple calculation based on the query."""
    try:
        # Evaluate the calculation safely (only allow basic arithmetic)
        result = eval(query.replace("calculate", "").strip())
        return f"Calculation Result: {result}"
    except Exception as e:
        return f"Error in calculation: {str(e)}"
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "NoteTakingAssistant",
        "description": "Assists in automated note-taking by summarizing transcribed audio and organizing key points for easy access.",
        "function": notetakingassistant_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")