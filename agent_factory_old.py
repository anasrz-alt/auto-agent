import os
from jinja2 import Template
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import json
import openai
from query_db import query_codeql_database
import sys

load_dotenv()
ALLOWED_STANDARDIZED_VALUES = {
    "Retrieval_Standardized": ["RAG", "Search", "Symbolic", "(Not Specified)"],
    "Persistence_Standardized": ["LTM", "STM", "(Not Specified)"],
    "Knowledge_Standardized": ["Internal", "External", "Both", "(Not Specified)"],
    "Collaboration_Standardized": ["Single-Agent", "Multi-Agent", "(Not Specified)"],
    "Task_Type_Standardized": ["Data Analysis", "Reasoning", "Planning", "Dialogue", "Coding", "Research", "(Not Specified)"],
    "Data_Modality_Standardized": ["Text", "Tabular", "Image", "Audio", "Multimodal", "(Not Specified)"],
    "Context_Depth_Standardized": ["Short", "Medium", "Long", "(Not Specified)"],
    "Env_Integration_Standardized": ["Local", "Cloud", "Hybrid", "(Not Specified)"],
    "Reasoning_Standardized": ["Analytical", "Logical", "Creative", "(Not Specified)"],
    "Scalability_Standardized": ["Low", "Medium", "High", "(Not Specified)"],
    "Explainability_Standardized": ["Low", "Medium", "High", "(Not Specified)"]
}
class TokenManager:
    def __init__(self):
        self.openai_token_env = "OPENAI_API_KEY"
        self.anthropic_token_env = "ANTHROPIC_API_KEY"
        self.gemini_token_env = "GEMINI_API_KEY"
    def get_token(self, service: str) -> Optional[str]:
        service = service.lower()
        if service == 'openai':
            return os.getenv(self.openai_token_env)
        elif service == 'anthropic':
            return os.getenv(self.anthropic_token_env)
        elif service == 'gemini':
            return os.getenv(self.gemini_token_env)
        return None
    def check_token(self, service: str, raise_error: bool = False) -> bool:
        token = self.get_token(service)
        if not token and raise_error:
            raise ValueError(f"API key for {service} not found in environment variable!")
        return token is not None
