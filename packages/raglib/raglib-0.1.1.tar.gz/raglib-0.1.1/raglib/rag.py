from agents import Runner, Agent, WebSearchTool
from agents.mcp import MCPServerStdio
import os


class Rag:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")
        self.ai_model = os.getenv("AI_MODEL")

    async def run_query(self, query: str):
        try:
            async with MCPServerStdio(
                cache_tools_list=True,
                params={
                    "command": "uvx",
                    "args": [
                        "--from",
                        "mcp-alchemy==2025.5.2.210242",
                        "--refresh-package",
                        "mcp-alchemy",
                        "mcp-alchemy",
                    ],
                    "env": {
                        "DB_URL": self.db_url,
                    },
                },
            ) as mcp_server_stdio_sqlite:
                spanish_agent = Agent(
                    name="Harrison Chacon",
                    instructions="You only speak Spanish.",
                    model=self.ai_model,
                    tools=[WebSearchTool()],
                    mcp_servers=[mcp_server_stdio_sqlite],
                )
                result = await Runner.run(spanish_agent, input=query)
                return {"result": result.final_output}
        except Exception as e:
            return {"status": "error", "message": str(e)}
