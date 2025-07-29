"""
Server module providing common FastAPI application setup
"""

import os
import uvicorn
import logging
from typing import List, Union, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Configure default logger
log = logging.getLogger(os.getenv("OTEL_SERVICE_NAME", "fluidgrids"))

def create_app(
    title: str,
    description: str,
    version: str,
    cors_origins: Optional[List[str]] = None,
    docs_url: str = "/api/docs",
    redoc_url: str = "/api/redoc",
    api_prefix: str = "/api/v1",
) -> FastAPI:
    """
    Create a FastAPI application with standard configuration.
    
    Args:
        title: Application title
        description: Application description
        version: Application version
        cors_origins: Allowed CORS origins, defaults to ["*"]
        docs_url: URL for Swagger docs
        redoc_url: URL for ReDoc docs
        api_prefix: API route prefix
        
    Returns:
        Configured FastAPI application
    """
    if cors_origins is None:
        cors_origins = ["*"]
        
    app = FastAPI(
        title=title,
        description=description,
        version=version,
        docs_url=docs_url,
        redoc_url=redoc_url
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Instrument with OpenTelemetry
    FastAPIInstrumentor.instrument_app(app)
    log.info(f"FastAPI application '{title}' instrumented with OpenTelemetry")
    
    return app

def run_server(
    app: FastAPI,
    host: str = "0.0.0.0",
    port: Optional[int] = None,
    reload: Optional[bool] = None,
    log_level: str = "error",
) -> None:
    """
    Run the FastAPI application with Uvicorn.
    
    Args:
        app: FastAPI application
        host: Host to bind to
        port: Port to bind to, defaults to APP_PORT env var or 8000
        reload: Enable auto-reload, defaults to True in development
        log_level: Uvicorn log level
    """
    # Determine port
    if port is None:
        port = int(os.getenv("APP_PORT", "8000"))
    
    # Determine reload setting
    auto_reload = False
    if reload is None:
        if os.getenv("APP_ENV") == "development":
            auto_reload = True
    else:
        auto_reload = reload
        
    app_name = app.title if hasattr(app, "title") else "FastAPI"
    
    log.info(f"Starting {app_name} server on {host}:{port} with reload={auto_reload}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        ws="auto",
        ws_per_message_deflate="true",
        log_level=log_level,
        reload=auto_reload,
        reload_dirs=["."],
        reload_includes=["*.py", "*.gql"]
    )
    
    log.info(f'-- Uvicorn server process for {app_name} started in {os.getenv("APP_ENV", "production")} mode with port {port} --') 