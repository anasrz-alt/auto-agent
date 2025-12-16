from typing import Any, Dict
import os

def dataanalyzer_func(query: str, files: dict | None = None) -> str:
    """A tool for performing statistical analysis and data mining, enabling the agent to derive actionable insights from datasets. 
    Inputs: a user query as a string and an optional dictionary of files where keys are filenames and values are file contents. 
    Output: a string containing the result of the analysis or an error message if applicable."""
    
    import json
    import csv
    from typing import Any

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
    elif "calculate" in query or "average" in query or "sum" in query:
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
                content = content.decode('utf-8', errors='ignore')  # Decode bytes safely
            file_contents[filename] = content

    # Step 4: Select strategy based on intent and available files
    if intent in ["summarize", "extract"] and not file_contents:
        return "Error: No files provided for summarization or extraction. Please supply files as a dictionary."

    results = []
    
    # Step 5: Execute the strategy
    try:
        if intent == "summarize":
            for filename, content in file_contents.items():
                results.append(f"Summary of {filename}: {content[:100]}...")  # Simple summary
            result_str = "\n".join(results)

        elif intent == "extract":
            for filename, content in file_contents.items():
                if content.strip().startswith('{'):  # Assuming JSON
                    data = json.loads(content)
                    results.append(f"Extracted data from {filename}: {json.dumps(data)}")
                elif content.strip().startswith('['):  # Assuming JSON array
                    data = json.loads(content)
                    results.append(f"Extracted data from {filename}: {json.dumps(data)}")
                else:  # Assuming plain text
                    results.append(f"Extracted text from {filename}: {content[:100]}...")
            result_str = "\n".join(results)

        elif intent == "calculate":
            for filename, content in file_contents.items():
                if content.strip().startswith('['):  # Assuming CSV-like data
                    reader = csv.reader(content.splitlines())
                    numbers = [float(row[0]) for row in reader if row and row[0].replace('.', '', 1).isdigit()]
                    avg = sum(numbers) / len(numbers) if numbers else 0
                    results.append(f"Average from {filename}: {avg}")
            result_str = "\n".join(results)

        elif intent == "search":
            search_term = query.split("search for")[-1].strip()
            for filename, content in file_contents.items():
                if search_term in content:
                    results.append(f"Found '{search_term}' in {filename}.")
            result_str = "\n".join(results) if results else "No matches found."

        else:
            result_str = "No actionable intent detected."

    except Exception as e:
        return f"Error during processing: {str(e)}"

    # Step 6: Produce a clear result string
    return result_str if results else "No results found."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "DataAnalyzer",
        "description": "A tool for performing statistical analysis and data mining, enabling the agent to derive actionable insights from datasets.",
        "function": dataanalyzer_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")