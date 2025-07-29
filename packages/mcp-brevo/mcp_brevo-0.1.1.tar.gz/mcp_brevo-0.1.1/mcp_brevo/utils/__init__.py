"""
Utility functions for Brevo MCP.
"""
from .api_client import (
    get_account_api,
    get_campaign_api,
    get_contact_api,
    get_email_api,
    get_smtp_api,
    get_transactional_email_api
)
from .error_handlers import handle_api_error, extract_attribute

__all__ = [
    'get_account_api',
    'get_campaign_api',
    'get_contact_api',
    'get_email_api',
    'get_smtp_api',
    'get_transactional_email_api',
    'handle_api_error',
    'extract_attribute'
]
