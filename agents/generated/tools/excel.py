from typing import Any, Dict
import os

def excel_func(query: str, files: dict | None = None) -> str:
    """Processes a user query to perform tasks related to data files, such as summarizing, extracting, or transforming data. 
    Inputs: 
        - query (str): The user's request or question.
        - files (dict | None): A dictionary mapping filenames to their content as strings or bytes. 
    Output: A string containing the result of the query or an error message if files are required but not provided."""
    
    import json
    import csv
    import io

    # Step 1: Validate inputs and normalize the query
    query = query.strip().lower()
    if not query:
        return "Error: The query cannot be empty."

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

    # Step 3: Handle files if provided
    if files is None:
        return "Error: No files provided. Please supply files in the format: {'filename.txt': 'content'}."

    parsed_data = {}
    for filename, content in files.items():
        try:
            if filename.endswith('.json'):
                parsed_data[filename] = json.loads(content)
            elif filename.endswith('.csv'):
                parsed_data[filename] = list(csv.reader(io.StringIO(content.decode('utf-8'))))
            elif filename.endswith('.txt') or filename.endswith('.md'):
                parsed_data[filename] = content.decode('utf-8').splitlines()
        except Exception as e:
            return f"Error: Failed to parse {filename}. Reason: {str(e)}"

    # Step 4: Select strategy based on intent and available files
    result = ""
    if intent == "summarize":
        for filename, content in parsed_data.items():
            result += f"Summary of {filename}:\n" + "\n".join(content[:3]) + "\n\n"  # Simple summary
    elif intent == "extract":
        result += json.dumps({filename: content for filename, content in parsed_data.items()})
    elif intent == "transform":
        result += "Transformation not implemented yet."
    elif intent == "calculate":
        result += "Calculation not implemented yet."
    else:
        result += "General query processing not implemented yet."

    # Step 5: Produce a clear result string
    if not result:
        return "Error: No valid action could be performed based on the query."

    return f"Result:\n{result}\n\nSTEPS:\n- Validated query\n- Detected intent: {intent}\n- Parsed files\n- Executed strategy"
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "Excel",
        "description": "A powerful spreadsheet tool for advanced data manipulation, analysis, and visualization, enabling the agent to perform complex calculations and generate reports.",
        "function": excel_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")