# Python Memory MCP Agent POC

- Ollama local chat model configured outside the agent code.
- Memory MCP server configured outside the agent code.
- Minimal Python code that only declares the agent and opens a chat session.
- `fast-agent.yaml` defines the MCP server, Ollama endpoint, and memory file path.
- Memory is persisted locally as a knowledge graph file in `data/memory.jsonl`.

## What Memory Stores

Memory MCP stores a local knowledge graph:

- `entities`: durable things such as a user, project, framework, decision, or POC.
- `relations`: directed links between entities.
- `observations`: atomic facts attached to one entity.

Example:

```json
{
  "name": "User",
  "entityType": "person",
  "observations": [
    "Prefers documentation and test prompts in English",
    "Does not want APIs that require adding a credit card"
  ]
}
```

## Files

- `fast-agent.yaml`: FastAgent configuration for Ollama and Memory MCP.
- `agent.py`: minimal FastAgent declaration and chat launcher.
- `pyproject.toml`: isolated Python dependency metadata for this POC.
- `package.json`: pinned Node MCP server dependency.
- `data/memory.jsonl`: local generated memory file, ignored by git.

## Setup

From this folder:

```bash
/opt/homebrew/bin/python3.14 -m venv .venv
. .venv/bin/activate
pip install -U pip
pip install -e .
npm install
ollama pull qwen3.5:latest
```

Use this POC virtual environment, not the repository root `.venv`. The root
environment uses Python 3.12, while `fast-agent-mcp` requires Python `>=3.13.5`.

IDE interpreter:

```text
/Users/politrons/development/Dive-into-Python/com/politrons/ai/mcp_memory_agent/.venv/bin/python
```

By default, `fast-agent.yaml` writes memory to:

```text
data/memory.jsonl
```

You can override it:

```bash
export MCP_MEMORY_FILE_PATH="$(pwd)/data/memory.jsonl"
```

## Run

Interactive chat:

```bash
python agent.py
```

Absolute command:

```bash
/Users/politrons/development/Dive-into-Python/com/politrons/ai/mcp_memory_agent/.venv/bin/python /Users/politrons/development/Dive-into-Python/com/politrons/ai/mcp_memory_agent/agent.py
```

`agent.py` loads the `fast-agent.yaml` file from this folder explicitly, so the
absolute command also works when the IDE working directory is the repository
root.

One-shot prompt:

```bash
python agent.py --message "Remember that for MCP POCs I prefer FastAgent, YAML configuration, minimal Python code, and English documentation."
```

## Practical POC Flows

### Flow 1: User Preference

First call:

```bash
python agent.py --message "Remember that I prefer all documentation and test prompts in English."
```

Expected behavior:

- The agent calls Memory MCP.
- It creates or updates a user entity.
- It stores the preference as an observation.

Second call:

```bash
python agent.py --message "Create a short test prompt for a new MCP browser agent."
```

Expected behavior:

- The agent reads Memory MCP first.
- It finds the English-language preference.
- It answers with the prompt in English.

### Flow 2: Project Constraint

First call:

```bash
python agent.py --message "Remember that we discarded Google Maps MCP because it requires enabling billing or adding a card."
```

Expected behavior:

- The agent stores `Google_Maps_MCP` as an entity.
- It stores the rejection reason as an observation.
- It can relate the decision to the MCP POC project.

Second call:

```bash
python agent.py --message "Suggest the next MCP POC we should build."
```

Expected behavior:

- The agent reads Memory MCP.
- It avoids proposing Google Maps MCP.
- It suggests an MCP that does not require paid credentials, such as Memory, Filesystem, Git, Fetch, or SQLite.

### Flow 3: Implementation Style

First call:

```bash
python agent.py --message "Remember that for these FastAgent POCs I do not want custom business logic if framework configuration can do the job."
```

Expected behavior:

- The agent stores the implementation preference.

Second call:

```bash
python agent.py --message "How should we design the next MCP proof of concept?"
```

Expected behavior:

- The agent uses the stored preference.
- It proposes a config-first FastAgent design with minimal Python code.

## Inspect Memory

The generated file is local:

```bash
cat data/memory.jsonl
```

The file is intentionally ignored by git because it can contain personal or project-specific memory.

## Notes

Memory MCP handles the JSONL persistence. This POC does not implement custom
read/write logic in Python. The agent only uses the MCP tools exposed by the
Memory server.
