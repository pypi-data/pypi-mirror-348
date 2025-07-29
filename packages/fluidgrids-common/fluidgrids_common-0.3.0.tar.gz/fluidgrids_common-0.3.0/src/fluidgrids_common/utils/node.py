"""
Node-related utilities for exposing node assets and manifest via APIs
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
from fastapi import APIRouter, HTTPException, FastAPI, Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette import status

# Configure default logger
log = logging.getLogger(os.getenv("OTEL_SERVICE_NAME", "fluidgrids"))

class NodeAPIManager:
    """
    Manager for exposing node assets and manifest via APIs
    """
    
    def __init__(self, node_dir: str, node_type: str, node_version: str):
        """
        Initialize the node API manager
        
        Args:
            node_dir: Directory where the node is located
            node_type: Type of the node
            node_version: Version of the node
        """
        self.node_dir = Path(node_dir)
        self.node_type = node_type
        self.node_version = node_version
        self.version_dir = node_version if node_version.startswith('v') else f"v{node_version}"
        self.manifest_path = self.node_dir / "manifest.json"
        self.assets_dir = self.node_dir / "assets"
        self.secured_assets_dir = self.node_dir / "secured_assets"
        
        # Validate
        if not self.node_dir.exists():
            raise ValueError(f"Node directory does not exist: {self.node_dir}")
        if not self.manifest_path.exists():
            raise ValueError(f"Manifest file not found at {self.manifest_path}")

    def register_routes(self, app: FastAPI):
        """
        Register node routes with the FastAPI application
        
        Args:
            app: FastAPI application to register routes with
        """
        router = APIRouter(tags=["Node"])
        
        # Register manifest endpoint
        @router.get("/manifest.json", response_model=Dict[str, Any])
        async def get_manifest():
            """Get the node manifest"""
            return self.get_manifest()
        
        # Register asset endpoint
        @router.get("/assets/{asset_path:path}")
        async def get_asset(asset_path: str):
            """Get an asset from the node"""
            return self.get_asset(asset_path)
        
        # Register secured asset endpoint
        @router.get("/secured-assets/{asset_path:path}")
        async def get_secured_asset(asset_path: str):
            """Get a secured asset from the node"""
            return self.get_secured_asset(asset_path)
        
        # Register routes
        app.include_router(router, prefix=f"/node/{self.node_type}/version/{self.node_version}")
        
        # Mount static assets directory if it exists
        if self.assets_dir.exists():
            app.mount(
                f"/node/{self.node_type}/version/{self.node_version}/static", 
                StaticFiles(directory=str(self.assets_dir)), 
                name=f"node_{self.node_type}_{self.node_version}_assets"
            )
        
        log.info(f"Registered API routes for node {self.node_type} version {self.node_version}")
    
    def get_manifest(self) -> Dict[str, Any]:
        """
        Get the node manifest
        
        Returns:
            Node manifest as a dictionary
        """
        try:
            with open(self.manifest_path, 'r') as f:
                manifest = json.load(f)
                return manifest
        except Exception as e:
            log.error(f"Error reading manifest file {self.manifest_path}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error reading manifest file: {e}"
            )
    
    def get_asset(self, asset_path: str) -> FileResponse:
        """
        Get an asset from the node
        
        Args:
            asset_path: Path to the asset relative to the assets directory
            
        Returns:
            FileResponse with the requested asset
        """
        full_path = self.assets_dir / asset_path
        
        # Check if file exists
        if not full_path.exists() or not full_path.is_file():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Asset not found: {asset_path}"
            )
            
        # Verify no directory traversal
        try:
            resolved_path = full_path.resolve(strict=True)
            assets_dir_resolved = self.assets_dir.resolve(strict=True)
            
            if not str(resolved_path).startswith(str(assets_dir_resolved)):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid asset path"
                )
                
            return FileResponse(str(resolved_path))
        except Exception as e:
            log.error(f"Error serving asset {asset_path}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error serving asset: {e}"
            )
    
    def get_secured_asset(self, asset_path: str) -> FileResponse:
        """
        Get a secured asset from the node
        
        Args:
            asset_path: Path to the asset relative to the secured_assets directory
            
        Returns:
            FileResponse with the requested asset
        """
        if not self.secured_assets_dir.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No secured assets available for this node"
            )
            
        full_path = self.secured_assets_dir / asset_path
        
        # Check if file exists
        if not full_path.exists() or not full_path.is_file():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Secured asset not found: {asset_path}"
            )
            
        # Verify no directory traversal
        try:
            resolved_path = full_path.resolve(strict=True)
            secured_assets_dir_resolved = self.secured_assets_dir.resolve(strict=True)
            
            if not str(resolved_path).startswith(str(secured_assets_dir_resolved)):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid secured asset path"
                )
                
            return FileResponse(str(resolved_path))
        except Exception as e:
            log.error(f"Error serving secured asset {asset_path}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error serving secured asset: {e}"
            ) 