from typing import Any, Dict
import os

def pythonexecutor_func(input: str, files: dict | None = None) -> str:
    """
    Executes Python and Biopython code for data parsing and computational tasks. 
    Accepts a user query as input and optional files for context. Returns the result of the execution 
    or an informative error message if the execution fails.

    Args:
        input (str): A string containing the Python or Biopython code to execute.
        files (dict | None): A dictionary mapping filenames to their content as strings or bytes.

    Returns:
        str: The result of the execution or an error message.
    """
    import ast
    import traceback

    # Step 1: Validate inputs and normalize the query
    if not isinstance(input, str) or not input.strip():
        return "Error: Input must be a non-empty string containing code to execute."
    
    # Step 2: Detect user intent (execution of code)
    # In this case, we assume the intent is to execute the provided code
    code_to_execute = input.strip()

    # Step 3: If files are provided, detect and parse file types
    if files:
        file_contents = {}
        for filename, content in files.items():
            if isinstance(content, (str, bytes)):
                file_contents[filename] = content.decode() if isinstance(content, bytes) else content

    # Step 4: Execute the code safely
    try:
        # Prepare a local execution environment
        local_env = {}
        if 'file_contents' in locals():
            local_env.update(file_contents)  # Add file contents to local environment

        # Execute the code
        exec(code_to_execute, {}, local_env)

        # Step 5: Produce a result string from the local environment
        result = local_env.get('result', 'Execution completed without a result variable.')
        return str(result)

    except Exception as e:
        # Handle exceptions and return an informative error message
        error_message = f"Error during execution: {str(e)}\nTraceback:\n{traceback.format_exc()}"
        return error_message


# Example runs and unit tests
if __name__ == "__main__":
    # Example 1: Simple arithmetic execution
    print(pythonexecutor_func("result = 5 + 10"))  # Expected output: "15"

    # Example 2: Using a file content
    files_example = {"data.txt": "Hello, World!"}
    print(pythonexecutor_func("result = file_contents['data.txt'] + ' from PythonExecutor'", files_example))  # Expected output: "Hello, World! from PythonExecutor"

    # Example 3: Error handling
    print(pythonexecutor_func("result = 5 / 0"))  # Expected output: Error message about division by zero

    # Example 4: No result variable
    print(pythonexecutor_func("x = 10"))  # Expected output: "Execution completed without a result variable."

    # Unit tests
    assert pythonexecutor_func("result = 2 * 3") == "6"
    assert pythonexecutor_func("result = 10 - 4") == "6"
    assert pythonexecutor_func("result = file_contents['data.txt'] + ' is loaded.'", {"data.txt": "File"}) == "File is loaded."
    assert "Error during execution" in pythonexecutor_func("result = 1 / 0")
    assert pythonexecutor_func("x = 5") == "Execution completed without a result variable."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "PythonExecutor",
        "description": "Executes Python and Biopython code for data parsing and computational tasks.",
        "function": pythonexecutor_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")