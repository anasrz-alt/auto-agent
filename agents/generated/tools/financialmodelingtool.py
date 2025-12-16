from typing import Any, Dict
import os

def financialmodelingtool_func(query: str, files: dict | None = None) -> str:
    """A tool for answering financial queries, extracting data, and performing calculations based on provided files. 
    Inputs: 
        - query: A string representing the user's request or question.
        - files: A dictionary mapping filenames to their content as strings or bytes.
    Output: A string containing the answer or result, including structured data in JSON format if applicable."""
    
    import json
    import csv
    from io import StringIO

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: Invalid query. Please provide a non-empty string query."
    
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
        return "Error: Unable to determine intent from the query."

    # Step 3: Handle provided files
    file_contents = {}
    if files:
        for filename, content in files.items():
            if isinstance(content, bytes):
                content = content.decode('utf-8', errors='ignore')  # Decode bytes to string
            file_contents[filename] = content

    # Step 4: Select strategy based on intent and available files
    if intent == "summarize" and file_contents:
        summaries = []
        for content in file_contents.values():
            summaries.append(content[:100] + '...')  # Simple summary of first 100 chars
        result = "Summaries:\n" + "\n".join(summaries)
    elif intent == "extract" and file_contents:
        extracted_data = {}
        for filename, content in file_contents.items():
            if filename.endswith('.json'):
                try:
                    extracted_data[filename] = json.loads(content)
                except json.JSONDecodeError:
                    return "Error: Invalid JSON format in file."
            elif filename.endswith('.csv'):
                try:
                    reader = csv.reader(StringIO(content))
                    extracted_data[filename] = list(reader)
                except Exception:
                    return "Error: Invalid CSV format in file."
            else:
                extracted_data[filename] = content.splitlines()
        result = "Extracted Data:\n" + json.dumps(extracted_data)
    elif intent == "calculate":
        # Placeholder for calculation logic
        result = "Calculation results are not implemented yet."
    elif intent == "search":
        if not file_contents:
            return "Error: No files provided to search within."
        search_results = []
        for filename, content in file_contents.items():
            if query in content.lower():
                search_results.append(f"Found in {filename}: {content[:100]}...")
        result = "Search Results:\n" + "\n".join(search_results) if search_results else "No matches found."
    else:
        return "Error: No applicable files provided for the selected intent."

    # Step 5: Produce a clear result string
    return result + "\n\nSTEPS:\n- Validated query and normalized input.\n- Detected user intent.\n- Processed provided files.\n- Executed strategy based on intent.\n- Generated result string."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "FinancialModelingTool",
        "description": "A specialized tool for building financial models and simulations based on input data.",
        "function": financialmodelingtool_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")