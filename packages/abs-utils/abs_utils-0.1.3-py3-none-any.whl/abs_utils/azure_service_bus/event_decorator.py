from functools import wraps
from fastapi import Request
from typing import Any, Callable
from .azure_service_bus import AzureServiceBus
from uuid import uuid4
import json

def azure_event_decorator(event_type: str):
    """
    A decorator that sends a message to Azure Service Bus after the function execution.
    
    Args:
        event_name (str): The name of the event to be sent
    
    Returns:
        Callable: The decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Extract required parameters from kwargs
            entity_name:str = kwargs.get('entity_name')
            entity_id:str = kwargs.get('entity_id') or None
            request:Request = kwargs.get('request')
            data:Any = kwargs.get('data')
            azure_service_bus:AzureServiceBus = kwargs.get('azure_service_bus')
            payload_id:str = kwargs.get('id') or None
            
            # Execute the original function
            result = await func(*args, **kwargs)
            
            event_payload = {
                "event_id": str(uuid4()),
                "event_key": event_type,
                "entity_name": entity_name,
                "entity_id": entity_id,
                "payload": data,
                "payload_id": payload_id,
                "user": {
                    "id": request.state.user.id,
                    "uuid": request.state.user.uuid,
                    "email": request.state.user.email,
                    "name": request.state.user.name,
                },
            }
            # Send message to Azure Service Bus
            event_payload = json.dumps(event_payload)
            await azure_service_bus.send(event_payload)
            return result
        return wrapper
    return decorator
