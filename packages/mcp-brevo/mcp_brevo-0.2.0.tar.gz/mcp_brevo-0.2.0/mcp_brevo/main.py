#!/usr/bin/env python3
"""
Brevo MCP - Experimental approach using global tool registration if possible
"""
import os
import sys
import inspect
import logging
import mcp
from mcp import Tool
from mcp.server import Server

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("brevo-mcp")

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

def create_input_schema(func):
    """Create an input schema based on a function's type annotations"""
    params = {}
    sig = inspect.signature(func)
    required = []
    
    for name, param in sig.parameters.items():
        if name == 'self':
            continue
            
        param_type = param.annotation
        if param_type is inspect.Parameter.empty:
            param_type = str
            
        # Convert Python type to JSON Schema type
        if param_type is str:
            type_info = {"type": "string"}
        elif param_type is int:
            type_info = {"type": "integer"}
        elif param_type is float:
            type_info = {"type": "number"}
        elif param_type is bool:
            type_info = {"type": "boolean"}
        elif param_type is list or param_type is dict:
            type_info = {"type": "object"}
        else:
            # Default to string for complex types
            type_info = {"type": "string"}
            
        # Add description if function has a docstring
        if func.__doc__:
            type_info["description"] = f"Parameter '{name}' for function {func.__name__}"
            
        params[name] = type_info
        
        # Add to required list if no default value
        if param.default is inspect.Parameter.empty:
            required.append(name)
    
    return {
        "type": "object",
        "properties": params,
        "required": required
    }

def setup_tools():
    """Create tools list"""
    return [
        Tool(
            name="manage_contact",
            description=manage_contact.__doc__,
            inputSchema=create_input_schema(manage_contact),
            function=manage_contact
        ),
        Tool(
            name="manage_list",
            description=manage_list.__doc__,
            inputSchema=create_input_schema(manage_list),
            function=manage_list
        ),
        Tool(
            name="manage_campaign",
            description=manage_campaign.__doc__,
            inputSchema=create_input_schema(manage_campaign),
            function=manage_campaign
        ),
        Tool(
            name="manage_template",
            description=manage_template.__doc__,
            inputSchema=create_input_schema(manage_template),
            function=manage_template
        ),
        Tool(
            name="send_email",
            description=send_email.__doc__,
            inputSchema=create_input_schema(send_email),
            function=send_email
        ),
        Tool(
            name="track_email",
            description=track_email.__doc__,
            inputSchema=create_input_schema(track_email),
            function=track_email
        ),
        Tool(
            name="manage_sms",
            description=manage_sms.__doc__,
            inputSchema=create_input_schema(manage_sms),
            function=manage_sms
        ),
        Tool(
            name="get_analytics",
            description=get_analytics.__doc__,
            inputSchema=create_input_schema(get_analytics),
            function=get_analytics
        ),
        Tool(
            name="get_account_info",
            description=get_account_info.__doc__,
            inputSchema=create_input_schema(get_account_info),
            function=get_account_info
        )
    ]

def main():
    """Run the Brevo MCP with stdio transport"""
    # Check API key
    if not BREVO_API_KEY:
        print("ERROR: BREVO_API_KEY environment variable is not set")
        print("Please set it with: export BREVO_API_KEY='your-api-key'")
        exit(1)
    
    logger.info("Brevo MCP starting...")
    
    # Create tools
    tools = setup_tools()
    logger.info(f"Created {len(tools)} tools")
    
    # Create a server 
    logger.info("Creating server...")
    server = Server(name="brevo-mcp")
    
    # Attempt to register tools if possible
    logger.info("Attempting to register tools...")
    
    # First check if server has an add_tool or register_tool method
    for method_name in ['add_tool', 'register_tool', 'register', 'tool']:
        if hasattr(server, method_name):
            register_method = getattr(server, method_name)
            logger.info(f"Found registration method: {method_name}")
            try:
                for tool in tools:
                    register_method(tool)
                logger.info(f"Successfully registered tools using {method_name}")
                break
            except Exception as e:
                logger.error(f"Error registering tools using {method_name}: {e}")
    
    # If server has a tools attribute that's a list/dict, try adding tools directly
    if hasattr(server, 'tools'):
        logger.info("Server has 'tools' attribute")
        try:
            if isinstance(server.tools, list):
                for tool in tools:
                    server.tools.append(tool)
                logger.info("Added tools to server.tools list")
            elif isinstance(server.tools, dict):
                for tool in tools:
                    server.tools[tool.name] = tool
                logger.info("Added tools to server.tools dict")
            else:
                # Try setting directly
                server.tools = tools
                logger.info("Set server.tools directly")
        except Exception as e:
            logger.error(f"Error setting tools directly: {e}")
    
    # Try global registration if available
    for name in dir(mcp):
        if ('tool' in name.lower() or 'register' in name.lower()) and not name.startswith('_'):
            obj = getattr(mcp, name)
            logger.info(f"Found potential global registry: {name}")
            
            try:
                if callable(obj):
                    for tool in tools:
                        obj(tool)
                    logger.info(f"Registered tools using {name}()")
                    break
            except Exception as e:
                logger.error(f"Error using {name}: {e}")
    
    # Start the server
    logger.info("Starting server with stdio transport...")
    try:
        server.start_stdio()
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        
        # If server.start_stdio() fails, try using mcp.stdio_server directly
        logger.info("Trying alternative approach with stdio_server...")
        try:
            mcp.stdio_server()
        except Exception as e2:
            logger.error(f"Error using stdio_server directly: {e2}")
            exit(1)

if __name__ == "__main__":
    main()
