from typing import Any, Dict
import os

def django_func(query: str, files: dict | None = None) -> str:
    """Processes a user query to answer questions or perform tasks using provided files. 
    Accepts a query string and an optional dictionary of files (filename -> content). 
    Returns a string with the result or an error message if files are needed but not provided."""

    import json
    import csv
    from io import StringIO

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: The query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize the query

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
    else:
        return "Error: Unable to determine intent from the query."

    # Step 3: Handle file input if provided
    if files is not None:
        file_contents = {}
        for filename, content in files.items():
            if isinstance(content, bytes):
                content = content.decode('utf-8', errors='ignore')  # Decode bytes safely
            file_contents[filename] = content

    # Step 4: Select a strategy based on intent and available files
    if intent == "summarize":
        if not files:
            return "Error: No files provided for summarization. Please provide files."
        summaries = []
        for content in file_contents.values():
            summaries.append(content[:100] + '...')  # Simple summary: first 100 chars
        result = "Summarized content: " + " | ".join(summaries)

    elif intent == "extract":
        if not files:
            return "Error: No files provided for extraction. Please provide files."
        extracted_data = {}
        for filename, content in file_contents.items():
            if filename.endswith('.json'):
                try:
                    extracted_data[filename] = json.loads(content)
                except json.JSONDecodeError:
                    return f"Error: Failed to parse JSON from {filename}."
            elif filename.endswith('.csv'):
                try:
                    reader = csv.reader(StringIO(content))
                    extracted_data[filename] = list(reader)
                except Exception:
                    return f"Error: Failed to parse CSV from {filename}."
        result = "Extracted data: " + json.dumps(extracted_data)

    elif intent == "transform":
        result = "Transformation not implemented yet."

    elif intent == "calculate":
        result = "Calculation not implemented yet."

    elif intent == "search":
        result = "Search functionality not implemented yet."

    # Step 5: Produce a clear result string
    return result + "\nSTEPS: \n- Validated input\n- Determined intent\n- Processed files\n- Generated result"
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "Django",
        "description": "A high-level Python web framework that encourages rapid development and clean, pragmatic design.",
        "function": django_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")