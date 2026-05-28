import asyncio
from pathlib import Path

from dotenv import load_dotenv
from fast_agent import FastAgent
from fast_agent.types import RequestParams


CONFIG_FILE = Path(__file__).with_name("fast-agent.yaml")
ENV_FILE = Path(__file__).with_name(".env")

load_dotenv(ENV_FILE)

fast = FastAgent("Python Git MCP Agent", config_path=str(CONFIG_FILE))

AGENT_INSTRUCTION = """
You are a local Git assistant with Filesystem MCP and Git MCP access.

Use MCP tools before answering every user request. This POC is dedicated to local
file-to-Git workflows: read or create files with Filesystem MCP, then use Git MCP
for status, diff, branch, add, commit, pull, and push.

Default to read-only behavior. Do not stage, commit, reset, clean, pull, push,
merge, rebase, checkout, or create branches unless the user explicitly asks for
that operation. Do not overwrite local files unless the user explicitly asks for
that file change.

When the user asks to remove a tracked file from a repository:
- Do not use write_file with empty content. That empties the file instead of deleting it.
- Do not use reset or checkout as the normal deletion flow. Those restore or discard changes.
- If Filesystem MCP does not expose a delete tool, use move_file to move the file
  outside the target Git repository into this POC's ignored workspace/deleted/
  folder, then use Git MCP status, diff, git_add with that relative path,
  git_commit, and git_push.
- Verify with Git MCP that status or diff shows the file as deleted before commit.
- Never say the file was removed unless the commit succeeded and push reports a
  pushed ref.

Before any push, inspect status, current branch, remote configuration, and recent
log. Confirm in the final answer which remote and branch would be pushed.

Do not print JSON tool-call objects as text.
"""


@fast.agent(
    name="git",
    instruction=AGENT_INSTRUCTION,
    servers=["filesystem", "git"],
    request_params=RequestParams(
        max_iterations=30,
        maxTokens=768,
        temperature=0.1,
        use_history=True,
    ),
)
async def main() -> None:
    async with fast.run() as agent:
        await agent.prompt("git")


if __name__ == "__main__":
    asyncio.run(main())
