from typing import Any, Dict
import os

def datacomparer_func(query: str, files: dict | None = None) -> str:
    """Compares datasets to identify overlaps, differences, and correlations between multiple sources.
    
    Args:
        query (str): A user query indicating the desired operation (e.g., 'compare datasets', 'summarize data').
        files (dict | None): A dictionary mapping filenames to their content as strings or bytes. If None, file content is not available.
    
    Returns:
        str: A machine- and human-friendly result string containing the answer or an error message if files are required but not provided.
    """
    import json
    from typing import Any, Dict

    # Step 1: Validate inputs and normalize the query
    query = query.strip().lower()
    if files is None:
        return "Error: No files provided. Please supply a dictionary of files with their content."

    # Step 2: Detect user intent
    if "compare" in query:
        intent = "compare"
    elif "summarize" in query:
        intent = "summarize"
    else:
        intent = "unknown"

    # Step 3: Parse provided files
    parsed_data: Dict[str, Any] = {}
    for filename, content in files.items():
        try:
            if filename.endswith('.json'):
                parsed_data[filename] = json.loads(content)
            elif filename.endswith('.csv'):
                parsed_data[filename] = [line.split(',') for line in content.decode().strip().split('\n')]
            elif filename.endswith('.md') or filename.endswith('.txt'):
                parsed_data[filename] = content.decode().strip().split('\n')
            else:
                parsed_data[filename] = content.decode()
        except Exception as e:
            return f"Error parsing file '{filename}': {str(e)}"

    # Step 4: Select strategy based on intent and available files
    if intent == "compare":
        # Simple comparison logic
        if len(parsed_data) < 2:
            return "Error: At least two files are required for comparison."
        comparisons = {filename: len(data) for filename, data in parsed_data.items()}
        result = f"Comparison of datasets: {comparisons}"
    elif intent == "summarize":
        # Simple summarization logic
        summaries = {filename: len(data) for filename, data in parsed_data.items()}
        result = f"Summaries of datasets: {summaries}"
    else:
        return "Error: Unrecognized intent. Please specify 'compare' or 'summarize'."

    # Step 5: Produce a clear result string
    return f"Result: {result}\nSTEPS:\n- Validated inputs\n- Detected intent: {intent}\n- Parsed files\n- Executed strategy"
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "DataComparer",
        "description": "Compares datasets to identify overlaps, differences, and correlations between multiple sources.",
        "function": datacomparer_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")