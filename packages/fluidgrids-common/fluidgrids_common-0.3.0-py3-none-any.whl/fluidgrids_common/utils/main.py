"""
Main utilities for Fluidgrids nodes
"""

import os
import json
import asyncio
import datetime
import logging
from typing import Dict, Optional, Any

# Configure default logger
log = logging.getLogger(os.getenv("OTEL_SERVICE_NAME", "fluidgrids"))
if not logging.getLogger().hasHandlers():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

from .nats import NatsManager, NatsManagerError, GraphQLNatsSubscriber

# Global NATS manager
nats_manager = NatsManager(nats_url=os.getenv("NATS_URL"))
gql_nats_subscriber: Optional[GraphQLNatsSubscriber] = None

async def init_nats() -> bool:
    """
    Initialize NATS connection.
    
    Returns:
        True if connection was successful, False otherwise
    """
    log.info("Initializing NATS connection...")
    connected = await nats_manager.connect()

    if not connected:
        log.error("Failed to connect to NATS.")
        return False
    
    log.info(f"NATS Connected: {nats_manager.is_connected}")
    return True

async def get_nats_subscriber() -> Optional[GraphQLNatsSubscriber]:
    """
    Get a NATS subscriber for GraphQL operations.
    
    Returns:
        GraphQLNatsSubscriber instance or None if not available
    """    
    log.info("Getting NATS subscriber...")
    if nats_manager.is_connected:
        subscriber = GraphQLNatsSubscriber(nats_manager.nc)

        if not subscriber.is_ready():
            log.critical("GraphQLNatsSubscriber could not be initialized properly (NATS client issue?).")
            return None
        else:
            log.info('GraphQLNatsSubscriber init complete')
            return subscriber
    else:
        log.warning("NATS client not connected. Attempting to initialize...")
        await init_nats()
        subscriber = GraphQLNatsSubscriber(nats_manager.nc)

        if not subscriber.is_ready():
            log.critical("GraphQLNatsSubscriber could not be initialized properly (NATS client issue?).")
            return None
        else:
            log.info('GraphQLNatsSubscriber init complete')
            return subscriber

def format_log_for_gql(raw_data: Dict) -> Dict:
    """
    Format raw NATS log data into GraphQL LogEntry structure.
    
    Args:
        raw_data: Log data dictionary
        
    Returns:
        Formatted log entry for GraphQL
    """
    log.debug("Formatting log data for GraphQL...")
    return {
        "runId": raw_data.get("runId", "unknown"),
        "nodeId": raw_data.get("nodeId", "unknown"),
        "timestamp": raw_data.get("timestamp", datetime.datetime.now(datetime.timezone.utc).isoformat()),
        "level": raw_data.get("level", "UNKNOWN"),
        "message": raw_data.get("message", ""),
        # Ensure details is a JSON string for GraphQL
        "details": json.dumps(raw_data.get("details", {}))
    }

def format_event_for_gql(raw_data: Dict) -> Dict:
    """
    Format raw NATS event data into GraphQL NodeEvent structure.
    
    Args:
        raw_data: Event data dictionary
        
    Returns:
        Formatted event for GraphQL
    """
    log.debug("Formatting event data for GraphQL...")
    return {
        "runId": raw_data.get("runId", "unknown"),
        "nodeId": raw_data.get("nodeId", "unknown"),
        "timestamp": raw_data.get("timestamp", datetime.datetime.now(datetime.timezone.utc).isoformat()),
        "eventType": raw_data.get("eventType", "UNKNOWN"),
        # Ensure payload is a JSON string for GraphQL
        "payload": json.dumps(raw_data.get("payload", {}))
    }

