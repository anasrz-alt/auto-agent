from typing import Any, Dict
import os

def calculatortool_func(query: str, files: dict | None = None) -> str:
    """A versatile tool for performing calculations, extracting information, and summarizing content from provided files. 
    Accepts a user query and optional file contents, returning a string with results or instructions. 
    The output format is a clear answer with steps taken, and structured data is returned as JSON when applicable."""
    
    import json
    import re

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: The query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize query to lowercase

    # Step 2: Detect user intent
    intent = None
    if "calculate" in query:
        intent = "calculate"
    elif "summarize" in query:
        intent = "summarize"
    elif "extract" in query:
        intent = "extract"
    elif "transform" in query:
        intent = "transform"
    elif "search" in query:
        intent = "search"
    
    # Step 3: Handle files if provided
    file_contents = {}
    if files:
        for filename, content in files.items():
            if isinstance(content, bytes):
                content = content.decode(errors='ignore')  # Safely decode bytes
            file_contents[filename] = content

    # Step 4: Select strategy based on intent
    if intent == "calculate":
        # Simple calculation extraction
        try:
            expression = re.search(r'calculate (.+)', query).group(1)
            result = eval(expression)  # Caution: eval can be dangerous; ensure input is controlled.
            return f"Result: {result}\nSTEPS:\n- Parsed calculation expression.\n- Evaluated the result."
        except Exception as e:
            return f"Error: Unable to perform calculation. {str(e)}"

    elif intent in ["summarize", "extract", "transform"] and not file_contents:
        return "Error: No files provided. Please supply files to summarize or extract data from."

    elif intent == "summarize" and file_contents:
        summaries = []
        for filename, content in file_contents.items():
            summaries.append(f"{filename}: {content[:100]}...")  # Summarize by showing first 100 chars
        return f"Summaries:\n" + "\n".join(summaries) + "\nSTEPS:\n- Read file contents.\n- Generated summaries."

    elif intent == "extract" and file_contents:
        extracted_data = {}
        for filename, content in file_contents.items():
            matches = re.findall(r'\b\d+\b', content)  # Extract all numbers as an example
            extracted_data[filename] = matches
        return f"Extracted Data: {json.dumps(extracted_data)}\nSTEPS:\n- Read file contents.\n- Extracted numbers."

    # Step 5: Handle unknown intents
    return "Error: Unable to determine the intent of the query. Please provide a valid query."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "CalculatorTool",
        "description": "A precise computation tool for performing mathematical calculations and financial modeling.",
        "function": calculatortool_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")