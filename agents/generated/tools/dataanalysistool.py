from typing import Any, Dict
import os

def dataanalysistool_func(query: str, files: dict | None = None) -> str:
    """A tool for performing statistical analysis and deriving insights from data sets. 
    It accepts a user query and optional files, processes the files if provided, 
    and returns a result string based on the detected intent.

    Args:
        query (str): The user's query regarding data analysis or file content.
        files (dict | None): A dictionary mapping filenames to their content as strings or bytes.

    Returns:
        str: A machine- and human-friendly result string with the analysis or an error message.
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
    elif "transform" in query:
        intent = "transform"
    elif "calculate" in query:
        intent = "calculate"
    elif "search" in query:
        intent = "search"

    # Step 3: Handle files if provided
    file_contents = {}
    if files:
        for filename, content in files.items():
            if isinstance(content, bytes):
                content = content.decode('utf-8', errors='ignore')
            file_contents[filename] = content

    # Step 4: Select strategy based on intent and available files
    if intent in ["summarize", "extract", "transform"] and not file_contents:
        return "Error: No files provided. Please supply files to analyze."

    result = ""
    steps = []

    try:
        if intent == "summarize" and file_contents:
            # Summarize text content
            for filename, content in file_contents.items():
                result += f"Summary of {filename}: {content[:100]}...\n"  # Simple summary
                steps.append(f"Summarized content from {filename}")

        elif intent == "extract" and file_contents:
            # Extract data from CSV or JSON
            for filename, content in file_contents.items():
                if filename.endswith('.csv'):
                    reader = csv.reader(StringIO(content))
                    headers = next(reader)
                    data = [dict(zip(headers, row)) for row in reader]
                    result += f"Extracted data from {filename}: {json.dumps(data)}\n"
                    steps.append(f"Extracted data from {filename}")

                elif filename.endswith('.json'):
                    data = json.loads(content)
                    result += f"Extracted data from {filename}: {json.dumps(data)}\n"
                    steps.append(f"Extracted data from {filename}")

        elif intent == "calculate":
            # Placeholder for calculation logic
            result = "Calculation functionality is not yet implemented."
            steps.append("Identified calculation intent.")

        elif intent == "transform":
            # Placeholder for transformation logic
            result = "Transformation functionality is not yet implemented."
            steps.append("Identified transformation intent.")

        elif intent == "search":
            # Placeholder for search logic
            result = "Search functionality is not yet implemented."
            steps.append("Identified search intent.")

        else:
            result = "Error: Unable to determine the intent or process the files."

    except Exception as e:
        result = f"Error: An exception occurred during processing: {str(e)}"

    # Step 5: Produce a clear result
    result += "\nSTEPS:\n" + "\n".join(steps)
    return result.strip()
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "DataAnalysisTool",
        "description": "A tool for performing statistical analysis and deriving insights from data sets.",
        "function": dataanalysistool_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")