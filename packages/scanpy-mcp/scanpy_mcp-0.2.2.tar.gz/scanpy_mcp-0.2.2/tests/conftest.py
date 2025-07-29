
import pytest

@pytest.fixture
def mcp_config():
    return {
        "mcpServers": {
            "scanpy-mcp": {
                "command": "scanpy-mcp",
                "args": ["run"]
            }
        }
    }