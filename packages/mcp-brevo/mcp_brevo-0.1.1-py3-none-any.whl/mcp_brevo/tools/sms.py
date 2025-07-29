"""
Tools for SMS messaging in Brevo.
"""
from typing import Optional, Dict
import brevo_python
from brevo_python.rest import ApiException

async def manage_sms(operation: str, campaign_id: Optional[int] = None,
                    to_number: Optional[str] = None, content: Optional[str] = None,
                    sender: Optional[str] = None, name: Optional[str] = None,
                    recipients: Optional[dict] = None, scheduled_at: Optional[str] = None,
                    limit: int = 50, offset: int = 0) -> str:
    """
    Perform operations related to SMS messaging and campaigns.
    
    Args:
        operation: One of "send", "list_campaigns", "get_campaign", "create_campaign"
        campaign_id: Required for get_campaign
        to_number: Required for send operation
        content: Required for send and create_campaign operations
        sender: Required for send and create_campaign operations
        name: Required for create_campaign operation
        recipients: Required for create_campaign operation
        scheduled_at: Optional for send and create_campaign operations
        limit: Used only for list_campaigns operation
        offset: Used only for list_campaigns operation
    """
    try:
        # Different operations use different API instances
        if operation == "send":
            if not to_number:
                return "Error: to_number is required for send operation"
            if not content:
                return "Error: content is required for send operation"
                
            # Prepare SMS object
            transac_sms_api = brevo_python.TransactionalSMSApi(brevo_python.ApiClient(brevo_python.Configuration()))
            send_sms = brevo_python.SendTransacSms(
                to=to_number,
                content=content,
                sender=sender
            )
            
            api_response = transac_sms_api.send_transac_sms(send_sms)
            return f"SMS sent successfully with message ID: {api_response.message_id}"
            
        elif operation == "list_campaigns":
            # Fetch SMS campaigns list
            sms_campaigns_api = brevo_python.SMSCampaignsApi(brevo_python.ApiClient(brevo_python.Configuration()))
            api_response = sms_campaigns_api.get_sms_campaigns(limit=limit, offset=offset)
            
            if not hasattr(api_response, 'campaigns') or not api_response.campaigns:
                return "No SMS campaigns found."
                
            campaign_details = []
            for campaign in api_response.campaigns:
                details = ""
                if hasattr(campaign, 'id'):
                    details += f"ID: {campaign.id}\n"
                if hasattr(campaign, 'name'):
                    details += f"Name: {campaign.name}\n"
                if hasattr(campaign, 'status'):
                    details += f"Status: {campaign.status}\n"
                if hasattr(campaign, 'content'):
                    details += f"Content preview: {campaign.content[:50]}...\n"
                if hasattr(campaign, 'scheduled_at') and campaign.scheduled_at:
                    details += f"Scheduled at: {campaign.scheduled_at}\n"
                if hasattr(campaign, 'created_at'):
                    details += f"Created at: {campaign.created_at}\n"
                    
                campaign_details.append(details)
                
            # Get total campaign count
            total_count = "Unknown"
            if hasattr(api_response, 'count'):
                total_count = api_response.count
                
            return f"Total SMS campaigns: {total_count}\n\n" + "\n---\n".join(campaign_details)
            
        elif operation == "get_campaign":
            if not campaign_id:
                return "Error: campaign_id is required for get_campaign operation"
                
            # Get specific SMS campaign
            sms_campaigns_api = brevo_python.SMSCampaignsApi(brevo_python.ApiClient(brevo_python.Configuration()))
            api_response = sms_campaigns_api.get_sms_campaign(campaign_id)
            
            details = ""
            if hasattr(api_response, 'id'):
                details += f"ID: {api_response.id}\n"
            if hasattr(api_response, 'name'):
                details += f"Name: {api_response.name}\n"
            if hasattr(api_response, 'status'):
                details += f"Status: {api_response.status}\n"
            if hasattr(api_response, 'content'):
                details += f"Content: {api_response.content}\n"
            if hasattr(api_response, 'sender'):
                details += f"Sender: {api_response.sender}\n"
            if hasattr(api_response, 'created_at'):
                details += f"Created at: {api_response.created_at}\n"
            if hasattr(api_response, 'scheduled_at') and api_response.scheduled_at:
                details += f"Scheduled at: {api_response.scheduled_at}\n"
                
            # Get statistics if available
            if hasattr(api_response, 'statistics') and api_response.statistics:
                stats = api_response.statistics
                details += "\nStatistics:\n"
                if hasattr(stats, 'delivered'):
                    details += f"  Delivered: {stats.delivered}\n"
                if hasattr(stats, 'sent'):
                    details += f"  Sent: {stats.sent}\n"
                if hasattr(stats, 'processed'):
                    details += f"  Processed: {stats.processed}\n"
                if hasattr(stats, 'soft_bounces'):
                    details += f"  Soft bounces: {stats.soft_bounces}\n"
                if hasattr(stats, 'hard_bounces'):
                    details += f"  Hard bounces: {stats.hard_bounces}\n"
                if hasattr(stats, 'unsubscriptions'):
                    details += f"  Unsubscriptions: {stats.unsubscriptions}\n"
                    
            return details
            
        elif operation == "create_campaign":
            # Validate required parameters
            if not name:
                return "Error: name is required for create_campaign operation"
            if not content:
                return "Error: content is required for create_campaign operation"
            if not sender:
                return "Error: sender is required for create_campaign operation"
            if not recipients or not isinstance(recipients, dict):
                return "Error: recipients (dict with 'list_ids' key) is required for create_campaign operation"
                
            # Create SMS campaign
            sms_campaigns_api = brevo_python.SMSCampaignsApi(brevo_python.ApiClient(brevo_python.Configuration()))
            create_campaign = brevo_python.CreateSmsCampaign(
                name=name,
                sender=sender,
                content=content,
                recipients=recipients
            )
            
            if scheduled_at:
                create_campaign.scheduled_at = scheduled_at
                
            api_response = sms_campaigns_api.create_sms_campaign(create_campaign)
            return f"SMS campaign created successfully with ID: {api_response.id}"
            
        else:
            return f"Error: Unknown operation '{operation}'. Supported operations: send, list_campaigns, get_campaign, create_campaign"
    
    except ApiException as e:
        return f"Error performing {operation} operation on SMS: {e}"
