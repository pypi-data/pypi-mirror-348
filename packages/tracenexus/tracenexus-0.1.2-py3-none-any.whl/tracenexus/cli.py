import argparse
import os
import sys

from dotenv import load_dotenv

from .server.mcp_server import TraceNexusServer


def main():
    """Main entry point for the CLI."""
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="TraceNexus: MCP server for LLM tracing platforms"
    )
    parser.add_argument(
        "--transport",
        choices=["streamable-http"],
        default="streamable-http",
        help="Transport protocol (only streamable-http is supported)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for the HTTP server (used with streamable-http transport)",
    )
    parser.add_argument(
        "--mount-path",
        type=str,
        default="/mcp",
        help="Path to mount the MCP endpoints (used with streamable-http transport)",
    )

    args = parser.parse_args()

    langsmith_api_key = os.environ.get("LANGSMITH_API_KEY")
    langsmith_project = os.environ.get("LANGSMITH_PROJECT")
    if langsmith_api_key or langsmith_project:
        if not langsmith_api_key or not langsmith_project:
            print(
                "Error: If using LangSmith, both LANGSMITH_API_KEY and LANGSMITH_PROJECT environment variables must be set."
            )
            sys.exit(1)

    langfuse_public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
    langfuse_secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
    if langfuse_public_key or langfuse_secret_key:
        if not langfuse_public_key or not langfuse_secret_key:
            print(
                "Error: If using Langfuse, both LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY environment variables must be set."
            )
            sys.exit(1)

    server = TraceNexusServer()
    server.run(transport=args.transport, port=args.port, mount_path=args.mount_path)


if __name__ == "__main__":
    main()
