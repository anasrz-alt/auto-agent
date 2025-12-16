from typing import Any, Dict
import os

def textprocessor_func(query: str, files: dict | None = None) -> str:
    """Processes and analyzes text data based on the user query and optional file contents. 
    Accepts a query string and an optional dictionary of files (filename -> content). 
    Returns a string with the result of the processing, including steps taken if applicable."""
    
    import json
    
    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: Query must be a non-empty string."
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
    elif "search" in query and files:
        intent = "search"
    
    # Step 3: Handle files if provided
    file_contents = {}
    if files:
        for filename, content in files.items():
            if isinstance(content, bytes):
                try:
                    file_contents[filename] = content.decode('utf-8')
                except UnicodeDecodeError:
                    return f"Error: File '{filename}' is not a valid text file."
            else:
                file_contents[filename] = content
    
    # Step 4: Select strategy based on intent
    if intent == "search":
        if not file_contents:
            return "Error: No files provided to search within."
        results = []
        for filename, content in file_contents.items():
            if query in content.lower():
                results.append(filename)
        return f"Found in files: {', '.join(results) if results else 'No matches found.'}"
    
    elif intent == "summarize":
        if not file_contents:
            return "Error: No files provided to summarize."
        summary = " ".join(content[:100] for content in file_contents.values())  # Simple summary
        return f"Summary: {summary}... STEPS: [1. Summarized content from files.]"
    
    elif intent == "extract":
        if not file_contents:
            return "Error: No files provided to extract from."
        extracted_data = {filename: content.splitlines() for filename, content in file_contents.items()}
        return f"Extracted Data: {json.dumps(extracted_data)} (JSON) STEPS: [1. Extracted lines from files.]"
    
    elif intent == "transform":
        return "Transformation not implemented yet. STEPS: [1. Received transform request.]"
    
    elif intent == "calculate":
        return "Calculation not implemented yet. STEPS: [1. Received calculation request.]"
    
    # Step 5: Handle unknown intent
    return "Error: Unable to determine intent from the query. Please clarify your request."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "TextProcessor",
        "description": "Processes and analyzes text data, enabling the agent to extract meaningful information and organize notes.",
        "function": textprocessor_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")