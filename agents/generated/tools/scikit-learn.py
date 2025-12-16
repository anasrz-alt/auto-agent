from typing import Any, Dict
import os

def scikit_learn_func(query: str, files: dict | None = None) -> str:
    """A versatile tool for processing user queries related to machine learning tasks, 
    including summarization, extraction, transformation, and computation based on provided file content.
    
    Args:
        query (str): The user's request or question regarding machine learning or file content.
        files (dict | None): A dictionary mapping filenames to their content as strings or bytes.
        
    Returns:
        str: A response string containing the answer or result of the query, including steps taken if applicable.
    """
    import json
    import csv
    from io import StringIO

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: Query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize query

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
                content = content.decode('utf-8', errors='ignore')  # Decode bytes safely
            file_contents[filename] = content

    # Step 4: Select strategy based on intent and available files
    if intent in ["summarize", "extract"] and not file_contents:
        return "Error: No files provided. Please supply files to summarize or extract from."
    
    result = ""
    steps = []

    try:
        if intent == "summarize" and file_contents:
            # Summarize the content of the first text file found
            first_file_content = next(iter(file_contents.values()))
            result = first_file_content[:100] + "..."  # Simple summary (first 100 chars)
            steps.append("Summarized content from the first file.")
        
        elif intent == "extract" and file_contents:
            # Extract data from the first CSV file found
            for filename, content in file_contents.items():
                if filename.endswith('.csv'):
                    reader = csv.DictReader(StringIO(content))
                    extracted_data = [row for row in reader]
                    result = json.dumps(extracted_data)  # Return as JSON
                    steps.append("Extracted data from CSV file.")
                    break
        
        elif intent == "transform":
            result = "Transformation not implemented yet."
            steps.append("Requested transformation.")
        
        elif intent == "calculate":
            result = "Calculation not implemented yet."
            steps.append("Requested calculation.")
        
        elif intent == "search":
            result = "Search functionality not implemented yet."
            steps.append("Requested search.")
        
        else:
            result = "No valid intent detected or no files to process."
        
    except Exception as e:
        return f"Error during processing: {str(e)}"

    # Step 5: Produce a clear result string
    response = f"Result: {result}\n"
    if steps:
        response += "STEPS:\n" + "\n".join(steps)
    
    return response.strip()
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "Scikit-learn",
        "description": "A machine learning library for Python that provides simple and efficient tools for data mining and data analysis.",
        "function": scikit-learn_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")