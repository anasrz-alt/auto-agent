from typing import Any, Dict
import os

def datacomparator_func(query: str, files: dict | None = None) -> str:
    """A tool for comparing datasets, allowing the agent to identify overlaps and differences in data.
    
    Args:
        query (str): The user query specifying the task to perform.
        files (dict | None): A dictionary mapping filenames to their content as strings or bytes.
    
    Returns:
        str: A response string containing the result of the operation, including steps taken or error messages.
    """
    import json
    import csv
    from io import StringIO

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: The query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize query to lowercase for easier processing

    # Step 2: Detect user intent
    if "compare" in query or "difference" in query:
        intent = "compare"
    elif "summarize" in query:
        intent = "summarize"
    elif "extract" in query:
        intent = "extract"
    else:
        return "Error: Unable to determine intent from the query."

    # Step 3: Handle provided files
    if files is None:
        return "Error: No files provided. Please supply files in the format: {'filename': 'content'}."

    # Step 4: Parse files and prepare data for comparison
    data_sets = {}
    for filename, content in files.items():
        if isinstance(content, bytes):
            content = content.decode('utf-8', errors='ignore')  # Decode bytes safely
        if filename.endswith('.json'):
            try:
                data_sets[filename] = json.loads(content)
            except json.JSONDecodeError:
                return f"Error: Failed to parse JSON from file '{filename}'."
        elif filename.endswith('.csv'):
            try:
                data_sets[filename] = list(csv.reader(StringIO(content)))
            except Exception:
                return f"Error: Failed to parse CSV from file '{filename}'."
        elif filename.endswith('.txt') or filename.endswith('.md'):
            data_sets[filename] = content.splitlines()
        else:
            return f"Error: Unsupported file type for file '{filename}'."

    # Step 5: Execute the strategy based on intent
    if intent == "compare":
        if len(data_sets) < 2:
            return "Error: At least two files are required for comparison."
        keys = list(data_sets.keys())
        comparison_result = {keys[0]: data_sets[keys[0]], keys[1]: data_sets[keys[1]]}
        # Simple comparison logic (for demonstration)
        differences = set(data_sets[keys[0]]) ^ set(data_sets[keys[1]])
        result = {
            "differences": list(differences),
            "common": list(set(data_sets[keys[0]]) & set(data_sets[keys[1]]))
        }
    elif intent == "summarize":
        summary = {filename: len(content) for filename, content in data_sets.items()}
        result = summary
    elif intent == "extract":
        # Example extraction logic (could be refined based on specific needs)
        result = {filename: content[:5] for filename, content in data_sets.items()}  # First 5 lines/entries

    # Step 6: Produce a clear result string
    return f"Result: {json.dumps(result)}\nSTEPS: - Validated inputs\n - Detected intent\n - Parsed files\n - Executed strategy"
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "DataComparator",
        "description": "A tool for comparing datasets, allowing the agent to identify overlaps and differences in data.",
        "function": datacomparator_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")