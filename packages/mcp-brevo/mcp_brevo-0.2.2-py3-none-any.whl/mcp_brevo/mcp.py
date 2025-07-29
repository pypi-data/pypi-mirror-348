#!/usr/bin/env python
"""
Brevo MCP Core Implementation
"""
import os
import mcp
import brevo_python
from brevo_python.rest import ApiException

# Import tools
from .tools.contacts import manage_contact
from .tools.lists import manage_list
from .tools.campaigns import manage_campaign
from .tools.templates import manage_template
from .tools.emails import send_email, track_email
from .tools.sms import manage_sms
from .tools.analytics import get_analytics
from .tools.account import get_account_info

# Import configuration
from .config import BREVO_API_KEY

def register_tools():
    """Register all tools with the MCP."""
    # Contact management
    mcp.tool()(manage_contact)
    
    # List management
    mcp.tool()(manage_list)
    
    # Campaign management
    mcp.tool()(manage_campaign)
    
    # Template management
    mcp.tool()(manage_template)
    
    # Email tools
    mcp.tool()(send_email)
    mcp.tool()(track_email)
    
    # SMS tools
    mcp.tool()(manage_sms)
    
    # Analytics tools
    mcp.tool()(get_analytics)
    
    # Account tools
    mcp.tool()(get_account_info)

def start_mcp(transport='stdio'):
    """
    Start the Brevo MCP server.
    
    Args:
        transport: The transport type to use ('stdio', 'http', etc.)
    """
    # Check API key
    if not BREVO_API_KEY:
        print("ERROR: BREVO_API_KEY environment variable is not set")
        print("Please set it with: export BREVO_API_KEY='your-api-key'")
        exit(1)
    
    # Register all tools
    register_tools()
    
    # Start the MCP server with the specified transport
    if transport == 'stdio':
        mcp.stdio()
    elif transport == 'http':
        mcp.http()
    else:
        print(f"Unsupported transport type: {transport}")
        print("Supported types: 'stdio', 'http'")
        exit(1)
