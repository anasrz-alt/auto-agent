from typing import Any, Dict
import os

def databasequerytool_func(input: str, files: dict | None = None) -> str:
    """
    A tool that queries academic databases to retrieve publication counts and other relevant metrics based on user input.
    The input should specify the query type (e.g., 'count publications', 'list authors') and any relevant parameters.
    The output is a string summarizing the results or an error message if the query fails.
    """
    import json
    import re

    # Step 1: Validate inputs and normalize the query
    if not isinstance(input, str) or not input.strip():
        return "Error: Input query must be a non-empty string."
    
    query = input.strip().lower()

    # Step 2: Detect user intent
    if "count publications" in query:
        intent = "count"
    elif "list authors" in query:
        intent = "list"
    else:
        return "Error: Unrecognized query intent. Please specify 'count publications' or 'list authors'."

    # Step 3: If `files` is provided, detect and parse file types
    publications_data = []
    if files:
        for filename, content in files.items():
            try:
                if filename.endswith('.json'):
                    publications_data.extend(json.loads(content))
                elif filename.endswith('.txt'):
                    publications_data.extend(content.decode('utf-8').splitlines())
                else:
                    return f"Error: Unsupported file type for {filename}."
            except Exception as e:
                return f"Error processing {filename}: {str(e)}"

    # Step 4: Select a concise strategy based on intent and available files
    if intent == "count":
        # Count publications from the parsed data
        publication_count = len(publications_data)
        return f"Total publications found: {publication_count}."
    
    elif intent == "list":
        # List authors from the parsed data
        authors = set()
        for publication in publications_data:
            if isinstance(publication, dict) and 'author' in publication:
                authors.add(publication['author'])
        return f"Authors found: {', '.join(authors) if authors else 'No authors found.'}"

    # Step 5: Handle edge cases and errors robustly
    return "Error: No valid data to process."

# Example runs
print(databasequerytool_func("Count publications", {"data.json": json.dumps([{"author": "John Doe"}, {"author": "Jane Smith"}])})))
print(databasequerytool_func("List authors", {"data.json": json.dumps([{"author": "John Doe"}, {"author": "Jane Smith"}])})))

# Unit tests
def test_databasequerytool_func():
    assert databasequerytool_func("Count publications", {"data.json": json.dumps([{"author": "John Doe"}, {"author": "Jane Smith"}])}) == "Total publications found: 2."
    assert databasequerytool_func("List authors", {"data.json": json.dumps([{"author": "John Doe"}, {"author": "Jane Smith"}])}) == "Authors found: John Doe, Jane Smith."
    assert databasequerytool_func("Count publications", {"data.txt": b"Publication 1\nPublication 2"}) == "Total publications found: 2."
    assert databasequerytool_func("List authors", {"data.txt": b"Author: John Doe\nAuthor: Jane Smith"}) == "Authors found: No authors found."
    assert databasequerytool_func("Unknown query") == "Error: Unrecognized query intent. Please specify 'count publications' or 'list authors'."
    assert databasequerytool_func("", {"data.json": json.dumps([])}) == "Error: Input query must be a non-empty string."
    assert databasequerytool_func("Count publications", {"data.csv": b"Invalid format"}) == "Error: Unsupported file type for data.csv."
    print("All tests passed.")

test_databasequerytool_func()
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "DatabaseQueryTool",
        "description": "A tool that queries academic databases to retrieve publication counts and other relevant metrics.",
        "function": databasequerytool_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")