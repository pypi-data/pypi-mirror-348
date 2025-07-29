"""
Tools for managing account information in Brevo.
"""
import brevo_python
from brevo_python.rest import ApiException
from ..utils import get_account_api

async def get_account_info() -> str:
    """Get account information and details from Brevo."""
    try:
        api_instance = get_account_api()
        api_response = api_instance.get_account()
        
        details = ""
        if hasattr(api_response, 'first_name'):
            details += f"First name: {api_response.first_name}\n"
        if hasattr(api_response, 'last_name'):
            details += f"Last name: {api_response.last_name}\n"
        if hasattr(api_response, 'email'):
            details += f"Email: {api_response.email}\n"
        if hasattr(api_response, 'company'):
            details += f"Company: {api_response.company}\n"
        if hasattr(api_response, 'plan') and api_response.plan:
            plan_info = "Unknown"
            if len(api_response.plan) > 0:
                plan_obj = api_response.plan[0]
                if hasattr(plan_obj, 'name'):
                    plan_info = plan_obj.name
                elif hasattr(plan_obj, 'type'):
                    plan_info = plan_obj.type
            details += f"Plan: {plan_info}\n"
        
        if hasattr(api_response, 'marketing_automation') and api_response.marketing_automation:
            details += "\nMarketing Automation:\n"
            if hasattr(api_response.marketing_automation, 'credits'):
                details += f"  Credits: {api_response.marketing_automation.credits}\n"
            if hasattr(api_response.marketing_automation, 'remaining_credits'):
                details += f"  Remaining credits: {api_response.marketing_automation.remaining_credits}\n"
        
        if hasattr(api_response, 'email') and api_response.email:
            details += "\nEmail Credits:\n"
            if hasattr(api_response.email, 'credits'):
                details += f"  Credits: {api_response.email.credits}\n"
            if hasattr(api_response.email, 'remaining_credits'):
                details += f"  Remaining credits: {api_response.email.remaining_credits}\n"
            
        return details
    except ApiException as e:
        return f"Error retrieving account info: {e}"
