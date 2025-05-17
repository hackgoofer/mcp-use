import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient


async def main():
    # Load environment variables
    load_dotenv()

    # Create configuration dictionary
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

    # Create MCPClient from configuration dictionary
    client = MCPClient.from_dict(config)

    # Create LLM
    llm = ChatOpenAI(model="gpt-4o")

    # Create agent with the client
    agent = MCPAgent(llm=llm, client=client, max_steps=30)

    # Run the query
    result = await agent.run(
        """Can you remove the empty text file (empty.txt) on this repo? https://github.com/edshen17/mcp-hackathon.""",
        # """Can you change a file on this repo? https://github.com/edshen17/mcp-hackathon. Can you add a new file called "README.md" under `server` directory and commit and submit a pull request?""",
        # """Can you tell me the contents of the README.md file in root directory?"""
    )
    print(f"\nResult: {result}")


if __name__ == "__main__":
    asyncio.run(main())