TOKEN_MANAGER = TokenManager()
import re
rules = [
    {
        "RID": (-1, 2),
        "weights": {
            "Episodic": 0.1249,
            "Long-Term": -0.0266,
            "Procedural": 0.01,
            "Semantic": 0.1595,
            "Short-Term": 0.1188,
            "Unknown": 0.1510
        },
        "Support": 0.2778,
        "Rule": "((Knowledge_Standardized_Internal & Reasoning_Standardized_High (Logging/Transparency)) | ~(Scalability_Standardized_Research/Reproduction | Reasoning_Standardized_High (Logging/Transparency) | Reasoning_Standardized_Other)) & ((Knowledge_Standardized_Internal & Reasoning_Standardized_High (Logging/Transparency)) | ~(Scalability_Standardized_Reinforcement Learning | Explainability_Standardized_Text/Code | Context_Depth_Standardized_Other | Reasoning_Standardized_High (Logging/Transparency) | Reasoning_Standardized_Other) | ~(Knowledge_Standardized_External | Knowledge_Standardized_Internal | Explainability_Standardized_Other | Data_Modality_Standardized_Logging/Telemetry | Env_Integration_Standardized_Scalable | Reasoning_Standardized_High (Logging/Transparency))) & ~((Scalability_Standardized_Reinforcement Learning | Explainability_Standardized_Text/Code | Context_Depth_Standardized_Other | Reasoning_Standardized_High (Logging/Transparency) | Reasoning_Standardized_Other) & (Task_Type_Standardized_Search | Collaboration_Standardized_Other | Data_Modality_Standardized_Other) & (Task_Type_Standardized_RAG | Task_Type_Standardized_Search | Retrieval_Standardized_LTM | Knowledge_Standardized_External | Persistence_Standardized_Multi-Agent | Scalability_Standardized_Automation | Scalability_Standardized_Research/Reproduction | Explainability_Standardized_Numerical/Categorical | Reasoning_Standardized_Other) & (Retrieval_Standardized_LTM | Persistence_Standardized_Multi-Agent | Context_Depth_Standardized_Other)) & ~((Task_Type_Standardized_Search | Knowledge_Standardized_Internal | Scalability_Standardized_Automation | Scalability_Standardized_Gaming/Simulation | Collaboration_Standardized_Session-Based | Data_Modality_Standardized_Simulation/Game | Reasoning_Standardized_Other) & ~(Collaboration_Standardized_Session-Based) & ~(Reasoning_Standardized_High (Logging/Transparency)))"
    },
    {
        "RID": (-1, 10),
        "weights": {
            "Episodic": 0.0090,
            "Long-Term": -0.0766,
            "Procedural": 0.01,
            "Semantic": 0.0109,
            "Short-Term": 0.0109,
            "Unknown": 0.1358
        },
        "Support": 0.4167,
        "Rule": "~((Scalability_Standardized_Reinforcement Learning | Explainability_Standardized_Text/Code | Context_Depth_Standardized_Other | Reasoning_Standardized_High (Logging/Transparency) | Reasoning_Standardized_Other) & (Task_Type_Standardized_Search | Collaboration_Standardized_Other | Data_Modality_Standardized_Other) & (Task_Type_Standardized_RAG | Task_Type_Standardized_Search | Retrieval_Standardized_LTM | Knowledge_Standardized_External | Persistence_Standardized_Multi-Agent | Scalability_Standardized_Automation | Scalability_Standardized_Research/Reproduction | Explainability_Standardized_Numerical/Categorical | Reasoning_Standardized_Other) & (Retrieval_Standardized_LTM | Persistence_Standardized_Multi-Agent | Context_Depth_Standardized_Other)) & ~((Scalability_Standardized_Reinforcement Learning | Explainability_Standardized_Text/Code | Context_Depth_Standardized_Other | Reasoning_Standardized_High (Logging/Transparency) | Reasoning_Standardized_Other) & (Retrieval_Standardized_LTM | Knowledge_Standardized_Internal))"
    },
    {
        "RID": (-1, 13),
        "weights": {
            "Episodic": 0.1107,
            "Long-Term": -0.0590,
            "Procedural": 0.01,
            "Semantic": 0.1199,
            "Short-Term": 0.0545,
            "Unknown": 0.1001
        },
        "Support": 0.9167,
        "Rule": "((Data_Modality_Standardized_Other) & (Knowledge_Standardized_Internal | Context_Depth_Standardized_Other) & (Explainability_Standardized_Text/Code) & ~(Retrieval_Standardized_STM)) | (~(Task_Type_Standardized_Search | Collaboration_Standardized_Other | Data_Modality_Standardized_Other | Data_Modality_Standardized_Simulation/Game) & ~(Persistence_Standardized_Multi-Agent | Scalability_Standardized_Data Analytics/Planning | Data_Modality_Standardized_Configurable | Data_Modality_Standardized_Other)) | ~((Task_Type_Standardized_RAG) | ~(Data_Modality_Standardized_Other)) | ~((Collaboration_Standardized_Session-Based) | ~(Retrieval_Standardized_LTM | Explainability_Standardized_Text/Code | Data_Modality_Standardized_Other) | ~(Task_Type_Standardized_Search | Knowledge_Standardized_Internal | Scalability_Standardized_Automation | Scalability_Standardized_Gaming/Simulation | Collaboration_Standardized_Session-Based | Data_Modality_Standardized_Simulation/Game | Reasoning_Standardized_Other))"
    },
    {
        "RID": (-1, 1),
        "weights": {
            "Episodic": 0.1198,
            "Long-Term": 0.0576,
            "Procedural": 0.01,
            "Semantic": 0.0908,
            "Short-Term": 0.1092,
            "Unknown": 0.0209
        },
        "Support": 0.8056,
        "Rule": "~((Knowledge_Standardized_External) & ~(Task_Type_Standardized_Search | Knowledge_Standardized_Internal | Persistence_Standardized_Multi-Agent | Scalability_Standardized_Automation | Scalability_Standardized_Data Analytics/Planning) & ~(Task_Type_Standardized_Search | Persistence_Standardized_Multi-Agent | Scalability_Standardized_Automation | Reasoning_Standardized_High (Logging/Transparency) | Reasoning_Standardized_Other))"
    },
    {
        "RID": (-1, 9),
        "weights": {
            "Episodic": 0.0733,
            "Long-Term": 0.0901,
            "Procedural": 0.01,
            "Semantic": 0.0776,
            "Short-Term": 0.0626,
            "Unknown": 0.1115
        },
        "Support": 0.4167,
        "Rule": "((Task_Type_Standardized_RAG) | ~(Data_Modality_Standardized_Other)) & ~(~(Task_Type_Standardized_Search | Knowledge_Standardized_Internal | Explainability_Standardized_Text/Code | Collaboration_Standardized_Other | Context_Depth_Standardized_Other | Reasoning_Standardized_Other) & ~(Task_Type_Standardized_RAG | Task_Type_Standardized_Search | Retrieval_Standardized_LTM | Knowledge_Standardized_External | Persistence_Standardized_Multi-Agent | Scalability_Standardized_Automation | Scalability_Standardized_Research/Reproduction | Explainability_Standardized_Numerical/Categorical | Reasoning_Standardized_Other))"
    },
    {
        "RID": (-1, 7),
        "weights": {
            "Episodic": -0.0046,
            "Long-Term": 0.1010,
            "Procedural": 0.01,
            "Semantic": 0.0025,
            "Short-Term": -0.0073,
            "Unknown": -0.1112
        },
        "Support": 0.7500,
        "Rule": "~(~(Task_Type_Standardized_Search | Retrieval_Standardized_LTM | Persistence_Standardized_Multi-Agent | Env_Integration_Standardized_Scalable | Reasoning_Standardized_Other) & ~(Task_Type_Standardized_Search | Knowledge_Standardized_Internal | Persistence_Standardized_Multi-Agent | Scalability_Standardized_Automation | Explainability_Standardized_Other) & ~(Task_Type_Standardized_RAG | Task_Type_Standardized_Search | Retrieval_Standardized_LTM | Knowledge_Standardized_External | Persistence_Standardized_Multi-Agent | Scalability_Standardized_Automation | Scalability_Standardized_Research/Reproduction | Explainability_Standardized_Numerical/Categorical | Reasoning_Standardized_Other))"
    },
    {
        "RID": (-1, 12),
        "weights": {
            "Episodic": 0.0451,
            "Long-Term": -0.1064,
            "Procedural": 0.01,
            "Semantic": 0.0733,
            "Short-Term": 0.0414,
            "Unknown": 0.0453
        },
        "Support": 0.5833,
        "Rule": "((Knowledge_Standardized_Internal | Context_Depth_Standardized_Other))"
    },
    {
        "RID": (-1, 6),
        "weights": {
            "Episodic": 0.0960,
            "Long-Term": 0.0309,
            "Procedural": 0.01,
            "Semantic": 0.1048,
            "Short-Term": 0.0648,
            "Unknown": 0.0303
        },
        "Support": 0.5833,
        "Rule": "(~(Knowledge_Standardized_Internal | Context_Depth_Standardized_Other) | ~(Knowledge_Standardized_Internal | Explainability_Standardized_Text/Code) | ~(Task_Type_Standardized_Search | Collaboration_Standardized_Other | Data_Modality_Standardized_Other) | ~(Task_Type_Standardized_Search | Knowledge_Standardized_Internal | Persistence_Standardized_Multi-Agent | Scalability_Standardized_Automation | Explainability_Standardized_Other) | ~(Task_Type_Standardized_RAG | Task_Type_Standardized_Search | Retrieval_Standardized_LTM | Knowledge_Standardized_External | Persistence_Standardized_Multi-Agent | Scalability_Standardized_Automation | Scalability_Standardized_Research/Reproduction | Explainability_Standardized_Numerical/Categorical | Reasoning_Standardized_Other)) & ~((Scalability_Standardized_Research/Reproduction | Reasoning_Standardized_High (Logging/Transparency) | Reasoning_Standardized_Other))"
    },
    {
        "RID": (-1, 5),
        "weights": {
            "Episodic": -0.0453,
            "Long-Term": -0.0528,
            "Procedural": 0.01,
            "Semantic": -0.0584,
            "Short-Term": 0.0078,
            "Unknown": -0.1035
        },
        "Support": 0.5556,
        "Rule": "~((Data_Modality_Standardized_Other) & (Knowledge_Standardized_Internal | Context_Depth_Standardized_Other) & (Explainability_Standardized_Text/Code) & ~(Retrieval_Standardized_STM)) & ~((Retrieval_Standardized_LTM | Scalability_Standardized_Data Analytics/Planning | Explainability_Standardized_Other) & (Task_Type_Standardized_Search | Knowledge_Standardized_Internal | Scalability_Standardized_Automation | Scalability_Standardized_Gaming/Simulation | Collaboration_Standardized_Session-Based | Data_Modality_Standardized_Simulation/Game | Reasoning_Standardized_Other))"
    },
    {
        "RID": (-1, 0),
        "weights": {
            "Episodic": -0.0609,
            "Long-Term": 0.0198,
            "Procedural": 0.01,
            "Semantic": -0.0586,
            "Short-Term": -0.0972,
            "Unknown": -0.0613
        },
        "Support": 0.1944,
        "Rule": "(~(Data_Modality_Standardized_Other) | ~(Knowledge_Standardized_Internal | Context_Depth_Standardized_Other) | ~(Task_Type_Standardized_RAG | Task_Type_Standardized_Search | Retrieval_Standardized_LTM | Knowledge_Standardized_External | Persistence_Standardized_Multi-Agent | Scalability_Standardized_Automation | Scalability_Standardized_Research/Reproduction | Explainability_Standardized_Numerical/Categorical | Reasoning_Standardized_Other) | ~(Task_Type_Standardized_Search | Knowledge_Standardized_Internal | Scalability_Standardized_Automation | Scalability_Standardized_Gaming/Simulation | Collaboration_Standardized_Session-Based | Data_Modality_Standardized_Simulation/Game | Reasoning_Standardized_Other)) & ((Task_Type_Standardized_Search | Collaboration_Standardized_Other | Context_Depth_Standardized_Other) | (Retrieval_Standardized_LTM | Collaboration_Standardized_Other) | (Task_Type_Standardized_Search | Knowledge_Standardized_Internal | Persistence_Standardized_Multi-Agent | Scalability_Standardized_Automation | Explainability_Standardized_Other)) & ~((Context_Depth_Standardized_Other) & (Knowledge_Standardized_Internal | Context_Depth_Standardized_Other))"
    },
    {
        "RID": (-1, 3),
        "weights": {
            "Episodic": 0.0654,
            "Long-Term": 0.0228,
            "Procedural": 0.01,
            "Semantic": 0.0913,
            "Short-Term": 0.0397,
            "Unknown": 0.0503
        },
        "Support": 0.5833,
        "Rule": "~((Task_Type_Standardized_Search | Knowledge_Standardized_Internal | Scalability_Standardized_Automation | Scalability_Standardized_Gaming/Simulation | Collaboration_Standardized_Session-Based | Data_Modality_Standardized_Simulation/Game | Reasoning_Standardized_Other) & ~(Collaboration_Standardized_Session-Based) & ~(Reasoning_Standardized_High (Logging/Transparency)))"
    },
    {
        "RID": (-1, 4),
        "weights": {
            "Episodic": -0.0022,
            "Long-Term": -0.0474,
            "Procedural": 0.01,
            "Semantic": 0.0352,
            "Short-Term": 0.0147,
            "Unknown": 0.0791
        },
        "Support": 0.3056,
        "Rule": "((Collaboration_Standardized_Session-Based) | ~(Task_Type_Standardized_Search | Knowledge_Standardized_Internal | Scalability_Standardized_Automation | Scalability_Standardized_Gaming/Simulation | Collaboration_Standardized_Session-Based | Data_Modality_Standardized_Simulation/Game | Reasoning_Standardized_Other)) & (~(Knowledge_Standardized_External) | ~(Scalability_Standardized_Reinforcement Learning | Explainability_Standardized_Text/Code | Context_Depth_Standardized_Other | Reasoning_Standardized_High (Logging/Transparency) | Reasoning_Standardized_Other))"
    },
    {
        "RID": (-1, 11),
        "weights": {
            "Episodic": 0.0344,
            "Long-Term": -0.0635,
            "Procedural": 0.01,
            "Semantic": 0.0264,
            "Short-Term": -0.0195,
            "Unknown": -0.0127
        },
        "Support": 0.4167,
        "Rule": "((Task_Type_Standardized_Search | Knowledge_Standardized_Internal | Persistence_Standardized_Multi-Agent | Scalability_Standardized_Automation | Explainability_Standardized_Other) & (Scalability_Standardized_Research/Reproduction | Reasoning_Standardized_High (Logging/Transparency) | Reasoning_Standardized_Other) & ~(Reasoning_Standardized_High (Logging/Transparency))) | ((Task_Type_Standardized_Search | Persistence_Standardized_Multi-Agent | Explainability_Standardized_Numerical/Categorical | Data_Modality_Standardized_Other) & (Explainability_Standardized_Text/Code | Reasoning_Standardized_Other) & (Task_Type_Standardized_Search | Persistence_Standardized_Multi-Agent | Scalability_Standardized_Automation | Reasoning_Standardized_High (Logging/Transparency) | Reasoning_Standardized_Other)) | ((Knowledge_Standardized_External) & (Data_Modality_Standardized_Other) & (Knowledge_Standardized_Internal | Context_Depth_Standardized_Other))"
    },
    {
        "RID": (-1, 8),
        "weights": {
            "Episodic": -0.0119,
            "Long-Term": -0.0134,
            "Procedural": 0.01,
            "Semantic": -0.0098,
            "Short-Term": 0.0155,
            "Unknown": -0.0046
        },
        "Support": 0.1111,
        "Rule": "~((Scalability_Standardized_Reinforcement Learning | Explainability_Standardized_Text/Code | Context_Depth_Standardized_Other | Reasoning_Standardized_High (Logging/Transparency) | Reasoning_Standardized_Other))"
    }
]
def evaluate_rules(rules, features, allow_closest=False):
    best_rules, max_support = [], -float('inf')
    closest_rule, closest_score = None, 0
    for rule in rules:
        expr = rule["Rule"]
        for feat, val in features.items():
            expr = re.sub(rf'\b{re.escape(feat)}\b', str(bool(val)), expr)
        expr = expr.replace("&", " and ").replace("|", " or ").replace("~", " not ")
        try:
            match = eval(expr)
        except Exception:
            match = False
        if match:
            if rule["Support"] > max_support:
                best_rules = [rule]
                max_support = rule["Support"]
            elif rule["Support"] == max_support:
                best_rules.append(rule)
        elif allow_closest:
            literals = re.findall(r'\b[A-Za-z0-9_/.]+\b', rule["Rule"])
            satisfied = sum(features.get(lit, False) for lit in literals)
            score = satisfied / len(literals) if literals else 0
            if score > closest_score:
                closest_rule, closest_score = rule, score
    if best_rules:
        result = {"match_type": "exact", "max_support": max_support, "rules": best_rules}
    elif allow_closest and closest_rule:
        result = {"match_type": "closest", "max_support": closest_rule["Support"], "rules": [closest_rule]}
    else:
        result = {"match_type": "none", "max_support": None, "rules": []}
    if result["rules"]:
        weights = result["rules"][0]["weights"]
        result["predicted_memory"] = max(weights, key=weights.get)
    else:
        result["predicted_memory"] = None
    return result
