"""
Tools for sending and tracking transactional emails in Brevo.
"""
from typing import Optional, List
import brevo_python
from brevo_python.rest import ApiException
from datetime import datetime, timedelta
import base64
import os
from urllib.parse import urlparse

# Try to import requests, but don't fail if it's not available
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
from ..utils import get_transactional_email_api

async def send_email(to_email: str, subject: str, html_content: str, 
                   from_email: Optional[str] = None, from_name: Optional[str] = None,
                   reply_to: Optional[str] = None, to_name: Optional[str] = None,
                   cc: Optional[List[str]] = None, bcc: Optional[List[str]] = None,
                   attachment_urls: Optional[List[str]] = None, 
                   track_opens: bool = True, track_clicks: bool = True,
                   tags: Optional[List[str]] = None) -> str:
    """
    Send a transactional email using Brevo's API.
    
    Args:
        to_email: Recipient email address
        subject: Email subject line
        html_content: HTML content of the email
        from_email: Sender email address (optional, uses default if not provided)
        from_name: Sender name (optional)
        reply_to: Reply-to email address (optional)
        to_name: Recipient name (optional)
        cc: List of CC recipients (optional)
        bcc: List of BCC recipients (optional)
        attachment_urls: List of URLs to files to attach (optional)
        track_opens: Enable open tracking (default: True)
        track_clicks: Enable click tracking (default: True)
        tags: List of tags for categorizing and filtering emails (optional)
    """
    try:
        api_instance = get_transactional_email_api()
        
        # Create email sender
        sender = {
            "email": from_email,
            "name": from_name
        }
        
        # Create email recipients
        to = [{"email": to_email}]
        if to_name:
            to[0]["name"] = to_name
            
        # Process CC and BCC if provided
        cc_list = None
        if cc and len(cc) > 0:
            cc_list = [{"email": email} for email in cc]
            
        bcc_list = None
        if bcc and len(bcc) > 0:
            bcc_list = [{"email": email} for email in bcc]
            
        # Process attachments if provided
        attachments = None
        if attachment_urls and len(attachment_urls) > 0:
            if not REQUESTS_AVAILABLE:
                return "Error: Unable to process attachments. The 'requests' library is not installed. Please install it with 'pip install requests'."
                
            attachments = []
            for url in attachment_urls:
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        # Get filename from URL
                        filename = os.path.basename(urlparse(url).path)
                        
                        # Encode content as base64
                        content = base64.b64encode(response.content).decode('utf-8')
                        
                        attachments.append({
                            "url": url,
                            "name": filename,
                            "content": content
                        })
                    else:
                        return f"Error downloading attachment from {url}: Status code {response.status_code}"
                except Exception as e:
                    return f"Error processing attachment from {url}: {str(e)}"
        
        # Build email object
        email = brevo_python.SendSmtpEmail(
            to=to,
            subject=subject,
            html_content=html_content,
            sender=sender,
            reply_to={"email": reply_to} if reply_to else None,
            cc=cc_list,
            bcc=bcc_list,
            attachment=attachments,
            tags=tags
        )
        
        # Set tracking options
        email.params = {
            "tracking": {
                "open": track_opens,
                "click": track_clicks
            }
        }
        
        # Send the email
        api_response = api_instance.send_transac_email(email)
        
        return f"Email sent successfully with message ID: {api_response.message_id}"
    
    except ApiException as e:
        return f"Error sending email: {e}"


