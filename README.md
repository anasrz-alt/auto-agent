# Autogent: From Task Descriptions to LLM Agents

## Table of Contents

- [Introduction & Motivation](#introduction--motivation)
- [Overview](#overview)
- [Agent Generation Workflow](#agent-generation-workflow)
- [Key Challenges Addressed](#key-challenges-addressed)
- [Setup](#setup)
  - [Create the Environment and Install Dependencies](#step-1-create-the-environment-and-install-dependencies)
  - [Configure API Keys](#step-2-configure-api-keys)
  - [Run the Application](#step-3-run-the-application)
- [Contributions](#contributions)

Recent work has explored the use of Large Language Models (LLMs) for software engineering and, more recently, for the automatic construction of agents. However, methods based on manual prompting, zero-shot generation, or one-shot examples often fail to produce functional agents. Common failure modes include:

- Mismatched framework or model versions  
- Incomplete understanding of task requirements  
- Incorrect or non-executable logic  
- Errors in tool definition and tool calling  
- Missing or poorly implemented memory components  

These issues highlight the need for a more reliable approach to automated agent development.

## Overview

The **<NAME> Framework** is an end-to-end system for generating dependable LLM-based agents. It operates through the following steps:

1. **Task Analysis** – Understands the task description and identifies required external tools.  
2. **Tool Retrieval or Synthesis** – Fetches tools from public repositories or builds them when necessary, followed by user confirmation.  
3. **Memory Recommendation** – Uses a rule-based representation learning module to select a suitable memory architecture.  
4. **Model Selection** – Consults recent performance benchmarks to recommend an LLM that aligns with the task and avoids version inconsistencies.  
5. **Template-Based Generation** – Instantiates the correct agent template and generates the agent code.  
6. **Integrated Testing** – Each agent includes basic tests to verify initial correctness before deployment.

## Key Challenges Addressed

- Ensuring consistent and correct integration of tools  
- Aligning generated agent logic with executable behavior  
- Recommending memory and model configurations that match task requirements

## Setup

### Step 1: Create the Environment and Install Dependencies

Create a Conda environment and install the required packages:

```
conda create --name <env_name> python=3.x
conda env create -f environment.yml
```
### Step 2: Configure API Keys

Create a `.env` file in the project root directory and add the required API keys. For example:
```
OPENAI_API_KEY=your_api_key_here
```
### Step 3: Run the Application

Execute the following command to run the project:
```
python autoagent.py
```


## Contributions

- A systematic analysis of failure modes in current LLM-based agent generation  
- The design of the **<NAME> Framework**, a full pipeline for reliable agent creation  
- Automated modules for tool discovery, memory selection, and benchmark-guided model choice  
- Template-driven code generation with built-in initial validation tests  
