# AI MCP Proofs of Concept

This folder contains local AI/MCP proof-of-concept projects built with Python,
FastAgent, Ollama, and MCP servers.

The common goal is to mirror the Spring AI style used in the Java project:

- Keep Python code minimal.
- Configure the LLM provider and MCP servers in YAML.
- Use a local Ollama model through the OpenAI-compatible endpoint.
- Run MCP servers through stdio.
- Let FastAgent own the CLI, interactive chat, one-shot messages, and optional server modes.

## Common Stack

- Python: `>=3.13.5`
- Framework: `fast-agent-mcp`
- Local LLM runtime: Ollama
- Default model used in these POCs: `qwen3.5:latest`
- MCP transport: `stdio`
- Node MCP dependencies: installed per POC through `package.json`

The repository root virtual environment uses Python `3.12`, so each POC has its
own virtual environment because `fast-agent-mcp` requires Python `>=3.13.5`.

## Modules

| Folder | MCP Server | Purpose | Persistence | Status |
| --- | --- | --- | --- | --- |
| `mcp_browser_agent` | Playwright Browser MCP | Browser automation and web navigation | Browser runtime artifacts only | Active POC |
| `mcp_memory_agent` | Memory MCP | Persistent agent memory as a local knowledge graph | `data/memory.jsonl` | Active POC |

## Module Details

### `mcp_browser_agent`

Browser MCP proof of concept using FastAgent and Playwright MCP.

Main files:

- `agent.py`: declares the FastAgent agent and binds it to the `browser` MCP server.
- `fast-agent.yaml`: configures Ollama and the Playwright MCP server.
- `package.json`: pins the local Node dependency `@playwright/mcp`.
- `pyproject.toml`: declares the Python dependency on `fast-agent-mcp`.
- `README.md`: module-specific setup, run commands, and tool-calling notes.

What it demonstrates:

- A local Ollama-backed FastAgent agent can receive Browser MCP tools from YAML configuration.
- The agent can navigate pages, inspect page state, and return browser-derived answers.
- Tool usage can be inspected through FastAgent's console output and usage summary.

Important note:

- Local Ollama models may not always respect OpenAI tool-calling controls such as
  `tool_choice`. When the output prints JSON like `{"name": "browser__..."}` and
  the usage summary says `Tools 0`, no MCP tool was actually executed.

### `mcp_memory_agent`

Memory MCP proof of concept using FastAgent and the official Memory MCP server.

Main files:

- `agent.py`: declares the FastAgent agent and binds it to the `memory` MCP server.
- `fast-agent.yaml`: configures Ollama, Memory MCP, and the memory file path.
- `package.json`: pins the local Node dependency `@modelcontextprotocol/server-memory`.
- `pyproject.toml`: declares the Python dependency on `fast-agent-mcp`.
- `data/.gitkeep`: keeps the memory data folder in the repository.
- `README.md`: module-specific setup and practical two-call memory flows.

What it demonstrates:

- Memory MCP stores durable information as a local knowledge graph.
- The graph contains entities, relations, and observations.
- The memory file is generated at `data/memory.jsonl` and ignored by git.
- A first call can store a user preference or project decision.
- A later call can read the persisted memory and adapt the answer.

Example memory flow:

```bash
python agent.py --message "Remember that I prefer all documentation and test prompts in English."
python agent.py --message "Create a short test prompt for a new MCP browser agent."
```

Expected result:

- The first call writes a durable observation through Memory MCP.
- The second call reads the graph with Memory MCP and answers using the stored preference.

## Runtime Artifacts

The following folders and files are generated locally and should not be treated
as source modules:

- `.venv/`: per-POC Python virtual environment.
- `node_modules/`: per-POC Node MCP server dependencies.
- `.fast-agent/`: FastAgent session data.
- `.playwright-mcp/`: Browser MCP snapshots and logs.
- `stream-debug/`: optional OpenAI/Ollama request traces.
- `fastagent.jsonl`: local FastAgent logs.
- `data/memory.jsonl`: generated Memory MCP graph data.

## How To Add Another MCP POC

Use the same structure:

```text
mcp_<name>_agent/
  agent.py
  fast-agent.yaml
  pyproject.toml
  package.json
  README.md
```

Recommended pattern:

- Keep `agent.py` as a small FastAgent declaration.
- Put model, provider, server command, server arguments, and environment variables in `fast-agent.yaml`.
- Pin Node MCP server dependencies in `package.json`.
- Keep secrets out of git.
- Document one-shot prompts that prove the MCP server is actually invoked.
