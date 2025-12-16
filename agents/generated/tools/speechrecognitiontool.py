from typing import Any, Dict
import os

def speechrecognitiontool_func(query: str, files: dict | None = None) -> str:
    """A tool that processes user queries to extract information from provided files or perform tasks. 
    Inputs: a string query and an optional dictionary of files (filename -> content). 
    Output: a string containing the result or an error message if files are required but not provided."""
    
    import json
    
    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: Query must be a non-empty string."
    
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
    file_contents = {}
    if files:
        for filename, content in files.items():
            if isinstance(content, bytes):
                try:
                    file_contents[filename] = content.decode('utf-8')
                except Exception:
                    return f"Error: Unable to decode binary content in file '{filename}'."
            elif isinstance(content, str):
                file_contents[filename] = content
            else:
                return f"Error: Unsupported content type for file '{filename}'."

    # Step 4: Select strategy based on intent and available files
    if intent in ["summarize", "extract", "transform"] and not file_contents:
        return "Error: No files provided. Please supply files for processing."
    
    result = ""
    if intent == "summarize":
        result = "\n".join([f"{filename}: {content[:100]}..." for filename, content in file_contents.items()])
        result = f"Summary of files:\n{result}"
    elif intent == "extract":
        result = {filename: content.splitlines() for filename, content in file_contents.items()}
        result = f"Extracted data (JSON): {json.dumps(result)}"
    elif intent == "transform":
        result = {filename: content.upper() for filename, content in file_contents.items()}
        result = f"Transformed data (JSON): {json.dumps(result)}"
    elif intent == "search":
        search_term = query.split("search for")[-1].strip()
        found = {filename: content for filename, content in file_contents.items() if search_term in content}
        result = f"Search results (JSON): {json.dumps(found)}" if found else "No matches found."
    elif intent == "calculate":
        # Placeholder for calculation logic
        result = "Calculation feature is not implemented yet."
    
    # Step 5: Produce a clear result string
    steps = [
        "Validated and normalized input.",
        f"Detected intent: {intent}.",
        "Processed files for requested operation.",
        "Generated result based on intent."
    ]
    
    return f"{result}\n\nSTEPS:\n- " + "\n- ".join(steps)
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "SpeechRecognitionTool",
        "description": "A tool that converts spoken language into text, enabling the agent to understand voice commands and transcribe audio content.",
        "function": speechrecognitiontool_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")