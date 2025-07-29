#!/usr/bin/env python3
"""
Brevo MCP - Entry point script for running the Brevo MCP
"""

def main():
    """Run the Brevo MCP with stdio transport"""
    # Import and run the MCP
    from mcp_brevo.mcp import start_mcp
    start_mcp()

if __name__ == "__main__":
    main()
