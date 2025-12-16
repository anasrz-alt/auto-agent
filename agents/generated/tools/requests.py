from typing import Any, Dict
import os

def requests_func(query: str, files: dict | None = None) -> str:
    """Processes a user query to extract information, summarize content, or perform tasks using provided files.
    
    Args:
        query (str): The user's request or question.
        files (dict | None): A dictionary mapping filenames to their content as strings or bytes.
        
    Returns:
        str: A response string containing the answer or result of the query, including steps taken if applicable.
    """
    import json

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: The query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize query for easier processing

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
    else:
        intent = "general"

    # Step 3: Handle files if provided
    if files is not None:
        file_contents = {}
        for filename, content in files.items():
            if isinstance(content, bytes):
                file_contents[filename] = content.decode(errors='ignore')  # Decode bytes safely
            else:
                file_contents[filename] = content

    # Step 4: Select strategy based on intent and available files
    if intent in ["summarize", "extract"] and files:
        combined_text = " ".join(file_contents.values())
        if intent == "summarize":
            result = f"Summary of provided content: {combined_text[:100]}..."  # Simple summary
        elif intent == "extract":
            result = json.dumps({"extracted": combined_text.split()[:5]})  # Example extraction
            result = f"Extracted data (JSON): {result}"
    elif intent == "calculate":
        # Placeholder for calculation logic
        result = "Calculation results: None (no calculation logic implemented)."
    elif intent == "search":
        if "in" in query:
            search_term = query.split("in")[-1].strip()
            result = f"Searching for '{search_term}' in provided files."
        else:
            result = "Error: No search term provided."
    else:
        result = "No specific action could be determined from the query."

    # Step 5: Produce a clear result string
    steps = [
        "Validated and normalized the query.",
        f"Detected intent: {intent}.",
        "Processed provided files.",
        "Executed the selected strategy."
    ]
    return f"{result}\n\nSTEPS:\n- " + "\n- ".join(steps)
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "Requests",
        "description": "A simple and elegant HTTP library for Python, used for making API calls.",
        "function": requests_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")