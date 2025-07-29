"""
Tools for managing email templates in Brevo.
"""
from typing import Optional
import brevo_python
from brevo_python.rest import ApiException
from ..utils import get_smtp_api

async def manage_template(operation: str, template_id: Optional[int] = None,
                         name: Optional[str] = None, html_content: Optional[str] = None,
                         subject: Optional[str] = None, is_active: Optional[bool] = None,
                         limit: int = 50, offset: int = 0) -> str:
    """
    Perform CRUD operations on email templates.
    
    Args:
        operation: One of "list", "get", "create", "update", "delete"
        template_id: Required for get, update, delete operations
        name: Required for create, optional for update
        html_content: Required for create, optional for update
        subject: Optional for create and update
        is_active: Optional for create and update
        limit: Used only for list operation
        offset: Used only for list operation
    """
    try:
        api_instance = get_smtp_api()
        
        if operation == "list":
            api_response = api_instance.get_smtp_templates(limit=limit, offset=offset)
            
            if not api_response.templates:
                return "No templates found."
                
            template_details = []
            for template in api_response.templates:
                details = ""
                # Handle both object attributes and dictionary keys
                if isinstance(template, dict):
                    # Handle as dictionary
                    template_id = template.get('id', 'Unknown')
                    template_name = template.get('name', 'Unknown')
                    template_subject = template.get('subject', 'Unknown')
                    template_status = "Active" if template.get('is_active', False) else "Inactive"
                    template_created = template.get('created_at', 'Unknown')
                    
                    details += f"ID: {template_id}\n"
                    details += f"Name: {template_name}\n"
                    details += f"Subject: {template_subject}\n"
                    details += f"Status: {template_status}\n"
                    details += f"Created at: {template_created}\n"
                else:
                    # Handle as object with attributes
                    if hasattr(template, 'id'):
                        details += f"ID: {template.id}\n"
                    if hasattr(template, 'name'):
                        details += f"Name: {template.name}\n"
                    if hasattr(template, 'subject'):
                        details += f"Subject: {template.subject}\n"
                    if hasattr(template, 'is_active'):
                        details += f"Status: {'Active' if template.is_active else 'Inactive'}\n"
                    if hasattr(template, 'created_at'):
                        details += f"Created at: {template.created_at}\n"
                
                template_details.append(details)
            
            # Get total template count safely
            total_count = "Unknown"
            if hasattr(api_response, 'count'):
                total_count = api_response.count
            elif isinstance(api_response, dict) and 'count' in api_response:
                total_count = api_response['count']
                
            return f"Total templates: {total_count}\n\n" + "\n---\n".join(template_details)
            
        elif operation == "get":
            if not template_id:
                return "Error: template_id is required for get operation"
                
            api_response = api_instance.get_smtp_template(template_id)
            
            details = ""
            if hasattr(api_response, 'id'):
                details += f"ID: {api_response.id}\n"
            if hasattr(api_response, 'name'):
                details += f"Name: {api_response.name}\n"
            if hasattr(api_response, 'subject'):
                details += f"Subject: {api_response.subject}\n"
            if hasattr(api_response, 'is_active'):
                details += f"Status: {'Active' if api_response.is_active else 'Inactive'}\n"
            if hasattr(api_response, 'created_at'):
                details += f"Created at: {api_response.created_at}\n"
            if hasattr(api_response, 'modified_at'):
                details += f"Modified at: {api_response.modified_at}\n"
            if hasattr(api_response, 'html_content'):
                details += f"\nHTML Preview (first 200 chars):\n{api_response.html_content[:200]}...\n"
                
            return details
            
        elif operation == "create":
            if not name:
                return "Error: name is required for create operation"
            if not html_content:
                return "Error: html_content is required for create operation"
                
            # Prepare template object
            smtp_template = brevo_python.CreateSmtpTemplate(
                name=name,
                html_content=html_content,
                subject=subject,
                is_active=is_active
            )
            
            api_response = api_instance.create_smtp_template(smtp_template)
            return f"Template created successfully with ID: {api_response.id}"
            
        elif operation == "update":
            if not template_id:
                return "Error: template_id is required for update operation"
                
            # Prepare update object
            update_template = brevo_python.UpdateSmtpTemplate()
            if name:
                update_template.name = name
            if html_content:
                update_template.html_content = html_content
            if subject is not None:
                update_template.subject = subject
            if is_active is not None:
                update_template.is_active = is_active
                
            api_instance.update_smtp_template(template_id, update_template)
            return f"Template with ID {template_id} updated successfully."
            
        elif operation == "delete":
            if not template_id:
                return "Error: template_id is required for delete operation"
                
            api_instance.delete_smtp_template(template_id)
            return f"Template with ID {template_id} deleted successfully."
            
        else:
            return f"Error: Unknown operation '{operation}'. Supported operations: list, get, create, update, delete"
    
    except ApiException as e:
        return f"Error performing {operation} operation on template: {e}"
