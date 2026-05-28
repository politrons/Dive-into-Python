import asyncio
from pathlib import Path

from fast_agent import FastAgent
from fast_agent.types import RequestParams


CONFIG_FILE = Path(__file__).with_name("fast-agent.yaml")

fast = FastAgent("Python Filesystem MCP Agent", config_path=str(CONFIG_FILE))

AGENT_INSTRUCTION = """
You are a local filesystem assistant with Filesystem MCP access.

Use Filesystem MCP before answering every user request. The configured MCP root
is the only filesystem area you can inspect or modify.

Default to read-only behavior. Do not create, update, rename, or delete files
unless the user explicitly asks for that change.

When you use filesystem data, mention the relevant path in the final answer.
Do not print JSON tool-call objects as text.
"""


@fast.agent(
    name="filesystem",
    instruction=AGENT_INSTRUCTION,
    servers=["filesystem"],
    request_params=RequestParams(
        max_iterations=25,
        maxTokens=768,
        temperature=0.1,
        use_history=True,
    ),
)
async def main() -> None:
    async with fast.run() as agent:
        await agent.prompt("filesystem")


if __name__ == "__main__":
    asyncio.run(main())
