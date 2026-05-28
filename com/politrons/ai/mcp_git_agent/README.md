# Python Git MCP Agent POC

- Ollama local chat model configured outside the agent code.
- Filesystem MCP and Git MCP servers configured outside the agent code.
- Minimal Python code that only declares the agent and opens a chat session.
- `fast-agent.yaml` defines both MCP servers, allowed directories, and the Ollama endpoint.
- The agent can read or create files through Filesystem MCP.
- The agent can perform local Git operations, including `git_push`, when explicitly requested.

## What These MCPs Do

This POC wires two MCP servers into one FastAgent agent:

- `@modelcontextprotocol/server-filesystem`: reads and writes files inside the configured root.
- `@cyanheads/git-mcp-server`: exposes local Git CLI operations through MCP tools.

It is useful for:

- reading a local file that should be committed
- copying or creating a file inside a local clone
- reading local Git status
- reading diffs and logs
- staging files
- creating commits
- creating and switching branches
- pulling and fetching
- pushing commits to remotes
- managing stashes, tags, and worktrees

This is different from GitHub MCP:

- GitHub MCP talks to the GitHub API.
- Git MCP talks to the local Git repository on disk.
- Filesystem MCP talks to the local filesystem on disk.
- A real `git push` from your local working tree belongs in Git MCP.
- A full "take this local file and push it to GitHub" flow needs both Filesystem
  MCP and Git MCP.

## Safety Defaults

The server is restricted by default to:

```text
/Users/politrons/development/Dive-into-Python
```

You can change the allowed base directory without editing Python code:

```bash
export MCP_GIT_BASE_DIR=/absolute/path/to/repos
export MCP_FILESYSTEM_ROOT=/absolute/path/to/repos
```

The agent instruction defaults to read-only behavior and requires an explicit
user request before staging, committing, pulling, pushing, merging, rebasing, or
resetting. It also avoids overwriting local files unless the prompt explicitly
asks for that file change.

## Files

