"""
3D Slicer Processing Endpoints
Handles requests from OHIF to trigger Slicer jobs
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

SLICER_HOST = os.getenv("SLICER_HOST", "slicer")
SLICER_PORT = int(os.getenv("SLICER_PORT", "5005"))
SLICER_URL = f"http://{SLICER_HOST}:{SLICER_PORT}"

class SlicerJobRequest(BaseModel):
    """Request model for Slicer processing jobs"""
    studyInstanceUID: str
    seriesInstanceUID: str

class SlicerJobResponse(BaseModel):
    """Response model for Slicer jobs"""
    status: str
    message: str
    job_id: str | None = None
    data: dict | None = None

@router.post("/segment", response_model=SlicerJobResponse)
async def trigger_segmentation(req: SlicerJobRequest):
    """
    Trigger CBCT segmentation in 3D Slicer
    
    This endpoint:
    1. Forwards the request to Slicer server
    2. Slicer loads CBCT from Orthanc
    3. Runs automatic segmentation
    4. Exports DICOM SEG back to Orthanc
    5. Returns segmentation UID
    
    Args:
        req: Request containing study and series UIDs
        
    Returns:
        SlicerJobResponse with segmentation details
    """
    try:
        logger.info(f"Segmentation requested for series: {req.seriesInstanceUID}")
        
        async with httpx.AsyncClient(timeout=600.0) as client:
            response = await client.post(
                f"{SLICER_URL}/segment",
                json={
                    "studyInstanceUID": req.studyInstanceUID,
                    "seriesInstanceUID": req.seriesInstanceUID
                }
            )
        
        if response.status_code != 200:
            error_detail = response.text
            logger.error(f"Slicer error: {error_detail}")
            raise HTTPException(
                status_code=500,
                detail=f"Slicer segmentation failed: {error_detail}"
            )
        
        result = response.json()
        logger.info(f"Segmentation completed: {result}")
        
        return SlicerJobResponse(
            status="success",
            message="Segmentation completed and stored in Orthanc",
            job_id=result.get("segmentation_uid"),
            data=result
        )
        
    except httpx.RequestError as e:
        logger.error(f"Slicer connection error: {e}")
        raise HTTPException(
            status_code=503,
            detail="3D Slicer server unavailable. Please ensure Slicer container is running."
        )
    except Exception as e:
        logger.error(f"Segmentation error: {e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/model", response_model=SlicerJobResponse)
async def generate_3d_model(req: SlicerJobRequest):
    """
    Generate 3D model (STL/GLB) from CBCT
    
    This endpoint:
    1. Triggers 3D model generation in Slicer
    2. Exports segmentation as STL/GLB
    3. Returns URL to download model
    
    Args:
        req: Request containing study and series UIDs
        
    Returns:
        SlicerJobResponse with model URL
    """
    try:
        logger.info(f"3D model generation requested for series: {req.seriesInstanceUID}")
        
        async with httpx.AsyncClient(timeout=600.0) as client:
            response = await client.post(
                f"{SLICER_URL}/model",
                json={
                    "studyInstanceUID": req.studyInstanceUID,
                    "seriesInstanceUID": req.seriesInstanceUID
                }
            )
        
        if response.status_code != 200:
            error_detail = response.text
            logger.error(f"Slicer error: {error_detail}")
            raise HTTPException(
                status_code=500,
                detail=f"Model generation failed: {error_detail}"
            )
        
        result = response.json()
        logger.info(f"Model generation completed: {result}")
        
        return SlicerJobResponse(
            status="success",
            message="3D model generated successfully",
            data=result
        )
        
    except httpx.RequestError as e:
        logger.error(f"Slicer connection error: {e}")
        raise HTTPException(
            status_code=503,
            detail="3D Slicer server unavailable"
        )
    except Exception as e:
        logger.error(f"Model generation error: {e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/panoramic", response_model=SlicerJobResponse)
async def generate_panoramic(req: SlicerJobRequest):
    """
    Generate panoramic reconstruction from CBCT
    
    This endpoint:
    1. Triggers panoramic CPR generation in Slicer
    2. Creates curved planar reformation
    3. Exports as new DICOM series to Orthanc
    4. Returns new series UID
    
    Args:
        req: Request containing study and series UIDs
        
    Returns:
        SlicerJobResponse with panoramic series UID
    """
    try:
        logger.info(f"Panoramic reconstruction requested for series: {req.seriesInstanceUID}")
        
        async with httpx.AsyncClient(timeout=600.0) as client:
            response = await client.post(
                f"{SLICER_URL}/panoramic",
                json={
                    "studyInstanceUID": req.studyInstanceUID,
                    "seriesInstanceUID": req.seriesInstanceUID
                }
            )
        
        if response.status_code != 200:
            error_detail = response.text
            logger.error(f"Slicer error: {error_detail}")
            raise HTTPException(
                status_code=500,
                detail=f"Panoramic generation failed: {error_detail}"
            )
        
        result = response.json()
        logger.info(f"Panoramic generation completed: {result}")
        
        return SlicerJobResponse(
            status="success",
            message="Panoramic reconstruction completed",
            data=result
        )
        
    except httpx.RequestError as e:
        logger.error(f"Slicer connection error: {e}")
        raise HTTPException(
            status_code=503,
            detail="3D Slicer server unavailable"
        )
    except Exception as e:
        logger.error(f"Panoramic generation error: {e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/health")
async def slicer_health():
    """
    Check 3D Slicer server health
    
    Returns:
        Health status of Slicer server
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{SLICER_URL}/health")
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=503,
                detail="Slicer server unhealthy"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Slicer server unavailable: {str(e)}"
        )
