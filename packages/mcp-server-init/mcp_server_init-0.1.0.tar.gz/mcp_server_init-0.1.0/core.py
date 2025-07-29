import asyncio
import os, sys
import shutil

from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerStdio
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel
import yaml

class MCPParameters(BaseModel):
    """
    MCP Parameters
    The parameters to start the MCP server
        - command: the command to run the server
        - args: the arguments to pass to the command
        - env: the environment variables to pass to the command
        - cwd: the working directory for the command
    """
    command: str
    args: list[str] = []
    env: dict[str, str] | None = None
    cwd: str | os.PathLike | None = None


class MCPServerConfig(BaseModel):
    """
    MCP Server provided by the user
    params: MCPParameters
        - command: the command to run the server
        - args: the arguments to pass to the command
        - env: the environment variables to pass to the command
        - cwd: the working directory for the command
    - name: the name of the server
    - cache_tools_list: whether to cache the tools list
    - client_session_timeout_seconds: the timeout for the client session

    """
    params: MCPParameters
    name: str | None = None
    cache_tools_list: bool = True
    client_session_timeout_seconds: float | None = 5.0


class MCPServerConnection:
    """
    MCPServerConnection is a class that manages the connection to the MCP server
    It is used to connect to the server, list the tools available, and disconnect from the server

    Attributes:
        server_config: path to the yaml configuration file

    Methods:
        connect: Connect to the MCP server
        disconnect: Disconnect from the MCP server

    Example:
        mcp_server = MCPServerConnection(
            server_config="server_config.yaml",
        )
        await mcp_server.connect()
        // agent logic here
        await mcp_server.disconnect()
    
    Example YAML configuration file:
        mcp_server_config:
            name: "Weather Agent Test"
            params:
                command: "uv"
                args:
                - "--directory"
                - "/home/moh/projects/work/mcp_try/mcp_server"
                - "run"
                - "weather.py"
            cache_tools_list: true
    """

    def __init__(self, server_config: MCPServerConfig | str = "server_config.yaml"):
        """
        Initialize the MCP client
        """

        if isinstance(server_config, str):
            if not os.path.exists(server_config):
                raise FileNotFoundError(f"File {server_config} does not exist")
            data = yaml.safe_load(open(server_config))
            server_config = MCPServerConfig(**data['mcp_server_config'])

        self.server_config = server_config

        params = self.server_config.params
        self._mcp = MCPServerStdio(
            name=self.server_config.name,
            params={
                "command": params.command,
                "args":    params.args,
                "env":     params.env,
                "cwd":     params.cwd,
            },
            cache_tools_list=self.server_config.cache_tools_list,
            client_session_timeout_seconds=self.server_config.client_session_timeout_seconds,
        )

    async def connect(self) -> MCPServerStdio:
        await self._mcp.__aenter__()              # actually start it
        print(f"Connected to {self._mcp.name} ✅")

        list_tools = await self._mcp.list_tools()
        print("List of tools available:")
        for i, tool in enumerate(list_tools):
            print(f"{i+1}. {tool.name} - {tool.description}")

        return self._mcp

    async def disconnect(self):
        await self._mcp.__aexit__(None, None, None)
        print(f"Disconnected from {self._mcp.name}  Successfully ✅")
    




# if __name__ == "__main__":
#     # read a yaml file and parse it
    
#     if len(sys.argv) < 2:
#         print("Please provide the path to the server_config.yaml file")
#         sys.exit(1)
#     file = sys.argv[1]
    
#     if not os.path.exists(file):
#         raise FileNotFoundError(f"File {file} does not exist")
#     with open(file, "r") as f:
#         data = yaml.safe_load(f)

#     server_config = MCPServerConfig(**data['mcp_server_config'])
#     print("Server config: ", server_config.model_dump_json(indent=2))
#     model = data['model']
#     print("Model: ", model)









        