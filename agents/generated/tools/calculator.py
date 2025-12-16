from typing import Any, Dict
import os

def calculator_func(query: str, files: dict | None = None) -> str:
    """A tool for performing numerical calculations and data analysis based on user queries and provided files. 
    It accepts a query string and an optional dictionary of files, returning a string with the result or an error message.
    
    Args:
        query (str): The user query describing the calculation or task.
        files (dict | None): A dictionary mapping filenames to their content as strings or bytes.
        
    Returns:
        str: The result of the calculation or task, or an error message if applicable.
    """
    import json
    import re

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: The query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize query to lowercase

    # Step 2: Detect user intent
    if "calculate" in query or "solve" in query:
        intent = "calculate"
    elif "extract" in query or "data" in query:
        intent = "extract"
    elif "summarize" in query:
        intent = "summarize"
    elif "transform" in query:
        intent = "transform"
    else:
        return "Error: Unrecognized intent in the query."

    # Step 3: Handle provided files
    file_contents = {}
    if files:
        for filename, content in files.items():
            if isinstance(content, bytes):
                content = content.decode('utf-8', errors='ignore')  # Decode bytes safely
            file_contents[filename] = content

    # Step 4: Select strategy based on intent
    if intent == "calculate":
        # Simple calculation extraction
        match = re.search(r'calculate (.+)', query)
        if match:
            expression = match.group(1)
            try:
                result = eval(expression)  # Caution: eval can be dangerous; assume trusted input
                return f"Result: {result}\nSTEPS: Calculated the expression '{expression}'."
            except Exception as e:
                return f"Error: Could not calculate the expression. {str(e)}"
        else:
            return "Error: No valid expression found to calculate."

    elif intent == "extract":
        if not file_contents:
            return "Error: No files provided for data extraction."
        extracted_data = {}
        for filename, content in file_contents.items():
            # Simple line extraction for demonstration
            lines = content.splitlines()
            extracted_data[filename] = lines[:5]  # Extract first 5 lines as a sample
        return f"Extracted Data: {json.dumps(extracted_data)}\nSTEPS: Extracted first 5 lines from each file."

    elif intent == "summarize":
        if not file_contents:
            return "Error: No files provided for summarization."
        summaries = {}
        for filename, content in file_contents.items():
            summaries[filename] = content[:100] + '...'  # Simple summary of the first 100 characters
        return f"Summaries: {json.dumps(summaries)}\nSTEPS: Summarized the content of each file."

    elif intent == "transform":
        if not file_contents:
            return "Error: No files provided for transformation."
        transformed_data = {}
        for filename, content in file_contents.items():
            transformed_data[filename] = content.upper()  # Simple transformation to uppercase
        return f"Transformed Data: {json.dumps(transformed_data)}\nSTEPS: Transformed content to uppercase for each file."

    return "Error: Unable to process the query."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "Calculator",
        "description": "A tool for performing numerical calculations, allowing the agent to solve mathematical problems and perform data analysis.",
        "function": calculator_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")