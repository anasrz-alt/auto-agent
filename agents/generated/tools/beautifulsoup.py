from typing import Any, Dict
import os

def beautifulsoup_func(query: str, files: dict | None = None) -> str:
    """A versatile tool for processing user queries and reading provided files to extract information, summarize content, or perform transformations. 
    Inputs: 
    - query: A string representing the user's request.
    - files: An optional dictionary mapping filenames to their content as strings or bytes.
    Output: A string containing the result of processing the query, or an error message if applicable."""
    
    import json
    from typing import Any
    from io import StringIO
    import csv
    
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
    
    # Step 3: Handle files if provided
    if files is None:
        return "Error: No files provided. Please supply a dictionary of files."
    
    parsed_data = {}
    for filename, content in files.items():
        if isinstance(content, bytes):
            content = content.decode('utf-8', errors='ignore')
        if filename.endswith('.json'):
            try:
                parsed_data[filename] = json.loads(content)
            except json.JSONDecodeError:
                return f"Error: Failed to parse JSON from {filename}."
        elif filename.endswith('.csv'):
            try:
                parsed_data[filename] = list(csv.reader(StringIO(content)))
            except Exception as e:
                return f"Error: Failed to parse CSV from {filename}. {str(e)}"
        elif filename.endswith('.md') or filename.endswith('.txt'):
            parsed_data[filename] = content.splitlines()
        else:
            return f"Error: Unsupported file type for {filename}."
    
    # Step 4: Execute the strategy based on intent
    result = ""
    if intent == "summarize":
        for filename, content in parsed_data.items():
            result += f"Summary of {filename}: {content[:3]}...\n"  # Simple summary
    elif intent == "extract":
        result = json.dumps(parsed_data)  # Return structured data as JSON
    elif intent == "transform":
        result = "Transformation not implemented."  # Placeholder
    elif intent == "calculate":
        result = "Calculation not implemented."  # Placeholder
    elif intent == "search":
        result = "Search functionality not implemented."  # Placeholder
    else:
        return "Error: Unrecognized intent based on the query."
    
    # Step 5: Produce a clear result string
    return f"Result:\n{result}\nSTEPS:\n- Validated query\n- Parsed files\n- Executed intent: {intent}"
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "BeautifulSoup",
        "description": "A library for parsing HTML and XML documents, useful for web scraping.",
        "function": beautifulsoup_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")