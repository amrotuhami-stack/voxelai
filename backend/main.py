"""
Voxel3Di Backend API
Orchestrates 3D Slicer processing jobs for CBCT analysis
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import slicer, dental_segmentator, implant_planner, panoramic_generator, dental_ai_opg
import os

app = FastAPI(
    title="Voxel3Di Backend API",
    description="CBCT Processing with 3D Slicer Integration and AI Segmentation",
    version="1.0.0"
)

# CORS configuration - allow VoxelApp frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8082",
        "http://localhost:8082",
        "http://127.0.0.1:8042",  # OHIF
        "http://localhost:8042",
        "http://127.0.0.1:3000",  # OHIF dev server
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(slicer.router, prefix="/process/slicer", tags=["slicer"])
app.include_router(dental_segmentator.router, prefix="/process/dental-segmentator", tags=["dental-segmentator"])
app.include_router(implant_planner.router, prefix="/process/implant-planner", tags=["implant-planner"])
app.include_router(panoramic_generator.router, prefix="/process/panoramic", tags=["panoramic"])
app.include_router(dental_ai_opg.router)  # OPG AI analysis (has its own /api/dental-ai prefix)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "voxel3di-backend",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Voxel3Di Backend API",
        "docs": "/docs",
        "health": "/health"
    }
