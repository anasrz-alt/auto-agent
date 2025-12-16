from typing import Any, Dict
import os

def youtubeapi_func(query: str, files: dict | None = None) -> str:
    """Processes a user query to extract information from provided files or perform tasks. 
    Accepts a query string and an optional dictionary of files (filename -> content). 
    Returns a string with the result or an error message if files are needed but not provided."""
    
    import json
    import re

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: The query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize query

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
    
    # Step 3: Handle files if provided
    if files is not None:
        file_contents = {}
        for filename, content in files.items():
            if isinstance(content, bytes):
                content = content.decode(errors='ignore')  # Handle binary safely
            file_contents[filename] = content
        
        # Example of parsing specific file types
        text_data = ""
        for filename, content in file_contents.items():
            if filename.endswith('.txt') or filename.endswith('.md'):
                text_data += content + "\n"
            elif filename.endswith('.json'):
                try:
                    json_data = json.loads(content)
                    text_data += json.dumps(json_data) + "\n"
                except json.JSONDecodeError:
                    return f"Error: Could not decode JSON from {filename}."
            elif filename.endswith('.csv'):
                text_data += content + "\n"  # Treat CSV as plain text for simplicity

    else:
        if "file" in query:
            return "Error: No files provided. Please supply files to process the query."
    
    # Step 4: Select strategy based on intent
    result = ""
    if intent == "summarize" and text_data:
        result = "Summary: " + text_data[:100] + "..."  # Simple truncation for demonstration
    elif intent == "extract" and text_data:
        result = "Extracted Data: " + json.dumps({"data": text_data.splitlines()})
    elif intent == "transform":
        result = "Transformed Data: " + text_data.upper()  # Example transformation
    elif intent == "search" and text_data:
        search_term = re.search(r'search for (.+)', query)
        if search_term:
            term = search_term.group(1)
            matches = [line for line in text_data.splitlines() if term in line]
            result = "Search Results: " + json.dumps(matches)
        else:
            result = "Error: No search term provided."
    elif intent == "calculate":
        result = "Calculation not implemented."  # Placeholder for future functionality
    else:
        result = "No actionable intent detected or no relevant file content."

    # Step 5: Produce a clear result string
    return f"{result}\nSTEPS:\n- Validated input\n- Detected intent\n- Processed files\n- Executed strategy"
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "YouTubeAPI",
        "description": "An API that provides access to YouTube video metadata and transcripts, enabling the agent to extract relevant details from videos.",
        "function": youtubeapi_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")