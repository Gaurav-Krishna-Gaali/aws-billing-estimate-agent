#!/usr/bin/env python3
"""
FastAPI Server for AWS Billing Automation
Provides REST API endpoints to create AWS Calculator estimates
"""

import json
import os
import sys
import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import tempfile

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Try pydantic_settings, fallback to pydantic BaseSettings
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from llm_processor.sow_to_schema_mapper import SOWToSchemaMapper
from llm_processor.schema_validator import SchemaValidator
# Use V2 builder which fixes the "View summary" issue
from aws_services.estimate_builder_v2 import AWSEstimateBuilderV2 as AWSEstimateBuilder


# Configuration
class Settings(BaseSettings):
    """Application settings"""
    aws_region: str = "us-east-1"
    bedrock_model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    headless: bool = False
    default_output_file: str = "estimate_url.txt"
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False
    }


settings = Settings()

# FastAPI app
app = FastAPI(
    title="AWS Billing Automation API",
    description="REST API for creating AWS Calculator estimates from service configurations",
    version="1.0.0"
)


# Request/Response Models
class ServiceConfig(BaseModel):
    """Individual service configuration"""
    description: Optional[str] = None
    region: Optional[str] = "us-east-1"
    # Allow arbitrary fields for service-specific configs
    model_config = {"extra": "allow"}


class EstimateRequest(BaseModel):
    """Request model for creating estimate - accepts SOW JSON or standardized services"""
    # Allow arbitrary fields for flexible SOW JSON input
    model_config = {"extra": "allow"}
    
    # Option 1: Pre-standardized services (skips LLM processing)
    services: Optional[Dict[str, List[Dict[str, Any]]]] = Field(
        None,
        description="Pre-standardized services dictionary (format: {'s3': [{...}], 'ec2': [{...}]}). If provided, LLM processing is skipped."
    )
    
    # Option 2: SOW data - if present and no 'services' key, will use LLM
    # The entire request body can be SOW JSON, we'll detect it
    
    # Control flags
    use_llm: Optional[bool] = Field(
        None,
        description="Force LLM processing (auto-detected if 'services' key missing in top-level)"
    )
    headless: Optional[bool] = Field(
        None,
        description="Run browser in headless mode (default: False)"
    )
    validate_only: bool = Field(
        False,
        description="Only validate configurations, do not build estimate"
    )


class EstimateResponse(BaseModel):
    """Response model for estimate creation"""
    success: bool
    estimate_url: Optional[str] = None
    message: str
    services_added: Optional[Dict[str, Dict[str, Any]]] = None
    validation_results: Optional[Dict[str, Any]] = None
    skipped_services: Optional[List[Dict[str, Any]]] = None
    skipped_count: Optional[int] = None
    timestamp: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    version: str


