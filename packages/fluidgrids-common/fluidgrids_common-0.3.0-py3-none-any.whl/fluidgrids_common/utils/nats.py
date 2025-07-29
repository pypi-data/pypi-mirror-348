# nats_manager.py
import os
import json
import asyncio
import logging
from typing import Optional, Callable, Awaitable, Any, Dict, List, Union, AsyncGenerator

import nats
from nats.aio.client import Client as NATSClient
from nats.aio.msg import Msg
from nats.aio.subscription import Subscription as NatsSubscription
from nats.aio.errors import ErrTimeout
from nats.js import JetStreamContext
from nats.js.api import StreamConfig, ConsumerConfig, DeliverPolicy, AckPolicy, RetentionPolicy, StorageType, DEFAULT_PREFIX as JS_DEFAULT_PREFIX
from nats.js.errors import APIError, NoStreamResponseError, ServiceUnavailableError
from nats.errors import ConnectionClosedError, TimeoutError as NatsTimeoutError, NoServersError, BadSubscriptionError

# --- Logging Setup ---
log = logging.getLogger(os.getenv("OTEL_SERVICE_NAME", "misc"))
# Basic config if not set up by the main application using this class
if not log.handlers and not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    )

class NatsManagerError(Exception):
    """Custom exception for NatsManager errors."""
    pass

