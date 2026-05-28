# Python Sequential Thinking MCP Agent POC

- Ollama local chat model configured outside the agent code.
- Sequential Thinking MCP server configured outside the agent code.
- Minimal Python code that only declares the agent and opens a chat session.
- `fast-agent.yaml` defines the MCP server and the Ollama OpenAI-compatible endpoint.
- The agent uses Sequential Thinking MCP before answering, then returns
  subtasks, assumptions, risks, and a practical plan when the prompt requires it.

## What This MCP Does

Sequential Thinking MCP exposes a tool for structured reasoning. It does not
read files, browse the internet, or persist memory. Its role is to help the LLM
think through a problem step by step.

It is useful for:

- decomposing a prompt into subtasks
- building an implementation plan
- comparing alternatives
- identifying assumptions and risks
- revising a plan when new information appears
- producing a clearer final answer after structured reasoning

## Files

- `fast-agent.yaml`: FastAgent configuration for Ollama and Sequential Thinking MCP.
- `agent.py`: minimal FastAgent declaration and chat launcher.
- `pyproject.toml`: isolated Python dependency metadata for this POC.
- `package.json`: pinned Node MCP server dependency.

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
/Users/politrons/development/Dive-into-Python/com/politrons/ai/mcp_sequential_thinking_agent/.venv/bin/python
```

## Run

Interactive chat:

```bash
python agent.py
```

Absolute command:

```bash
/Users/politrons/development/Dive-into-Python/com/politrons/ai/mcp_sequential_thinking_agent/.venv/bin/python /Users/politrons/development/Dive-into-Python/com/politrons/ai/mcp_sequential_thinking_agent/agent.py
```

`agent.py` loads the `fast-agent.yaml` file from this folder explicitly, so the
absolute command also works when the IDE working directory is the repository
root.

One-shot prompt:

```bash
python agent.py --message "Create a plan to implement a new FastAgent POC using Git MCP. Break it into subtasks, risks, and validation steps."
```

## Practical POC Calls

### Flow 1: Planning A New MCP Agent

```bash
python agent.py --message "Plan a new FastAgent POC for Git MCP. I want minimal Python code, YAML configuration, setup steps, and validation commands."
```

Expected behavior:

- The agent calls Sequential Thinking MCP.
- It breaks the request into implementation subtasks.
- It identifies assumptions and risks.
- It returns a concise plan.

### Flow 2: Debugging A Failed POC

```bash
python agent.py --message "The Memory MCP agent fails with ModuleNotFoundError: fast_agent. Diagnose the likely causes and give a step-by-step fix plan."
```

Expected behavior:

- The agent uses Sequential Thinking MCP to reason through environment,
  dependency, interpreter, and working-directory causes.
- It returns a practical diagnosis plan.

### Flow 3: Comparing MCP Options

```bash
python agent.py --message "Compare Memory MCP, Fetch MCP, and Filesystem MCP for the next local FastAgent POC. Give a decision matrix and recommendation."
```

Expected behavior:

- The agent uses Sequential Thinking MCP to structure the comparison.
- It returns criteria, tradeoffs, and a recommendation.

## How FastAgent Wires This MCP

There are three layers:

1. Node dependency

   `package.json` declares the concrete MCP server package:

   ```json
   "@modelcontextprotocol/server-sequential-thinking": "2025.12.18"
   ```

   `npm install` downloads it into `node_modules/` and creates the local binary:

   ```text
   node_modules/.bin/mcp-server-sequential-thinking
   ```

2. FastAgent YAML server configuration

   `fast-agent.yaml` gives that MCP process a logical server name:

   ```yaml
   mcp:
     servers:
       sequential_thinking:
         transport: "stdio"
         command: "/Users/politrons/development/Dive-into-Python/com/politrons/ai/mcp_sequential_thinking_agent/node_modules/.bin/mcp-server-sequential-thinking"
   ```

   This tells FastAgent how to start the MCP server process.

3. Agent declaration

   `agent.py` selects that logical server by name:

   ```python
   @fast.agent(
       name="planner",
       servers=["sequential_thinking"],
   )
   ```

   The value in `servers=[...]` must match the key under `mcp.servers` in YAML.

`FastAgent("...", config_path="fast-agent.yaml")` loads the YAML. The decorator
connects the agent to the selected MCP server. When the agent runs, FastAgent
starts the configured command and exposes the MCP tools to the LLM.

## Notes

Sequential Thinking MCP does not execute the subtasks. It helps the LLM reason
about them. Execution still requires other tools or manual implementation.

This POC instructs the agent to call Sequential Thinking MCP before every user
request so tool usage is visible during tests.
