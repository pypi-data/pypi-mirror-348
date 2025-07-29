#!/usr/bin/env python
"""
Brevo MCP Core Implementation
"""
import os
from mcp import Model, Tool  # Import Tool instead of using mcp.tool()
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

def register_tools(model):
    """Register all tools with the MCP."""
    # Contact management
    model.add_tool(Tool.from_function(manage_contact))
    
    # List management
    model.add_tool(Tool.from_function(manage_list))
    
    # Campaign management
    model.add_tool(Tool.from_function(manage_campaign))
    
    # Template management
    model.add_tool(Tool.from_function(manage_template))
    
    # Email tools
    model.add_tool(Tool.from_function(send_email))
    model.add_tool(Tool.from_function(track_email))
    
    # SMS tools
    model.add_tool(Tool.from_function(manage_sms))
    
    # Analytics tools
    model.add_tool(Tool.from_function(get_analytics))
    
    # Account tools
    model.add_tool(Tool.from_function(get_account_info))

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
    
    # Create a new model
    model = Model()
    
    # Register all tools
    register_tools(model)
    
    # Start the MCP server with the specified transport
    if transport == 'stdio':
        model.stdio()
    elif transport == 'http':
        model.http()
    else:
        print(f"Unsupported transport type: {transport}")
        print("Supported types: 'stdio', 'http'")
        exit(1)