async def track_email(message_id: Optional[str] = None, email: Optional[str] = None, 
                    days: int = 7, event_types: Optional[List[str]] = None) -> str:
    """
    Track delivery and engagement status of sent emails.
    
    Args:
        message_id: The message ID of a specific email to track (optional)
        email: Email address to track events for (optional)
        days: Number of days in the past to check (default: 7)
        event_types: List of event types to filter by (e.g., "delivered", "opened", "clicked") (optional)
    """
    try:
        # Initialize the API client
        api_instance = get_transactional_email_api()
        
        # Set up event types if provided
        events = None
        if event_types and len(event_types) > 0:
            valid_events = ["delivered", "sent", "hardBounce", "softBounce", "blocked", 
                           "spam", "invalid", "deferred", "opened", "clicked", "unsubscribed"]
            filtered_events = [e for e in event_types if e in valid_events]
            if filtered_events:
                events = filtered_events
        
        # Prepare API call parameters - completely empty by default
        kwargs = {}
        
        # Define a default limit for the number of events to fetch
        limit = 100
        
        # Only add parameters if they are explicitly provided or needed
        # Everything is truly optional, let the SDK use its defaults
        if days is not None:
            kwargs['days'] = days
            
        if message_id is not None:
            kwargs['message_id'] = message_id
            
        if email is not None:
            kwargs['email'] = email
            
        if events is not None:
            kwargs['event'] = events
            
        # Log parameters before API call
        print(f"DEBUG - API call parameters: {kwargs}")
              
        # Get email events using only the parameters that were provided
        api_response = api_instance.get_email_event_report(**kwargs)
        
        if not hasattr(api_response, 'events') or not api_response.events:
            if message_id:
                return f"No events found for message ID: {message_id} in the past {days} days."
            elif email:
                return f"No events found for email: {email} in the past {days} days."
            else:
                return f"No email events found in the past {days} days."
        
        # Process the events
        if message_id:
            # Group events by type for a specific message
            events_by_type = {}
            email_recipient = None
            email_subject = None
            
            for event in api_response.events:
                event_type = event.event if hasattr(event, 'event') else "unknown"
                if event_type not in events_by_type:
                    events_by_type[event_type] = []
                
                event_details = {}
                
                # Record the timestamp
                if hasattr(event, 'date'):
                    event_details['date'] = event.date
                
                # Record any reason (like bounce reason)
                if hasattr(event, 'reason') and event.reason:
                    event_details['reason'] = event.reason
                
                # Record email and subject if not already captured
                if not email_recipient and hasattr(event, 'email'):
                    email_recipient = event.email
                if not email_subject and hasattr(event, 'subject'):
                    email_subject = event.subject
                
                events_by_type[event_type].append(event_details)
            
            # Begin building the response
            result = f"Tracking Report for Message ID: {message_id}\n\n"
            
            if email_recipient:
                result += f"Recipient: {email_recipient}\n"
            if email_subject:
                result += f"Subject: {email_subject}\n\n"
            
            # Process event timeline for the message
            result += "Email Status Timeline:\n"
            
            # Define event priority for chronological ordering
            event_priority = {
                "sent": 1,
                "delivered": 2,
                "opened": 3, 
                "clicked": 4,
                "softBounce": 5,
                "hardBounce": 5,
                "blocked": 5,
                "spam": 6,
                "unsubscribed": 7
            }
            
            # Sort events by priority
            sorted_events = sorted(events_by_type.items(), 
                               key=lambda x: event_priority.get(x[0], 10))
            
            for event_type, events in sorted_events:
                # Map event type to user-friendly description
                event_desc = {
                    "sent": "Email was sent",
                    "delivered": "Email was delivered",
                    "opened": "Email was opened",
                    "clicked": "Email links were clicked",
                    "hardBounce": "Email hard bounced (permanent failure)",
                    "softBounce": "Email soft bounced (temporary failure)",
                    "blocked": "Email was blocked",
                    "spam": "Email was marked as spam",
                    "invalid": "Email address was invalid",
                    "deferred": "Email delivery was deferred",
                    "unsubscribed": "Recipient unsubscribed"
                }.get(event_type, event_type)
                
                # Sort events by date if available
                sorted_timestamp_events = sorted(
                    [e for e in events if 'date' in e],
                    key=lambda x: x['date']
                )
                
                if sorted_timestamp_events:
                    first_event = sorted_timestamp_events[0]
                    result += f"- {event_desc} on {first_event['date']}"
                    
                    # Add reason if available
                    if 'reason' in first_event and first_event['reason']:
                        result += f" (Reason: {first_event['reason']})"
                    
                    result += "\n"
                    
                    # For opens and clicks, show all occurrences
                    if event_type in ["opened", "clicked"] and len(sorted_timestamp_events) > 1:
                        result += f"  Additional {event_type} events:\n"
                        for i, event in enumerate(sorted_timestamp_events[1:], 1):
                            result += f"  {i}. {event['date']}\n"
                else:
                    # Events without timestamps
                    result += f"- {event_desc} (timestamp not available)\n"
            
            return result
            
        else:
            # Group events by message ID when looking at all events or events for a specific email
            events_by_message = {}
            
            for event in api_response.events:
                if not hasattr(event, 'message_id'):
                    continue
                    
                message_id = event.message_id
                if message_id not in events_by_message:
                    events_by_message[message_id] = {
                        'email': event.email if hasattr(event, 'email') else "Unknown",
                        'subject': event.subject if hasattr(event, 'subject') else "Unknown",
                        'events': {}
                    }
                
                event_type = event.event if hasattr(event, 'event') else "unknown"
                if event_type not in events_by_message[message_id]['events']:
                    events_by_message[message_id]['events'][event_type] = []
                
                event_details = {}
                if hasattr(event, 'date'):
                    event_details['date'] = event.date
                if hasattr(event, 'reason') and event.reason:
                    event_details['reason'] = event.reason
                    
                events_by_message[message_id]['events'][event_type].append(event_details)
            
            # Build summary response for multiple messages
            if email:
                result = f"Email Tracking Report for: {email} (Past {days} days)\n\n"
            else:
                result = f"Email Tracking Report (Past {days} days)\n\n"
                
            result += f"Total tracked messages: {len(events_by_message)}\n\n"
            
            # Process each message
            for msg_id, data in events_by_message.items():
                result += f"Message ID: {msg_id}\n"
                result += f"Recipient: {data['email']}\n"
                result += f"Subject: {data['subject']}\n"
                
                # Build status summary
                status = "Unknown"
                if "delivered" in data['events']:
                    status = "Delivered"
                    if "opened" in data['events']:
                        status = "Opened"
                        if "clicked" in data['events']:
                            status = "Clicked"
                elif "hardBounce" in data['events'] or "softBounce" in data['events'] or "blocked" in data['events']:
                    status = "Failed"
                elif "sent" in data['events']:
                    status = "Sent"
                    
                result += f"Status: {status}\n"
                
                # Add the most recent event time
                all_dated_events = []
                for event_list in data['events'].values():
                    for event in event_list:
                        if 'date' in event:
                            all_dated_events.append(event['date'])
                            
                if all_dated_events:
                    most_recent = max(all_dated_events)
                    result += f"Last Activity: {most_recent}\n"
                    
            if hasattr(api_response, 'events') and len(api_response.events) >= limit:                
                result += f"\nShowing first {limit} events. There may be more events available."
                
            return result
                
    except ApiException as e:
        return f"Error tracking email: {e}"
