"""
Brevo MCP - A Claude Model Control Panel for Brevo Marketing Automation
"""
from .tools import (
    manage_contact,
    manage_list,
    manage_campaign,
    manage_template,
    send_email,
    track_email,
    manage_sms,
    get_analytics,
    get_account_info
)

__version__ = "0.1.0"

__all__ = [
    'manage_contact',
    'manage_list',
    'manage_campaign',
    'manage_template',
    'send_email',
    'track_email',
    'manage_sms',
    'get_analytics',
    'get_account_info'
]
