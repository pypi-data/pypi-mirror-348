"""
Tools for analytics and reporting in Brevo.
"""
from typing import Optional, List
import brevo_python
from brevo_python.rest import ApiException
from ..utils import get_campaign_api, get_transactional_email_api

async def get_analytics(report_type: str, campaign_id: Optional[int] = None,
                       start_date: Optional[str] = None, end_date: Optional[str] = None,
                       email: Optional[str] = None, channel: str = "email",
                       limit: int = 50, offset: int = 0) -> str:
    """
    Retrieve various analytics reports.
    
    Args:
        report_type: One of "campaign_stats", "aggregate", "events"
        campaign_id: Required for campaign_stats
        start_date: Required for aggregate and events reports (YYYY-MM-DD format)
        end_date: Required for aggregate and events reports (YYYY-MM-DD format)
        email: Optional filter for events report
        channel: Optional channel type for aggregate report ("email" or "sms")
        limit: Used for pagination in events report
        offset: Used for pagination in events report
    """
    try:
        if report_type == "campaign_stats":
            if not campaign_id:
                return "Error: campaign_id is required for campaign_stats report"
                
            # Get campaign statistics
            api_instance = get_campaign_api()
            api_response = api_instance.get_email_campaign(campaign_id)
            
            if not hasattr(api_response, 'statistics') or not api_response.statistics:
                return f"No statistics available for campaign with ID {campaign_id}."
                
            stats = api_response.statistics
            details = f"Campaign Statistics (ID: {campaign_id}):\n"
            
            if hasattr(stats, 'sent') and stats.sent is not None:
                details += f"Sent: {stats.sent}\n"
            if hasattr(stats, 'delivered') and stats.delivered is not None:
                details += f"Delivered: {stats.delivered}\n"
            if hasattr(stats, 'opens') and stats.opens is not None:
                details += f"Opens: {stats.opens}\n"
            if hasattr(stats, 'unique_opens') and stats.unique_opens is not None:
                details += f"Unique opens: {stats.unique_opens}\n"
            if hasattr(stats, 'clicks') and stats.clicks is not None:
                details += f"Clicks: {stats.clicks}\n"
            if hasattr(stats, 'unique_clicks') and stats.unique_clicks is not None:
                details += f"Unique clicks: {stats.unique_clicks}\n"
            if hasattr(stats, 'unsubscriptions') and stats.unsubscriptions is not None:
                details += f"Unsubscriptions: {stats.unsubscriptions}\n"
            if hasattr(stats, 'complaints') and stats.complaints is not None:
                details += f"Complaints: {stats.complaints}\n"
            if hasattr(stats, 'hard_bounces') and stats.hard_bounces is not None:
                details += f"Hard bounces: {stats.hard_bounces}\n"
            if hasattr(stats, 'soft_bounces') and stats.soft_bounces is not None:
                details += f"Soft bounces: {stats.soft_bounces}\n"
                
            # Calculate rates if possible
            if hasattr(stats, 'delivered') and stats.delivered and hasattr(stats, 'opens'):
                open_rate = (stats.opens / stats.delivered) * 100 if stats.delivered > 0 else 0
                details += f"Open rate: {open_rate:.2f}%\n"
                
            if hasattr(stats, 'opens') and stats.opens and hasattr(stats, 'clicks'):
                click_through_rate = (stats.clicks / stats.opens) * 100 if stats.opens > 0 else 0
                details += f"Click-through rate: {click_through_rate:.2f}%\n"
                
            return details
            
        elif report_type == "aggregate":
            if not start_date or not end_date:
                return "Error: start_date and end_date are required for aggregate report"
                
            # Convert dates to appropriate format if not already
            if len(start_date) == 10:  # YYYY-MM-DD format
                start_date += "T00:00:00+00:00"
            if len(end_date) == 10:  # YYYY-MM-DD format
                end_date += "T23:59:59+00:00"
                
            # Use the TransactionalEmailsApi for aggregate reports
            api_instance = get_transactional_email_api()
            
            # Validate channel
            if channel not in ["email", "sms"]:
                return f"Error: Invalid channel '{channel}'. Valid values are: email, sms"
                
            # Get appropriate report based on channel
            if channel == "email":
                # Use get_email_event_report to collect aggregate data
                api_response = api_instance.get_email_event_report(
                    start_date=start_date, 
                    end_date=end_date,
                    limit=1000,  # Get a large number of events for aggregation
                    offset=0
                )
                
                # Aggregate results manually
                aggregate_data = {
                    'sent': 0,
                    'delivered': 0,
                    'opens': 0,
                    'clicks': 0,
                    'bounces': 0,
                    'soft_bounces': 0,
                    'hard_bounces': 0,
                    'unsubscribed': 0,
                    'complaints': 0
                }
                
                # Count events by type
                if hasattr(api_response, 'events') and api_response.events:
                    for event in api_response.events:
                        if not hasattr(event, 'event'):
                            continue
                            
                        event_type = event.event
                        if event_type == 'sent':
                            aggregate_data['sent'] += 1
                        elif event_type == 'delivered':
                            aggregate_data['delivered'] += 1
                        elif event_type == 'opened':
                            aggregate_data['opens'] += 1
                        elif event_type == 'clicked':
                            aggregate_data['clicks'] += 1
                        elif event_type == 'softBounce':
                            aggregate_data['soft_bounces'] += 1
                            aggregate_data['bounces'] += 1
                        elif event_type == 'hardBounce':
                            aggregate_data['hard_bounces'] += 1
                            aggregate_data['bounces'] += 1
                        elif event_type == 'unsubscribed':
                            aggregate_data['unsubscribed'] += 1
                        elif event_type == 'complaint':
                            aggregate_data['complaints'] += 1
                
                details = f"Aggregate Email Report ({start_date} to {end_date}):\n\n"
                details += f"Total emails sent: {aggregate_data['sent']}\n"
                details += f"Delivered: {aggregate_data['delivered']}\n"
                details += f"Opens: {aggregate_data['opens']}\n"
                details += f"Clicks: {aggregate_data['clicks']}\n"
                details += f"Bounces: {aggregate_data['bounces']}\n"
                details += f"  Soft bounces: {aggregate_data['soft_bounces']}\n"
                details += f"  Hard bounces: {aggregate_data['hard_bounces']}\n"
                details += f"Unsubscribed: {aggregate_data['unsubscribed']}\n"
                details += f"Complaints: {aggregate_data['complaints']}\n"
                
                # Calculate rates if possible
                if aggregate_data['delivered'] > 0:
                    open_rate = (aggregate_data['opens'] / aggregate_data['delivered']) * 100
                    details += f"\nOpen rate: {open_rate:.2f}%\n"
                
                if aggregate_data['opens'] > 0:
                    click_rate = (aggregate_data['clicks'] / aggregate_data['opens']) * 100
                    details += f"Click-to-open rate: {click_rate:.2f}%\n"
                
                if aggregate_data['sent'] > 0:
                    delivery_rate = (aggregate_data['delivered'] / aggregate_data['sent']) * 100
                    bounce_rate = (aggregate_data['bounces'] / aggregate_data['sent']) * 100
                    details += f"Delivery rate: {delivery_rate:.2f}%\n"
                    details += f"Bounce rate: {bounce_rate:.2f}%\n"
                    
            else:  # SMS
                # For SMS, we would need similar API for SMS events
                # This is a placeholder for SMS aggregate reports
                details = f"SMS aggregate reports are not currently available through this API."
                    
            return details
            
        elif report_type == "events":
            if not start_date or not end_date:
                return "Error: start_date and end_date are required for events report"
                
            # Convert dates to appropriate format if not already
            if len(start_date) == 10:  # YYYY-MM-DD format
                start_date += "T00:00:00+00:00"
            if len(end_date) == 10:  # YYYY-MM-DD format
                end_date += "T23:59:59+00:00"
                
            # Get email events
            api_instance = get_transactional_email_api()
            
            # Set up events filter
            events = None
            message_id = None
            
            api_response = api_instance.get_email_event_report(
                limit=limit, 
                offset=offset, 
                start_date=start_date, 
                end_date=end_date, 
                email=email,
                event=events,
                message_id=message_id
            )
            
            if not hasattr(api_response, 'events') or not api_response.events:
                return f"No email events found for the specified period" + (f" and email {email}" if email else "") + "."
                
            event_details = []
            for event in api_response.events:
                details = ""
                if hasattr(event, 'email'):
                    details += f"Email: {event.email}\n"
                if hasattr(event, 'date'):
                    details += f"Date: {event.date}\n"
                if hasattr(event, 'subject'):
                    details += f"Subject: {event.subject}\n"
                if hasattr(event, 'message_id'):
                    details += f"Message ID: {event.message_id}\n"
                if hasattr(event, 'event'):
                    details += f"Event: {event.event}\n"
                if hasattr(event, 'reason'):
                    details += f"Reason: {event.reason}\n"
                if hasattr(event, 'tag'):
                    details += f"Tag: {event.tag}\n"
                    
                event_details.append(details)
                
            # Check for pagination information
            has_more = False
            if hasattr(api_response, 'events') and len(api_response.events) >= limit:
                has_more = True
                
            result = f"Email Events Report ({start_date} to {end_date}"
            if email:
                result += f" for {email}"
            result += f"):\n\n" + "\n---\n".join(event_details)
            
            if has_more:
                result += f"\n\nMore events available. Use offset={offset + limit} to see next page."
                
            return result
            
        else:
            return f"Error: Unknown report_type '{report_type}'. Supported types: campaign_stats, aggregate, events"
    
    except ApiException as e:
        return f"Error retrieving {report_type} report: {e}"