class NatsManager:
    """
    A helper class to manage NATS connection, JetStream context,
    publishing, and subscribing with basic error handling.
    """
    DEFAULT_CONNECT_TIMEOUT = 10
    DEFAULT_RECONNECT_WAIT = 5
    DEFAULT_JS_TIMEOUT = 5.0
    DEFAULT_PUBLISH_TIMEOUT = 2.0 # Standard publish doesn't usually wait for ack

    def __init__(self,
                 nats_url: Union[str, List[str]],
                 client_name: str = "nats_manager_client",
                 connect_timeout: int = DEFAULT_CONNECT_TIMEOUT,
                 reconnect_wait: int = DEFAULT_RECONNECT_WAIT,
                 js_domain: Optional[str] = None, # For multi-domain JetStream
                 **nats_connect_options):
        """
        Initializes the NatsManager.

        Args:
            nats_url: Single NATS URL string or list of URLs.
            client_name: Name for the NATS client connection.
            connect_timeout: Timeout in seconds for initial connection.
            reconnect_wait: Time in seconds to wait between reconnect attempts.
            js_domain: Optional JetStream domain.
            **nats_connect_options: Additional options for nats.connect()
                                     (e.g., user, password, token, tls).
        """
        self.nats_servers = nats_url if isinstance(nats_url, list) else [nats_url]
        self.client_name = client_name
        self.connect_timeout = connect_timeout
        self.reconnect_wait = reconnect_wait
        self.js_domain = js_domain
        self.nats_connect_options = nats_connect_options
        self.nc: Optional[NATSClient] = None
        self.js: Optional[JetStreamContext] = None
        self.log = logging.getLogger(f"{__name__}.{self.__class__.__name__}") # Specific logger

    @property
    def is_connected(self) -> bool:
        """Checks if the NATS client is currently connected."""
        return self.nc is not None and self.nc.is_connected

    async def connect(self, retries: int = 5, delay_base: int = 2) -> bool:
        """
        Establishes connection to NATS server(s) and gets JetStream context.
        Includes retry logic with exponential backoff.

        Args:
            retries: Maximum number of connection attempts.
            delay_base: Initial delay in seconds between retries.

        Returns:
            True if connection successful and JetStream context obtained, False otherwise.
        """
        if self.is_connected:
            log.info("Already connected to NATS.")
            return True

        for attempt in range(1, retries + 1):
            try:
                log.info(f"Attempting NATS connection (attempt {attempt}/{retries})... Servers: {self.nats_servers}")
                self.nc = await nats.connect(
                    servers=self.nats_servers,
                    name=self.client_name,
                    connect_timeout=self.connect_timeout,
                    reconnect_time_wait=self.reconnect_wait,
                    max_reconnect_attempts=-1, # Infinite reconnects handled by library once connected
                    **self.nats_connect_options
                )
                log.info(f"NATS connected successfully to {self.nc.connected_url.netloc}")

                # Get JetStream context
                try:
                    self.js = self.nc.jetstream(domain=self.js_domain, timeout=self.DEFAULT_JS_TIMEOUT)
                    await self.js.account_info() # Verify JetStream is responsive
                    log.info("JetStream context obtained successfully.")
                    return True # Both connection and JS context successful
                except (NatsTimeoutError, ServiceUnavailableError) as js_err:
                    log.error(f"NATS connected, but failed to get/verify JetStream context: {js_err}")
                    await self.close() # Close base connection if JS fails critically
                    return False # Failed to initialize JS
                except Exception as js_e: # Catch other JS errors
                     log.exception(f"Unexpected error getting JetStream context: {js_e}")
                     await self.close(); return False

            except (NoServersError, ErrTimeout, ConnectionRefusedError) as e:
                log.warning(f"NATS connection attempt {attempt} failed: {e}")
                if attempt < retries:
                    sleep_time = delay_base * (2 ** (attempt - 1)) # Exponential backoff
                    log.info(f"Retrying NATS connection in {sleep_time} seconds...")
                    await asyncio.sleep(sleep_time)
                else:
                    log.error(f"NATS connection failed after {retries} attempts.")
                    self.nc = None # Ensure nc is None if connection failed
                    self.js = None
                    return False
            except Exception as e:
                log.exception(f"Unexpected error during NATS connection attempt {attempt}: {e}")
                self.nc = None; self.js = None
                return False # Fail on unexpected errors
        return False # Should not be reached if retries > 0

    async def close(self):
        """Gracefully drains and closes the NATS connection."""
        if self.nc and self.nc.is_connected:
            log.info("Draining and closing NATS connection...")
            try:
                await self.nc.drain() # Wait for pending messages to be sent/processed
                await self.nc.close()
                log.info("NATS connection closed.")
            except Exception as e:
                log.exception(f"Error during NATS connection close: {e}")
        else:
            log.info("NATS connection already closed or not established.")
        self.nc = None
        self.js = None

    async def ensure_stream(self,
                            stream_name: str,
                            subjects: List[str],
                            storage: StorageType = StorageType.FILE,
                            retention: RetentionPolicy = RetentionPolicy.LIMITS,
                            num_replicas: int = 1,
                            **stream_options) -> bool:
        """
        Ensures a JetStream stream exists with the specified configuration.
        Creates or updates the stream.

        Args:
            stream_name: Name of the stream.
            subjects: List of subjects the stream should capture.
            storage: Storage type (FILE or MEMORY).
            retention: Retention policy (LIMITS, INTEREST, WORK_QUEUE).
            num_replicas: Number of replicas (for clustered NATS).
            **stream_options: Other StreamConfig options (e.g., max_age, max_bytes).

        Returns:
            True if stream exists/was created/updated successfully, False otherwise.
        """
        if not self.js:
            log.error("Cannot ensure stream: JetStream context not available.")
            return False
        log.info(f"Ensuring JetStream stream '{stream_name}' exists for subjects: {subjects}")
        try:
            config = StreamConfig(
                name=stream_name, subjects=subjects, storage=storage,
                retention=retention, num_replicas=num_replicas, **stream_options
            )
            await self.js.update_stream(config=config) # Creates if needed, updates if possible
            log.info(f"Stream '{stream_name}' created or configuration updated.")
            return True
        except APIError as e:
             log.warning(f"API Error configuring stream '{stream_name}': {e.description} ({e.err_code}). Verifying existence.")
             try: await self.js.stream_info(stream_name); log.info(f"Stream '{stream_name}' verified exist."); return True # Exists, good enough
             except: log.error(f"Stream '{stream_name}' could not be configured or verified."); return False
        except (ServiceUnavailableError, NatsTimeoutError) as e:
             log.error(f"NATS/JS service error ensuring stream '{stream_name}': {e}"); return False
        except Exception as e:
             log.exception(f"Unexpected error ensuring stream '{stream_name}': {e}"); return False

    async def publish(self, subject: str, payload: bytes, timeout: float = DEFAULT_PUBLISH_TIMEOUT):
        """
        Publishes a message to a standard NATS subject (non-JetStream).

        Args:
            subject: The subject to publish to.
            payload: The message payload as bytes.
            timeout: Optional timeout in seconds.

        Raises:
            NatsManagerError: If not connected or publish fails.
        """
        if not self.is_connected or self.nc is None:
            raise NatsManagerError("Cannot publish: Not connected to NATS.")
        log.debug(f"Publishing {len(payload)} bytes to NATS subject '{subject}'")
        try:
            await self.nc.publish(subject, payload, timeout=timeout)
            log.debug(f"Successfully published to '{subject}'")
        except ErrTimeout:
            log.error(f"Timeout publishing to NATS subject '{subject}'")
            raise NatsManagerError(f"Timeout publishing to {subject}") from ErrTimeout
        except Exception as e:
            log.exception(f"Error publishing to NATS subject '{subject}': {e}")
            raise NatsManagerError(f"Failed to publish to {subject}") from e

    async def js_publish(self,
                         subject: str,
                         payload: bytes,
                         stream: Optional[str] = None, # Optional: Specify stream for validation
                         timeout: float = DEFAULT_JS_TIMEOUT) -> Optional[nats.js.api.PubAck]:
        """
        Publishes a message to a JetStream subject and waits for acknowledgement.

        Args:
            subject: The subject to publish to (must be bound to a stream).
            payload: The message payload as bytes.
            stream: Optional: Expected stream name (helps catch misconfiguration).
            timeout: Timeout in seconds to wait for acknowledgement.

        Returns:
            The PubAck object on success, None on failure.

        Raises:
            NatsManagerError: If not connected, JetStream unavailable, or publish fails critically.
        """
        if not self.js:
            raise NatsManagerError("Cannot publish to JetStream: JetStream context not available.")
        log.debug(f"Publishing {len(payload)} bytes to JetStream subject '{subject}' (stream hint: {stream})")
        try:
            # Publish and wait for ack from the stream
            ack = await self.js.publish(subject, payload, timeout=timeout, stream=stream)
            log.debug(f"JetStream publish successful to '{subject}' (Stream: {ack.stream}, Seq: {ack.seq})")
            return ack
        except NoStreamResponseError as e:
             log.error(f"No response from stream when publishing to '{subject}'. Is subject bound to stream '{stream or 'any'}'? Err: {e}")
             raise NatsManagerError("NATS stream did not respond to publish") from e
        except ErrTimeout:
            log.error(f"Timeout waiting for JetStream ACK for subject '{subject}'")
            raise NatsManagerError(f"Timeout waiting for JS ACK for {subject}") from ErrTimeout
        except ServiceUnavailableError as e:
             log.error(f"JetStream service unavailable during publish to '{subject}': {e}");
             raise NatsManagerError("JetStream service unavailable") from e
        except Exception as e:
            log.exception(f"Error publishing to JetStream subject '{subject}': {e}")
            raise NatsManagerError(f"Failed to publish to JetStream {subject}") from e

    async def subscribe(self,
                        subject: str,
                        queue: str = "", # For core NATS queue group load balancing
                        callback: Callable[[Msg], Awaitable[None]] = None
                        ) -> Optional[nats.aio.subscription.Subscription]:
        """
        Creates a standard NATS subscription (non-JetStream).

        Args:
            subject: Subject to subscribe to (can include wildcards).
            queue: Optional queue group name.
            callback: Async function to process received messages (`async def cb(msg): ...`).

        Returns:
            The Subscription object or None on error.
        """
        if not self.is_connected or self.nc is None:
            log.error("Cannot subscribe: Not connected to NATS.")
            return None
        log.info(f"Creating NATS subscription: Subject='{subject}', Queue='{queue or 'N/A'}'")
        try:
            sub = await self.nc.subscribe(subject, queue=queue, cb=callback)
            log.info(f"Successfully subscribed to NATS subject '{subject}'.")
            return sub
        except Exception as e:
            log.exception(f"Failed to create NATS subscription for subject '{subject}': {e}")
            return None

    async def js_subscribe(self,
                           subject: str,
                           durable: Optional[str] = None, # Name for durable consumer state
                           queue: str = "", # JetStream queue group name
                           callback: Callable[[Msg], Awaitable[None]] = None, # Async callback
                           manual_ack: bool = True, # Recommended for resilient processing
                           **consumer_config_options # Pass other ConsumerConfig kwargs directly
                           ) -> Optional[nats.aio.subscription.Subscription]:
        """
        Creates a JetStream PUSH subscription.

        Args:
            subject: Subject to subscribe to.
            durable: Name for durable consumer (required for persistence across restarts).
            queue: JetStream queue group name for load balancing.
            callback: Async callback function (`async def cb(msg): await msg.ack() ...`).
            manual_ack: If True (default), callback MUST call `msg.ack()`, `nak()`, or `term()`.
            **consumer_config_options: Additional options for nats.js.api.ConsumerConfig
                                       (e.g., deliver_policy, ack_wait, max_deliver, idle_heartbeat).

        Returns:
            The JetStream Subscription object or None on error.
        """
        if not self.js:
            log.error("Cannot create JetStream subscription: JetStream context not available.")
            return None

        if manual_ack and consumer_config_options.get('ack_policy', AckPolicy.EXPLICIT) != AckPolicy.EXPLICIT:
             log.warning(f"Manual ack requested for JS sub '{subject}', but AckPolicy is not EXPLICIT. Forcing EXPLICIT.")
             consumer_config_options['ack_policy'] = AckPolicy.EXPLICIT

        # Remove 'cb' and 'config' if they exist in consumer_config_options, as they are not part of ConsumerConfig
        if 'cb' in consumer_config_options:
            del consumer_config_options['cb']
        if 'config' in consumer_config_options:
            del consumer_config_options['config']

        log.info(f"Creating JetStream subscription: Subject='{subject}', Durable='{durable}', Queue='{queue or 'N/A'}'")
        try:
            # Create the ConsumerConfig instance first
            consumer_config_instance = ConsumerConfig(**consumer_config_options)

            sub = await self.js.subscribe(
                subject=subject,
                durable=durable,
                queue=queue,
                cb=callback, # Pass callback directly here
                manual_ack=manual_ack,
                config=consumer_config_instance # Pass the created instance here
            )
            log.info(f"Successfully created JetStream subscription for subject '{subject}'.")
            return sub
        except (APIError, ServiceUnavailableError, NatsTimeoutError, ValueError) as e:
            # ValueError can happen on bad ConsumerConfig
            log.exception(f"Failed to create JetStream subscription for subject '{subject}': {e}")
            return None
        except Exception as e: # Catch other unexpected errors
            log.exception(f"Unexpected error creating JetStream subscription for subject '{subject}': {e}")
            return None
        


