#!/usr/bin/env python3
"""
Brevo MCP - Entry point script for running the Brevo MCP
"""
import os
import sys
import mcp

# Import tools
from mcp_brevo.tools.contacts import manage_contact
from mcp_brevo.tools.lists import manage_list
from mcp_brevo.tools.campaigns import manage_campaign
from mcp_brevo.tools.templates import manage_template
from mcp_brevo.tools.emails import send_email, track_email
from mcp_brevo.tools.sms import manage_sms
from mcp_brevo.tools.analytics import get_analytics
from mcp_brevo.tools.account import get_account_info

# Import configuration
from mcp_brevo.config import BREVO_API_KEY

def main():
    """Run the Brevo MCP with stdio transport"""
    # Check API key
    if not BREVO_API_KEY:
        print("ERROR: BREVO_API_KEY environment variable is not set")
        print("Please set it with: export BREVO_API_KEY='your-api-key'")
        exit(1)
    
    # Register all tools using decorator syntax
    mcp.tool()(manage_contact)
    mcp.tool()(manage_list)
    mcp.tool()(manage_campaign)
    mcp.tool()(manage_template)
    mcp.tool()(send_email)
    mcp.tool()(track_email)
    mcp.tool()(manage_sms)
    mcp.tool()(get_analytics)
    mcp.tool()(get_account_info)
    
    # Start the MCP server with stdio transport
    mcp.stdio()

if __name__ == "__main__":
    main()
