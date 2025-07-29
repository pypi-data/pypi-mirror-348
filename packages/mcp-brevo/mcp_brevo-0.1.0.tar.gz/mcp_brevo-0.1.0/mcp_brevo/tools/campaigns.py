"""
Tools for managing email campaigns in Brevo.
"""
from typing import Optional, List, Dict, Any
import brevo_python
from brevo_python.rest import ApiException
from ..utils import get_campaign_api

async def manage_campaign(operation: str, campaign_id: Optional[int] = None,
                         name: Optional[str] = None, subject: Optional[str] = None,
                         sender: Optional[dict] = None, html_content: Optional[str] = None,
                         recipients: Optional[dict] = None, scheduled_at: Optional[str] = None,
                         status: Optional[str] = None, test_emails: Optional[List[str]] = None,
                         limit: int = 50, offset: int = 0) -> str:
    """
    Perform operations on email campaigns.
    
    Args:
        operation: One of "list", "get", "create", "update", "schedule", "test", "status"
        campaign_id: Required for all operations except list and create
        name: Required for create
        subject: Required for create, optional for update
        sender: Required for create (dict with 'name' and 'email' keys)
        html_content: Required for create, optional for update
        recipients: Required for create (dict with 'list_ids' key)
        scheduled_at: Required for schedule, optional for create/update
        status: Required for status operation
        test_emails: Required for test operation
        limit: Used only for list operation
        offset: Used only for list operation
    """
    try:
        api_instance = get_campaign_api()
        
        if operation == "list":
            api_response = api_instance.get_email_campaigns(limit=limit, offset=offset)
            
            if not api_response.campaigns:
                return "No campaigns found."
                
            campaign_details = []
            for campaign in api_response.campaigns:
                details = ""
                # Handle both object attributes and dictionary keys
                if isinstance(campaign, dict):
                    # Handle as dictionary
                    campaign_id = campaign.get('id', 'Unknown')
                    campaign_name = campaign.get('name', 'Unknown')
                    campaign_subject = campaign.get('subject', 'Unknown')
                    campaign_status = campaign.get('status', 'Unknown')
                    campaign_created = campaign.get('created_at', 'Unknown')
                    
                    details += f"ID: {campaign_id}\n"
                    details += f"Name: {campaign_name}\n"
                    details += f"Subject: {campaign_subject}\n"
                    details += f"Status: {campaign_status}\n"
                    details += f"Created at: {campaign_created}\n"
                    
                    if 'scheduled_at' in campaign and campaign['scheduled_at']:
                        details += f"Scheduled at: {campaign['scheduled_at']}\n"
                else:
                    # Handle as object with attributes
                    if hasattr(campaign, 'id'):
                        details += f"ID: {campaign.id}\n"
                    if hasattr(campaign, 'name'):
                        details += f"Name: {campaign.name}\n"
                    if hasattr(campaign, 'subject'):
                        details += f"Subject: {campaign.subject}\n"
                    if hasattr(campaign, 'status'):
                        details += f"Status: {campaign.status}\n"
                    if hasattr(campaign, 'created_at'):
                        details += f"Created at: {campaign.created_at}\n"
                    
                    if hasattr(campaign, 'scheduled_at') and campaign.scheduled_at:
                        details += f"Scheduled at: {campaign.scheduled_at}\n"
                
                campaign_details.append(details)
            
            # Get total campaign count safely
            total_count = "Unknown"
            if hasattr(api_response, 'count'):
                total_count = api_response.count
            elif isinstance(api_response, dict) and 'count' in api_response:
                total_count = api_response['count']
                
            return f"Total campaigns: {total_count}\n\n" + "\n---\n".join(campaign_details)
            
        elif operation == "get":
            if not campaign_id:
                return "Error: campaign_id is required for get operation"
                
            api_response = api_instance.get_email_campaign(campaign_id)
            
            details = ""
            if hasattr(api_response, 'id'):
                details += f"ID: {api_response.id}\n"
            if hasattr(api_response, 'name'):
                details += f"Name: {api_response.name}\n"
            if hasattr(api_response, 'subject'):
                details += f"Subject: {api_response.subject}\n"
            if hasattr(api_response, 'status'):
                details += f"Status: {api_response.status}\n"
            if hasattr(api_response, 'created_at'):
                details += f"Created at: {api_response.created_at}\n"
            
            if hasattr(api_response, 'scheduled_at') and api_response.scheduled_at:
                details += f"Scheduled at: {api_response.scheduled_at}\n"
                
            if hasattr(api_response, 'recipients') and api_response.recipients:
                if hasattr(api_response.recipients, 'list_ids') and api_response.recipients.list_ids:
                    details += f"List IDs: {', '.join(str(id) for id in api_response.recipients.list_ids)}\n"
            
            if hasattr(api_response, 'statistics') and api_response.statistics:
                stats = api_response.statistics
                details += "\nStatistics:\n"
                if hasattr(stats, 'sent') and stats.sent is not None:
                    details += f"  Sent: {stats.sent}\n"
                if hasattr(stats, 'delivered') and stats.delivered is not None:
                    details += f"  Delivered: {stats.delivered}\n"
                if hasattr(stats, 'opens') and stats.opens is not None:
                    details += f"  Opens: {stats.opens}\n"
                if hasattr(stats, 'clicks') and stats.clicks is not None:
                    details += f"  Clicks: {stats.clicks}\n"
                if hasattr(stats, 'unsubscriptions') and stats.unsubscriptions is not None:
                    details += f"  Unsubscriptions: {stats.unsubscriptions}\n"
                
            return details
            
        elif operation == "create":
            # Validate required parameters
            if not name:
                return "Error: name is required for create operation"
            if not subject:
                return "Error: subject is required for create operation"
            if not sender or not isinstance(sender, dict):
                return "Error: sender (dict with 'name' and 'email' keys) is required for create operation"
            if not html_content:
                return "Error: html_content is required for create operation"
            if not recipients or not isinstance(recipients, dict):
                return "Error: recipients (dict with 'list_ids' key) is required for create operation"
                
            # Prepare campaign object
            email_campaign = brevo_python.CreateEmailCampaign(
                name=name,
                subject=subject,
                sender=sender,
                html_content=html_content,
                recipients=recipients
            )
            
            if scheduled_at:
                email_campaign.scheduled_at = scheduled_at
                
            api_response = api_instance.create_email_campaign(email_campaign)
            return f"Campaign created successfully with ID: {api_response.id}"
            
        elif operation == "update":
            if not campaign_id:
                return "Error: campaign_id is required for update operation"
                
            # Prepare update object
            update_campaign = brevo_python.UpdateEmailCampaign()
            if name:
                update_campaign.name = name
            if subject:
                update_campaign.subject = subject
            if html_content:
                update_campaign.html_content = html_content
            if recipients:
                update_campaign.recipients = recipients
            if scheduled_at:
                update_campaign.scheduled_at = scheduled_at
                
            api_instance.update_email_campaign(campaign_id, update_campaign)
            return f"Campaign with ID {campaign_id} updated successfully."
            
        elif operation == "schedule":
            if not campaign_id:
                return "Error: campaign_id is required for schedule operation"
            if not scheduled_at:
                return "Error: scheduled_at is required for schedule operation"
                
            schedule_data = brevo_python.UpdateCampaignStatus(status="schedule")
            api_instance.update_campaign_status(campaign_id, schedule_data)
            
            update_campaign = brevo_python.UpdateEmailCampaign(scheduled_at=scheduled_at)
            api_instance.update_email_campaign(campaign_id, update_campaign)
            
            return f"Campaign with ID {campaign_id} scheduled for {scheduled_at}."
            
        elif operation == "test":
            if not campaign_id:
                return "Error: campaign_id is required for test operation"
            if not test_emails or not isinstance(test_emails, list) or len(test_emails) == 0:
                return "Error: test_emails list is required for test operation"
                
            send_test = brevo_python.SendTestEmail(email_to=test_emails)
            api_instance.send_test_email(campaign_id, send_test)
            return f"Test email sent for campaign with ID {campaign_id} to {', '.join(test_emails)}."
            
        elif operation == "status":
            if not campaign_id:
                return "Error: campaign_id is required for status operation"
            if not status:
                return "Error: status is required for status operation"
                
            # Validate status
            valid_statuses = ["suspended", "archive", "draft", "sent", "schedule", "replicate"]
            if status not in valid_statuses:
                return f"Error: Invalid status '{status}'. Valid values are: {', '.join(valid_statuses)}"
                
            status_data = brevo_python.UpdateCampaignStatus(status=status)
            api_instance.update_campaign_status(campaign_id, status_data)
            return f"Campaign with ID {campaign_id} status changed to {status}."
            
        else:
            return f"Error: Unknown operation '{operation}'. Supported operations: list, get, create, update, schedule, test, status"
    
    except ApiException as e:
        return f"Error performing {operation} operation on campaign: {e}"
