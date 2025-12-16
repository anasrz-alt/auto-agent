from typing import Any, Dict
import os

def exceltool_func(query: str, files: dict | None = None) -> str:
    """A tool for advanced data manipulation, analysis, and visualization using Excel spreadsheets. 
    It accepts a user query and optional files, processes the query to determine user intent, 
    and returns a result based on the content of the files or the query itself.

    Args:
        query (str): The user query describing the task or question.
        files (dict | None): A dictionary mapping filenames to their content as strings or bytes.

    Returns:
        str: A response string containing the result of processing the query, or an error message if applicable.
    """
    import json
    import csv
    from io import StringIO

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: The query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize query to lowercase

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
    if files is None or not files:
        return "Error: No files provided. Please supply files in the format: {'filename': 'file content'}."

    file_contents = {}
    for filename, content in files.items():
        if isinstance(content, bytes):
            content = content.decode('utf-8', errors='ignore')  # Decode bytes safely
        file_contents[filename] = content

    # Step 4: Select strategy based on intent and available files
    results = []
    for filename, content in file_contents.items():
        if filename.endswith('.csv'):
            # Parse CSV
            try:
                reader = csv.reader(StringIO(content))
                data = list(reader)
                results.append({"filename": filename, "data": data})
            except Exception as e:
                return f"Error processing {filename}: {str(e)}"
        elif filename.endswith('.json'):
            # Parse JSON
            try:
                data = json.loads(content)
                results.append({"filename": filename, "data": data})
            except Exception as e:
                return f"Error processing {filename}: {str(e)}"
        elif filename.endswith('.md') or filename.endswith('.txt'):
            # Handle plain text or markdown
            results.append({"filename": filename, "data": content.splitlines()})
    
    # Step 5: Execute the strategy
    if intent == "summarize":
        summary = "\n".join([f"{res['filename']}: {len(res['data'])} lines" for res in results])
        return f"Summary:\n{summary}\nSTEPS:\n- Validated input\n- Detected intent\n- Processed files\n- Generated summary"
    
    elif intent == "extract":
        extracted_data = {res['filename']: res['data'] for res in results}
        return f"Extracted Data: {json.dumps(extracted_data)}\nSTEPS:\n- Validated input\n- Detected intent\n- Processed files\n- Extracted data"

    elif intent == "transform":
        transformed_data = {res['filename']: [line.upper() for line in res['data']] for res in results}
        return f"Transformed Data: {json.dumps(transformed_data)}\nSTEPS:\n- Validated input\n- Detected intent\n- Processed files\n- Transformed data"

    elif intent == "calculate":
        return "Error: Calculation intent requires specific instructions on what to calculate."

    elif intent == "search":
        return "Error: Search intent requires specific keywords to search for."

    return "Error: Unable to determine the appropriate action based on the query."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "ExcelTool",
        "description": "A tool for advanced data manipulation, analysis, and visualization using Excel spreadsheets.",
        "function": exceltool_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")