class GraphQLNatsSubscriberError(Exception):
    """Custom exception for subscriber errors."""
    pass

class GraphQLNatsSubscriber:
    """
    Manages NATS subscriptions specifically for feeding GraphQL async generators.
    """

    def __init__(self, nats_client: Optional[NATSClient]):
        """
        Initializes the subscriber with a connected NATS client.

        Args:
            nats_client: An active NATS client instance (nc).
        """
        if not nats_client or not nats_client.is_connected:
            log.error("GraphQLNatsSubscriber initialized without a connected NATS client.")
            # Store it anyway, but checks are needed before use
        self.nc = nats_client
        log.info("GraphQLNatsSubscriber initialized.")

    def is_ready(self) -> bool:
        """Checks if the NATS client is available and connected."""
        return self.nc is not None and self.nc.is_connected

    async def listen(self, subject: str, gql_type_formatter: callable) -> AsyncGenerator[Dict, None]:
        """
        Listens to a NATS subject and yields formatted messages for GraphQL.

        Args:
            subject: The NATS subject (potentially with wildcards) to subscribe to.
            gql_type_formatter: A callable that takes the raw NATS message data (dict)
                                and formats it into the dictionary structure expected
                                by the corresponding GraphQL type (e.g., LogEntry, NodeEvent).

        Yields:
            Dictionaries formatted according to gql_type_formatter.

        Raises:
            GraphQLNatsSubscriberError: If NATS is not connected.
            asyncio.CancelledError: Propagated when the client disconnects.
        """
        if not self.is_ready():
            log.error(f"Cannot listen to '{subject}': NATS client not ready.")
            raise GraphQLNatsSubscriberError(f"NATS client not connected, cannot subscribe to {subject}")

        local_queue = asyncio.Queue()
        nats_subscription: Optional[NatsSubscription] = None
        log.info(f"Attempting to subscribe to NATS subject: {subject}")

        async def message_handler(msg: Msg):
            """Callback for NATS subscription. Decodes, formats, and queues the message."""
            nats_subject = msg.subject
            data = msg.data.decode()
            log.debug(f"Received NATS msg on '{nats_subject}': {data[:100]}...")
            try:
                raw_data_dict = json.loads(data)
                # Use the provided formatter to structure the data for GraphQL
                formatted_data = gql_type_formatter(raw_data_dict)
                await local_queue.put(formatted_data)
            except json.JSONDecodeError:
                log.error(f"Failed to decode JSON from NATS msg on '{nats_subject}': {data}")
                # Optionally put an error message onto the queue?
                # await local_queue.put({"error": "Invalid JSON received"})
            except Exception as e:
                log.exception(f"Error processing NATS message in handler for '{nats_subject}': {e}")
                # Optionally put an error message onto the queue?
                # await local_queue.put({"error": f"Processing error: {e}"})

        try:
            # Create an ephemeral core NATS subscription
            nats_subscription = await self.nc.subscribe(subject, cb=message_handler)
            log.info(f"NATS subscription successful for subject: {subject}")

            # Keep yielding messages from the local queue until client disconnects
            while True:
                log_item = await local_queue.get()
                yield log_item
                local_queue.task_done()

        except asyncio.CancelledError:
            # This happens when the GraphQL client disconnects
            log.info(f"Client disconnected for NATS subject '{subject}'. Cleaning up subscription.")
            # CancelledError should be propagated up as Ariadne expects it
            raise
        except Exception as e:
            log.exception(f"Error in NATS listen generator for subject '{subject}': {e}")
            # Depending on desired behavior, you might yield an error or just log
            # yield {"error": f"Subscription error for {subject}: {e}"}
            # Or re-raise a specific error
            raise GraphQLNatsSubscriberError(f"Error during subscription for {subject}: {e}") from e
        finally:
            # --- Crucial Cleanup ---
            if nats_subscription:
                log.info(f"Cleaning up NATS subscription for subject '{subject}'")
                try:
                    if self.nc and self.nc.is_connected: # Check connection before unsubscribing
                        await nats_subscription.unsubscribe()
                        log.info(f"NATS subscription successfully unsubscribed for '{subject}'")
                    else:
                        # If not connected, unsubscribe might fail or be unnecessary
                        log.warning(f"NATS disconnected, cannot explicitly unsubscribe from '{subject}'. Server might clean it up.")
                except Exception as unsub_e:
                    # Log error but don't prevent cleanup flow
                    log.error(f"Error unsubscribing from NATS subject '{subject}': {unsub_e}")
            else:
                 log.warning(f"No active NATS subscription object found to clean up for subject '{subject}'")
            # ----------------------