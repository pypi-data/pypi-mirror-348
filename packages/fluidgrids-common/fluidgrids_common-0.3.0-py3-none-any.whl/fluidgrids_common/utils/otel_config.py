"""
OpenTelemetry configuration for Fluidgrids nodes
"""

import os
import logging
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

def setup_opentelemetry_for_node(
    service_name: Optional[str] = None,
    otlp_endpoint: Optional[str] = None,
    resource_attributes: Optional[Dict[str, Any]] = None
) -> None:
    """
    Set up OpenTelemetry for a node with standard configuration.
    
    Args:
        service_name: The service name for tracing. If None, will use the OTEL_SERVICE_NAME env var
                     or default to "fluidgrids-node" 
        otlp_endpoint: OpenTelemetry collector endpoint. If None, will use the OTEL_EXPORTER_OTLP_ENDPOINT
                       env var or default to "http://localhost:4317"
        resource_attributes: Additional resource attributes to include with telemetry data
    """
    try:
        # Import OpenTelemetry modules
        from opentelemetry import trace
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
        from opentelemetry.semconv.resource import ResourceAttributes
        
        # Determine service name
        if service_name is None:
            service_name = os.environ.get("OTEL_SERVICE_NAME", "fluidgrids-node")
            
        # Sanitize service name for OpenTelemetry (no dots or special chars)
        service_name = service_name.replace(".", "-").lower()
        
        # Determine OTLP endpoint
        if otlp_endpoint is None:
            otlp_endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
            
        # Set up resource attributes
        attrs = {
            ResourceAttributes.SERVICE_NAME: service_name,
            ResourceAttributes.SERVICE_VERSION: os.environ.get("APP_VERSION", "unknown"),
            ResourceAttributes.DEPLOYMENT_ENVIRONMENT: os.environ.get("APP_ENV", "development"),
        }
        
        # Add additional resource attributes if provided
        if resource_attributes:
            attrs.update(resource_attributes)
            
        # Create resource
        resource = Resource.create(attrs)
        
        # Set up tracer provider
        tracer_provider = TracerProvider(resource=resource)
        
        # Configure OTLP exporter
        otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
        span_processor = BatchSpanProcessor(otlp_exporter)
        tracer_provider.add_span_processor(span_processor)
        
        # Set as global tracer provider
        trace.set_tracer_provider(tracer_provider)
        
        # Set up instrumentation - commonly used in nodes
        # Add instrumentation for common libraries if they're installed
        
        # FastAPI instrumentation is applied in the server.py module
        
        # Try to add HTTPX instrumentation if it's available
        try:
            from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
            HTTPXClientInstrumentor().instrument()
            logger.info("HTTPX instrumentation added")
        except (ImportError, Exception) as e:
            logger.debug(f"HTTPX instrumentation not added: {e}")
            
        # Try to add Requests instrumentation if it's available
        try:
            from opentelemetry.instrumentation.requests import RequestsInstrumentor
            RequestsInstrumentor().instrument()
            logger.info("Requests instrumentation added")
        except (ImportError, Exception) as e:
            logger.debug(f"Requests instrumentation not added: {e}")
            
        # Try to add NATS instrumentation if it's available
        try:
            from opentelemetry.instrumentation.nats import NatsInstrumentor
            NatsInstrumentor().instrument()
            logger.info("NATS instrumentation added")
        except (ImportError, Exception) as e:
            logger.debug(f"NATS instrumentation not added: {e}")
            
        logger.info(f"OpenTelemetry configured for service: {service_name} with endpoint: {otlp_endpoint}")
        
    except ImportError as ie:
        logger.warning(f"OpenTelemetry not fully set up due to missing dependencies: {ie}")
    except Exception as exc:
        logger.exception(f"Failed to set up OpenTelemetry: {exc}")
        
    # Always succeed, even if OpenTelemetry setup fails
    return 