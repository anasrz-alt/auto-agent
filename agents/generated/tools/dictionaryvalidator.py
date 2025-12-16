from typing import Any, Dict
import os

def dictionaryvalidator_func(query: str, files: dict | None = None) -> str:
    """Validates words against specified dictionaries, ensuring case-insensitive matches and filtering as needed.
    
    Args:
        query (str): The user query that specifies the validation task.
        files (dict | None): A dictionary mapping filenames to their contents, which may include dictionary data.
        
    Returns:
        str: A result string containing the validation outcome or an error message if files are missing.
    """
    import json

    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: Query must be a non-empty string."
    
    query = query.strip().lower()  # Normalize query to lowercase

    # Step 2: Detect user intent
    if "validate" in query:
        intent = "validate"
    else:
        return "Error: Unsupported query. Please use a query that includes 'validate'."

    # Step 3: Detect and parse provided files
    if files is None or not isinstance(files, dict):
        return "Error: No files provided. Please supply a dictionary of files."
    
    dictionaries = {}
    
    for filename, content in files.items():
        try:
            if filename.endswith('.json'):
                dictionaries.update(json.loads(content))
            elif filename.endswith('.txt'):
                for line in content.splitlines():
                    word = line.strip().lower()
                    if word:
                        dictionaries[word] = True
            elif filename.endswith('.csv'):
                for line in content.splitlines()[1:]:  # Skip header
                    word = line.split(',')[0].strip().lower()
                    if word:
                        dictionaries[word] = True
            elif filename.endswith('.md'):
                for line in content.splitlines():
                    word = line.strip().lower()
                    if word:
                        dictionaries[word] = True
        except Exception as e:
            return f"Error: Failed to parse file '{filename}'. Reason: {str(e)}"

    # Step 4: Execute the strategy based on intent
    if intent == "validate":
        words_to_validate = query.split()[1:]  # Assume words follow the 'validate' command
        results = {word: (word in dictionaries) for word in words_to_validate}

    # Step 5: Produce a clear result string
    result_json = json.dumps(results)
    return f"Validation results: {result_json}\nSTEPS:\n- Normalized query.\n- Parsed provided files.\n- Validated words against dictionaries."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "DictionaryValidator",
        "description": "Validates words against specified dictionaries, ensuring case-insensitive matches and filtering as needed.",
        "function": dictionaryvalidator_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")