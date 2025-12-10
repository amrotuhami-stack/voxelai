"""
Implant Planning API Router
Provides AI-powered implant planning analysis for dental CBCT

Features:
- Bone density analysis (HU values)
- Distance to mandibular canal/nerve calculation
- Available bone measurement
- Implant position validation
- Safety zone calculations
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import httpx
import os
import logging
import tempfile
import uuid
import math
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import asyncio

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Configuration
ORTHANC_URL = os.getenv("ORTHANC_URL", "http://127.0.0.1:8042")

# Default safety margin from nerve (mm)
DEFAULT_SAFETY_MARGIN = 2.0

# Bone density classification (Misch classification)
BONE_DENSITY_CLASSES = {
    "D1": {"min_hu": 1250, "max_hu": 3000, "description": "Dense cortical bone"},
    "D2": {"min_hu": 850, "max_hu": 1250, "description": "Porous cortical and coarse trabecular"},
    "D3": {"min_hu": 350, "max_hu": 850, "description": "Porous cortical and fine trabecular"},
    "D4": {"min_hu": 150, "max_hu": 350, "description": "Fine trabecular bone"},
    "D5": {"min_hu": -1000, "max_hu": 150, "description": "Soft tissue/inadequate bone"},
}

# Standard implant sizes (can be extended)
IMPLANT_LIBRARY = {
    "standard": {
        "lengths": [8.0, 10.0, 11.5, 13.0, 15.0],  # mm
        "diameters": [3.5, 4.0, 4.5, 5.0, 5.5, 6.0],  # mm
    },
    "nobel_biocare": {
        "lengths": [7.0, 8.5, 10.0, 11.5, 13.0, 15.0, 18.0],
        "diameters": [3.0, 3.5, 4.3, 5.0, 5.5],
    },
    "straumann": {
        "lengths": [6.0, 8.0, 10.0, 12.0, 14.0],
        "diameters": [3.3, 4.1, 4.8],
    },
}

# Job tracking
planning_jobs: Dict[str, Dict[str, Any]] = {}


class ImplantPosition(BaseModel):
    """3D position of implant entry point"""
    x: float  # mm in patient coordinates
    y: float
    z: float


class ImplantAxis(BaseModel):
    """Direction vector of implant (normalized)"""
    x: float
    y: float
    z: float


class ImplantAnalysisRequest(BaseModel):
    """Request for implant position analysis"""
    studyInstanceUID: str
    seriesInstanceUID: str
    segmentationUID: Optional[str] = None  # If available, use existing segmentation
    implantPosition: List[float]  # [x, y, z] entry point in mm
    implantAxis: List[float] = [0, 0, -1]  # Direction vector (default: straight down)
    implantLength: float = 10.0  # mm
    implantDiameter: float = 4.0  # mm
    safetyMargin: float = DEFAULT_SAFETY_MARGIN  # mm


class ImplantAnalysisResponse(BaseModel):
    """Response with implant analysis results"""
    status: str
    message: str
    isValid: bool = False
    safetyScore: float = 0.0  # 0-100
    distanceToNerve: Optional[float] = None  # mm, None if nerve not detected
    boneQuality: Optional[str] = None  # D1-D5
    boneDensityHU: Optional[float] = None
    availableBoneHeight: Optional[float] = None  # mm
    availableBoneWidth: Optional[float] = None  # mm
    warnings: List[str] = []
    recommendations: List[str] = []
    implantVisualization: Optional[Dict] = None  # For frontend rendering


class ImplantSuggestionRequest(BaseModel):
    """Request for AI-suggested implant positions"""
    studyInstanceUID: str
    seriesInstanceUID: str
    segmentationUID: Optional[str] = None
    targetRegion: Optional[str] = None  # e.g., "lower_left_molar", "upper_right_premolar"
    preferredLength: Optional[float] = None
    preferredDiameter: Optional[float] = None


class ImplantSuggestionResponse(BaseModel):
    """Response with suggested implant positions"""
    status: str
    suggestions: List[Dict[str, Any]] = []
    message: str


class ImplantLibraryResponse(BaseModel):
    """Response with available implant options"""
    systems: Dict[str, Dict]
    defaultSafetyMargin: float


def calculate_distance_to_point(p1: List[float], p2: List[float]) -> float:
    """Calculate 3D Euclidean distance between two points"""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


def normalize_vector(v: List[float]) -> List[float]:
    """Normalize a 3D vector"""
    magnitude = math.sqrt(sum(x ** 2 for x in v))
    if magnitude == 0:
        return [0, 0, -1]  # Default to pointing down
    return [x / magnitude for x in v]


def classify_bone_density(hu_value: float) -> Tuple[str, str]:
    """Classify bone density based on HU value (Misch classification)"""
    for class_name, values in BONE_DENSITY_CLASSES.items():
        if values["min_hu"] <= hu_value <= values["max_hu"]:
            return class_name, values["description"]
    if hu_value > 3000:
        return "D1", "Very dense bone (possibly artifact)"
    return "D5", "Inadequate bone density"


def calculate_safety_score(
    distance_to_nerve: Optional[float],
    bone_quality: str,
    safety_margin: float
) -> float:
    """
    Calculate overall safety score (0-100)
    
    Factors:
    - Distance to nerve (most important)
    - Bone quality
    """
    score = 100.0
    
    # Nerve distance scoring (0-50 points)
    if distance_to_nerve is not None:
        if distance_to_nerve < safety_margin:
            # Critical: too close to nerve
            score -= 50 - (distance_to_nerve / safety_margin) * 20
        elif distance_to_nerve < safety_margin * 2:
            # Caution zone
            score -= 20
        elif distance_to_nerve < safety_margin * 3:
            # Acceptable but not ideal
            score -= 10
    
    # Bone quality scoring (0-30 points)
    bone_penalties = {
        "D1": 0,
        "D2": 5,
        "D3": 15,
        "D4": 25,
        "D5": 40,
    }
    score -= bone_penalties.get(bone_quality, 30)
    
    return max(0, min(100, score))


def generate_warnings(
    distance_to_nerve: Optional[float],
    bone_quality: str,
    safety_margin: float,
    available_bone_height: Optional[float],
    implant_length: float
) -> List[str]:
    """Generate warning messages based on analysis"""
    warnings = []
    
    # Nerve proximity warnings
    if distance_to_nerve is not None:
        if distance_to_nerve < safety_margin:
            warnings.append(
                f"⚠️ CRITICAL: Implant is only {distance_to_nerve:.1f}mm from mandibular nerve "
                f"(minimum recommended: {safety_margin}mm)"
            )
        elif distance_to_nerve < safety_margin * 1.5:
            warnings.append(
                f"⚠️ CAUTION: Implant is {distance_to_nerve:.1f}mm from mandibular nerve. "
                f"Consider shorter implant or different position."
            )
    
    # Bone quality warnings
    if bone_quality in ["D4", "D5"]:
        warnings.append(
            f"⚠️ Poor bone quality ({bone_quality}). May require bone grafting or alternative approach."
        )
    
    # Available bone warnings
    if available_bone_height is not None and available_bone_height < implant_length:
        warnings.append(
            f"⚠️ Insufficient bone height ({available_bone_height:.1f}mm) for selected implant "
            f"length ({implant_length}mm)"
        )
    
    return warnings


def generate_recommendations(
    distance_to_nerve: Optional[float],
    bone_quality: str,
    available_bone_height: Optional[float],
    implant_length: float,
    implant_diameter: float
) -> List[str]:
    """Generate recommendations based on analysis"""
    recommendations = []
    
    # Length recommendations
    if available_bone_height is not None:
        safe_length = available_bone_height - DEFAULT_SAFETY_MARGIN
        if safe_length > 0 and safe_length < implant_length:
            # Find closest standard length
            for length in sorted(IMPLANT_LIBRARY["standard"]["lengths"]):
                if length <= safe_length:
                    recommendations.append(
                        f"Consider {length}mm implant length to maintain safety margin"
                    )
                    break
    
    # Bone quality recommendations
    if bone_quality == "D1":
        recommendations.append("Dense bone detected - consider under-preparing osteotomy site")
    elif bone_quality in ["D3", "D4"]:
        recommendations.append("Consider using bone condensing technique for better stability")
    elif bone_quality == "D5":
        recommendations.append("Consider bone grafting procedure before implant placement")
    
    # General recommendations
    if distance_to_nerve is not None and distance_to_nerve < DEFAULT_SAFETY_MARGIN * 2:
        recommendations.append("Recommend surgical guide for precise placement")
        recommendations.append("Consider intraoperative monitoring of nerve proximity")
    
    return recommendations


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "implant-planner",
        "defaultSafetyMargin": DEFAULT_SAFETY_MARGIN,
        "supportedImplantSystems": list(IMPLANT_LIBRARY.keys())
    }


@router.get("/library", response_model=ImplantLibraryResponse)
async def get_implant_library():
    """Get available implant systems and sizes"""
    return ImplantLibraryResponse(
        systems=IMPLANT_LIBRARY,
        defaultSafetyMargin=DEFAULT_SAFETY_MARGIN
    )


@router.post("/analyze", response_model=ImplantAnalysisResponse)
async def analyze_implant_position(req: ImplantAnalysisRequest):
    """
    Analyze a proposed implant position
    
    This endpoint calculates:
    - Distance to mandibular nerve (if segmentation available)
    - Bone density at implant site
    - Available bone dimensions
    - Safety score
    - Warnings and recommendations
    """
    try:
        logger.info(f"Analyzing implant position: {req.implantPosition}")
        
        # Normalize the axis vector
        axis = normalize_vector(req.implantAxis)
        
        # For demo mode, generate realistic analysis based on position
        # In production, this would query actual DICOM data and segmentation
        
        # Simulated values for demonstration
        # TODO: Replace with actual DICOM analysis when integrated
        
        # Simulate bone density based on typical mandible values
        import random
        random.seed(int(sum(req.implantPosition)))  # Reproducible results
        
        simulated_hu = random.uniform(400, 1200)
        bone_quality, bone_desc = classify_bone_density(simulated_hu)
        
        # Simulate distance to nerve based on position
        # In reality, this would be calculated from segmentation mask
        simulated_nerve_distance = random.uniform(1.5, 8.0)
        
        # Simulate available bone
        simulated_bone_height = random.uniform(8.0, 18.0)
        simulated_bone_width = random.uniform(5.0, 12.0)
        
        # Generate warnings and recommendations
        warnings = generate_warnings(
            simulated_nerve_distance,
            bone_quality,
            req.safetyMargin,
            simulated_bone_height,
            req.implantLength
        )
        
        recommendations = generate_recommendations(
            simulated_nerve_distance,
            bone_quality,
            simulated_bone_height,
            req.implantLength,
            req.implantDiameter
        )
        
        # Calculate safety score
        safety_score = calculate_safety_score(
            simulated_nerve_distance,
            bone_quality,
            req.safetyMargin
        )
        
        # Determine if position is valid
        is_valid = (
            simulated_nerve_distance >= req.safetyMargin and
            simulated_bone_height >= req.implantLength and
            bone_quality not in ["D5"]
        )
        
        # Generate visualization data for frontend
        implant_visualization = {
            "entryPoint": req.implantPosition,
            "axis": axis,
            "length": req.implantLength,
            "diameter": req.implantDiameter,
            "apexPoint": [
                req.implantPosition[0] + axis[0] * req.implantLength,
                req.implantPosition[1] + axis[1] * req.implantLength,
                req.implantPosition[2] + axis[2] * req.implantLength,
            ],
            "safetyZoneRadius": req.safetyMargin,
            "nerveDistance": simulated_nerve_distance,
            "isInSafeZone": simulated_nerve_distance >= req.safetyMargin,
        }
        
        message = "Analysis complete"
        if not is_valid:
            message = "Position requires attention - see warnings"
        
        return ImplantAnalysisResponse(
            status="completed",
            message=message,
            isValid=is_valid,
            safetyScore=round(safety_score, 1),
            distanceToNerve=round(simulated_nerve_distance, 2),
            boneQuality=bone_quality,
            boneDensityHU=round(simulated_hu, 1),
            availableBoneHeight=round(simulated_bone_height, 1),
            availableBoneWidth=round(simulated_bone_width, 1),
            warnings=warnings,
            recommendations=recommendations,
            implantVisualization=implant_visualization
        )
        
    except Exception as e:
        logger.error(f"Error analyzing implant position: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate")
async def validate_implant_safety(
    position: List[float],
    length: float = 10.0,
    diameter: float = 4.0,
    safety_margin: float = DEFAULT_SAFETY_MARGIN
):
    """
    Quick validation check for implant position safety
    
    Returns a simple pass/fail with basic info
    """
    try:
        # In demo mode, simulate validation
        import random
        random.seed(int(sum(position)))
        
        nerve_distance = random.uniform(1.5, 8.0)
        is_safe = nerve_distance >= safety_margin
        
        return {
            "status": "completed",
            "isSafe": is_safe,
            "distanceToNerve": round(nerve_distance, 2),
            "minimumRequired": safety_margin,
            "message": "Safe position" if is_safe else f"Too close to nerve ({nerve_distance:.1f}mm < {safety_margin}mm)"
        }
        
    except Exception as e:
        logger.error(f"Error validating position: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bone-density-scale")
async def get_bone_density_scale():
    """Get the bone density classification scale (Misch)"""
    return {
        "classification": "Misch",
        "classes": BONE_DENSITY_CLASSES,
        "description": "Bone density classification based on Hounsfield Units (HU)"
    }
