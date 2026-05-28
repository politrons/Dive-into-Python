import asyncio
from pathlib import Path

from fast_agent import FastAgent
from fast_agent.types import RequestParams


CONFIG_FILE = Path(__file__).with_name("fast-agent.yaml")

fast = FastAgent("Python Sequential Thinking MCP Agent", config_path=str(CONFIG_FILE))

AGENT_INSTRUCTION = """
You are a local planning and decomposition agent with Sequential Thinking MCP access.

Use Sequential Thinking MCP before answering every user request. For small
requests, keep the reasoning short, but still use the configured MCP tool first.

Your job is to transform the user's request into a clear sequence of subtasks,
risks, assumptions, and a practical next-action plan.

Do not print JSON tool-call objects as text.
After using Sequential Thinking MCP, return a concise final answer with:
1. Goal
2. Subtasks
3. Risks or assumptions
4. Recommended next step
"""


@fast.agent(
    name="planner",
    instruction=AGENT_INSTRUCTION,
    servers=["sequential_thinking"],
    request_params=RequestParams(
        max_iterations=25,
        maxTokens=768,
        temperature=0.1,
        use_history=True,
    ),
)
async def main() -> None:
    async with fast.run() as agent:
        await agent.prompt("planner")


if __name__ == "__main__":
    asyncio.run(main())
