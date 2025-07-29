"""
API client initialization for Brevo services.
"""
import brevo_python
from ..config import configuration

def get_contact_api():
    """Initialize and return a ContactsApi instance."""
    return brevo_python.ContactsApi(brevo_python.ApiClient(configuration))

def get_email_api():
    """Initialize and return a TransactionalEmailsApi instance."""
    return brevo_python.TransactionalEmailsApi(brevo_python.ApiClient(configuration))

def get_campaign_api():
    """Initialize and return an EmailCampaignsApi instance."""
    return brevo_python.EmailCampaignsApi(brevo_python.ApiClient(configuration))

def get_account_api():
    """Initialize and return an AccountApi instance."""
    return brevo_python.AccountApi(brevo_python.ApiClient(configuration))

def get_transactional_email_api():
    """Initialize and return a TransactionalEmailsApi instance."""
    return brevo_python.TransactionalEmailsApi(brevo_python.ApiClient(configuration))

def get_smtp_api():
    """Initialize and return a TransactionalEmailsApi instance for SMTP operations."""
    return brevo_python.TransactionalEmailsApi(brevo_python.ApiClient(configuration))
