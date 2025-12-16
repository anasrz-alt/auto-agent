from typing import Any, Dict
import os

def ocrtool_func(query: str, files: dict | None = None) -> str:
    """OCRTool processes user queries to extract information from provided files or perform tasks. 
    It accepts a query string and an optional dictionary of files, returning a string response with the result 
    or an error message if files are needed but not provided."""
    
    import json

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: Query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize query to lowercase

    # Step 2: Detect user intent
    intent = None
    if "extract" in query:
        intent = "extract"
    elif "summarize" in query:
        intent = "summarize"
    elif "transform" in query:
        intent = "transform"
    elif "search" in query:
        intent = "search"
    else:
        intent = "general"

    # Step 3: Handle files if provided
    if files is not None:
        file_contents = {}
        for filename, content in files.items():
            if isinstance(content, bytes):
                try:
                    file_contents[filename] = content.decode('utf-8')
                except Exception:
                    file_contents[filename] = "Error: Unable to decode binary content."
            elif isinstance(content, str):
                file_contents[filename] = content
            else:
                file_contents[filename] = "Error: Unsupported file content type."

    # Step 4: Select a strategy based on intent and available files
    if intent in ["extract", "summarize", "transform"] and files is None:
        return "Error: No files provided. Please supply files to extract or summarize content."
    
    result = ""
    if intent == "extract" and files:
        # Example extraction logic (placeholder)
        result = {filename: content for filename, content in file_contents.items() if isinstance(content, str)}
        result = json.dumps(result)
        result = f"Extracted content: {result}"

    elif intent == "summarize" and files:
        # Example summarization logic (placeholder)
        combined_text = " ".join(content for content in file_contents.values() if isinstance(content, str))
        result = f"Summary: {combined_text[:100]}..."  # Simple truncation for demonstration

    elif intent == "transform":
        # Example transformation logic (placeholder)
        result = "Transformation completed."  # Placeholder for actual transformation logic

    elif intent == "search" and files:
        # Example search logic (placeholder)
        search_term = query.split("search")[-1].strip()
        found = {filename: content for filename, content in file_contents.items() if search_term in content}
        result = json.dumps(found)
        result = f"Search results: {result}"

    else:
        result = "No actionable intent detected or unsupported operation."

    # Step 5: Produce a clear result string
    return result + "\nSTEPS:\n- Validated input query.\n- Detected intent.\n- Processed files.\n- Executed strategy."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "OCRTool",
        "description": "Optical Character Recognition tool that extracts text from images or documents, converting visual information into editable and searchable text.",
        "function": ocrtool_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")