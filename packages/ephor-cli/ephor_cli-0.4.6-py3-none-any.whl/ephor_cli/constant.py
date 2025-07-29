import os

API_SERVER_URL = os.getenv("API_SERVER_URL", "https://mcp-hive.ti.trilogy.com/api")

AGENT_SERVER_URL = os.getenv("AGENT_SERVER_URL", "https://agents.ti.trilogy.com")

DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "mcp-hive")

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "https://mcp-server.ti.trilogy.com")

print(f"API_SERVER_URL: {API_SERVER_URL}")
print(f"AGENT_SERVER_URL: {AGENT_SERVER_URL}")
print(f"MCP_SERVER_URL: {MCP_SERVER_URL}")
print(f"DYNAMODB_TABLE_NAME: {DYNAMODB_TABLE_NAME}")
