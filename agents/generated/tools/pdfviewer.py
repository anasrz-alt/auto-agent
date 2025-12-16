from typing import Any, Dict
import os

def pdfviewer_func(query: str, files: dict | None = None) -> str:
    """A tool for viewing and analyzing PDF documents, enabling the agent to extract and process information from files.
    
    Args:
        query (str): The user query specifying the task to perform.
        files (dict | None): A dictionary mapping filenames to their content as strings or bytes.
    
    Returns:
        str: A machine- and human-friendly result string containing the answer or an error message.
    """
    import json

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: Query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize query to lowercase

    # Step 2: Detect user intent
    intent = None
    if "extract" in query:
        intent = "extract"
    elif "summarize" in query:
        intent = "summarize"
    elif "search" in query:
        intent = "search"
    elif "transform" in query:
        intent = "transform"
    else:
        return "Error: Unable to determine intent from the query."

    # Step 3: Handle files if provided
    if files is None or not isinstance(files, dict) or not files:
        return "Error: No files provided. Please supply a dictionary of files."

    # Step 4: Initialize a container for extracted data
    extracted_data = {}

    # Step 5: Process each file based on its type
    for filename, content in files.items():
        try:
            if isinstance(content, bytes):
                content = content.decode('utf-8', errors='ignore')  # Safely decode bytes
            
            if filename.endswith('.txt'):
                extracted_data[filename] = content.splitlines()
            elif filename.endswith('.json'):
                extracted_data[filename] = json.loads(content)
            elif filename.endswith('.csv'):
                extracted_data[filename] = [line.split(',') for line in content.splitlines()]
            elif filename.endswith('.md'):
                extracted_data[filename] = content.splitlines()
            else:
                return f"Error: Unsupported file type for {filename}."
        except Exception as e:
            return f"Error processing file {filename}: {str(e)}"

    # Step 6: Execute the strategy based on intent
    if intent == "extract":
        result = json.dumps(extracted_data)
        return f"Extracted data: {result}\nSTEPS:\n- Validated input\n- Detected intent\n- Processed files\n- Extracted data"
    
    elif intent == "summarize":
        summary = {filename: content[:2] for filename, content in extracted_data.items()}  # Simple summary
        return f"Summary: {json.dumps(summary)}\nSTEPS:\n- Validated input\n- Detected intent\n- Processed files\n- Generated summary"
    
    elif intent == "search":
        search_results = {filename: [line for line in content if query in line] for filename, content in extracted_data.items()}
        return f"Search results: {json.dumps(search_results)}\nSTEPS:\n- Validated input\n- Detected intent\n- Processed files\n- Searched for '{query}'"
    
    elif intent == "transform":
        transformed_data = {filename: [line.upper() for line in content] for filename, content in extracted_data.items()}
        return f"Transformed data: {json.dumps(transformed_data)}\nSTEPS:\n- Validated input\n- Detected intent\n- Processed files\n- Transformed data to uppercase"

    return "Error: Unable to complete the request."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "PDFViewer",
        "description": "A tool for viewing and analyzing PDF documents, enabling the agent to extract and process information from files.",
        "function": pdfviewer_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")