async def publish_log_to_nats(
    run_id: str, 
    node_id: str, 
    level: str, 
    message: str, 
    details: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Publish log to NATS.
    
    Args:
        run_id: Workflow run ID
        node_id: Node ID
        level: Log level
        message: Log message
        details: Additional log details
        
    Returns:
        True if publish was successful, False otherwise
    """
    log.debug(f"Entering publish_log_to_nats for {run_id}/{node_id}")
    if not run_id or not node_id:
        log.warning("Skipping NATS log publish: run_id or node_id missing.")
        log.debug(f"Exiting publish_log_to_nats early (missing ids)")
        return False

    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    # Prepare payload for NATS
    nats_payload = {
        "runId": run_id,
        "nodeId": node_id,
        "timestamp": timestamp,
        "level": level.upper(),
        "message": message,
        "details": details if details else {}
    }
    # Subject includes run and node IDs for targeted subscriptions
    log_subject = f"run.{run_id}.node.{node_id}.logs"
    log.debug(f"Attempting NATS publish to subject: {log_subject}")

    try:
        payload_bytes = json.dumps(nats_payload).encode('utf-8')
        if nats_manager.is_connected:
            # Using JetStream publish
            ack = await nats_manager.js_publish(log_subject, payload_bytes, timeout=2.0)
            if ack:
                log.info(f"NATS Log published: Subj='{log_subject}', Seq={ack.seq}")
                return True
            else:
                log.warning(f"NATS Log publish failed (no ACK): Subj='{log_subject}'")
                return False
        else:
            log.warning(f"NATS Log publish skipped: Not connected. Subj='{log_subject}'")
            return False
    except NatsManagerError as e:
        log.error(f"NATS Manager Error publishing log to '{log_subject}': {e}")
        return False
    except Exception as e:
        log.exception(f"Unexpected error publishing log to NATS subject '{log_subject}': {e}")
        return False
    
    log.debug(f"Exiting publish_log_to_nats for {run_id}/{node_id}")
    return True

async def publish_event_to_nats(
    run_id: str, 
    node_id: str, 
    event_type: str, 
    payload: Dict[str, Any]
) -> bool:
    """
    Publish event to NATS.
    
    Args:
        run_id: Workflow run ID
        node_id: Node ID
        event_type: Event type
        payload: Event payload
        
    Returns:
        True if publish was successful, False otherwise
    """
    log.debug(f"Entering publish_event_to_nats for {run_id}/{node_id}, type: {event_type}")
    if not run_id or not node_id or not event_type:
        log.warning("Skipping NATS event publish: run_id, node_id, or event_type missing.")
        log.debug(f"Exiting publish_event_to_nats early (missing ids/type)")
        return False

    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    # Payload structure for NATS
    nats_payload = {
        "runId": run_id,
        "nodeId": node_id,
        "timestamp": timestamp,
        "eventType": event_type,
        "payload": payload
    }
    # Subject includes event type for potential filtering
    event_subject = f"run.{run_id}.node.{node_id}.events.{event_type}"
    log.debug(f"Attempting NATS publish to subject: {event_subject}")

    try:
        payload_bytes = json.dumps(nats_payload).encode('utf-8')
        if nats_manager.is_connected:
            ack = await nats_manager.js_publish(event_subject, payload_bytes, timeout=2.0)
            if ack:
                log.info(f"NATS Event published: Subj='{event_subject}', Seq={ack.seq}")
                return True
            else:
                log.warning(f"NATS Event publish failed (no ACK): Subj='{event_subject}'")
                return False
        else:
            log.warning(f"NATS Event publish skipped: Not connected. Subj='{event_subject}'")
            return False
    except NatsManagerError as e:
        log.error(f"NATS Manager Error publishing event to '{event_subject}': {e}")
        return False
    except Exception as e:
        log.exception(f"Unexpected error publishing event to NATS subject '{event_subject}': {e}")
        return False
    
    log.debug(f"Exiting publish_event_to_nats for {run_id}/{node_id}")
    return True

# Initialize NATS on module load
log.info("Checking event loop for NATS initialization...")
try:
    loop = asyncio.get_running_loop()
except RuntimeError:  # 'RuntimeError: There is no current event loop...'
    log.warning("No running event loop found for NATS init.")
    loop = None

if loop and loop.is_running():
    log.info("Running event loop found. Creating NATS init task.")
    init_task = loop.create_task(init_nats())
else:
    log.info("No running event loop. NATS will be initialized when needed.")

log.info("NATS setup process complete.") 