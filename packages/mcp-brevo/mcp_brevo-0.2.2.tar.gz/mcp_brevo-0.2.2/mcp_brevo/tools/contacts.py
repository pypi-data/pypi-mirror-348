"""
Tools for managing contacts in Brevo.
"""
from typing import Any, Dict, List, Optional
import brevo_python
from brevo_python.rest import ApiException
from ..utils import get_contact_api

async def manage_contact(operation: str, email: Optional[str] = None, 
                        attributes: Optional[Dict[str, Any]] = None, 
                        list_ids: Optional[List[int]] = None,
                        limit: int = 50, offset: int = 0) -> str:
    """
    Perform CRUD operations on contacts.
    
    Args:
        operation: One of "list", "get", "create", "update", "delete"
        email: Required for get, create, update, delete operations
        attributes: Optional for create and update operations
        list_ids: Optional for create and update operations
        limit: Used only for list operation
        offset: Used only for list operation
    """
    try:
        api_instance = get_contact_api()
        
        if operation == "list":
            api_response = api_instance.get_contacts(limit=limit, offset=offset)
            
            if not api_response.contacts:
                return "No contacts found."
                
            contact_details = []
            for contact in api_response.contacts:
                # Handle both object attributes and dictionary keys
                if isinstance(contact, dict):
                    # Handle as dictionary
                    contact_id = contact.get('id', 'Unknown')
                    contact_email = contact.get('email', 'Unknown')
                    details = f"ID: {contact_id}\nEmail: {contact_email}\n"
                    
                    if 'attributes' in contact and contact['attributes']:
                        details += "Attributes:\n"
                        for key, value in contact['attributes'].items():
                            details += f"  {key}: {value}\n"
                else:
                    # Handle as object with attributes
                    details = ""
                    if hasattr(contact, 'id'):
                        details += f"ID: {contact.id}\n"
                    if hasattr(contact, 'email'):
                        details += f"Email: {contact.email}\n"
                    
                    if hasattr(contact, 'attributes') and contact.attributes:
                        details += "Attributes:\n"
                        for key, value in contact.attributes.items():
                            details += f"  {key}: {value}\n"
                contact_details.append(details)
                
            # Get total contact count safely
            total_count = "Unknown"
            if hasattr(api_response, 'count'):
                total_count = api_response.count
            elif isinstance(api_response, dict) and 'count' in api_response:
                total_count = api_response['count']
                
            return f"Total contacts: {total_count}\n\n" + "\n---\n".join(contact_details)
            
        elif operation == "get":
            if not email:
                return "Error: email is required for get operation"
                
            api_response = api_instance.get_contact_info(email)
            
            details = ""
            if hasattr(api_response, 'id'):
                details += f"ID: {api_response.id}\n"
            if hasattr(api_response, 'email'):
                details += f"Email: {api_response.email}\n"
                
            if hasattr(api_response, 'attributes') and api_response.attributes:
                details += "Attributes:\n"
                for key, value in api_response.attributes.items():
                    details += f"  {key}: {value}\n"
            
            if hasattr(api_response, 'created_at'):
                details += f"Created at: {api_response.created_at}\n"
            if hasattr(api_response, 'modified_at'):
                details += f"Modified at: {api_response.modified_at}\n"
            
            if hasattr(api_response, 'list_ids') and api_response.list_ids:
                details += f"List IDs: {', '.join(str(id) for id in api_response.list_ids)}\n"
                
            return details
            
        elif operation == "create":
            if not email:
                return "Error: email is required for create operation"
                
            create_contact = brevo_python.CreateContact(
                email=email,
                attributes=attributes if attributes else {},
                list_ids=list_ids if list_ids else []
            )
            api_instance.create_contact(create_contact)
            return f"Contact {email} created successfully."
            
        elif operation == "update":
            if not email:
                return "Error: email is required for update operation"
                
            update_contact = brevo_python.UpdateContact(
                attributes=attributes if attributes else {},
                list_ids=list_ids if list_ids else None
            )
            api_instance.update_contact(email, update_contact)
            return f"Contact {email} updated successfully."
            
        elif operation == "delete":
            if not email:
                return "Error: email is required for delete operation"
                
            api_instance.delete_contact(email)
            return f"Contact {email} deleted successfully."
            
        else:
            return f"Error: Unknown operation '{operation}'. Supported operations: list, get, create, update, delete"
    
    except ApiException as e:
        return f"Error performing {operation} operation on contact: {e}"