import re
def safe_parse_list(text: str, dataset_cols):
    m = re.search(r"\[(.*)\]", text, flags=re.S)
    if not m:
        return [dataset_cols[0]]
    inner = m.group(1)
    parts = re.findall(r"'([^']*)'|\"([^\"]*)\"", inner)
    extracted = [p[0] or p[1] for p in parts]
    if not extracted:
        for col in dataset_cols:
            if col in text:
                return [col]
        return [dataset_cols[0]]
    return extracted
def llm_select_best_model_by_dataset(child_repo_path: str, description=None) -> str:
    import os
    import sys
    import glob
    import subprocess
    import pandas as pd
    script_path = os.path.join(child_repo_path, "src", "main.py")
    subprocess.run([sys.executable, script_path], check=True)
    csv_files = glob.glob(os.path.join(child_repo_path, "data", "leaderboard*.csv"))
    if not csv_files:
        raise FileNotFoundError(" No leaderboard CSV files found in /data/")
    df = pd.read_csv(csv_files[0])
    dataset_cols = [
        c for c in df.columns
        if df[c].dtype in ["float64", "int64"] and c not in ["Artificial Analysis Intelligence Index"]
    ]
    if not dataset_cols:
        raise ValueError("No numeric dataset columns found to evaluate relevance.")
    dataset_prompt = f
    if TOKEN_MANAGER.check_token("openai"):
        import openai
        openai.api_key = TOKEN_MANAGER.get_token("openai")
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": dataset_prompt}],
            temperature=0
        )
        content = response.choices[0].message["content"].strip()
    elif TOKEN_MANAGER.check_token("gemini"):
        from google import genai
        client = genai.Client(api_key=TOKEN_MANAGER.get_token("gemini"))
        result = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=dataset_prompt
        )
        content = result.text.strip()
    elif TOKEN_MANAGER.check_token("anthropic"):
        import anthropic
        client = anthropic.Anthropic(api_key=TOKEN_MANAGER.get_token("anthropic"))
        result = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            messages=[{"role": "user", "content": dataset_prompt}],
            max_tokens=100
        )
        content = result.content[0].text.strip()
    else:
        print(" No LLM key found. Using top dataset column heuristically.")
        content = [dataset_cols[0]]
    try:
       relevant_cols = safe_parse_list(content, dataset_cols)
    except:
        relevant_cols = [dataset_cols[0]]
    best_col = relevant_cols[0]
    df = df.dropna(subset=[best_col])
    top5 = df.sort_values(best_col, ascending=False).head(5)
    model_summary = top5[["Model", best_col]].to_string(index=False)
    prompt = f
    if TOKEN_MANAGER.check_token("openai"):
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        content = response.choices[0].message["content"].strip()
    elif TOKEN_MANAGER.check_token("gemini"):
        result = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        content = result.text.strip()
    elif TOKEN_MANAGER.check_token("anthropic"):
        result = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )
        content = result.content[0].text.strip()
    else:
        return top5.iloc[0]["Model"]
    best_model = content.split("\n")[0].strip()
    return best_model
