from typing import Any, Dict
import os

def dataorganizer_func(query: str, files: dict | None = None) -> str:
    """Organizes and categorizes data extracted from audio and text, facilitating efficient retrieval and management.
    
    Args:
        query (str): The user query specifying the task to perform.
        files (dict | None): A dictionary mapping filenames to their content as strings or bytes. 
                              If None, file content is not available for processing.
    
    Returns:
        str: A string containing the result of the query, including any structured data in JSON format if applicable.
    """
    import json
    import re

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: Invalid query. Please provide a non-empty string."
    
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
                content = content.decode(errors='ignore')
            file_contents[filename] = content

    # Step 4: Select strategy based on intent and available files
    if intent == "summarize":
        if not file_contents:
            return "Error: No files provided for summarization. Please supply files."
        # Simple summarization by taking the first few lines
        summary = {filename: content.splitlines()[:3] for filename, content in file_contents.items()}
        return f"Summary: {summary}\nSTEPS: [1. Validate input, 2. Detect intent, 3. Summarize files]"

    elif intent == "extract":
        if not file_contents:
            return "Error: No files provided for extraction. Please supply files."
        # Example extraction: find all email addresses in the text
        extracted_data = {}
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        for filename, content in file_contents.items():
            extracted_data[filename] = re.findall(email_pattern, content)
        return f"Extracted Emails: {json.dumps(extracted_data)}\nSTEPS: [1. Validate input, 2. Detect intent, 3. Extract emails]"

    elif intent == "transform":
        return "Error: Transformation tasks require specific instructions. Please clarify."

    elif intent == "calculate":
        return "Error: Calculation tasks require specific data. Please provide numerical data."

    elif intent == "search":
        return "Error: Search tasks require specific keywords and files. Please clarify."

    # Step 5: Handle cases where intent is not recognized
    return "Error: Unrecognized query. Please specify a valid task (summarize, extract, transform, calculate, search)."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "DataOrganizer",
        "description": "Organizes and categorizes data extracted from audio and text, facilitating efficient retrieval and management.",
        "function": dataorganizer_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")