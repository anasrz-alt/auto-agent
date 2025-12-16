from typing import Any, Dict
import os

def speechtotext_func(query: str, files: dict | None = None) -> str:
    """Converts spoken audio into text, allowing the agent to process verbal commands and transcribe audio files.
    
    Args:
        query (str): The user query specifying the desired action or information.
        files (dict | None): A dictionary mapping filenames to their content as strings or bytes.
    
    Returns:
        str: A response string containing the result of the query processing or an error message.
    """
    import json

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
    elif "search" in query:
        intent = "search"
    elif "calculate" in query:
        intent = "calculate"
    else:
        intent = "general"

    # Step 3: Handle files if provided
    file_contents = {}
    if files:
        for filename, content in files.items():
            if isinstance(content, bytes):
                try:
                    file_contents[filename] = content.decode('utf-8')
                except UnicodeDecodeError:
                    return f"Error: File '{filename}' is not a valid UTF-8 text."
            elif isinstance(content, str):
                file_contents[filename] = content
            else:
                return f"Error: Unsupported content type for file '{filename}'."

    # Step 4: Select a strategy based on intent and available files
    if intent == "summarize" and file_contents:
        # Summarize the content of the first file
        first_file_content = next(iter(file_contents.values()))
        summary = first_file_content[:100] + "..."  # Simple summary (first 100 chars)
        result = f"Summary: {summary}\nSTEPS: 1. Identified intent. 2. Summarized content."
    
    elif intent == "extract" and file_contents:
        # Extract data from the first file (assuming it's plain text)
        first_file_content = next(iter(file_contents.values()))
        extracted_data = first_file_content.splitlines()  # Simple line extraction
        result = f"Extracted Data: {json.dumps(extracted_data)}\nSTEPS: 1. Identified intent. 2. Extracted lines."
    
    elif intent == "search" and file_contents:
        # Search for a keyword in the first file
        keyword = query.split("search for")[-1].strip() if "search for" in query else ""
        if keyword and file_contents:
            first_file_content = next(iter(file_contents.values()))
            occurrences = first_file_content.lower().count(keyword)
            result = f"Occurrences of '{keyword}': {occurrences}\nSTEPS: 1. Identified intent. 2. Searched for keyword."
        else:
            result = "Error: No keyword provided for search."
    
    elif intent == "calculate":
        # Simple calculation example (e.g., sum of numbers in query)
        numbers = [int(num) for num in query.split() if num.isdigit()]
        if numbers:
            total = sum(numbers)
            result = f"Total: {total}\nSTEPS: 1. Identified intent. 2. Calculated sum."
        else:
            result = "Error: No valid numbers found for calculation."
    
    else:
        result = "Error: No actionable files provided or unrecognized intent."

    return result
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "SpeechToText",
        "description": "Converts spoken audio into text, allowing the agent to process verbal commands and transcribe audio files.",
        "function": speechtotext_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")