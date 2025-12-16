from typing import Any, Dict
import os

def realtimestreamingapi_func(query: str, files: dict | None = None) -> str:
    """Processes a user query to answer questions or perform tasks using provided files. 
    Inputs: a string query and an optional dictionary of files (filename -> content). 
    Outputs: a string containing the result or an error message if files are missing or invalid."""
    
    import json
    
    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: The query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize query for processing

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
                content = content.decode(errors='ignore')  # Safely decode bytes
            file_contents[filename] = content
            
    else:
        return "Error: No files provided. Please supply a dictionary of files (filename -> content)."

    # Step 4: Select strategy based on intent and available files
    if intent == "summarize":
        result = "Summary: " + " ".join(content[:100] for content in file_contents.values())
        steps = ["Validated input", "Detected intent: summarize", "Summarized file contents"]
    elif intent == "extract":
        extracted_data = {filename: content.splitlines() for filename, content in file_contents.items()}
        result = f"Extracted Data (JSON): {json.dumps(extracted_data)}"
        steps = ["Validated input", "Detected intent: extract", "Extracted data from files"]
    elif intent == "transform":
        transformed_data = {filename: content.upper() for filename, content in file_contents.items()}
        result = f"Transformed Data (JSON): {json.dumps(transformed_data)}"
        steps = ["Validated input", "Detected intent: transform", "Transformed file contents to uppercase"]
    elif intent == "calculate":
        # Placeholder for simple calculations (e.g., counting lines)
        line_counts = {filename: content.count('\n') + 1 for filename, content in file_contents.items()}
        result = f"Line Counts (JSON): {json.dumps(line_counts)}"
        steps = ["Validated input", "Detected intent: calculate", "Calculated line counts"]
    elif intent == "search":
        search_term = query.split("search for")[-1].strip()
        search_results = {filename: content for filename, content in file_contents.items() if search_term in content}
        result = f"Search Results (JSON): {json.dumps(search_results)}"
        steps = ["Validated input", "Detected intent: search", "Searched for term in files"]
    else:
        return "Error: Unrecognized intent. Please specify a valid action (summarize, extract, transform, calculate, search)."

    # Step 5: Produce final result
    return f"{result}\n\nSTEPS:\n" + "\n".join(steps)
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "RealTimeStreamingAPI",
        "description": "An API that facilitates the processing of live video streams for immediate analysis.",
        "function": realtimestreamingapi_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")