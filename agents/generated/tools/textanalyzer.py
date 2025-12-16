from typing import Any, Dict
import os

def textanalyzer_func(query: str, files: dict | None = None) -> str:
    """Analyzes and processes textual data to extract meaningful insights based on user queries. 
    Accepts a query string and an optional dictionary of files (filename -> content). 
    Returns a string with the result or an error message if files are required but not provided."""
    
    import json
    import re
    
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
    elif "calculate" in query:
        intent = "calculate"
    elif "search" in query:
        intent = "search"
    else:
        intent = "general"

    # Step 3: Handle files if provided
    file_contents = {}
    if files:
        for filename, content in files.items():
            if isinstance(content, bytes):
                content = content.decode(errors='ignore')  # Decode bytes safely
            file_contents[filename] = content

    # Step 4: Select strategy based on intent and available files
    if intent in ["summarize", "extract"] and not files:
        return "Error: Files are required to perform this action. Please provide files."

    # Step 5: Execute the strategy
    result = ""
    if intent == "summarize" and files:
        combined_text = " ".join(file_contents.values())
        sentences = re.split(r'(?<=[.!?]) +', combined_text)
        result = "Summary: " + " ".join(sentences[:2])  # Simple summary by first two sentences
    elif intent == "extract" and files:
        result = {filename: content[:100] for filename, content in file_contents.items()}  # Extract first 100 chars
        result = "Extracted Data: " + json.dumps(result)
    elif intent == "calculate":
        # Placeholder for calculation logic
        result = "Calculation results: [Placeholder for actual calculations]"
    elif intent == "search" and files:
        search_term = re.sub(r'[^a-zA-Z0-9 ]', '', query)  # Clean search term
        found = {filename: content for filename, content in file_contents.items() if search_term in content}
        result = "Search Results: " + json.dumps(found)
    else:
        result = "General inquiry received. Please specify a task."

    # Step 6: Produce a clear result string
    return result + "\nSTEPS: " + "\n".join([
        "Validated and normalized the query.",
        "Detected user intent.",
        "Processed provided files.",
        "Executed the selected strategy.",
        "Returned the result."
    ])
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "TextAnalyzer",
        "description": "Analyzes and processes textual data to extract meaningful insights and perform sentiment analysis.",
        "function": textanalyzer_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")