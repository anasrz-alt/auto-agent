from typing import Any, Dict
import os

def wikipedia_func(query: str, files: dict | None = None) -> str:
    """A tool for processing user queries and reading provided files to extract or summarize information. 
    Inputs: a query string and an optional dictionary of files (filename -> content). 
    Output: a string containing the answer or instructions if files are needed but not provided."""
    
    import json
    
    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: The query must be a non-empty string."
    
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
    else:
        intent = "search"

    # Step 3: Handle files if provided
    file_contents = {}
    if files:
        for filename, content in files.items():
            if isinstance(content, bytes):
                try:
                    content = content.decode('utf-8')
                except UnicodeDecodeError:
                    return f"Error: Unable to decode {filename}. Please provide valid text content."
            file_contents[filename] = content

    # Step 4: Select a strategy based on intent and available files
    if intent in ["summarize", "extract"] and not files:
        return "Error: No files provided. Please supply files to summarize or extract information."
    
    result = ""
    if intent == "summarize":
        # Summarizing content from the first file if available
        if file_contents:
            first_file_content = next(iter(file_contents.values()))
            result = f"Summary of the content: {first_file_content[:100]}..."  # Simple summary
        else:
            result = "Error: No content to summarize."
    
    elif intent == "extract":
        # Extracting structured data from JSON if available
        for filename, content in file_contents.items():
            try:
                data = json.loads(content)
                result = f"Extracted JSON data from {filename}: {json.dumps(data)}"
                break
            except json.JSONDecodeError:
                continue
        else:
            result = "Error: No valid JSON content found in provided files."
    
    elif intent == "transform":
        # Simple transformation example (uppercase)
        if file_contents:
            transformed_content = {filename: content.upper() for filename, content in file_contents.items()}
            result = f"Transformed content: {json.dumps(transformed_content)}"
        else:
            result = "Error: No content to transform."
    
    elif intent == "calculate":
        # Placeholder for calculation logic
        result = "Calculation functionality is not implemented yet."
    
    else:
        # Default search strategy
        result = "No specific intent recognized. Please refine your query."

    # Step 5: Produce a clear result string
    return f"Result: {result}\nSTEPS: - Validated input\n- Detected intent: {intent}\n- Processed files: {len(file_contents)}"
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "Wikipedia",
        "description": "A tool for accessing structured knowledge from Wikipedia, enabling the agent to provide accurate and contextual information on a wide range of topics.",
        "function": wikipedia_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")