from typing import Any, Dict
import os

def pdfextractor_func(query: str, files: dict | None = None) -> str:
    """Extracts information from provided files based on the user query. 
    Accepts a query string and an optional dictionary of files (filename -> content). 
    Returns a string with the result or an error message if no files are provided or if the query cannot be fulfilled."""
    
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
    elif "search" in query:
        intent = "search"
    elif "transform" in query:
        intent = "transform"
    else:
        return "Error: Unable to determine intent from the query."

    # Step 3: Handle files if provided
    if files is None or not files:
        return "Error: No files provided. Please supply files in the format: {filename: content}."

    # Step 4: Define a helper function to parse file content
    def parse_file_content(content: bytes | str) -> str:
        if isinstance(content, bytes):
            return content.decode('utf-8', errors='ignore')  # Decode bytes to string
        return content  # Return string as is

    # Step 5: Initialize a result variable
    results = []

    # Step 6: Process each file based on intent
    for filename, content in files.items():
        try:
            text = parse_file_content(content)  # Parse file content
            if intent == "extract":
                results.append(f"Extracted from {filename}: {text[:100]}...")  # Example extraction
            elif intent == "summarize":
                results.append(f"Summary of {filename}: {text[:100]}...")  # Example summary
            elif intent == "search":
                if query in text.lower():
                    results.append(f"Found '{query}' in {filename}.")
                else:
                    results.append(f"'{query}' not found in {filename}.")
            elif intent == "transform":
                results.append(f"Transformed content from {filename}: {text.upper()[:100]}...")  # Example transformation
        except Exception as e:
            results.append(f"Error processing {filename}: {str(e)}")

    # Step 7: Produce a clear result string
    if results:
        return "\n".join(results) + "\nSTEPS:\n- Validated query.\n- Determined intent.\n- Processed files."
    else:
        return "Error: No results generated."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "PDFExtractor",
        "description": "A tool that extracts text and data from PDF documents for analysis and extraction tasks.",
        "function": pdfextractor_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")