def llm_select_template(framework: str, description: str, templates: List[str]) -> str:
    base_template = f"{framework.lower()}_agent.py.jinja"
    if base_template in templates:
        return base_template
    return templates[0] if templates else ""
def llm_determine_tools(description: str) -> List[str]:
    if TOKEN_MANAGER.check_token('openai'):
        openai.api_key = TOKEN_MANAGER.get_token('openai')
        model_name = "gpt-4o-mini"
        prompt = f
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        content = response.choices[0].message["content"]
    elif TOKEN_MANAGER.check_token('gemini'):
        client = genai.Client(api_key=TOKEN_MANAGER.get_token('gemini'))
        prompt = f
        result = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        content = result.text
    elif TOKEN_MANAGER.check_token('anthropic'):
        client = anthropic.Anthropic(api_key=TOKEN_MANAGER.get_token('anthropic'))
        prompt = f
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        content = response.content[0].text
    else:
        print(" No LLM API key found. Using mock logic instead.")
        if "data" in description.lower():
            return ["PandasTool", "PlottingTool"]
        elif "web" in description.lower():
            return ["SearchTool", "WebBrowser"]
        elif "file" in description.lower():
            return ["FileIO"]
        else:
            return ["SearchTool"]
    try:
        content_clean = re.sub(r"```.*?\n|```", "", content).strip()
        parsed = json.loads(content_clean)
        tools = parsed.get("tools", [])
        if isinstance(tools, list):
            return [str(t) for t in tools]
        else:
            return []
    except Exception as e:
        print(f" Failed to parse LLM output, falling back. Error: {e}")
        print("Raw content:", content)
        return ["SearchTool"]
def llm_write_codeql_query(required_tools: List[str]) -> str:
    tool_list_str = ", ".join(f"'{t}'" for t in required_tools)
    return f"select tool, code from agents_db where tool_name in ({tool_list_str})"
def llm_generate_feature_values(description: str) -> Dict[str, str]:
    allowed_values = {
        "Retrieval_Standardized": ["RAG", "Search", "Symbolic", "(Not Specified)"],
        "Persistence_Standardized": ["LTM", "STM", "(Not Specified)"],
        "Knowledge_Standardized": ["Internal", "External", "Both", "(Not Specified)"],
        "Collaboration_Standardized": ["Single-Agent", "Multi-Agent", "(Not Specified)"],
        "Task_Type_Standardized": ["Data Analysis", "Reasoning", "Planning", "Dialogue", "Coding", "Research", "(Not Specified)"],
        "Data_Modality_Standardized": ["Text", "Tabular", "Image", "Audio", "Multimodal", "(Not Specified)"],
        "Context_Depth_Standardized": ["Short", "Medium", "Long", "(Not Specified)"],
        "Env_Integration_Standardized": ["Local", "Cloud", "Hybrid", "(Not Specified)"],
        "Reasoning_Standardized": ["Analytical", "Logical", "Creative", "(Not Specified)"],
        "Scalability_Standardized": ["Low", "Medium", "High", "(Not Specified)"],
        "Explainability_Standardized": ["Low", "Medium", "High", "(Not Specified)"]
    }
    prompt = f
    content = ""
    try:
        if TOKEN_MANAGER.check_token('openai'):
            openai.api_key = TOKEN_MANAGER.get_token('openai')
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            content = response.choices[0].message["content"]
        elif TOKEN_MANAGER.check_token('gemini'):
            client = genai.Client(api_key=TOKEN_MANAGER.get_token('gemini'))
            result = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            content = result.text
        elif TOKEN_MANAGER.check_token('anthropic'):
            client = anthropic.Anthropic(api_key=TOKEN_MANAGER.get_token('anthropic'))
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400
            )
            content = response.content[0].text
        else:
            print(" No LLM API key found. Using mock standardization.")
            return {
                "Retrieval_Standardized": "RAG" if "retrieval" in description.lower() else "(Not Specified)",
                "Persistence_Standardized": "LTM" if "long" in description.lower() else "STM",
                "Knowledge_Standardized": "External" if "api" in description.lower() else "Internal",
                "Collaboration_Standardized": "Multi-Agent" if "team" in description.lower() else "Single-Agent",
                "Task_Type_Standardized": "Data Analysis",
                "Data_Modality_Standardized": "Text",
                "Context_Depth_Standardized": "Medium",
                "Env_Integration_Standardized": "Local",
                "Reasoning_Standardized": "Analytical",
                "Scalability_Standardized": "Medium",
                "Explainability_Standardized": "High"
            }
        content_clean = content.strip()
        if content_clean.startswith("```"):
            content_clean = re.sub(r"```[a-zA-Z]*", "", content_clean).replace("```", "").strip()
        parsed = json.loads(content_clean)
        result = {}
        for key, valid_opts in allowed_values.items():
            val = parsed.get(key, "(Not Specified)")
            if val not in valid_opts:
                result[key] = "(Not Specified)"
            else:
                result[key] = val
        return result
    except Exception as e:
        print(f" Error in llm_generate_feature_values: {e}")
        print("Raw content:", content)
        return {k: "(Not Specified)" for k in allowed_values.keys()}
