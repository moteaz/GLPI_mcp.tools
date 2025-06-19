from mcp.server.fastmcp import FastMCP
import httpx

# Create an MCP server
mcp = FastMCP("GLPI MCP")

# Helper: GLPI API client
class GLPIClient:
    def __init__(self, base_url, app_token, session_token):
        self.base_url = base_url.rstrip('/')  
        self.headers = {
            "App-Token": app_token,
            "Session-Token": session_token,
            "Content-Type": "application/json"
        }

    async def get(self, path, params=None):
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}{path}"
            resp = await client.get(url, headers=self.headers, params=params)
            resp.raise_for_status()
            return resp.json()

    async def post(self, path, data):
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}{path}"
            resp = await client.post(url, headers=self.headers, json=data)
            resp.raise_for_status()
            return resp.json()

    async def put(self, path, data):
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}{path}"
            resp = await client.put(url, headers=self.headers, json=data)
            resp.raise_for_status()
            return resp.json()

    async def delete(self, path):
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}{path}"
            resp = await client.delete(url, headers=self.headers)
            resp.raise_for_status()
            return resp.json()

# Tool: Authenticate and get session token
@mcp.tool()
async def init_session(base_url: str, app_token: str, user_token: str):
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
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

# Tool: List all tickets
@mcp.tool()
async def list_tickets(base_url: str, app_token: str, session_token: str):
    """List all tickets."""
    glpi = GLPIClient(base_url, app_token, session_token)
    return await glpi.get("/apirest.php/Ticket")

# Tool: Get ticket details
@mcp.tool()
async def get_ticket(base_url: str, app_token: str, session_token: str, ticket_id: int):
    """Get details for a specific ticket."""
    glpi = GLPIClient(base_url, app_token, session_token)
    return await glpi.get(f"/apirest.php/Ticket/{ticket_id}")

# Tool: Create a new ticket
@mcp.tool()
async def create_ticket(base_url: str, app_token: str, session_token: str, name: str, content: str):
    """Create a new ticket."""
    glpi = GLPIClient(base_url, app_token, session_token)
    data = {
        "input": {
            "name": name,
            "content": content
        }
    }
    return await glpi.post("/apirest.php/Ticket", data)

# Tool: Update a ticket
@mcp.tool()
async def update_ticket(base_url: str, app_token: str, session_token: str, ticket_id: int, update_fields: dict):
    """Update a ticket with the given fields."""
    glpi = GLPIClient(base_url, app_token, session_token)
    data = {"input": update_fields}
    return await glpi.put(f"/apirest.php/Ticket/{ticket_id}", data)

# Tool: Delete a ticket
@mcp.tool()
async def delete_ticket(base_url: str, app_token: str, session_token: str, ticket_id: int):
    """Delete a ticket by its ID."""
    glpi = GLPIClient(base_url, app_token, session_token)
    return await glpi.delete(f"/apirest.php/Ticket/{ticket_id}")


if __name__ == "__main__":
    mcp.run(transport="stdio") 