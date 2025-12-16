from typing import Any, Dict
import os

def dataorganizationtool_func(query: str, files: dict | None = None) -> str:
    """A tool for organizing and structuring data efficiently for easy access and analysis. 
    It accepts a user query and optional files, processes the query to determine intent, 
    and returns a structured response or error message if necessary.

    Args:
        query (str): The user query specifying the task or information needed.
        files (dict | None): A dictionary mapping filenames to their content as strings or bytes.

    Returns:
        str: A machine- and human-friendly result string, including JSON if applicable.
    """
    import json

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: Query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize query for easier processing

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
        return "Error: Unable to determine intent from the query."

    # Step 3: Handle files if provided
    file_contents = {}
    if files:
        for filename, content in files.items():
            if isinstance(content, bytes):
                try:
                    file_contents[filename] = content.decode('utf-8')
                except UnicodeDecodeError:
                    return f"Error: Unable to decode binary content from {filename}."
            elif isinstance(content, str):
                file_contents[filename] = content
            else:
                return f"Error: Unsupported content type for {filename}."

    # Step 4: Select strategy based on intent and available files
    if intent in ["summarize", "extract"] and not file_contents:
        return "Error: No files provided. Please supply files to extract or summarize data."

    result = ""
    steps = []

    # Step 5: Execute the strategy
    try:
        if intent == "summarize":
            for filename, content in file_contents.items():
                result += f"Summary of {filename}: {content[:100]}...\n"  # Simple summary
                steps.append(f"Summarized {filename}")

        elif intent == "extract":
            extracted_data = {filename: content.splitlines() for filename, content in file_contents.items()}
            result = f"Extracted data: {json.dumps(extracted_data)}"  # Return as JSON
            steps.append("Extracted structured data.")

        elif intent == "transform":
            for filename, content in file_contents.items():
                transformed_content = content.upper()  # Example transformation
                result += f"Transformed content of {filename}: {transformed_content}\n"
                steps.append(f"Transformed {filename}")

        elif intent == "search":
            search_term = query.split("search for")[-1].strip()
            for filename, content in file_contents.items():
                if search_term in content:
                    result += f"Found '{search_term}' in {filename}.\n"
                    steps.append(f"Searched {filename} for '{search_term}'.")

        elif intent == "calculate":
            # Placeholder for calculation logic
            result = "Calculation results would be here."
            steps.append("Performed calculations.")

    except Exception as e:
        return f"Error: An unexpected error occurred: {str(e)}"

    # Step 6: Produce a clear result string
    return f"{result}\nSTEPS: {', '.join(steps)}" if result else "No relevant results found."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "DataOrganizationTool",
        "description": "A tool for organizing and structuring data efficiently for easy access and analysis.",
        "function": dataorganizationtool_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")