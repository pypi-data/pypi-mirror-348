"""
Configuration and shared settings for Brevo MCP.
"""
from typing import Any, Dict, List, Optional, Union
import os
import brevo_python

# Global configuration
BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "") 

# Configure API key authorization
configuration = brevo_python.Configuration()
configuration.api_key['api-key'] = BREVO_API_KEY
