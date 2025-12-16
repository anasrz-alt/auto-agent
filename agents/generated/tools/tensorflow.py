from typing import Any, Dict
import os

def tensorflow_func(query: str, files: dict | None = None) -> str:
    """Processes a user query to extract information, summarize, or perform tasks based on provided files. 
    Inputs:
        query: A string containing the user's request.
        files: A dictionary mapping filenames to their content (as strings or bytes).
    Output:
        A string containing the result of the query processing, including any extracted data or summaries.
    """
    import json
    import re

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: Invalid query. Please provide a non-empty string query."
    
    query = query.strip().lower()  # Normalize the query

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
    file_contents = {}
    if files:
        for filename, content in files.items():
            if isinstance(content, bytes):
                content = content.decode(errors='ignore')  # Safely decode bytes
            file_contents[filename] = content

    # Step 4: Select strategy based on intent and available files
    if intent in ["extract", "summarize"] and not file_contents:
        return "Error: File content is required for extraction or summarization. Please provide files."

    result = ""
    if intent == "summarize":
        # Summarize text from files
        summaries = {filename: content[:100] + '...' for filename, content in file_contents.items()}  # Simple summary
        result = "Summaries:\n" + "\n".join(f"{filename}: {summary}" for filename, summary in summaries.items())
    
    elif intent == "extract":
        # Extract structured data (e.g., JSON-like patterns)
        extracted_data = {}
        for filename, content in file_contents.items():
            matches = re.findall(r'\{.*?\}', content)  # Simple regex for JSON-like structures
            extracted_data[filename] = matches
        result = "Extracted Data (JSON): " + json.dumps(extracted_data)

    elif intent == "transform":
        # Simple transformation (e.g., convert to uppercase)
        transformed = {filename: content.upper() for filename, content in file_contents.items()}
        result = "Transformed Content:\n" + "\n".join(f"{filename}: {content}" for filename, content in transformed.items())

    elif intent == "calculate":
        # Placeholder for calculations, assuming a simple arithmetic expression in the query
        try:
            expression = re.sub(r'[^0-9+\-*/().]', '', query)  # Sanitize input
            result = f"Calculation Result: {eval(expression)}"
        except Exception as e:
            result = f"Error in calculation: {str(e)}"

    else:
        result = "General query processed. No specific action taken."

    # Step 5: Produce a clear result string
    return result + "\nSTEPS: " + "\n".join([
        "Validated and normalized the query.",
        "Detected user intent.",
        "Processed provided files.",
        "Executed the strategy based on intent.",
        "Generated the result."
    ])
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "TensorFlow",
        "description": "An open-source library for numerical computation and machine learning, providing a flexible ecosystem for building ML models.",
        "function": tensorflow_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")