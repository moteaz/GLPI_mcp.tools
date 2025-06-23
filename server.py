import logging
from typing import Any, Dict, Optional
from mcp.server.fastmcp import FastMCP
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create an MCP server
mcp = FastMCP("GLPI MCP")

class GLPIClient:
    """
    Asynchronous client for interacting with the GLPI REST API.
    """
    def __init__(self, base_url: str, app_token: str, session_token: str) -> None:
        self.base_url = base_url.rstrip('/')  
        self.headers = {
            "App-Token": app_token,
            "Session-Token": session_token,
            "Content-Type": "application/json"
        }

    async def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Send a GET request to the GLPI API."""
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}{path}"
            try:
                resp = await client.get(url, headers=self.headers, params=params)
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                logger.error(f"GET {url} failed: {e}")
                raise

    async def post(self, path: str, data: Dict[str, Any]) -> Any:
        """Send a POST request to the GLPI API."""
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}{path}"
            try:
                resp = await client.post(url, headers=self.headers, json=data)
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                logger.error(f"POST {url} failed: {e}")
                raise

    async def put(self, path: str, data: Dict[str, Any]) -> Any:
        """Send a PUT request to the GLPI API."""
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}{path}"
            try:
                resp = await client.put(url, headers=self.headers, json=data)
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                logger.error(f"PUT {url} failed: {e}")
                raise

    async def delete(self, path: str) -> Any:
        """Send a DELETE request to the GLPI API."""
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}{path}"
            try:
                resp = await client.delete(url, headers=self.headers)
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                logger.error(f"DELETE {url} failed: {e}")
                raise

@mcp.tool()
async def init_session(base_url: str, app_token: str, user_token: str) -> Any:
    """
    Authenticate with GLPI and return the session token.
    """
    url = f"{base_url.rstrip('/')}/apirest.php/initSession"
    headers = {
        "App-Token": app_token,
        "Authorization": f"user_token {user_token}",
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.error(f"init_session failed: {e}")
            raise

@mcp.tool()
async def list_tickets(base_url: str, app_token: str, session_token: str) -> Any:
    """List all tickets."""
    glpi = GLPIClient(base_url, app_token, session_token)
    return await glpi.get("/apirest.php/Ticket")

@mcp.tool()
async def get_ticket(base_url: str, app_token: str, session_token: str, ticket_id: int) -> Any:
    """Get details for a specific ticket."""
    glpi = GLPIClient(base_url, app_token, session_token)
    return await glpi.get(f"/apirest.php/Ticket/{ticket_id}")

@mcp.tool()
async def create_ticket(base_url: str, app_token: str, session_token: str, name: str, content: str) -> Any:
    """Create a new ticket."""
    glpi = GLPIClient(base_url, app_token, session_token)
    data = {
        "input": {
            "name": name,
            "content": content
        }
    }
    return await glpi.post("/apirest.php/Ticket", data)

@mcp.tool()
async def update_ticket(base_url: str, app_token: str, session_token: str, ticket_id: int, update_fields: Dict[str, Any]) -> Any:
    """Update a ticket with the given fields."""
    glpi = GLPIClient(base_url, app_token, session_token)
    data = {"input": update_fields}
    return await glpi.put(f"/apirest.php/Ticket/{ticket_id}", data)

@mcp.tool()
async def delete_ticket(base_url: str, app_token: str, session_token: str, ticket_id: int) -> Any:
    """Delete a ticket by its ID."""
    glpi = GLPIClient(base_url, app_token, session_token)
    return await glpi.delete(f"/apirest.php/Ticket/{ticket_id}")

@mcp.tool()
async def get_users(base_url: str, app_token: str, session_token: str) -> Any:
    """Get all users."""
    glpi = GLPIClient(base_url, app_token, session_token)
    return await glpi.get("/apirest.php/User")

@mcp.tool()
async def get_computers(base_url: str, app_token: str, session_token: str) -> Any:
    """Get all computers."""
    glpi = GLPIClient(base_url, app_token, session_token)
    return await glpi.get("/apirest.php/Computer")

@mcp.tool()
async def get_groups(base_url: str, app_token: str, session_token: str) -> Any:
    """Get all groups."""
    glpi = GLPIClient(base_url, app_token, session_token)
    return await glpi.get("/apirest.php/Group")

@mcp.tool()
async def add_computer(base_url: str, app_token: str, session_token: str, name: str, content: str) -> Any:
    """Add a new computer."""
    glpi = GLPIClient(base_url, app_token, session_token)
    data = {
        "input": {
            "name": name,
            "content": content
        }
    }
    return await glpi.post("/apirest.php/Computer", data)

if __name__ == "__main__":
    mcp.run(transport="stdio") 