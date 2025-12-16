from typing import Any, Dict
import os

def websearchtool_func(query: str, files: dict | None = None) -> str:
    """Processes a user query to answer questions, extract information, or perform tasks using provided files. 
    Inputs: 
        - query (str): The user's request or question.
        - files (dict | None): A dictionary mapping filenames to their content (string or bytes). 
    Output: 
        - A string containing the answer or result, including steps taken if applicable."""
    
    import json
    import re

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: The query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize query to lowercase

    # Step 2: Detect user intent
    intent = "unknown"
    if "extract" in query:
        intent = "extract"
    elif "summarize" in query:
        intent = "summarize"
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
                content = content.decode(errors='ignore')  # Safely decode bytes
            file_contents[filename] = content

    # Step 4: Select strategy based on intent and available files
    if intent in ["extract", "summarize", "transform"] and not file_contents:
        return "Error: No files provided to perform the requested action. Please provide files."

    result = ""
    steps = []

    try:
        if intent == "extract":
            # Example extraction logic (simple regex for demonstration)
            matches = {filename: re.findall(r'\b\w+\b', content) for filename, content in file_contents.items()}
            result = json.dumps(matches)
            steps.append("Extracted words from files.")

        elif intent == "summarize":
            # Example summarization logic (simple character count)
            summaries = {filename: len(content) for filename, content in file_contents.items()}
            result = json.dumps(summaries)
            steps.append("Summarized file content lengths.")

        elif intent == "transform":
            # Example transformation (convert to uppercase)
            transformed = {filename: content.upper() for filename, content in file_contents.items()}
            result = json.dumps(transformed)
            steps.append("Transformed file contents to uppercase.")

        elif intent == "calculate":
            # Example calculation (dummy implementation)
            result = "Calculation results are not implemented."
            steps.append("Requested calculation, but no implementation available.")

        elif intent == "search":
            # Example search logic (search for a keyword)
            search_results = {filename: content for filename, content in file_contents.items() if query in content}
            result = json.dumps(search_results)
            steps.append("Searched for the query in files.")

        else:
            result = "No valid action could be determined based on the query."
            steps.append("No valid intent detected.")

    except Exception as e:
        return f"Error: An unexpected error occurred: {str(e)}"

    # Step 5: Produce a clear result string
    steps_info = "STEPS:\n" + "\n".join(steps)
    return f"Result: {result}\n{steps_info}"
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "WebSearchTool",
        "description": "Performs targeted web searches to retrieve contextual dates and additional information.",
        "function": websearchtool_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")