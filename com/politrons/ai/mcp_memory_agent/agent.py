import asyncio
from pathlib import Path

from fast_agent import FastAgent
from fast_agent.types import RequestParams


CONFIG_FILE = Path(__file__).with_name("fast-agent.yaml")

fast = FastAgent("Python Memory MCP Agent", config_path=str(CONFIG_FILE))

AGENT_INSTRUCTION = """
You are a local assistant with persistent Memory MCP access.

At the start of every user request, call Memory MCP read_graph to load existing
entities, relations, and observations before answering. If the graph is large,
also use search_nodes for focused retrieval.

Use Memory MCP to store durable, reusable information such as:
- user preferences
- technical decisions
- project constraints
- rejected approaches and their reasons
- stable facts that should influence future answers

Do not store transient facts, one-off calculations, secrets, API keys, tokens,
passwords, or sensitive personal data.

When the user asks you to remember something, or when the user states a durable
preference or project decision, write it to Memory MCP using entities,
relations, and observations. Keep observations atomic: one fact per observation.

When Memory MCP contains relevant information, apply it explicitly in the answer.
If memory contains a language preference for documentation or test prompts, use
that language for the entire answer when producing documentation or test prompts.
Do not print JSON tool-call objects as text.
"""


@fast.agent(
    name="memory",
    instruction=AGENT_INSTRUCTION,
    servers=["memory"],
    request_params=RequestParams(
        max_iterations=25,
        maxTokens=768,
        temperature=0.1,
        use_history=True,
    ),
)
async def main() -> None:
    async with fast.run() as agent:
        await agent.prompt("memory")


if __name__ == "__main__":
    asyncio.run(main())
