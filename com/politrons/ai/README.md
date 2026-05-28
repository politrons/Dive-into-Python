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
- MCP runtime dependencies: installed per POC through `package.json` or run as Docker images

The repository root virtual environment uses Python `3.12`, so each POC has its
own virtual environment because `fast-agent-mcp` requires Python `>=3.13.5`.

## Modules

| Folder | MCP Server | Purpose | Persistence | Status |
| --- | --- | --- | --- | --- |
| `mcp_browser_agent` | Playwright Browser MCP | Browser automation and web navigation | Browser runtime artifacts only | Active POC |
| `mcp_filesystem_agent` | Filesystem MCP | Controlled local file listing, reading, writing, and editing | Files under the configured root | Active POC |
| `mcp_git_agent` | Filesystem MCP + Git MCP | Local file-to-Git workflows: read/write files, status, diff, commit, pull, and push | Git working tree and remotes | Active POC |
| `mcp_github_agent` | GitHub MCP | GitHub repository, issue, pull request, branch, commit, and code inspection | None | Active POC |
| `mcp_memory_agent` | Memory MCP | Persistent agent memory as a local knowledge graph | `data/memory.jsonl` | Active POC |
| `mcp_sequential_thinking_agent` | Sequential Thinking MCP | Prompt decomposition, structured planning, assumptions, and risks | None | Active POC |

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

### `mcp_filesystem_agent`

Filesystem MCP proof of concept using FastAgent and the official Filesystem MCP
server.

Main files:

- `agent.py`: declares the FastAgent agent and binds it to the `filesystem` MCP server.
- `fast-agent.yaml`: configures Ollama, Filesystem MCP, and the allowed root folder.
- `package.json`: pins the local Node dependency `@modelcontextprotocol/server-filesystem`.
- `pyproject.toml`: declares the Python dependency on `fast-agent-mcp`.
- `workspace/.gitkeep`: keeps the default sandbox folder in the repository.
- `README.md`: module-specific setup, run commands, and wiring explanation.

What it demonstrates:

- Filesystem MCP can expose controlled local filesystem access to the LLM.
- The default allowed root is `mcp_filesystem_agent/workspace`.
- The allowed root can be changed with `MCP_FILESYSTEM_ROOT` without editing Python code.
- A first call can list files; a later call can create, read, or edit files if explicitly requested.

Example filesystem flow:

```bash
python agent.py --message "Use Filesystem MCP to list the files in the configured root."
```

Expected result:

- The agent calls Filesystem MCP.
- It returns files from the configured root only.

### `mcp_git_agent`

Filesystem MCP plus Git MCP proof of concept using FastAgent,
`@modelcontextprotocol/server-filesystem`, and `@cyanheads/git-mcp-server`.

Main files:

- `agent.py`: declares the FastAgent agent and binds it to the `filesystem` and `git` MCP servers.
- `fast-agent.yaml`: configures Ollama, Filesystem MCP, Git MCP, and the allowed roots.
- `package.json`: pins the local Node dependencies for Filesystem MCP and Git MCP.
- `pyproject.toml`: declares the Python dependency on `fast-agent-mcp`.
- `.env.example`: documents optional Git MCP runtime settings.
- `README.md`: module-specific setup, run commands, local push notes, and wiring explanation.

What it demonstrates:

- Filesystem MCP can read or write local files inside the configured root.
- Git MCP can operate on a local Git working tree, unlike GitHub MCP, which talks
  to GitHub APIs.
- The agent can inspect status, diff, branches, remotes, and logs.
- The agent can stage, commit, pull, and push only when the user explicitly asks
  for those write operations.
- The default allowed root for both MCPs is `/Users/politrons/development/Dive-into-Python`.
- Push authentication comes from the local Git setup: SSH agent, HTTPS credential
  helper, or the remote configuration already present in the repository.

Example Git flow:

```bash
python agent.py --message "Use Git MCP to show git status for /Users/politrons/development/Dive-into-Python. Do not stage, commit, pull, or push anything."
```

Expected result:

- The agent calls Git MCP.
- It returns local repository status without changing the working tree.

### `mcp_github_agent`

GitHub MCP proof of concept using FastAgent and GitHub's official MCP server.

Main files:

- `agent.py`: declares the FastAgent agent and binds it to the `github` MCP server.
- `fast-agent.yaml`: configures Ollama and runs `ghcr.io/github/github-mcp-server` through Docker.
- `pyproject.toml`: declares the Python dependency on `fast-agent-mcp`.
- `README.md`: module-specific setup, credential handling, run commands, and wiring explanation.

What it demonstrates:

- GitHub MCP can expose GitHub repository, issue, pull request, branch, commit, and code tools.
- The GitHub server is configured in read-only mode by default with `GITHUB_READ_ONLY=1`.
- Credentials stay outside git through `GITHUB_PERSONAL_ACCESS_TOKEN`.
- FastAgent starts the Docker command declared in YAML and exposes the MCP tools to the LLM.
- This MCP is for GitHub API operations. Use `mcp_git_agent` for local commits
  and real `git push` from the checked-out repository.

Example GitHub flow:

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN=github_pat_your_token_here
python agent.py --message "Use GitHub MCP to summarize the repository modelcontextprotocol/servers."
```

Expected result:

- The agent calls GitHub MCP.
- It returns repository-derived information from GitHub.

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

### `mcp_sequential_thinking_agent`

Sequential Thinking MCP proof of concept using FastAgent and the official
Sequential Thinking MCP server.

Main files:

- `agent.py`: declares the FastAgent agent and binds it to the `sequential_thinking` MCP server.
- `fast-agent.yaml`: configures Ollama and the Sequential Thinking MCP server command.
- `package.json`: pins the local Node dependency `@modelcontextprotocol/server-sequential-thinking`.
- `pyproject.toml`: declares the Python dependency on `fast-agent-mcp`.
- `README.md`: module-specific setup, run commands, and wiring explanation.

What it demonstrates:

- Sequential Thinking MCP helps the LLM structure a request before answering.
- It can break a prompt into subtasks, risks, assumptions, and next actions.
- It does not execute tasks, read files, browse, or persist memory by itself.
- The concrete MCP implementation is downloaded through `npm install`; FastAgent
  only starts the configured command from YAML.

Example planning flow:

```bash
python agent.py --message "Plan a new FastAgent POC for Git MCP. I want minimal Python code, YAML configuration, setup steps, and validation commands."
```

Expected result:

- The agent calls Sequential Thinking MCP.
- It returns a structured plan with subtasks, risks, assumptions, and validation steps.

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
- `mcp_filesystem_agent/workspace/*`: Files created during Filesystem MCP tests.
- `mcp_git_agent/logs/*`: Git MCP runtime logs.
- `mcp_git_agent/workspace/*`: Optional local clones or files used during Git MCP tests.

## How To Add Another MCP POC

Use the same structure:

```text
mcp_<name>_agent/
  agent.py
  fast-agent.yaml
  pyproject.toml
  package.json  # only when the MCP server is distributed through NPM
  README.md
```

Recommended pattern:

- Keep `agent.py` as a small FastAgent declaration.
- Put model, provider, server command, server arguments, and environment variables in `fast-agent.yaml`.
- Pin Node MCP server dependencies in `package.json` when the MCP server is distributed through NPM.
- Use Docker in `fast-agent.yaml` when the official MCP server is distributed as a container.
- Keep secrets out of git.
- Document one-shot prompts that prove the MCP server is actually invoked.