def convert_to_boolean_features(std_features: Dict[str, str]) -> Dict[str, bool]:
    boolean_features = {}
    for key, selected_value in std_features.items():
        for possible_value in ALLOWED_STANDARDIZED_VALUES[key]:
            feature_name = f"{key}_{possible_value}".replace(" ", "_")
            boolean_features[feature_name] = (possible_value == selected_value)
    return boolean_features
def mock_codeql_query(query: str, db_path: str) -> List[Dict[str, Any]]:
    if "FileIO" in query:
        return [
            {
                "name": "FileIO",
                "description": "Reads and writes files on the local system.",
                "func_code": "lambda action, path, content=None: f'File operation {action} on {path}'"
            }
        ]
    return []
def llm_generate_tool_code(tool_name: str, description: str, mode: str = "tool_file") -> Dict[str, Any]:
    func_name = f"{tool_name.lower()}_func"
    base_prompt = f
    content = ""
    if TOKEN_MANAGER.check_token('openai'):
        openai.api_key = TOKEN_MANAGER.get_token('openai')
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You generate production-ready Python tool code."},
                {"role": "user", "content": base_prompt}
            ],
            temperature=0.3
        )
        content = response.choices[0].message["content"]
    elif TOKEN_MANAGER.check_token('gemini'):
        client = genai.Client(api_key=TOKEN_MANAGER.get_token('gemini'))
        result = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=base_prompt
        )
        content = result.text
    elif TOKEN_MANAGER.check_token('anthropic'):
        client = anthropic.Anthropic(api_key=TOKEN_MANAGER.get_token('anthropic'))
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            messages=[{"role": "user", "content": base_prompt}],
            max_tokens=500
        )
        content = response.content[0].text
    else:
        print(" No valid LLM API key found — using mock tool implementation.")
        func_code = (
            f"def {func_name}(query: str) -> str:\n"
            f"    return f'Mock output for {tool_name} with input: {{query}}'"
        )
        return {
            "name": tool_name,
            "description": description,
            "func_code": func_code,
            "func_name": func_name,
            "path": f"agents.generated.tools.{tool_name.lower()}"
        }
    try:
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("python"):
                cleaned = cleaned[len("python"):].strip()
        func_code = cleaned
    except Exception as e:
        print(f" Failed to clean LLM output: {e}")
        func_code = (
            f"def {func_name}(query: str) -> str:\n"
            f"    return f'Generated output for {tool_name} with input: {{query}}'"
        )
    return {
        "name": tool_name,
        "description": description,
        "func_code": func_code,
        "func_name": func_name,
        "path": f"agents.generated.tools.{tool_name.lower()}"
    }
def llm_select_model(framework: str) -> str:
    if framework.lower() == "langchain":
        if TOKEN_MANAGER.check_token('openai'):
            return "openai/gpt-4o"
        elif TOKEN_MANAGER.check_token('gemini'):
            return "google/gemini-2.5-pro"
    return "ollama/llama3"
def mock_run_agent(agent_path: str, user_query: str) -> str:
    if "wrong answer" in user_query.lower():
        return "Agent output: The capital is 'Paris', but the question was about Rome."
    return f"Agent output: I correctly processed your query: {user_query}. Using FileIO tool."
TEMPLATE_DIR = "agents/templates"
GENERATED_DIR = "agents/generated"
CODEQL_DB_PATH = "codeql/agents_db"
TOOL_TEMPLATE_PATH = os.path.join("agents", "tools", "base_tool.py.jinja")
MEMORY: Dict[str, Any] = {"history": []}
AGENT_STRUCTURE: Dict[str, Any] = {}
BASE_TOOL_TEMPLATE_CONTENT = 
def render_template(template_path: str, context: dict) -> str:
    with open(template_path, "r") as f:
        template = Template(f.read())
    return template.render(**context)
def render_tool_template(tool_name: str, description: str, func_code: str) -> str:
    func_name = f"{tool_name.lower()}_func"
    context = {
        "tool_name": tool_name,
        "tool_description": description,
        "tool_func_definition": func_code,
        "tool_func_name": func_name
    }
    return render_template(TOOL_TEMPLATE_PATH, context)
def save_tool(tool_code: str, tool_name: str) -> str:
    tool_dir = os.path.join(GENERATED_DIR, "tools")
    os.makedirs(tool_dir, exist_ok=True)
    path = os.path.join(tool_dir, f"{tool_name.lower()}.py")
    with open(path, "w") as f:
        f.write(tool_code)
    print(f"Tool saved: {path}")
    return path
def save_agent(code: str, framework: str, agent_name: str) -> str:
    os.makedirs(GENERATED_DIR, exist_ok=True)
    path = os.path.join(GENERATED_DIR, f"{framework}_{agent_name}.py")
    with open(path, "w") as f:
        f.write(code)
    return path
def get_available_templates(framework: str) -> List[str]:
    return [
        "autogen_agent.py.jinja", "autonomous_gpt_agent.py.jinja", "crewai_agent.py.jinja",
        "dify_agent.py.jinja", "langchain_agent.py.jinja", "llamaindex_agent.py.jinja",
        "metagpt_agent.py.jinja", "smolagents_agent.py.jinja"
    ]
def step_1_select_framework(available_frameworks: List[str]) -> str:
    return "langchain"
