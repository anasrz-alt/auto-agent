from typing import Any, Dict
import os

def wikipediaapi_func(query: str, files: dict | None = None) -> str:
    """A tool to process user queries, optionally utilizing provided files to answer questions, extract data, or perform tasks. 
    Inputs: a query string and an optional dictionary of files. 
    Output: a string containing the answer or result, including steps taken if applicable."""
    
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
    elif "calculate" in query:
        intent = "calculate"
    elif "search" in query:
        intent = "search"
    
    # Step 3: Handle files if provided
    file_contents = {}
    if files:
        for filename, content in files.items():
            try:
                if isinstance(content, bytes):
                    content = content.decode('utf-8')
                file_contents[filename] = content
            except Exception as e:
                return f"Error reading file '{filename}': {str(e)}"

    # Step 4: Select strategy based on intent and available files
    if intent and file_contents:
        if intent == "summarize":
            return summarize_files(file_contents)
        elif intent == "extract":
            return extract_data(file_contents)
        elif intent == "transform":
            return transform_data(file_contents)
        elif intent == "calculate":
            return calculate_from_files(file_contents)
        elif intent == "search":
            return search_in_files(file_contents, query)
    elif intent and not files:
        return "Error: No files provided to perform the requested action. Please provide files to assist with your query."
    
    return "Error: Unable to determine intent or no actionable files provided."

def summarize_files(file_contents):
    # Simple summarization logic (placeholder)
    summaries = {filename: content[:100] + '...' for filename, content in file_contents.items()}
    return f"Summaries: {json.dumps(summaries)}"

def extract_data(file_contents):
    # Simple data extraction logic (placeholder)
    extracted_data = {filename: content.splitlines() for filename, content in file_contents.items()}
    return f"Extracted Data: {json.dumps(extracted_data)}"

def transform_data(file_contents):
    # Simple transformation logic (placeholder)
    transformed_data = {filename: content.upper() for filename, content in file_contents.items()}
    return f"Transformed Data: {json.dumps(transformed_data)}"

def calculate_from_files(file_contents):
    # Simple calculation logic (placeholder)
    calculations = {filename: len(content.split()) for filename, content in file_contents.items()}
    return f"Calculations: {json.dumps(calculations)}"

def search_in_files(file_contents, query):
    # Simple search logic (placeholder)
    results = {filename: content for filename, content in file_contents.items() if query in content.lower()}
    return f"Search Results: {json.dumps(results)}"
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "WikipediaAPI",
        "description": "An API that allows the agent to retrieve and parse information from Wikipedia articles, useful for historical trivia and detailed queries.",
        "function": wikipediaapi_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")