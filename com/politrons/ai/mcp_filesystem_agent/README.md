# Python Filesystem MCP Agent POC

- Ollama local chat model configured outside the agent code.
- Filesystem MCP server configured outside the agent code.
- Minimal Python code that only declares the agent and opens a chat session.
- `fast-agent.yaml` defines the MCP server, allowed filesystem root, and Ollama endpoint.
- The agent can inspect and modify files through Filesystem MCP when the user asks.

## What This MCP Does

Filesystem MCP exposes controlled access to local directories. It is useful for:

- listing files and directories
- reading files
- creating files
- editing files
- moving or renaming files
- searching inside the configured root

This POC is intentionally scoped to this folder by default:

```text
/Users/politrons/development/Dive-into-Python/com/politrons/ai/mcp_filesystem_agent/workspace
```

You can change the allowed root without editing Python code:

```bash
export MCP_FILESYSTEM_ROOT=/absolute/path/to/another/folder
```

## Files

- `fast-agent.yaml`: FastAgent configuration for Ollama and Filesystem MCP.
- `agent.py`: minimal FastAgent declaration and chat launcher.
- `pyproject.toml`: isolated Python dependency metadata for this POC.
- `package.json`: pinned Node MCP server dependency.
- `workspace/`: default allowed filesystem root for the POC.

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
/Users/politrons/development/Dive-into-Python/com/politrons/ai/mcp_filesystem_agent/.venv/bin/python
```

## Run

Interactive chat:

```bash
python agent.py
```

Absolute command:

```bash
/Users/politrons/development/Dive-into-Python/com/politrons/ai/mcp_filesystem_agent/.venv/bin/python /Users/politrons/development/Dive-into-Python/com/politrons/ai/mcp_filesystem_agent/agent.py
```

One-shot prompt:

```bash
python agent.py --message "Use Filesystem MCP to list the files in the configured root and summarize what is there."
```

## Practical POC Calls

### Flow 1: List The Workspace

```bash
python agent.py --message "Use Filesystem MCP to list the files in the configured root."
```

Expected behavior:

- The agent calls Filesystem MCP.
- It returns the visible files under the configured root.

### Flow 2: Create A File

```bash
python agent.py --message "Use Filesystem MCP to create notes.md with a short note that says this folder is managed by Filesystem MCP."
```

Expected behavior:

- The agent calls Filesystem MCP.
- It creates `notes.md` inside the configured root.

### Flow 3: Read The File Back

```bash
python agent.py --message "Use Filesystem MCP to read notes.md and summarize it in one sentence."
```

Expected behavior:

- The agent calls Filesystem MCP.
- It reads the persisted file and summarizes the content.

## How FastAgent Wires This MCP

There are three layers:

1. Node dependency

   `package.json` declares the concrete MCP server package:

   ```json
   "@modelcontextprotocol/server-filesystem": "2026.1.14"
   ```

   `npm install` downloads it into `node_modules/` and creates the local binary:

   ```text
   node_modules/.bin/mcp-server-filesystem
   ```

2. FastAgent YAML server configuration

   `fast-agent.yaml` gives that MCP process a logical server name:

   ```yaml
   mcp:
     servers:
       filesystem:
         command: ".../node_modules/.bin/mcp-server-filesystem"
         args:
           - "${MCP_FILESYSTEM_ROOT:/absolute/default/root}"
   ```

   This tells FastAgent how to start the MCP server and which root folder it can access.

3. Agent declaration

   `agent.py` selects that logical server by name:

   ```python
   @fast.agent(
       name="filesystem",
       servers=["filesystem"],
   )
   ```

   The value in `servers=[...]` must match the key under `mcp.servers` in YAML.

## Notes

This POC uses a small local workspace by default so the Filesystem MCP cannot
inspect or modify the whole repository unless you explicitly widen the root.
