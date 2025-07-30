from .server import mcp
import sys

def main() -> None:
    try:
        print("Starting SWAPNIL MCP Server...")
        mcp.run()
    except Exception as e:
        print(f"Error starting MCP server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()