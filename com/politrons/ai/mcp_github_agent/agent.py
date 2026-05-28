import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fast_agent import FastAgent
from fast_agent.types import RequestParams


CONFIG_FILE = Path(__file__).with_name("fast-agent.yaml")
ENV_FILE = Path(__file__).with_name(".env")

load_dotenv(ENV_FILE)

HELP_ARGS = {"-h", "--help", "--version"}

if not HELP_ARGS.intersection(sys.argv[1:]) and not os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"):
    raise SystemExit(
        "Missing GITHUB_PERSONAL_ACCESS_TOKEN. Export it in this shell or create "
        ".env from .env.example before running python agent.py."
    )

fast = FastAgent("Python GitHub MCP Agent", config_path=str(CONFIG_FILE))

AGENT_INSTRUCTION = """
You are a local GitHub assistant with GitHub MCP access.

Use GitHub MCP before answering every user request. This POC is dedicated to
GitHub repository, issue, pull request, branch, commit, code search, and user
workflows.

Default to read-only behavior. Do not create, update, merge, close, or delete
GitHub resources unless the user explicitly asks for that change.

When you use GitHub data, mention the repository or URL in the final answer.
Do not print JSON tool-call objects as text.
"""


@fast.agent(
    name="github",
    instruction=AGENT_INSTRUCTION,
    servers=["github"],
    request_params=RequestParams(
        max_iterations=25,
        maxTokens=768,
        temperature=0.1,
        use_history=True,
    ),
)
async def main() -> None:
    async with fast.run() as agent:
        await agent.prompt("github")


if __name__ == "__main__":
    asyncio.run(main())