def step_2_select_template_path(framework: str, description: str) -> str:
    templates = get_available_templates(framework)
    framework_templates = [t for t in templates if t.startswith(f"{framework.lower()}_")]
    selected_template_name = llm_select_template(framework, description, framework_templates)
    template_path = os.path.join(TEMPLATE_DIR, selected_template_name)
    if not os.path.exists(template_path):
        with open(template_path, "w") as f:
            f.write(BASE_TOOL_TEMPLATE_CONTENT)
        print(f"Warning: Template not found, created dummy template at {template_path}")
    return template_path
def step_3_determine_tools(description: str) -> List[str]:
    return llm_determine_tools(description)
def llm_generate_feature_values(description: str) -> Dict[str, str]:
    allowed_values = {
        "Retrieval_Standardized": ["RAG", "Search", "Symbolic", "(Not Specified)"],
        "Persistence_Standardized": ["LTM", "STM", "(Not Specified)"],
        "Knowledge_Standardized": ["Internal", "External", "Both", "(Not Specified)"],
        "Collaboration_Standardized": ["Single-Agent", "Multi-Agent", "(Not Specified)"],
        "Task_Type_Standardized": ["Data Analysis", "Reasoning", "Planning", "Dialogue", "Coding", "Research", "(Not Specified)"],
        "Data_Modality_Standardized": ["Text", "Tabular", "Image", "Audio", "Multimodal", "(Not Specified)"],
        "Context_Depth_Standardized": ["Short", "Medium", "Long", "(Not Specified)"],
        "Env_Integration_Standardized": ["Local", "Cloud", "Hybrid", "(Not Specified)"],
        "Reasoning_Standardized": ["Analytical", "Logical", "Creative", "(Not Specified)"],
        "Scalability_Standardized": ["Low", "Medium", "High", "(Not Specified)"],
        "Explainability_Standardized": ["Low", "Medium", "High", "(Not Specified)"]
    }
    prompt = f
    content = ""
    try:
        if TOKEN_MANAGER.check_token('openai'):
            openai.api_key = TOKEN_MANAGER.get_token('openai')
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            content = response.choices[0].message["content"]
        elif TOKEN_MANAGER.check_token('gemini'):
            client = genai.Client(api_key=TOKEN_MANAGER.get_token('gemini'))
            result = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            content = result.text
        elif TOKEN_MANAGER.check_token('anthropic'):
            client = anthropic.Anthropic(api_key=TOKEN_MANAGER.get_token('anthropic'))
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400
            )
            content = response.content[0].text
        else:
            print(" No LLM API key found. Using mock standardization.")
            return {
                "Retrieval_Standardized": "RAG" if "retrieval" in description.lower() else "(Not Specified)",
                "Persistence_Standardized": "LTM" if "long" in description.lower() else "STM",
                "Knowledge_Standardized": "External" if "api" in description.lower() else "Internal",
                "Collaboration_Standardized": "Multi-Agent" if "team" in description.lower() else "Single-Agent",
                "Task_Type_Standardized": "Data Analysis",
                "Data_Modality_Standardized": "Text",
                "Context_Depth_Standardized": "Medium",
                "Env_Integration_Standardized": "Local",
                "Reasoning_Standardized": "Analytical",
                "Scalability_Standardized": "Medium",
                "Explainability_Standardized": "High"
            }
        content_clean = content.strip()
        if content_clean.startswith("```"):
            content_clean = re.sub(r"```[a-zA-Z]*", "", content_clean).replace("```", "").strip()
        parsed = json.loads(content_clean)
        result = {}
        for key, valid_opts in allowed_values.items():
            val = parsed.get(key, "(Not Specified)")
            if val not in valid_opts:
                result[key] = "(Not Specified)"
            else:
                result[key] = val
        return result
    except Exception as e:
        print(f" Error in llm_generate_feature_values: {e}")
        print("Raw content:", content)
        return {k: "(Not Specified)" for k in allowed_values.keys()}
def step_4_and_5_find_or_create_tools(required_tools: List[str], agent_structure: Dict[str, Any]) -> List[Dict[str, str]]:
    final_tools: List[Dict[str, str]] = []
    os.makedirs(os.path.dirname(TOOL_TEMPLATE_PATH), exist_ok=True)
    if not os.path.exists(TOOL_TEMPLATE_PATH):
        with open(TOOL_TEMPLATE_PATH, "w") as f:
            f.write(BASE_TOOL_TEMPLATE_CONTENT)
    tool_descriptions = {t['name']: t['description'] for t in agent_structure.get('tools', [])}
    for tool_name in required_tools:
        description = tool_descriptions.get(tool_name, f"Tool for {tool_name} functionality.")
        print(f"\nTool: '{tool_name}'")
        print(f"Proposed description: {description}")
        user_input = input("Press Enter to accept, or type a new description: ").strip()
        if user_input:
            description = user_input
        print(f"Using description: {description}")
        codeql_query = f
        codeql_results = []
        try:
            codeql_results = query_codeql_database(codeql_query)
        except Exception as e:
            print(f" CodeQL query failed for {tool_name}: {e}")
        if codeql_results:
            best_match = codeql_results[0]
            func_name = best_match.get("f.getName()", f"{tool_name.lower()}_func")
            func_code = best_match.get("source", f"def {func_name}(query: str):\n    pass")
            print(f" Found existing tool for '{tool_name}' in CodeQL DB.")
        else:
            print(f" No CodeQL match found for '{tool_name}', generating new tool with LLM...")
            new_tool_data = llm_generate_tool_code(tool_name, description)
            func_name = new_tool_data["func_name"]
            func_code = new_tool_data["func_code"]
        tool_code = render_tool_template(
            tool_name=tool_name,
            description=description,
            func_code=func_code
        )
        tool_file_path = save_tool(tool_code, tool_name)
        final_tools.append({
            "name": tool_name,
            "description": description,
            "func_name": func_name,
            "import_path": f"agents.generated.tools.{tool_name.lower()}",
            "file_path": tool_file_path
        })
    return final_tools
