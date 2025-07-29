"""
Adapter utilities for Fluidgrids nodes
"""

import os
import json
import logging
import httpx
from typing import Dict, Any, Optional, Union

# Configure logging
log = logging.getLogger(os.getenv("OTEL_SERVICE_NAME", "fluidgrids"))

class AdapterError(Exception):
    """Exception raised for adapter-related errors."""
    pass

async def execute_adapter_operation(
    adapter_name: str,
    operation: str,
    parameters: Dict[str, Any],
    credentials: Optional[Dict[str, Any]] = None,
    timeout: float = 30.0
) -> Dict[str, Any]:
    """
    Execute an operation on an adapter.
    
    Args:
        adapter_name: Name of the adapter
        operation: Operation to execute
        parameters: Operation parameters
        credentials: Optional credentials for the adapter
        timeout: Request timeout in seconds
        
    Returns:
        Operation result
        
    Raises:
        AdapterError: If the operation fails
    """
    # Check for mocking mode
    if os.getenv("ADAPTER_MOCKING_ENABLED", "false").lower() == "true":
        return _mock_adapter_response(adapter_name, operation, parameters)
    
    adapter_url = _get_adapter_url(adapter_name)
    
    if not adapter_url:
        raise AdapterError(f"No URL found for adapter '{adapter_name}'")
        
    # Construct request payload
    payload = {
        "operation": operation,
        "parameters": parameters
    }
    
    # Add credentials if provided
    if credentials:
        payload["credentials"] = credentials
        
    try:
        log.info(f"Executing {operation} on adapter {adapter_name}")
        log.debug(f"Adapter URL: {adapter_url}")
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{adapter_url}/api/v1/execute",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                log.error(f"Adapter request failed with status {response.status_code}: {response.text}")
                raise AdapterError(f"Adapter request failed with status {response.status_code}: {response.text}")
                
            result = response.json()
            return result
            
    except httpx.TimeoutException:
        log.error(f"Request to adapter {adapter_name} timed out after {timeout}s")
        raise AdapterError(f"Request to adapter {adapter_name} timed out")
        
    except httpx.RequestError as e:
        log.error(f"Request to adapter {adapter_name} failed: {e}")
        raise AdapterError(f"Request to adapter {adapter_name} failed: {e}")
        
    except Exception as e:
        log.exception(f"Unexpected error calling adapter {adapter_name}: {e}")
        raise AdapterError(f"Unexpected error calling adapter {adapter_name}: {e}")

def _get_adapter_url(adapter_name: str) -> Optional[str]:
    """
    Get URL for an adapter.
    
    Args:
        adapter_name: Name of the adapter
        
    Returns:
        Adapter URL or None if not found
    """
    # Check direct environment variable first
    direct_url = os.getenv(f"ADAPTER_{adapter_name.upper()}_URL")
    if direct_url:
        return direct_url
        
    # Check for registry environment variable
    registry_env = os.getenv("ADAPTER_REGISTRY")
    if registry_env:
        try:
            registry = json.loads(registry_env)
            if adapter_name in registry:
                return registry[adapter_name]
        except json.JSONDecodeError:
            log.error(f"Failed to parse ADAPTER_REGISTRY environment variable: {registry_env}")
            
    # Check for a default adapter URL format
    host = os.getenv("ADAPTER_HOST", "adapter")
    port = os.getenv("ADAPTER_PORT", "8000")
    return f"http://{adapter_name}-{host}:{port}"

def _mock_adapter_response(
    adapter_name: str,
    operation: str,
    parameters: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate a mock response for an adapter operation.
    
    Args:
        adapter_name: Name of the adapter
        operation: Operation to execute
        parameters: Operation parameters
        
    Returns:
        Mock response
    """
    log.warning(f"Using MOCK for adapter {adapter_name}.{operation}")
    
    # Check for mock data file
    mock_dir = os.getenv("ADAPTER_MOCK_DIR", "./adapter_mocks")
    mock_file = f"{mock_dir}/{adapter_name}/{operation}.json"
    
    if os.path.exists(mock_file):
        try:
            with open(mock_file, 'r') as f:
                mock_data = json.load(f)
            log.info(f"Loaded mock response from {mock_file}")
            return mock_data
        except Exception as e:
            log.error(f"Failed to load mock data from {mock_file}: {e}")
    
    # Return a generic mock response
    return {
        "status": "success",
        "data": {
            "message": "This is a mock response",
            "adapter": adapter_name,
            "operation": operation,
            "parameters": parameters
        }
    } 