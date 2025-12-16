from typing import Any, Dict
import os

def searchengine_func(query: str, files: dict | None = None) -> str:
    """A tool for processing user queries and reading provided files to answer questions or perform tasks. 
    Accepts a query string and an optional dictionary of files, returning a response string with the result or an error message."""
    
    import json
    
    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: Query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize query to lowercase
    
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
    if files is not None:
        file_contents = {}
        for filename, content in files.items():
            if isinstance(content, bytes):
                file_contents[filename] = content.decode(errors='ignore')
            else:
                file_contents[filename] = content
        
        # Step 4: Select strategy based on intent and available files
        if intent == "summarize" and file_contents:
            summaries = {filename: content[:100] + '...' for filename, content in file_contents.items()}  # Simple summary
            result = f"Summaries: {summaries}"
            return result + "\nSTEPS: \n- Normalized query\n- Detected intent\n- Summarized file contents"
        
        elif intent == "extract" and file_contents:
            extracted_data = {}
            for filename, content in file_contents.items():
                if filename.endswith('.json'):
                    try:
                        extracted_data[filename] = json.loads(content)
                    except json.JSONDecodeError:
                        return "Error: Invalid JSON format in file."
                elif filename.endswith('.csv'):
                    extracted_data[filename] = content.splitlines()  # Simple CSV extraction
                elif filename.endswith('.md') or filename.endswith('.txt'):
                    extracted_data[filename] = content.splitlines()  # Simple text extraction
            return f"Extracted Data: {json.dumps(extracted_data)}\nSTEPS: \n- Normalized query\n- Detected intent\n- Extracted data from files"
        
        elif intent == "transform" and file_contents:
            transformed_data = {filename: content.upper() for filename, content in file_contents.items()}  # Simple transformation
            return f"Transformed Data: {json.dumps(transformed_data)}\nSTEPS: \n- Normalized query\n- Detected intent\n- Transformed file contents"
        
        elif intent == "calculate":
            return "Error: Calculation requires specific numerical inputs, please specify."
        
        elif intent == "search":
            return "Error: Searching requires specific keywords, please specify."
    
    # Step 5: Handle case where files are required but not provided
    return "Error: No files provided. Please supply a dictionary of files with their content."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "SearchEngine",
        "description": "A tool for querying web search engines to retrieve real-time information and data from the internet, enhancing the agent's ability to answer complex questions.",
        "function": searchengine_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")