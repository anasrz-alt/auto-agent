from typing import Any, Dict
import os

def contentmoderationtool_func(query: str, files: dict | None = None) -> str:
    """A tool for filtering and moderating content based on user queries and provided files. 
    It accepts a query string and an optional dictionary of files, processes the input, 
    and returns a response string with the results or instructions on how to use the tool.
    
    Args:
        query (str): The user query to process.
        files (dict | None): A dictionary mapping filenames to their content as strings or bytes.
        
    Returns:
        str: A response string containing the result of the query or an error message.
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
    elif "search" in query:
        intent = "search"
    elif "calculate" in query:
        intent = "calculate"
    else:
        return "Error: Unable to determine intent from the query."
    
    # Step 3: Detect and parse files if provided
    file_contents = {}
    if files:
        for filename, content in files.items():
            if isinstance(content, bytes):
                content = content.decode(errors='ignore')  # Safely decode bytes
            file_contents[filename] = content
    
    # Step 4: Select strategy based on intent and available files
    if intent == "summarize":
        if not file_contents:
            return "Error: No files provided for summarization. Please provide files."
        summary = " ".join(content[:100] for content in file_contents.values())  # Simple summary
        result = f"Summary: {summary}"
    
    elif intent == "extract":
        if not file_contents:
            return "Error: No files provided for extraction. Please provide files."
        extracted_data = {filename: content.splitlines() for filename, content in file_contents.items()}
        result = f"Extracted Data (JSON): {json.dumps(extracted_data)}"
    
    elif intent == "transform":
        result = "Transformation not implemented. Please specify how to transform the content."
    
    elif intent == "search":
        if not file_contents:
            return "Error: No files provided for searching. Please provide files."
        search_results = {filename: [line for line in content.splitlines() if query in line] 
                          for filename, content in file_contents.items()}
        result = f"Search Results (JSON): {json.dumps(search_results)}"
    
    elif intent == "calculate":
        result = "Calculation not implemented. Please specify what to calculate."
    
    else:
        return "Error: Unsupported intent."
    
    # Step 5: Produce a clear result string
    return f"{result}\n\nSTEPS:\n- Validated input query.\n- Detected intent: {intent}.\n- Processed files: {len(file_contents)}.\n- Generated result."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "ContentModerationTool",
        "description": "A tool that helps in filtering and moderating content based on predefined guidelines.",
        "function": contentmoderationtool_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")