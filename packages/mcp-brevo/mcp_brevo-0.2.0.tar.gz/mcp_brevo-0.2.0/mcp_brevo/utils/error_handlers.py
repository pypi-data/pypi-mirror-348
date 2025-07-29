"""
Common error handling utilities for Brevo API operations.
"""
from brevo_python.rest import ApiException
from typing import Callable, Any
import functools

def handle_api_error(func: Callable) -> Callable:
    """
    Decorator to handle API exceptions.
    Wraps a function and catches any ApiException, returning a formatted error message.
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ApiException as e:
            # Extract operation name from function name (e.g., 'list_contacts' -> 'list')
            operation = func.__name__.split('_')[0] if '_' in func.__name__ else 'operation'
            return f"Error performing {operation}: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"
    return wrapper

def extract_attribute(obj: Any, attribute: str, default: Any = "Unknown") -> Any:
    """
    Safely extracts an attribute from an object or a dictionary.
    
    Args:
        obj: The object or dictionary to extract from
        attribute: The attribute or key to extract
        default: The default value to return if attribute is not found
        
    Returns:
        The value of the attribute/key or the default
    """
    if isinstance(obj, dict):
        return obj.get(attribute, default)
    
    return getattr(obj, attribute, default)
