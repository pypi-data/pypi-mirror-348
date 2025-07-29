from mcp.server.fastmcp import FastMCP

# Create an MCP server instance
mcp = FastMCP("SimpleMCPDemo", dependencies=["mcp[cli]"])

# Define a tool for adding two numbers
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return a + b

# Define a tool for multiplying two numbers
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers and return the result."""
    return a * b

# Define a dynamic resource for a personalized greeting
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Return a personalized greeting for the given name."""
    return f"Hello, {name}! Welcome to the MCP Demo Server."

def main():
    mcp.run(transport="stdio")

# Run the server
if __name__ == "__main__":
    mcp.run(transport="stdio")