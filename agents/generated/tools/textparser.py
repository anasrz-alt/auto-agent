from typing import Any, Dict
import os

def textparser_func(query: str, files: dict | None = None) -> str:
    """A tool for parsing and formatting text outputs according to specific instructions, ensuring data is presented in the required formats. It accepts a user query and optional files, processes the query to determine intent, and returns a formatted response based on the content of the files or the query itself."""
    
    import json
    import re

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: Invalid query. Please provide a non-empty string as the query."
    
    query = query.strip().lower()  # Normalize the query

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
        intent = "generate"

    # Step 3: Handle files if provided
    file_contents = {}
    if files:
        for filename, content in files.items():
            if isinstance(content, bytes):
                content = content.decode(errors='ignore')  # Safely decode bytes
            file_contents[filename] = content

    # Step 4: Select strategy based on intent and available files
    if intent in ["summarize", "extract", "search"] and not file_contents:
        return "Error: No files provided. Please supply files to process with your query."

    result = ""
    if intent == "summarize" and file_contents:
        # Summarize the content of the first file
        first_file_content = next(iter(file_contents.values()))
        result = f"Summary: {first_file_content[:100]}..."  # Simple summary (first 100 chars)
    elif intent == "extract" and file_contents:
        # Extract data using regex as an example
        extracted_data = re.findall(r'\b\w+\b', first_file_content)
        result = json.dumps(extracted_data)  # Return as JSON
    elif intent == "search" and file_contents:
        # Search for a keyword in the first file
        keyword = re.search(r'search for (.+)', query)
        if keyword:
            keyword = keyword.group(1)
            if keyword in first_file_content:
                result = f"Found '{keyword}' in the file."
            else:
                result = f"'{keyword}' not found in the file."
    elif intent == "calculate":
        # Simple calculation example (just return a placeholder)
        result = "Calculation results: [Placeholder for calculation results]"
    else:
        result = "No specific action taken based on the query."

    # Step 5: Produce a clear result string
    steps = [
        "Validated and normalized the query.",
        f"Detected intent: {intent}.",
        "Processed files if provided.",
        "Executed the strategy based on intent."
    ]
    return f"{result}\n\nSTEPS:\n" + "\n".join(steps)
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "TextParser",
        "description": "A tool for parsing and formatting text outputs according to specific instructions, ensuring data is presented in the required formats.",
        "function": textparser_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")