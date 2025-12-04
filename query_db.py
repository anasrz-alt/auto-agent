import json
import subprocess
import tempfile
import os
from typing import List, Dict, Any
CODEQL_DB_PATH = "codeql_db"  
CODEQL_CLI = "codeql"         
def query_codeql_database(query: str) -> List[Dict[str, Any]]:
    results = []
    with tempfile.TemporaryDirectory() as tmpdir:
        query_file = os.path.join(tmpdir, "query.ql")
        json_output = os.path.join(tmpdir, "results.json")
        with open(query_file, "w") as f:
            f.write(query)
        try:
            cmd = [
                CODEQL_CLI,
                "query", "run",
                "--database", CODEQL_DB_PATH,
                "--output", json_output,
                query_file
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            decode_cmd = [
                CODEQL_CLI,
                "bqrs", "decode",
                "--format", "json",
                "--output", json_output,
                json_output
            ]
            subprocess.run(decode_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            with open(json_output, "r") as f:
                data = json.load(f)
            for row in data.get("tuples", []):
                entry = {}
                for idx, col in enumerate(data.get("columns", [])):
                    entry[col["name"]] = row[idx]
                results.append(entry)
        except subprocess.CalledProcessError as e:
            print(f"CodeQL execution error: {e.stderr.decode('utf-8', errors='ignore')}")
        except Exception as e:
            print(f"Unexpected error while querying CodeQL: {e}")
    return results
