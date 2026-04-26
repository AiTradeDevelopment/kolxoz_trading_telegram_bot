from pydantic import validate_call
from agno.tools import tool

class FetchMCP:
    command = "uvx"
    args = ["mcp-server-fetch"]

    @validate_call
    def __init__(self, url: str):
        self.url = url

@tool
def fetch_mcp_data(url: str) -> str:
    """Fetch data using FetchMCP."""
    instance = FetchMCP(url=url)
    return f"Data from {instance.url}"