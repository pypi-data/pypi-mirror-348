"""
Credential management utilities for Fluidgrids nodes
"""

import os
import json
import base64
import logging
from typing import Dict, Any, Optional, Union, List

# Configure logging
log = logging.getLogger(os.getenv("OTEL_SERVICE_NAME", "fluidgrids"))

class CredentialError(Exception):
    """Exception raised for credential-related errors."""
    pass

async def get_credentials(
    credential_name: str,
    run_id: Optional[str] = None,
    node_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get credentials by name.
    
    Args:
        credential_name: Name of the credential
        run_id: Optional run ID for run-specific credentials
        node_id: Optional node ID for node-specific credentials
        
    Returns:
        Credential data
        
    Raises:
        CredentialError: If credentials cannot be retrieved
    """
    # Try to get credentials from different sources in order of preference
    
    # 1. Environment variable with exact name
    creds = _get_credentials_from_env(credential_name, run_id, node_id)
    if creds:
        return creds
        
    # 2. Environment variable with credential data JSON
    creds = _get_credentials_from_json_env()
    if creds and credential_name in creds:
        return creds[credential_name]
        
    # 3. Credential files
    creds = _get_credentials_from_files(credential_name)
    if creds:
        return creds
    
    # Nothing found
    raise CredentialError(f"Credentials '{credential_name}' not found")

def _get_credentials_from_env(
    credential_name: str,
    run_id: Optional[str] = None,
    node_id: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Get credentials from environment variables.
    
    Args:
        credential_name: Name of the credential
        run_id: Optional run ID for run-specific credentials
        node_id: Optional node ID for node-specific credentials
        
    Returns:
        Credential data or None if not found
    """
    # Try different environment variable patterns
    env_var_patterns = [
        f"CREDENTIAL_{credential_name.upper()}",
        f"CRED_{credential_name.upper()}",
        f"CREDENTIAL_{credential_name.upper()}_JSON",
        f"CRED_{credential_name.upper()}_JSON",
    ]
    
    # Add run and node specific patterns if provided
    if run_id and node_id:
        env_var_patterns.extend([
            f"CREDENTIAL_{run_id}_{node_id}_{credential_name.upper()}",
            f"CRED_{run_id}_{node_id}_{credential_name.upper()}"
        ])
    elif node_id:
        env_var_patterns.extend([
            f"CREDENTIAL_{node_id}_{credential_name.upper()}",
            f"CRED_{node_id}_{credential_name.upper()}"
        ])
    
    # Check each pattern
    for pattern in env_var_patterns:
        env_value = os.getenv(pattern)
        if env_value:
            try:
                # Try to parse as JSON first
                return json.loads(env_value)
            except json.JSONDecodeError:
                # If not JSON, treat as base64 encoded JSON
                try:
                    decoded = base64.b64decode(env_value).decode('utf-8')
                    return json.loads(decoded)
                except Exception:
                    # If not base64, return as simple string value
                    return {"value": env_value}
    
    return None

def _get_credentials_from_json_env() -> Optional[Dict[str, Dict[str, Any]]]:
    """
    Get all credentials from a JSON environment variable.
    
    Returns:
        Dictionary of all credentials or None if not found
    """
    # Check for environment variables containing all credentials
    for env_var in ["CREDENTIALS_JSON", "CREDS_JSON", "ALL_CREDENTIALS"]:
        env_value = os.getenv(env_var)
        if env_value:
            try:
                return json.loads(env_value)
            except json.JSONDecodeError as e:
                log.error(f"Failed to parse JSON from {env_var}: {e}")
    
    return None

def _get_credentials_from_files(credential_name: str) -> Optional[Dict[str, Any]]:
    """
    Get credentials from files.
    
    Args:
        credential_name: Name of the credential
        
    Returns:
        Credential data or None if not found
    """
    # Check credential directories
    search_dirs = [
        os.getenv("CREDENTIALS_DIR", "./credentials"),
        "/run/secrets",  # Docker Swarm / Kubernetes secrets
        os.path.expanduser("~/.credentials")
    ]
    
    # Check file patterns
    file_patterns = [
        f"{credential_name}.json",
        f"{credential_name.lower()}.json",
        f"{credential_name.upper()}.json",
        credential_name,
        credential_name.lower(),
        credential_name.upper()
    ]
    
    # Search for credential files
    for directory in search_dirs:
        if not os.path.exists(directory):
            continue
            
        for pattern in file_patterns:
            file_path = os.path.join(directory, pattern)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        # Try to parse as JSON first
                        try:
                            return json.loads(f.read())
                        except json.JSONDecodeError:
                            # If not JSON, return file content as value
                            return {"value": f.read().strip()}
                except Exception as e:
                    log.error(f"Failed to read credential file {file_path}: {e}")
    
    return None

async def store_credential(
    credential_name: str,
    credential_data: Dict[str, Any],
    temporary: bool = True
) -> bool:
    """
    Store credentials.
    
    Args:
        credential_name: Name of the credential
        credential_data: Credential data to store
        temporary: Whether to store temporarily in memory (True) or persistently (False)
        
    Returns:
        True if successful, False otherwise
    """
    if temporary:
        # Store in memory cache (would typically use Redis or similar in production)
        # This is just a stub implementation
        log.info(f"Storing credential {credential_name} in memory (stub implementation)")
        return True
    else:
        # Store in a credential file
        cred_dir = os.getenv("CREDENTIALS_DIR", "./credentials")
        if not os.path.exists(cred_dir):
            try:
                os.makedirs(cred_dir, exist_ok=True)
            except Exception as e:
                log.error(f"Failed to create credentials directory {cred_dir}: {e}")
                return False
                
        cred_file = os.path.join(cred_dir, f"{credential_name}.json")
        try:
            with open(cred_file, 'w') as f:
                json.dump(credential_data, f)
            os.chmod(cred_file, 0o600)  # Restrict access to owner only
            log.info(f"Credential {credential_name} stored to {cred_file}")
            return True
        except Exception as e:
            log.error(f"Failed to write credential to {cred_file}: {e}")
            return False 