from typing import Any, Dict
import os

def insightextractiontool_func(query: str, files: dict | None = None) -> str:
    """Extract insights based on a user query and optional file contents. 
    The function processes the query to determine intent and utilizes provided files 
    (if any) to generate a response, returning a structured string with results.

    Args:
        query (str): The user query to process.
        files (dict | None): A dictionary mapping filenames to their content as strings or bytes.

    Returns:
        str: A response string containing the primary answer and, if applicable, a JSON representation of extracted data.
    """
    import json

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: The query must be a non-empty string."

    query = query.strip().lower()  # Normalize the query

    # Step 2: Detect user intent
    intent = "unknown"
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
                try:
                    file_contents[filename] = content.decode('utf-8')
                except UnicodeDecodeError:
                    return f"Error: The file '{filename}' is not a valid text file."
            elif isinstance(content, str):
                file_contents[filename] = content
            else:
                return f"Error: Unsupported content type for file '{filename}'."

    # Step 4: Select strategy based on intent and available files
    if intent == "unknown" and not files:
        return "Error: No actionable intent detected and no files provided. Please provide a query and files."

    results = []
    if intent == "summarize" and files:
        for content in file_contents.values():
            results.append(content[:100] + "...")  # Simple summarization by truncation
        response = "Summary: " + " | ".join(results)
    elif intent == "extract" and files:
        extracted_data = {filename: content.splitlines() for filename, content in file_contents.items()}
        response = "Extracted Data: " + json.dumps(extracted_data)
    elif intent == "calculate":
        # Placeholder for calculation logic
        response = "Calculation results are not implemented yet."
    elif intent == "transform":
        # Placeholder for transformation logic
        response = "Transformation results are not implemented yet."
    elif intent == "search":
        # Placeholder for search logic
        response = "Search functionality is not implemented yet."
    else:
        response = "No specific action could be determined."

    # Step 5: Produce a clear result string
    steps = [
        "Validated and normalized the query.",
        "Detected user intent.",
        "Processed provided files.",
        "Executed the selected strategy."
    ]
    return f"{response}\n\nSTEPS: " + " | ".join(steps)
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "InsightExtractionTool",
        "description": "A tool that extracts meaningful insights from video content and associated data.",
        "function": insightextractiontool_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")