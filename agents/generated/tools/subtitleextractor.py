from typing import Any, Dict
import os

def subtitleextractor_func(query: str, files: dict | None = None) -> str:
    """Extracts subtitle text from provided files or answers queries about them. 
    Accepts a user query and a dictionary of files (filename -> content). 
    Returns a string with the result or an error message if files are missing or invalid."""
    
    import json
    import re
    
    # Step 1: Validate inputs and normalize the query
    if not isinstance(query, str) or not query.strip():
        return "Error: Query must be a non-empty string."
    
    query = query.strip().lower()
    
    # Step 2: Detect user intent
    intent = None
    if "extract" in query or "subtitle" in query:
        intent = "extract"
    elif "summarize" in query:
        intent = "summarize"
    elif "search" in query:
        intent = "search"
    
    # Step 3: Handle files if provided
    if files is None or not isinstance(files, dict) or not files:
        return "Error: No files provided. Please supply a dictionary of files (filename -> content)."
    
    subtitles = []
    
    # Step 4: Parse files based on their type
    for filename, content in files.items():
        try:
            if isinstance(content, bytes):
                content = content.decode('utf-8', errors='ignore')
            
            if filename.endswith('.txt') or filename.endswith('.md'):
                subtitles.append(content)
            elif filename.endswith('.json'):
                json_content = json.loads(content)
                subtitles.append(json.dumps(json_content))
            elif filename.endswith('.csv'):
                csv_lines = content.splitlines()
                subtitles.extend(csv_lines)
        except Exception as e:
            return f"Error processing file '{filename}': {str(e)}"
    
    # Step 5: Execute the strategy based on intent
    if intent == "extract":
        result = "\n".join(subtitles)
    elif intent == "summarize":
        result = " ".join(subtitles)[:200] + "..."  # Simple truncation for summary
    elif intent == "search":
        search_term = re.sub(r'\s+', ' ', query.replace("search", "").strip())
        result = "\n".join([line for line in subtitles if search_term in line])
    else:
        return "Error: Unrecognized intent. Please clarify your query."
    
    # Step 6: Produce a clear result string
    return f"Result:\n{result}\n\nSTEPS:\n- Validated query\n- Detected intent: {intent}\n- Parsed files\n- Executed strategy: {intent}\n- Produced result."
# should include what is input of the tool as well as what it returns

def get_tool_definition() -> Dict[str, Any]:
    return {
        "name": "SubtitleExtractor",
        "description": "Extracts subtitle text from video files to provide narrative context for analysis.",
        "function": subtitleextractor_func
    }

if __name__ == "__main__":
    tool_def = get_tool_definition()
    print(f"Tool: {tool_def['name']} loaded successfully.")