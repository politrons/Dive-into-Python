import asyncio

from fast_agent import FastAgent
from fast_agent.types import RequestParams


fast = FastAgent("Python Browser MCP Agent")

AGENT_INSTRUCTION = """
You are a helpful local assistant with optional Browser MCP access.

Always use one Browser MCP tool before answering any user request.
Use Browser MCP even when you already know the answer.
Do not print JSON tool-call objects as text.
"""


@fast.agent(
    name="browser",
    instruction=AGENT_INSTRUCTION,
    servers=["browser"],
    request_params=RequestParams(
        max_iterations=25,
        maxTokens=512,
        temperature=0.1,
        metadata={
            "tool_choice": {
                "type": "function",
                "function": {"name": "browser__browser_navigate"},
            }
        },
        use_history=True,
    ),
)
async def main() -> None:
    async with fast.run() as agent:
        await agent.prompt("browser")


if __name__ == "__main__":
    asyncio.run(main())