def llm_generate_agent_structure(agent_name: str, description: str, framework: str, required_tools: List[str]) -> Dict[str, Any]:
    model_name = llm_select_model(framework)
    json_schema = {
    "type": "object",
    "title": "AI Agent Schema",
    "description": "A universal JSON schema describing all key components of an AI agent.",
    "properties": {
        "agent_name": {
            "type": "string",
            "description": "The unique name of the agent."
        },
        "description": {
            "type": "string",
            "description": "A detailed description of the agent’s purpose, goals, and behavior."
        },
        "framework_target": {
            "type": "string",
            "description": "The agent’s target framework or runtime (e.g., langchain, autogen, crewai, custom)."
        },
        "architecture": {
            "type": "string",
            "description": "The reasoning and control pattern (e.g., ReAct, Plan-and-Execute, Chain-of-Thought, Reflexive, Multi-Agent)."
        },
        "core_model": {
            "type": "object",
            "description": "The main reasoning engine or model driving the agent.",
            "properties": {
                "type": {"type": "string", "enum": ["LLM", "Hybrid", "Symbolic"], "description": "The type of model."},
                "name": {"type": "string", "description": "The model identifier (e.g., gpt-5, claude-3.5, mistral-large)."},
                "role": {"type": "string", "description": "The model’s role (e.g., Orchestrator, Planner, Reasoner, Executor)."}
            },
            "required": ["type", "name", "role"]
        },
        "perception": {
            "type": "object",
            "description": "The perception layer — how the agent receives and interprets input from the environment.",
            "properties": {
                "inputs": {
                    "type": "array",
                    "description": "List of input modalities or sources (e.g., text, image, audio, environment sensors).",
                    "items": {"type": "string"}
                },
                "preprocessing": {
                    "type": "array",
                    "description": "List of preprocessing or recognition tools (e.g., OCR, speech-to-text, vision model).",
                    "items": {"type": "string"}
                }
            }
        },
        "reasoning": {
            "type": "object",
            "description": "The reasoning and decision-making subsystem.",
            "properties": {
                "strategy": {"type": "string", "description": "Reasoning method (e.g., symbolic, neural, hybrid, CoT, ToT)."},
                "knowledge_base": {"type": "string", "description": "Type of stored knowledge (e.g., RAG, ontology, embedding store)."},
                "planner": {"type": "string", "description": "Planning module (e.g., task decomposition, goal graph)."}
            }
        },
        "action": {
            "type": "object",
            "description": "The action layer defining what the agent can do in its environment.",
            "properties": {
                "execution_mode": {"type": "string", "description": "How the agent executes (e.g., synchronous, asynchronous, batched)."},
                "output_channels": {
                    "type": "array",
                    "description": "Where the agent sends actions (e.g., console, API, web, robot control).",
                    "items": {"type": "string"}
                }
            }
        },
        "communication": {
            "type": "object",
            "description": "Defines how the agent interacts with users or other agents.",
            "properties": {
                "input_format": {"type": "string", "description": "Input communication type (e.g., chat, voice, API message)."},
                "output_format": {"type": "string", "description": "Output type (e.g., text, structured JSON, command)."},
                "multi_agent_protocol": {"type": "string", "description": "Defines multi-agent communication style (e.g., message passing, shared memory, broadcast)."}
            }
        },
        "tools": {
            "type": "array",
            "description": "All external tools or APIs the agent can call.",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "The tool name."},
                    "description": {"type": "string", "description": "Description of the tool’s function and usage context."},
                    "type": {"type": "string", "description": "Category of tool (e.g., Search, Calculator, FileIO, Vision, Audio)."}
                },
                "required": ["name", "description", "type"]
            }
        },
        "memory": {
            "type": "object",
            "description": "Defines the agent’s memory system and scope.",
            "properties": {
                "type": {"type": "string", "description": "Memory type (e.g., Conversational, VectorStore, Summary, Episodic)."},
                "scope": {"type": "string", "description": "Scope of memory (e.g., ShortTerm, LongTerm, Global)."},
                "storage": {"type": "string", "description": "Storage backend or mechanism (e.g., Redis, ChromaDB, InMemory)."}
            },
            "required": ["type"]
        },
        "learning": {
            "type": "object",
            "description": "Specifies how the agent learns or adapts over time.",
            "properties": {
                "method": {"type": "string", "description": "Learning type (e.g., reinforcement, self-improvement, feedback-driven)."},
                "data_sources": {
                    "type": "array",
                    "description": "Sources of learning data (e.g., user feedback, logs, environment states).",
                    "items": {"type": "string"}
                }
            }
        },
        "control_orchestration": {
            "type": "object",
            "description": "Defines how the agent manages its internal flow and tool orchestration.",
            "properties": {
                "controller_type": {"type": "string", "description": "Type of control mechanism (e.g., step-based loop, state machine, event-driven)."},
                "coordination": {"type": "string", "description": "How submodules are coordinated (e.g., sequential, hierarchical, concurrent)."}
            }
        },
        "environment": {
            "type": "object",
            "description": "Describes the environment or domain the agent operates in.",
            "properties": {
                "type": {"type": "string", "description": "Type of environment (e.g., digital, physical, simulation, web)."},
                "state_representation": {"type": "string", "description": "How the environment state is represented (e.g., JSON, vector, symbolic)."}
            }
        }
    },
    "required": [
        "agent_name",
        "description",
        "framework_target",
        "architecture",
        "core_model",
        "tools",
        "memory"
    ]
}
    tools_list_str = ", ".join(required_tools)
    prompt = f
    content = ""
    if TOKEN_MANAGER.check_token('openai'):
        openai.api_key = TOKEN_MANAGER.get_token('openai')
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            response_format={"type": "json_object"} 
        )
        content = response.choices[0].message["content"]
    elif TOKEN_MANAGER.check_token('gemini'):
        client = genai.Client(api_key=TOKEN_MANAGER.get_token('gemini'))
        result = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        content = result.text
    elif TOKEN_MANAGER.check_token('anthropic'):
        client = anthropic.Anthropic(api_key=TOKEN_MANAGER.get_token('anthropic'))
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500
        )
        content = response.content[0].text
    else:
        print(" No LLM API key found. Using mock Agent-IR logic.")
        return {
            "agent_name": agent_name,
            "description": description,
            "framework_target": framework,
            "architecture": "ReAct",
            "core_model": {"type": "LLM", "name": "ollama/llama3", "role": "Orchestrator"},
            "tools": [{"name": t, "description": f"Tool for {t}.", "type": "Tool"} for t in required_tools],
            "memory": {"type": "ConversationalMemory", "scope": "Session"}
        }
    try:
        if content.strip().startswith("```"):
            content = content.split("```json")[1].split("```")[0].strip()
        parsed_structure = json.loads(content)
        structure_dir = os.path.join(GENERATED_DIR, "structures")
        os.makedirs(structure_dir, exist_ok=True)
        file_path = os.path.join(structure_dir, f"{agent_name.lower()}_structure.json")
        with open(file_path, "w") as f:
            json.dump(parsed_structure, f, indent=4)
        print(f" LLM-Generated Agent structure (Agent-IR) saved to: {file_path}")
        global AGENT_STRUCTURE
        AGENT_STRUCTURE = parsed_structure
        return parsed_structure
    except Exception as e:
        print(f" Failed to parse LLM Agent-IR output, falling back to mock structure. Error: {e}")
        return llm_generate_agent_structure(agent_name, description, framework, required_tools) 
