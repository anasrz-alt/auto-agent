from typing import Any, Dict
import os

def fileio_func(input: str, files: dict | None = None) -> str:
    """
    Handles reading and writing of file-based data, including Excel and PDB formats.
    Accepts a user query to specify the operation and optional files for processing.
    Returns a string with the result of the operation or an error message.
    
    Parameters:
    - input (str): The user query specifying the operation to perform.
    - files (dict | None): A dictionary mapping filenames to file content as strings or bytes.
    
    Returns:
    - str: The result of the operation or an error message.
    """
    import pandas as pd
    from io import BytesIO

    # Step 1: Validate inputs and normalize the query
    if not isinstance(input, str):
        return "Invalid input: query must be a string."
    input = input.strip().lower()

    # Step 2: Detect user intent
    if "read excel" in input:
        intent = "read_excel"
    elif "read pdb" in input:
        intent = "read_pdb"
    else:
        return "Invalid query: Please specify 'read excel' or 'read pdb'."

    # Step 3: If files are provided, detect and parse file types
    if files is not None:
        if not isinstance(files, dict):
            return "Invalid files: must be a dictionary mapping filenames to content."
    else:
        return "No files provided for processing."

    # Step 4: Select a strategy based on intent and available files
    results = []
    for filename, content in files.items():
        try:
            if intent == "read_excel" and filename.endswith('.xlsx'):
                # Read Excel file
                df = pd.read_excel(BytesIO(content))
                results.append(f"Data from {filename}:\n{df.head()}")
            elif intent == "read_pdb" and filename.endswith('.pdb'):
                # Read PDB file
                pdb_data = content.decode('utf-8')
                results.append(f"Data from {filename}:\n{pdb_data[:100]}...")  # Show first 100 chars
            else:
                return f"Unsupported file type for {filename}."
        except Exception as e:
            return f"Error processing {filename}: {str(e)}"

    # Step 5: Produce a clear result string
    return "\n\n".join(results) if results else "No valid files processed."


# Unit tests for the fileio_func
def test_fileio_func():
    import pandas as pd
    from io import BytesIO

    # Prepare test data
    excel_file = BytesIO()
    pd.DataFrame({'A': [1, 2], 'B': [3, 4]}).to_excel(excel_file, index=False)
    excel_file.seek(0)

    pdb_file = BytesIO(b"HEADER\nATOM      1  N   MET A   1      20.154  34.250  27.500  1.00 20.00           N\n")

    # Test reading Excel file
    files = {'test.xlsx': excel_file.getvalue()}
    result = fileio_func("read excel", files)
    assert "Data from test.xlsx:" in result
    assert "A" in result
    assert "B" in result

    # Test reading PDB file
    files = {'test.pdb': pdb_file.getvalue()}
    result = fileio_func("read pdb", files)
    assert "Data from test.pdb:" in result
    assert "HEADER" in result

    # Test unsupported file type
    files = {'test.txt': b"Some text data"}
    result = fileio_func("read excel", files)
    assert "Unsupported file type for test.txt." in result

    # Test invalid input
    result = fileio_func(123, None)
    assert "Invalid input: query must be a string." in result

    # Test no files provided
    result = fileio_func("read excel", None)
    assert "No files provided for processing." in result

    print("All tests passed!")

# Uncomment to run tests
# test_fileio_func()
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "FileIO",
        "description": "Handles reading and writing of file-based data, including Excel and PDB formats.",
        "function": fileio_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")