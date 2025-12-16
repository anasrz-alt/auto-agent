from typing import Any, Dict
import os

def objectdetectionmodel_func(query: str, files: dict | None = None) -> str:
    """Processes a user query to perform tasks related to object detection, 
    including reading provided files for context. Returns a string with the 
    result or an error message if no files are provided when needed.

    Args:
        query (str): The user query detailing the task to perform.
        files (dict | None): A dictionary mapping filenames to their content.

    Returns:
        str: The result of processing the query, or an error message if applicable.
    """
    import json

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
    elif "search" in query:
        intent = "search"
    elif "calculate" in query:
        intent = "calculate"
    else:
        intent = "unknown"

    # Step 3: Handle files if provided
    if files is not None:
        file_contents = {}
        for filename, content in files.items():
            if isinstance(content, bytes):
                content = content.decode(errors='ignore')  # Safely decode bytes
            file_contents[filename] = content

    # Step 4: Select strategy based on intent and available files
    if intent in ["extract", "summarize", "search"] and (files is None or not files):
        return "Error: No files provided. Please supply files for processing."

    result = ""
    steps = []

    try:
        if intent == "summarize":
            # Summarize text content from files
            for content in file_contents.values():
                result += content[:100] + "...\n"  # Simple summary (first 100 chars)
            steps.append("Summarized content from files.")

        elif intent == "extract":
            # Extract structured data from JSON or CSV
            for filename, content in file_contents.items():
                if filename.endswith('.json'):
                    data = json.loads(content)
                    result += json.dumps(data, indent=2) + "\n"
                    steps.append(f"Extracted JSON data from {filename}.")
                elif filename.endswith('.csv'):
                    rows = content.splitlines()
                    result += json.dumps([row.split(',') for row in rows], indent=2) + "\n"
                    steps.append(f"Extracted CSV data from {filename}.")

        elif intent == "transform":
            # Simple transformation example
            for content in file_contents.values():
                result += content.upper() + "\n"  # Transform to uppercase
            steps.append("Transformed content to uppercase.")

        elif intent == "search":
            # Search for a keyword in the files
            keyword = query.split("search for")[-1].strip()
            for filename, content in file_contents.items():
                if keyword in content:
                    result += f"Found '{keyword}' in {filename}.\n"
            steps.append(f"Searched for '{keyword}' in files.")

        elif intent == "calculate":
            # Placeholder for calculation logic
            result = "Calculation feature is not implemented yet."
            steps.append("Attempted to perform a calculation.")

        else:
            result = "Error: Unknown intent. Please refine your query."

    except Exception as e:
        result = f"Error processing files: {str(e)}"

    # Step 5: Produce a clear result string
    if result:
        return f"Result:\n{result}\nSTEPS:\n" + "\n".join(steps)
    return "No relevant result found."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "ObjectDetectionModel",
        "description": "A model that identifies and locates objects within video frames.",
        "function": objectdetectionmodel_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")