def step_6_create_agent(framework: str, template_path: str, tools: List[Dict[str, str]], agent_name: str, description: str, memory_type: str='') -> str:
    model_name = llm_select_model(framework)
    if "openai" in model_name.lower() and not TOKEN_MANAGER.check_token('openai'):
        print(f" WARNING: Model '{model_name}' requires OPENAI_API_KEY, but it's not set. Proceeding with dummy model name.")
    with open(template_path, "r") as f:
        template_content = f.read()
    memory_context = f"Previous agent issues or lessons: {MEMORY['history']}"
    tool_imports = "\n".join(
        [f"from {t['import_path']} import {t['func_name']}" for t in tools]
    )
    tool_names = [t["name"] for t in tools]
    llm_prompt = f
    if TOKEN_MANAGER.check_token('openai'):
        openai.api_key = TOKEN_MANAGER.get_token('openai')
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You generate high-quality production-ready Python agent code."},
                {"role": "user", "content": llm_prompt}
            ],
            temperature=0.4
        )
        content = response.choices[0].message["content"]
    elif TOKEN_MANAGER.check_token('gemini'):
        client = genai.Client(api_key=TOKEN_MANAGER.get_token('gemini'))
        result = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=llm_prompt
        )
        content = result.text
    elif TOKEN_MANAGER.check_token('anthropic'):
        client = anthropic.Anthropic(api_key=TOKEN_MANAGER.get_token('anthropic'))
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            messages=[{"role": "user", "content": llm_prompt}],
            max_tokens=2000
        )
        content = response.content[0].text
    else:
        print(" No valid LLM API key found — using static fallback agent.")
        code = render_template(template_path, {
            "agent_name": agent_name,
            "tools": tools,
            "model_name": model_name,
            "agent_type": "react",
            "description": description,
            "memory_context": memory_context
        })
        return save_agent(code, framework, agent_name)
    cleaned_code = content.strip()
    if cleaned_code.startswith("```"):
        cleaned_code = cleaned_code.split("```")[1]
        if cleaned_code.startswith("python"):
            cleaned_code = cleaned_code[len("python"):].strip()
    agent_path = save_agent(cleaned_code, framework, agent_name)
    print(f" Agent created with {framework} framework at: {agent_path}")
    return agent_path
def step_7_and_8_test_and_refine(agent_path: str, user_query: str, framework: str, agent_name: str, description: str, tools: List[Dict[str, str]]) -> str:
    agent_output = mock_run_agent(agent_path, user_query)
    if "wrong answer" in agent_output.lower() or "mistake" in agent_output.lower():
        mistake_details = {
            "query": user_query,
            "output": agent_output,
            "mistake": "Example: Agent reasoning failed due to tool misuse. (LLM would analyze this mistake)",
            "timestamp": os.path.getmtime(agent_path)
        }
        MEMORY["history"].append(mistake_details)
        return step_6_create_agent(framework, step_2_select_template_path(framework, description), tools, agent_name, description)
    else:
        return agent_path
import subprocess
import traceback
def run_agent_with_feedback(agent_path: str, task_description: str, user_query: str) -> None:
    try:
        result = subprocess.run(
            [sys.executable, agent_path, task_description, user_query],
            capture_output=True,
            text=True,
            check=True
        )
        print(" Agent executed successfully:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        error_message = e.stderr or e.stdout or str(e)
        print(" Agent execution failed. Captured error:\n", error_message)
        prompt = f
        if TOKEN_MANAGER.check_token("openai"):
            import openai
            openai.api_key = TOKEN_MANAGER.get_token("openai")
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            advice = response.choices[0].message["content"].strip()
        elif TOKEN_MANAGER.check_token("gemini"):
            from google import genai
            client = genai.Client(api_key=TOKEN_MANAGER.get_token("gemini"))
            result = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            advice = result.text.strip()
        elif TOKEN_MANAGER.check_token("anthropic"):
            import anthropic
            client = anthropic.Anthropic(api_key=TOKEN_MANAGER.get_token("anthropic"))
            result = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            advice = result.content[0].text.strip()
        else:
            advice = " No LLM API key found. Cannot provide feedback."
        print("\n--- LLM Feedback / Debugging Advice ---\n")
        print(advice)
def autoagent_orchestrator(task_description: str, agent_name: str, user_query: str) -> str:
    os.makedirs(TEMPLATE_DIR, exist_ok=True)
    for t_name in get_available_templates(""):
        if not os.path.exists(os.path.join(TEMPLATE_DIR, t_name)):
            with open(os.path.join(TEMPLATE_DIR, t_name), "w") as f:
                f.write(BASE_TOOL_TEMPLATE_CONTENT)
    framework = step_1_select_framework(get_available_templates(""))
    template_path = step_2_select_template_path(framework, task_description)
    raw_features  = llm_generate_feature_values(task_description)
    features = convert_to_boolean_features(raw_features)
    required_tools = step_3_determine_tools(task_description)
    agent_structure = llm_generate_agent_structure(agent_name, task_description, framework, required_tools)
    best_model = llm_select_best_model_by_dataset("./artificial-analysis-leaderboards-scraper", description=task_description)
    print("Best Model:", best_model)
    result = evaluate_rules(rules, features, allow_closest=True)
    print("Match Type:", result["match_type"])
    print("Max Support:", result["max_support"])
    print("Best Rule IDs:", [r["RID"] for r in result["rules"]])
    print("Predicted Memory Type:", result["predicted_memory"])
    tools = step_4_and_5_find_or_create_tools(required_tools, agent_structure)
    agent_path = step_6_create_agent(framework, template_path, tools, agent_name, task_description, memory_type='Episodic')
    final_agent_path = step_7_and_8_test_and_refine(agent_path, user_query, framework, agent_name, task_description, tools)
    return final_agent_path
if __name__ == "__main__":
    if TOKEN_MANAGER.check_token('openai'):
        print(" OpenAI API Key found. Real LLM calls can be implemented.")
    else:
        print(" OpenAI API Key not found. Using mock/fallback model selection.")
    if TOKEN_MANAGER.check_token('gemini'):
        print(" Gemini API Key found.")
    print("\n--- Autoagent Framework Startup ---")
    task_description = input("Enter task description (e.g., data analysis): ")
    agent_name = input("Enter agent name (e.g., AnalystBot): ")
    test_query_1 = input("Enter test query (e.g., process sales data or give a wrong answer): ")
    final_path_1 = autoagent_orchestrator(task_description, agent_name, test_query_1)
    print(f"\nFinal Agent Path after potential refinement: {final_path_1}")
    print(f"Current Memory History ({len(MEMORY['history'])} entries): {MEMORY['history'][0]['mistake'] if MEMORY['history'] else 'None'}")
