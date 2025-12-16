from typing import Any, Dict
import os

def dataformatter_func(query: str, files: dict | None = None) -> str:
    """Processes a user query to extract, summarize, or transform data from provided files. 
    Accepts a query string and an optional dictionary of files (filename -> content). 
    Returns a formatted string response, including JSON when structured data is extracted."""
    
    import json

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: The query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize the query for processing

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
    else:
        intent = "general"

    # Step 3: Handle file input
    if files is None:
        return "Error: No files provided. Please supply a dictionary of files (filename -> content)."

    # Step 4: Select a concise strategy based on intent and available files
    results = []
    for filename, content in files.items():
        try:
            if isinstance(content, bytes):
                content = content.decode('utf-8', errors='ignore')  # Handle binary safely
            
            if intent == "summarize" and content:
                results.append(f"Summary of {filename}: {content[:100]}...")  # Simple summary
            elif intent == "extract" and content:
                results.append(f"Extracted data from {filename}: {content.splitlines()[:3]}")  # Simple extraction
            elif intent == "transform" and content:
                results.append(f"Transformed content from {filename}: {content.upper()}")  # Simple transformation
            elif intent == "calculate" and content:
                # Example calculation: count lines
                line_count = len(content.splitlines())
                results.append(f"Line count in {filename}: {line_count}")
            else:
                results.append(f"No actionable content in {filename}.")
        except Exception as e:
            results.append(f"Error processing {filename}: {str(e)}")

    # Step 5: Produce a clear result string
    if results:
        response = "\n".join(results)
        response += "\n\nSTEPS:\n- Validated and normalized query.\n- Detected intent: {}\n- Processed files.\n".format(intent)
        return response
    else:
        return "No results found based on the provided query and files."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "DataFormatter",
        "description": "Formats the output results into structured data (e.g., integer counts or name strings) for final presentation.",
        "function": dataformatter_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")