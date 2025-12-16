from typing import Any, Dict
import os

def excelanalyzer_func(query: str, files: dict | None = None) -> str:
    """Analyzes provided files based on the user query, performing tasks like extraction, summarization, or simple calculations. 
    Inputs: 
        - query (str): The user's request or question regarding the files.
        - files (dict | None): A dictionary mapping filenames to their content as strings or bytes.
    Output: 
        - A string containing the result of the analysis or an error message if files are missing or the query is invalid.
    """
    import json
    import csv
    from io import StringIO

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
    elif "count" in query:
        intent = "count"
    elif "search" in query:
        intent = "search"
    else:
        return "Error: Unable to determine intent from the query."

    # Step 3: Handle files if provided
    if files is None or not files:
        return "Error: No files provided. Please supply files as a dictionary mapping filenames to their content."

    parsed_data = {}
    for filename, content in files.items():
        try:
            if filename.endswith('.csv'):
                # Parse CSV files
                parsed_data[filename] = list(csv.reader(StringIO(content.decode('utf-8'))))
            elif filename.endswith('.json'):
                # Parse JSON files
                parsed_data[filename] = json.loads(content)
            elif filename.endswith('.txt') or filename.endswith('.md'):
                # Handle plain text or markdown files
                parsed_data[filename] = content.decode('utf-8').splitlines()
            else:
                return f"Error: Unsupported file type for {filename}."
        except Exception as e:
            return f"Error: Failed to parse {filename}. Reason: {str(e)}"

    # Step 4: Select strategy based on intent and available files
    result = []
    if intent == "summarize":
        for filename, data in parsed_data.items():
            result.append(f"Summary of {filename}: {len(data)} lines.")
    elif intent == "extract":
        for filename, data in parsed_data.items():
            result.append(f"Extracted data from {filename}: {data[:3]}...")  # Show first 3 lines
    elif intent == "count":
        for filename, data in parsed_data.items():
            result.append(f"Count in {filename}: {len(data)} rows.")
    elif intent == "search":
        search_term = query.split("search for")[-1].strip()
        for filename, data in parsed_data.items():
            matches = [line for line in data if search_term in line]
            result.append(f"Matches in {filename}: {matches}")

    # Step 5: Produce a clear result string
    if not result:
        return "Error: No relevant data found based on the query."
    
    output = "\n".join(result)
    output += "\nSTEPS:\n- Validated query.\n- Detected intent.\n- Parsed provided files.\n- Executed strategy based on intent."
    
    return output
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "ExcelAnalyzer",
        "description": "A tool for analyzing Excel files, providing functionalities for counts, comparisons, and data extraction.",
        "function": excelanalyzer_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")