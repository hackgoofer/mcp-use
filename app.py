import asyncio
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_anthropic import ChatAnthropic
from mcp_use import MCPAgent, MCPClient

app = FastAPI()
load_dotenv()

config = {
    "mcpServers": {
        "github": {
            "command": "docker",
            "args": [
                "run",
                "-i",
                "--rm",
                "-e",
                "GITHUB_PERSONAL_ACCESS_TOKEN",
                "-e",
                "GITHUB_TOOLSETS",
                "ghcr.io/github/github-mcp-server",
            ],
            "env": {
                "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv(
                    "GITHUB_PERSONAL_ACCESS_TOKEN"
                ),
                "GITHUB_TOOLSETS": "repos,issues,pull_requests,code_security,experiments",
            },
        }
    }
}

client = MCPClient.from_dict(config)
llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
agent = MCPAgent(llm=llm, client=client, max_steps=30)


@app.get("/run")
async def run_agent(query: str):
    result = await agent.run(query)
    return {"result": result}