# Helper Functions
def process_with_llm(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process input data with AWS Bedrock to standardize service configurations"""
    try:
        mapper = SOWToSchemaMapper(region=settings.aws_region, model_id=settings.bedrock_model_id)
        standardized = mapper.map_sow_to_schemas(input_data)
        
        if not standardized:
            raise ValueError("Bedrock processing failed to produce any services")
        
        return standardized
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Bedrock processing failed: {str(e)}. Make sure AWS credentials are configured and Bedrock access is enabled."
        )


def validate_services(services_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Validate service configurations against schemas"""
    try:
        validator = SchemaValidator()
        results = validator.validate_multiple_services(services_dict)
        
        total_services = sum(result['total'] for result in results.values())
        valid_services = sum(result['valid'] for result in results.values())
        invalid_services = sum(result['invalid'] for result in results.values())
        
        return {
            "valid": invalid_services == 0,
            "total_services": total_services,
            "valid_services": valid_services,
            "invalid_services": invalid_services,
            "details": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


def _build_estimate_sync(services_dict: Dict[str, Any], headless: bool = None) -> Dict[str, Any]:
    """Build AWS estimate with multiple services (sync version for thread execution)"""
    if headless is None:
        headless = settings.headless
    
    builder = AWSEstimateBuilder(headless=headless)
    
    try:
        # Start session
        if not builder.start_session():
            raise Exception("Failed to start estimate session")
        
        # Add services
        results = builder.add_multiple_services(services_dict)
        
        # Build summary - skip internal summary key
        services_summary = {}
        total_successful = 0
        total_services = 0
        skipped_services = []
        
        for service_type, result in results.items():
            if service_type == '_summary':
                # Extract skipped services from summary
                skipped_services = result.get('skipped_services', [])
                continue
            
            services_summary[service_type] = {
                "successful": result['successful'],
                "total": result['total'],
                "failed": result.get('failed', 0),
                "failed_instances": result.get('failed_instances', [])
            }
            total_successful += result['successful']
            total_services += result['total']
        
        # Finalize estimate
        url = builder.finalize_estimate()
        
        if not url:
            raise Exception("Failed to create estimate URL")
        
        return {
            "url": url,
            "services_added": services_summary,
            "total_successful": total_successful,
            "total_services": total_services,
            "skipped_services": skipped_services,
            "skipped_count": len(skipped_services)
        }
        
    except Exception as e:
        raise Exception(f"Estimate building failed: {str(e)}")
    finally:
        builder.close_session()


async def build_estimate(services_dict: Dict[str, Any], headless: bool = None) -> Dict[str, Any]:
    """
    Build AWS estimate with multiple services (async wrapper)
    Runs sync Playwright code in thread executor to avoid async context issues
    """
    # Get or create event loop
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    # Run sync Playwright code in thread executor
    with ThreadPoolExecutor(max_workers=1) as executor:
        result = await loop.run_in_executor(
            executor,
            _build_estimate_sync,
            services_dict,
            headless
        )
    
    return result


# API Endpoints
@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.post("/estimate")
async def create_estimate(body: Dict[str, Any] = Body(...)):
    """
    Create AWS Calculator estimate from service configurations
    
    **Accepts flexible JSON input:**
    
    1. **SOW JSON (Recommended)**: Send your raw SOW analysis JSON directly.
       The LLM will automatically normalize it to the required format.
       Example: `{"result": {"estimate": [{"service_name": "S3", ...}]}}`
       
    2. **Pre-standardized services**: If you already have standardized format:
       `{"services": {"s3": [...], "ec2": [...]}}`
    
    **Auto-detection logic:**
    - If `services` key exists at top level → uses directly (no LLM)
    - Otherwise → processes with LLM to standardize (default behavior)
    
    **Optional flags in JSON body:**
    - `use_llm`: true/false (default: auto-detected)
    - `validate_only`: true/false (default: false) - only validate, don't build
    - `headless`: true/false (default: false) - run browser in headless mode
    
    **Important:** Set Content-Type header to `application/json` when making requests.
    """
    try:
        
        services_dict = None
        
        # Check for control flags
        use_llm = body.get('use_llm')
        validate_only = body.get('validate_only', False)
        headless = body.get('headless')
        
        # Auto-detect input format
        if 'services' in body and isinstance(body['services'], dict):
            # Pre-standardized format - use directly (skips LLM)
            services_dict = body['services']
            print("[INFO] Using pre-standardized services (no LLM processing needed)")
        else:
            # SOW format detected - needs LLM processing
            if use_llm is None:
                use_llm = True  # Auto-enable LLM for SOW format
            
            if use_llm:
                # Process entire request body as SOW data with LLM
                sow_data = body
                print("[INFO] Detected SOW format - processing with LLM...")
                services_dict = process_with_llm(sow_data)
            else:
                # Try to find services in nested structure (without LLM)
                if 'services' in body.get('result', {}):
                    services_dict = body['result']['services']
                elif 'services' in body:
                    services_dict = body['services']
                else:
                    raise HTTPException(
                        status_code=400,
                        detail="No 'services' key found. Set 'use_llm': true to process SOW JSON, or provide standardized 'services' structure."
                    )
        
        if not services_dict:
            raise HTTPException(
                status_code=400,
                detail="No services found in input"
            )
        
        # Validate services
        validation_results = validate_services(services_dict)
        
        # If validate-only, return validation results
        if validate_only:
            return EstimateResponse(
                success=True,
                estimate_url=None,
                message="Validation completed (validate_only=true)",
                services_added=None,
                validation_results=validation_results,
                timestamp=datetime.now().isoformat()
            )
        
        # Build estimate (run in thread executor to avoid async/sync conflicts)
        result = await build_estimate(services_dict, headless=headless)
        
        # Build message with skipped services info
        message = f"Estimate created successfully. {result['total_successful']}/{result['total_services']} services added."
        if result.get('skipped_count', 0) > 0:
            message += f" {result['skipped_count']} service(s) skipped."
        
        return EstimateResponse(
            success=True,
            estimate_url=result["url"],
            message=message,
            services_added=result["services_added"],
            validation_results=validation_results,
            skipped_services=result.get("skipped_services", []),
            skipped_count=result.get("skipped_count", 0),
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid request format: {str(e)}. Make sure to send valid JSON with Content-Type: application/json"
        )
    except TypeError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid data type: {str(e)}. Expected JSON object."
        )
    except Exception as e:
        import traceback
        error_msg = str(e)
        # Check if it's a JSON decode error
        if "JSON" in error_msg or "json" in error_msg.lower() or "plain" in error_msg.lower():
            raise HTTPException(
                status_code=400,
                detail=f"JSON parsing error: {error_msg}. Make sure to set Content-Type: application/json header and send valid JSON."
            )
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Internal error: {error_msg}"
        )


@app.get("/services")
async def list_services():
    """List all available AWS services"""
    try:
        from aws_services.service_registry import list_available_services, SERVICE_ALIASES
        
        available_services = list_available_services()
        
        return {
            "services": available_services,
            "aliases": SERVICE_ALIASES,
            "total": len(available_services)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list services: {str(e)}")


@app.get("/services/{service_type}")
async def get_service_info(service_type: str):
    """Get information about a specific service"""
    try:
        from aws_services.service_registry import get_service_info
        
        info = get_service_info(service_type)
        
        if not info:
            raise HTTPException(
                status_code=404,
                detail=f"Service '{service_type}' not found"
            )
        
        return info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get service info: {str(e)}")


# Background task endpoint (for async processing)
@app.post("/estimate/async")
async def create_estimate_async(request: EstimateRequest, background_tasks: BackgroundTasks):
    """
    Create estimate asynchronously (returns job ID immediately)
    
    Note: For full async support, consider using Celery or similar task queue
    """
    # For now, this is a placeholder - you'd need to implement proper async job handling
    raise HTTPException(
        status_code=501,
        detail="Async endpoint not yet implemented. Use /estimate endpoint for synchronous processing."
    )


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"Starting AWS Billing Automation API server on {host}:{port}")
    print(f"API Documentation available at: http://{host}:{port}/docs")
    
    uvicorn.run(
        "api_server:app",
        host=host,
        port=port,
        reload=True if os.getenv("DEBUG", "False").lower() == "true" else False
    )

