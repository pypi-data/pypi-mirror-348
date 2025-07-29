"""
Tools for managing contact lists in Brevo.
"""
from typing import Optional, List
import brevo_python
from brevo_python.rest import ApiException
from ..utils import get_contact_api

async def manage_list(operation: str, list_id: Optional[int] = None, 
                     name: Optional[str] = None, folder_id: Optional[int] = None,
                     emails: Optional[List[str]] = None, limit: int = 50, offset: int = 0) -> str:
    """
    Perform CRUD operations on contact lists.
    
    Args:
        operation: One of "list", "get", "create", "update", "delete", "add_contacts", "remove_contacts"
        list_id: Required for all operations except list and create
        name: Required for create, optional for update
        folder_id: Optional for create and update
        emails: Required for add_contacts and remove_contacts
        limit: Used only for list operation
        offset: Used only for list operation
    """
    try:
        api_instance = get_contact_api()
        
        if operation == "list":
            api_response = api_instance.get_lists(limit=limit, offset=offset)
            
            if not api_response.lists:
                return "No lists found."
                
            list_details = []
            for contact_list in api_response.lists:
                details = ""
                # Handle both object attributes and dictionary keys
                if isinstance(contact_list, dict):
                    # Handle as dictionary
                    list_id = contact_list.get('id', 'Unknown')
                    list_name = contact_list.get('name', 'Unknown')
                    list_subscribers = contact_list.get('total_subscribers', 'Unknown')
                    list_created = contact_list.get('created_at', 'Unknown')
                    
                    details += f"ID: {list_id}\n"
                    details += f"Name: {list_name}\n"
                    details += f"Total subscribers: {list_subscribers}\n"
                    details += f"Created at: {list_created}\n"
                else:
                    # Handle as object with attributes
                    if hasattr(contact_list, 'id'):
                        details += f"ID: {contact_list.id}\n"
                    if hasattr(contact_list, 'name'):
                        details += f"Name: {contact_list.name}\n"
                    if hasattr(contact_list, 'total_subscribers'):
                        details += f"Total subscribers: {contact_list.total_subscribers}\n"
                    if hasattr(contact_list, 'created_at'):
                        details += f"Created at: {contact_list.created_at}\n"
                
                list_details.append(details)
            
            # Get total list count safely
            total_count = "Unknown"
            if hasattr(api_response, 'count'):
                total_count = api_response.count
            elif isinstance(api_response, dict) and 'count' in api_response:
                total_count = api_response['count']
                
            return f"Total lists: {total_count}\n\n" + "\n---\n".join(list_details)
            
        elif operation == "get":
            if not list_id:
                return "Error: list_id is required for get operation"
                
            api_response = api_instance.get_list(list_id)
            
            details = ""
            if hasattr(api_response, 'id'):
                details += f"ID: {api_response.id}\n"
            if hasattr(api_response, 'name'):
                details += f"Name: {api_response.name}\n"
            if hasattr(api_response, 'total_subscribers'):
                details += f"Total subscribers: {api_response.total_subscribers}\n"
            if hasattr(api_response, 'created_at'):
                details += f"Created at: {api_response.created_at}\n"
            if hasattr(api_response, 'folder_id'):
                details += f"Folder ID: {api_response.folder_id}\n"
                
            return details
            
        elif operation == "create":
            if not name:
                return "Error: name is required for create operation"
                
            create_list = brevo_python.CreateList(
                name=name,
                folder_id=folder_id
            )
            api_response = api_instance.create_list(create_list)
            return f"List created successfully with ID: {api_response.id}"
            
        elif operation == "update":
            if not list_id:
                return "Error: list_id is required for update operation"
            if not name:
                return "Error: name is required for update operation"
                
            update_list = brevo_python.UpdateList(
                name=name,
                folder_id=folder_id
            )
            api_instance.update_list(list_id, update_list)
            return f"List with ID {list_id} updated successfully."
            
        elif operation == "delete":
            if not list_id:
                return "Error: list_id is required for delete operation"
                
            api_instance.delete_list(list_id)
            return f"List with ID {list_id} deleted successfully."
            
        elif operation == "add_contacts":
            if not list_id:
                return "Error: list_id is required for add_contacts operation"
            if not emails or not isinstance(emails, list) or len(emails) == 0:
                return "Error: emails list is required for add_contacts operation"
                
            add_contacts = brevo_python.AddContactToList(emails=emails)
            api_instance.add_contacts_to_list(list_id, add_contacts)
            return f"Successfully added {len(emails)} contact(s) to list with ID {list_id}."
            
        elif operation == "remove_contacts":
            if not list_id:
                return "Error: list_id is required for remove_contacts operation"
            if not emails or not isinstance(emails, list) or len(emails) == 0:
                return "Error: emails list is required for remove_contacts operation"
                
            remove_contacts = brevo_python.RemoveContactFromList(emails=emails)
            api_instance.remove_contact_from_list(list_id, remove_contacts)
            return f"Successfully removed {len(emails)} contact(s) from list with ID {list_id}."
            
        else:
            return f"Error: Unknown operation '{operation}'. Supported operations: list, get, create, update, delete, add_contacts, remove_contacts"
    
    except ApiException as e:
        return f"Error performing {operation} operation on list: {e}"
