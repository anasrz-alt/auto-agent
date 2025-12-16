from typing import Any, Dict
import os

def dataaggregator_func(input: str, files: dict | None = None) -> str:
    """Aggregates and filters data based on specified criteria, such as beak lengths and food categories.
    
    Args:
        input (str): The query specifying the data aggregation criteria.
        files (dict | None): Optional dictionary mapping filename to file content as string or bytes.
        
    Returns:
        str: A machine- and human-friendly result string based on the input query and provided files.
    """
    import json
    import pandas as pd
    from typing import Any

    # Stage 1: Validate inputs and normalize the query
    if not isinstance(input, str) or not input.strip():
        return "Invalid input: Please provide a valid query string."
    
    query = input.strip().lower()

    # Stage 2: Detect user intent
    if "summarize" in query:
        intent = "summarize"
    elif "filter" in query:
        intent = "filter"
    else:
        return "Intent not recognized. Please specify 'summarize' or 'filter'."

    # Stage 3: Detect and parse file types if provided
    data_frames = {}
    if files:
        for filename, content in files.items():
            try:
                if filename.endswith('.json'):
                    data_frames[filename] = pd.json_normalize(json.loads(content))
                elif filename.endswith('.csv'):
                    data_frames[filename] = pd.read_csv(pd.compat.StringIO(content.decode('utf-8')))
                else:
                    return f"Unsupported file type for {filename}. Only JSON and CSV are supported."
            except Exception as e:
                return f"Error reading {filename}: {str(e)}"

    # Stage 4: Select a strategy based on intent and available files
    if not data_frames:
        return "No data files provided for processing."

    results = []
    for df in data_frames.values():
        if intent == "summarize":
            summary = df.describe(include='all').to_string()
            results.append(summary)
        elif intent == "filter":
            # Example filter criteria: filter by beak length greater than a threshold
            if 'beak_length' in df.columns:
                filtered = df[df['beak_length'] > 5]  # Example threshold
                results.append(filtered.to_string(index=False))
            else:
                return "No 'beak_length' column found for filtering."

    # Stage 5: Produce a clear result string
    if results:
        return "\n\n".join(results)
    else:
        return "No results found based on the provided criteria."

# Unit tests
def test_dataaggregator_func():
    # Test case 1: Valid summarize query with JSON input
    json_input = {
        "species": ["sparrow", "eagle", "parrot"],
        "beak_length": [3.5, 7.2, 4.1],
        "food_category": ["seeds", "meat", "fruits"]
    }
    result = dataaggregator_func("summarize", {"test.json": json.dumps(json_input)})
    assert "count" in result and "mean" in result, "Test case 1 failed"

    # Test case 2: Valid filter query with CSV input
    csv_input = "species,beak_length,food_category\nsparrow,3.5,seeds\neagle,7.2,meat\nparrot,4.1,fruits"
    result = dataaggregator_func("filter", {"test.csv": csv_input.encode('utf-8')})
    assert "eagle" in result, "Test case 2 failed"

    # Test case 3: Invalid input
    result = dataaggregator_func("", None)
    assert result == "Invalid input: Please provide a valid query string.", "Test case 3 failed"

    # Test case 4: Unsupported file type
    result = dataaggregator_func("summarize", {"test.txt": b"some text"})
    assert "Unsupported file type" in result, "Test case 4 failed"

    # Test case 5: No data files provided
    result = dataaggregator_func("filter", None)
    assert result == "No data files provided for processing.", "Test case 5 failed"

    print("All test cases passed!")

# Uncomment to run tests
# test_dataaggregator_func()
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "DataAggregator",
        "description": "Aggregates and filters data based on specified criteria, such as beak lengths and food categories.",
        "function": dataaggregator_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")