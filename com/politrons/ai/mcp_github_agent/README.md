# Python GitHub MCP Agent POC

- Ollama local chat model configured outside the agent code.
- GitHub MCP server configured outside the agent code.
- Minimal Python code that only declares the agent and opens a chat session.
- `fast-agent.yaml` defines the MCP server, GitHub token environment variable, and Ollama endpoint.
- The agent can inspect GitHub repositories, issues, pull requests, branches, commits, and related data.
- This POC is not the right tool for local `git push` from your checked-out repository.
  Use `../mcp_git_agent` for local Git status, commits, pulls, and pushes.

## What This MCP Does

GitHub MCP exposes GitHub API operations as MCP tools. It is useful for:

- repository inspection
- issue search and issue summaries
- pull request inspection
- branch and commit lookup
- code search
- repository file access through GitHub APIs
- controlled repository changes when explicitly requested

It does not read your local filesystem or operate on the local Git working tree.
A real local `git push` belongs to the Git MCP POC in `../mcp_git_agent`,
because that MCP executes Git operations against the checked-out repository and
uses your local Git credentials.

This POC uses GitHub's official MCP server Docker image:

```text
ghcr.io/github/github-mcp-server
```

It runs in read-only mode by default through:

```text
GITHUB_READ_ONLY=1
```

## Credentials

This POC does not store any GitHub token in the repository.

Set the token in your shell before running the agent:

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN=github_pat_your_token_here
```

Or create a local `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Then edit `.env` and replace the placeholder value. `.env` is ignored by git.

Use the minimum permissions needed for the test. For read-only tests against
public repositories, prefer a token with no broad write permissions. For private
repositories, grant only the repository access required for the POC.

## Files

- `fast-agent.yaml`: FastAgent configuration for Ollama and GitHub MCP.
- `agent.py`: minimal FastAgent declaration and chat launcher.
- `pyproject.toml`: isolated Python dependency metadata for this POC.
- `.env.example`: local template for the required GitHub token variable.

## Setup

Requirements:

- Docker installed and running.
- GitHub personal access token available in `GITHUB_PERSONAL_ACCESS_TOKEN`.

From this folder:

```bash
/opt/homebrew/bin/python3.14 -m venv .venv
. .venv/bin/activate
pip install -U pip
pip install -e .
ollama pull qwen3.5:latest
export GITHUB_PERSONAL_ACCESS_TOKEN=github_pat_your_token_here
```

Docker will pull `ghcr.io/github/github-mcp-server` on first run if the image is
not already available locally.

Use this POC virtual environment, not the repository root `.venv`. The root
environment uses Python 3.12, while `fast-agent-mcp` requires Python `>=3.13.5`.

IDE interpreter:

```text
/Users/politrons/development/Dive-into-Python/com/politrons/ai/mcp_github_agent/.venv/bin/python
```

## Run

Interactive chat:

```bash
python agent.py
```

Absolute command:

```bash
/Users/politrons/development/Dive-into-Python/com/politrons/ai/mcp_github_agent/.venv/bin/python /Users/politrons/development/Dive-into-Python/com/politrons/ai/mcp_github_agent/agent.py
```

One-shot prompt:

```bash
python agent.py --message "Use GitHub MCP to inspect the repository modelcontextprotocol/servers and summarize the latest open issues."
```

## Practical POC Calls

### Flow 1: Repository Summary

```bash
python agent.py --message "Use GitHub MCP to summarize the repository modelcontextprotocol/servers. Include description, default branch, and recent activity if available."
```

Expected behavior:

- The agent calls GitHub MCP.
- It returns a repository-derived summary.

### Flow 2: Issue Search

```bash
python agent.py --message "Use GitHub MCP to search open issues in modelcontextprotocol/servers related to filesystem MCP. Return titles and URLs."
```

Expected behavior:

- The agent calls GitHub MCP.
- It searches GitHub issues and returns source URLs.

### Flow 3: Pull Request Review Context

```bash
python agent.py --message "Use GitHub MCP to inspect the latest open pull requests in modelcontextprotocol/servers and summarize what each one changes."
```

Expected behavior:

- The agent calls GitHub MCP.
- It summarizes PR metadata from GitHub.

## How FastAgent Wires This MCP

There are three layers:

1. Runtime dependency

   This POC does not use a Node dependency. GitHub's official MCP server is run
   as a Docker image:

   ```bash
   docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server
   ```

2. FastAgent YAML server configuration

   `fast-agent.yaml` gives that MCP process a logical server name:

   ```yaml
   mcp:
     servers:
       github:
         command: "docker"
         args:
           - "run"
           - "-i"
           - "--rm"
           - "-e"
           - "GITHUB_PERSONAL_ACCESS_TOKEN"
           - "-e"
           - "GITHUB_READ_ONLY=1"
           - "ghcr.io/github/github-mcp-server"
         env:
           GITHUB_PERSONAL_ACCESS_TOKEN: "${GITHUB_PERSONAL_ACCESS_TOKEN:}"
   ```

   This tells FastAgent how to start the MCP server and which environment
   variable provides the GitHub credential.

3. Agent declaration

   `agent.py` selects that logical server by name:

   ```python
   @fast.agent(
       name="github",
       servers=["github"],
   )
   ```

   The value in `servers=[...]` must match the key under `mcp.servers` in YAML.

## Notes

GitHub MCP requires credentials for useful calls and may require additional
repository permissions depending on the operation. Keep the token outside git.

## Troubleshooting

### `McpError: Connection closed`

FastAgent can show this when the Docker MCP process exits during startup. For
this POC, the most common cause is a missing GitHub token.

Check it from the same shell where you run `python agent.py`:

```bash
printenv GITHUB_PERSONAL_ACCESS_TOKEN
```

If it prints nothing, set the token:

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN=github_pat_your_token_here
python agent.py
```

The underlying Docker error is:

```text
GITHUB_PERSONAL_ACCESS_TOKEN not set
```

`agent.py` also loads a local `.env` file before FastAgent reads
`fast-agent.yaml`, so either of these approaches works:

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN=github_pat_your_token_here
```

or:

```bash
cp .env.example .env
```

Reference: <https://github.com/github/github-mcp-server>
