from .server import mcp
import sys

def main() -> None:
    try:
        print("Starting MISTFS MCP Server...")
        mcp.run()
    except Exception as e:
        print(f"Error starting MISTFS MCP server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()