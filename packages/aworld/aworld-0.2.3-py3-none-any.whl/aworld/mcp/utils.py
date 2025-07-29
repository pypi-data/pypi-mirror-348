import logging
from typing import List, Dict, Any
import json
import os
from contextlib import AsyncExitStack

from aworld.logs.util import logger
from aworld.mcp.server import MCPServer, MCPServerSse
from aworld.utils.common import find_file

MCP_SERVERS_CONFIG = {}

async def run(mcp_servers: list[MCPServer]) -> List[Dict[str, Any]]:
    openai_tools = []
    for i, server in enumerate(mcp_servers):
        try:
            tools = await server.list_tools()
            for tool in tools:
                required = []
                properties = {}
                if tool.inputSchema and tool.inputSchema.get("properties"):
                    required = tool.inputSchema.get("required", [])
                    _properties = tool.inputSchema["properties"]
                    for param_name, param_info in _properties.items():
                        param_type = param_info.get("type") if param_info.get("type") != "str" and param_info.get("type") is not None else "string"
                        param_desc = param_info.get("description", "")
                        if param_type == "array":
                            # Handle array type parameters
                            item_type = param_info.get("items", {}).get("type", "string")
                            if item_type == "str":
                                item_type = "string"
                            properties[param_name] = {
                                "description": param_desc,
                                "type": param_type,
                                "items": {
                                    "type": item_type
                                }
                            }
                        else:
                            # Handle non-array type parameters
                            properties[param_name] = {
                                "description": param_desc,
                                "type": param_type
                            }
                        if param_info.get("required", False):
                            required.append(param_name)

                openai_function_schema = {
                    "name": f'{server.name}__{tool.name}',
                    "description": tool.description,
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": required
                    }
                }
                openai_tools.append({
                    "type": "function",
                    "function": openai_function_schema,
                })
            logging.debug(f"✅ server #{i + 1} ({server.name}) connected success，tools: {len(tools)}")

        except Exception as e:
            logging.error(f"❌ server #{i + 1} ({server.name}) connect fail: {e}")
            return []

    return openai_tools


async def mcp_tool_desc_transform(tools: List[str] = None,mcp_config: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """Default implement transform framework standard protocol to openai protocol of tool description."""
    config = {}
    global MCP_SERVERS_CONFIG
    def _replace_env_variables(config):
        if isinstance(config, dict):
            for key, value in config.items():
                if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                    env_var_name = value[2:-1]
                    config[key] = os.getenv(env_var_name, value)
                    logging.info(f"Replaced {value} with {config[key]}")
                elif isinstance(value, dict) or isinstance(value, list):
                    _replace_env_variables(value)
        elif isinstance(config, list):
            for index, item in enumerate(config):
                if isinstance(item, str) and item.startswith("${") and item.endswith("}"):
                    env_var_name = item[2:-1]
                    config[index] = os.getenv(env_var_name, item)
                    logging.info(f"Replaced {item} with {config[index]}")
                elif isinstance(item, dict) or isinstance(item, list):
                    _replace_env_variables(item)

    if mcp_config:
        try:
            config = mcp_config
            MCP_SERVERS_CONFIG = config
        except Exception as e:
            logging.error(f"mcp_config error: {e}")
            return []
    else:
        # Priority given to the running path.
        config_path = find_file(filename='mcp.json')
        if not os.path.exists(config_path):
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.normpath(os.path.join(current_dir, "../config/mcp.json"))
        logger.info(f"mcp conf path: {config_path}")

        if not os.path.exists(config_path):
            logging.info(f"mcp config is not exist: {config_path}")
            return []

        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except Exception as e:
            logging.info(f"load config fail: {e}")
            return []
        _replace_env_variables(config)

        MCP_SERVERS_CONFIG = config

    mcp_servers_config = config.get("mcpServers", {})

    server_configs = []
    for server_name, server_config in mcp_servers_config.items():
        # Skip disabled servers
        if server_config.get("disabled", False):
            continue

        if tools is None or server_name in tools:
            # Handle SSE server
            if "url" in server_config:
                server_configs.append({
                    "name": "mcp__" + server_name,
                    "type": "sse",
                    "params": {"url": server_config["url"]}
                })
            # Handle stdio server
            elif "command" in server_config:
                server_configs.append({
                    "name": "mcp__" + server_name,
                    "type": "stdio",
                    "params": {
                        "command": server_config["command"],
                        "args": server_config.get("args", []),
                        "env": server_config.get("env", {}),
                        "cwd": server_config.get("cwd"),
                        "encoding": server_config.get("encoding", "utf-8"),
                        "encoding_error_handler": server_config.get("encoding_error_handler", "strict")
                    }
                })

    if not server_configs:
        return []

    async with AsyncExitStack() as stack:
        servers = []
        for server_config in server_configs:
            if server_config["type"] == "sse":
                server = MCPServerSse(
                    name=server_config["name"],
                    params=server_config["params"]
                )
            elif server_config["type"] == "stdio":
                from aworld.mcp.server import MCPServerStdio
                server = MCPServerStdio(
                    name=server_config["name"],
                    params=server_config["params"]
                )
            else:
                logging.warning(f"Unsupported MCP server type: {server_config['type']}")
                continue

            server = await stack.enter_async_context(server)
            servers.append(server)

        openai_tools = await run(servers)

    return openai_tools
