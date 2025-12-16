from typing import Any, Dict
import os

def pdfextractortool_func(query: str, files: dict | None = None) -> str:
    """Extracts information from provided files based on the user query. 
    Inputs: a query string and an optional dictionary of files (filename -> content). 
    Outputs: a string containing the answer or results, including JSON if structured data is extracted."""
    
    import json
    
    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: Query must be a non-empty string."
    
    query = query.strip().lower()
    
    # Step 2: Detect user intent
    intent = None
    if "extract" in query:
        intent = "extract"
    elif "summarize" in query:
        intent = "summarize"
    elif "transform" in query:
        intent = "transform"
    elif "search" in query:
        intent = "search"
    else:
        return "Error: Unable to determine intent from the query."

    # Step 3: Detect and parse provided files
    if files is None or not isinstance(files, dict) or not files:
        return "Error: No files provided. Please supply a dictionary of files (filename -> content)."

    file_contents = {}
    for filename, content in files.items():
        if isinstance(content, bytes):
            try:
                file_contents[filename] = content.decode('utf-8')
            except UnicodeDecodeError:
                return f"Error: Unable to decode the content of file '{filename}'."
        elif isinstance(content, str):
            file_contents[filename] = content
        else:
            return f"Error: Unsupported content type for file '{filename}'."

    # Step 4: Select strategy based on intent and available files
    results = []
    for filename, content in file_contents.items():
        if intent == "extract":
            results.append(content)  # Simple extraction of text
        elif intent == "summarize":
            results.append(content[:100] + "...")  # Simple summarization (first 100 chars)
        elif intent == "transform":
            results.append(content.upper())  # Simple transformation (to uppercase)
        elif intent == "search":
            if any(word in content.lower() for word in query.split()):
                results.append(f"Found in {filename}: {content}")
            else:
                results.append(f"No match found in {filename}.")
    
    # Step 5: Handle edge cases and errors
    if not results:
        return "Error: No relevant information found based on the query."

    # Step 6: Produce a clear result string
    result_json = json.dumps(results)
    return f"Results: {result_json}\nSTEPS:\n- Validated input\n- Detected intent\n- Parsed files\n- Executed strategy\n- Generated results."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "PDFExtractorTool",
        "description": "A tool for extracting text and data from PDF documents for analysis and processing.",
        "function": pdfextractortool_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")