- `fast-agent.yaml`: FastAgent configuration for Ollama, Filesystem MCP, and Git MCP.
- `agent.py`: minimal FastAgent declaration and chat launcher.
- `pyproject.toml`: isolated Python dependency metadata for this POC.
- `package.json`: pinned Node MCP server dependency.
- `.env.example`: optional environment template.
- `logs/`: local Git MCP logs.
- `workspace/`: optional ignored folder for temporary local clones.

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
/Users/politrons/development/Dive-into-Python/com/politrons/ai/mcp_git_agent/.venv/bin/python
```

## Run

Interactive chat:

```bash
python agent.py
```

Absolute command:

```bash
/Users/politrons/development/Dive-into-Python/com/politrons/ai/mcp_git_agent/.venv/bin/python /Users/politrons/development/Dive-into-Python/com/politrons/ai/mcp_git_agent/agent.py
```

One-shot prompt:

```bash
python agent.py --message "Use Git MCP to show the status of /Users/politrons/development/Dive-into-Python."
```

## Practical POC Calls

### Flow 1: Read Status

```bash
python agent.py --message "Use Git MCP to show git status for /Users/politrons/development/Dive-into-Python."
```

Expected behavior:

- The agent calls Git MCP.
- It returns the local repository status.

### Flow 2: Inspect Pending Changes

```bash
python agent.py --message "Use Git MCP to show unstaged and staged diffs for /Users/politrons/development/Dive-into-Python."
```

Expected behavior:

- The agent calls Git MCP.
- It returns diff information from the local repository.

### Flow 3: Commit Explicitly

```bash
python agent.py --message "Use Git MCP to stage README.md and create a commit with message 'docs: update MCP POC notes' in /Users/politrons/development/Dive-into-Python."
```

Expected behavior:

- The agent calls Git MCP.
- It stages the requested file and creates a local commit.

### Flow 4: Push Explicitly

```bash
python agent.py --message "Use Git MCP to push the current branch of /Users/politrons/development/Dive-into-Python to origin."
```

Expected behavior:

- The agent calls Git MCP.
- It checks status, branch, remote configuration, and recent log.
- It pushes only because the user explicitly requested a push.

### Flow 5: Copy Local File Into A Clone And Push

This is the flow that GitHub MCP cannot do by itself because it needs local
filesystem access and local Git access.

```bash
python agent.py --message "Use Filesystem MCP and Git MCP to read /Users/politrons/development/Dive-into-Python/com/politrons/ai/mcp_github_agent/hello.txt, clone https://github.com/politrons/AgentCode into /Users/politrons/development/Dive-into-Python/com/politrons/ai/mcp_git_agent/workspace/AgentCode if it is not already cloned, write hello.txt at the repository root, show status and diff, commit it with message 'Add hello file from MCP POC', and push the current branch to origin."
```

Expected behavior:

- The agent calls Filesystem MCP to read the source file.
- The agent calls Git MCP to clone or inspect the local clone.
- The agent calls Filesystem MCP to write the file into the clone.
- The agent calls Git MCP to status, diff, add, commit, and push.

### Flow 6: Remove A Tracked File And Push

The official Filesystem MCP used here exposes `move_file`, but not `delete_file`.
For a Git deletion, the practical flow is to move the file out of the target
repository into this POC's ignored workspace and then stage the deletion with Git.

```bash
python agent.py --message "Use Filesystem MCP and Git MCP to remove package.json from /Users/politrons/development/Dive-into-Python/AgentCode and push the deletion. First inspect status, branch, remote, and log. If package.json exists, move it to /Users/politrons/development/Dive-into-Python/com/politrons/ai/mcp_git_agent/workspace/deleted/AgentCode/package.json instead of emptying it. Then verify git status and diff show package.json as deleted, stage package.json, commit with message 'Remove package.json', and push main to origin."
```

Expected behavior:

- The agent calls Filesystem MCP to move the file out of the local clone.
- The agent calls Git MCP to verify the deletion.
- The agent calls Git MCP to stage, commit, and push the deletion.
- The agent does not use `write_file` with empty content to simulate deletion.

## How FastAgent Wires This MCP

There are three layers:

1. Node dependencies

   `package.json` declares the concrete MCP server packages:

   ```json
   "@modelcontextprotocol/server-filesystem": "2026.1.14",
   "@cyanheads/git-mcp-server": "2.15.1"
   ```

   `npm install` downloads them into `node_modules/` and creates the local binaries:

   ```text
   node_modules/.bin/mcp-server-filesystem
   node_modules/.bin/git-mcp-server
   ```

2. FastAgent YAML server configuration

   `fast-agent.yaml` gives that MCP process a logical server name:

   ```yaml
   mcp:
     servers:
       filesystem:
         command: ".../node_modules/.bin/mcp-server-filesystem"
         args:
           - "${MCP_FILESYSTEM_ROOT:/Users/politrons/development/Dive-into-Python}"
       git:
         command: ".../node_modules/.bin/git-mcp-server"
         env:
           MCP_TRANSPORT_TYPE: "stdio"
           GIT_BASE_DIR: "${MCP_GIT_BASE_DIR:/Users/politrons/development/Dive-into-Python}"
           GIT_TERMINAL_PROMPT: "0"
           SSH_AUTH_SOCK: "${SSH_AUTH_SOCK:}"
   ```

   This tells FastAgent how to start both MCP servers and restricts allowed file
   and Git operations to the configured base directories.

3. Agent declaration

   `agent.py` selects that logical server by name:

   ```python
   @fast.agent(
       name="git",
       servers=["filesystem", "git"],
   )
   ```

   The value in `servers=[...]` must match the key under `mcp.servers` in YAML.

## Authentication For Push

Git MCP uses your local Git remote configuration and local credentials.

For SSH remotes:

- Make sure your SSH key is loaded.
- Make sure `SSH_AUTH_SOCK` is available in the shell or `.env`.

For HTTPS remotes:

- Configure your normal Git credential helper before using the MCP.
- `GIT_TERMINAL_PROMPT=0` is set so the MCP fails instead of hanging on an
  interactive credential prompt.

Reference: <https://github.com/cyanheads/git-mcp-server>
