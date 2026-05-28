# Python Browser MCP Agent POC

- Ollama local chat model configured outside the agent code.
- Browser MCP server configured outside the agent code.
- Minimal Python code that only declares the agent and opens a chat session.
- `fast-agent.yaml` defines MCP servers.
- `generic.*` models target OpenAI-compatible endpoints, including Ollama at `http://localhost:11434/v1`.
- The framework owns the CLI, including interactive and one-shot runs.
- The LLM automatically sees the MCP tools declared for the agent.
- The current agent instruction asks the model to use Browser MCP before answering every user request.

## Files

- `fast-agent.yaml`: equivalent of Spring's `application.yml` for the POC.
- `agent.py`: minimal agent declaration and chat launcher.
- `pyproject.toml`: isolated dependency metadata for this POC.

## Prerequisites

The latest `fast-agent-mcp` package currently requires Python `>=3.13.5`. The root project venv here is Python `3.12.7`, but this machine has `/opt/homebrew/bin/python3.14`, so create a dedicated environment for this POC.

You also need:

- Ollama running on `http://localhost:11434`
- Node.js 20+
- Firefox browser binaries for Playwright MCP

## Setup

From this folder:

```bash
/opt/homebrew/bin/python3.14 -m venv .venv
. .venv/bin/activate
pip install -U pip
pip install -e .
npm install
npx -y playwright install firefox
ollama pull qwen3.5:latest
```

You can also override the model at runtime:

```bash
python agent.py --model generic.qwen3.5:latest --message "Open https://example.com and return the title" --quiet
```

## Run

Interactive chat:

```bash
python agent.py
```

One-shot prompt:

```bash
python agent.py --message "Find the official Spring AI MCP client documentation and summarize how it configures MCP tools with Ollama." --quiet
```

Browser tool prompt:

```bash
python agent.py --message "Use the MCP browser to find the latest news about corruption allegations involving Jose Luis Rodriguez Zapatero. Summarize only what reputable sources report, state allegations as allegations, and include source URLs."
```

When debugging tool usage, run without `--quiet`. The fast-agent usage summary shows whether the model emitted real MCP tool calls. The option is `--quiet`, not `--quite`.

## Tool-calling model note

This POC defaults to `qwen3.5:latest` because it produced better tool-calling behavior than `llama3.1` through Ollama's OpenAI-compatible endpoint during local tests.

The current agent instruction asks the model to use Browser MCP before every answer. The code also passes an OpenAI-compatible `tool_choice` override for `browser__browser_navigate`; however, local Ollama streaming behavior can still ignore or mishandle tool forcing depending on the model.

If the answer prints JSON such as `{"name": "browser__browser_navigate", ...}` and the usage summary says `Tools 0`, the MCP server was not called. That is a model/tool-calling compatibility problem, not a Playwright MCP browser problem.

## Runtime model

By default this POC does not start a REST service or expose Spring Boot-style endpoints. `python agent.py` starts the configured agent process and opens an interactive chat. `python agent.py --message "..."` is handled by the fast-agent CLI, sends one prompt, prints the answer, and exits.

The underlying `fast-agent` framework can run agents through MCP/agent transports, but it is not a custom REST endpoint like `/api/chat`. For that shape, wrap the agent with FastAPI.

## Config AI mapping

Python `fast-agent`:

```yaml
default_model: "generic.qwen3.5:latest"

generic:
  api_key: "ollama"
  base_url: "http://localhost:11434/v1"

mcp:
  servers:
    browser:
      transport: "stdio"
      command: "./node_modules/.bin/playwright-mcp"
      args: ["--headless", "--browser", "firefox"]
```
