"""
Dental AI API Router for OPG/Panoramic X-ray Analysis

Provides endpoints for:
- Tooth detection with FDI numbering
- Pathology detection (caries, periapical, impacted)
- Instance segmentation masks
- Report generation
"""

import os
import io
import base64
import json
from pathlib import Path
from typing import Optional, List
from datetime import datetime

import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

# Import label schema
import sys
sys.path.append(str(Path(__file__).parent.parent / "dental-ai" / "scripts"))
try:
    from label_schema import FDI_TOOTH_NAMES, LESION_TYPES, TOOTH_TYPES
except ImportError:
    # Fallback definitions
    FDI_TOOTH_NAMES = {f"{q}{t}": f"Tooth {q}{t}" for q in [1,2,3,4] for t in range(1,9)}
    LESION_TYPES = {"caries": {"id": 1}, "periapical_lesion": {"id": 2}, "impacted": {"id": 3}}
    TOOTH_TYPES = {}

# Configuration
MODEL_DIR = Path(__file__).parent.parent / "dental-ai" / "models"
TOOTH_MODEL_PATH = MODEL_DIR / "yolov8" / "dental_unified_v2" / "weights" / "best.pt"

# Initialize router
router = APIRouter(prefix="/api/dental-ai", tags=["Dental AI OPG"])

# Global model cache
_model_cache = {}


# ============ Pydantic Models ============

class ToothDetection(BaseModel):
    """Single tooth detection result"""
    tooth_id: str                      # FDI number (e.g., "11", "36")
    tooth_name: str                    # Full name
    tooth_type: str                    # "incisor", "canine", "premolar", "molar"
    bbox: List[float]                  # [x1, y1, x2, y2] in pixels
    confidence: float
    mask: Optional[str] = None         # Base64-encoded mask (if segmentation)


class LesionDetection(BaseModel):
    """Single lesion detection result"""
    lesion_type: str                   # "caries", "periapical_lesion", "impacted"
    tooth_id: Optional[str] = None     # Associated tooth FDI number
    bbox: List[float]                  # [x1, y1, x2, y2]
    confidence: float
    severity: Optional[str] = None


class AnalysisResult(BaseModel):
    """Complete OPG analysis result"""
    image_id: str
    timestamp: str
    teeth: List[ToothDetection]
    lesions: List[LesionDetection]
    summary: dict
    overlay_image: Optional[str] = None  # Base64-encoded annotated image


class AnalysisRequest(BaseModel):
    """Analysis request parameters"""
    include_overlay: bool = True
    include_masks: bool = False
    confidence_threshold: float = 0.5


# ============ Helper Functions ============

def load_model():
    """Load YOLOv8 model (cached)"""
    if "tooth_model" not in _model_cache:
        if not TOOTH_MODEL_PATH.exists():
            raise HTTPException(
                status_code=503,
                detail=f"Tooth detection model not found. Please train the model first."
            )

        from ultralytics import YOLO
        _model_cache["tooth_model"] = YOLO(str(TOOTH_MODEL_PATH))

    return _model_cache["tooth_model"]


def get_tooth_type(fdi: str) -> str:
    """Get tooth type from FDI number"""
    for ttype, fdi_list in TOOTH_TYPES.items():
        if fdi in fdi_list:
            return ttype
    return "unknown"


def class_id_to_fdi(class_id: int) -> Optional[str]:
    """Convert YOLO class ID to FDI number"""
    if class_id < 32:
        # Tooth class: map back to FDI
        quadrant = (class_id // 8) + 1
        position = (class_id % 8) + 1
        return f"{quadrant}{position}"
    return None


def class_id_to_lesion(class_id: int) -> Optional[str]:
    """Convert YOLO class ID to lesion type"""
    lesion_map = {32: "caries", 33: "deep_caries", 34: "periapical_lesion", 35: "impacted"}
    return lesion_map.get(class_id)


def generate_overlay(image: np.ndarray, teeth: List[dict], lesions: List[dict]) -> np.ndarray:
    """Generate annotated overlay image"""
    overlay = image.copy()

    # Draw tooth detections (green boxes)
    for tooth in teeth:
        x1, y1, x2, y2 = map(int, tooth["bbox"])
        cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Label
        label = f"{tooth['tooth_id']}"
        cv2.putText(overlay, label, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Draw lesion detections (red boxes)
    lesion_colors = {
        "caries": (0, 0, 255),        # Red
        "deep_caries": (0, 0, 200),   # Dark red
        "periapical_lesion": (0, 165, 255),  # Orange
        "impacted": (255, 0, 128),    # Purple
    }

    for lesion in lesions:
        x1, y1, x2, y2 = map(int, lesion["bbox"])
        color = lesion_colors.get(lesion["lesion_type"], (255, 0, 0))
        cv2.rectangle(overlay, (x1, y1), (x2, y2), color, 2)

        label = lesion["lesion_type"].replace("_", " ").title()
        cv2.putText(overlay, label, (x1, y2 + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

    return overlay


def image_to_base64(image: np.ndarray) -> str:
    """Convert OpenCV image to base64 string"""
    _, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 90])
    return base64.b64encode(buffer).decode('utf-8')


def generate_summary(teeth: List[dict], lesions: List[dict]) -> dict:
    """Generate analysis summary"""
    summary = {
        "total_teeth_detected": len(teeth),
        "teeth_by_quadrant": {1: 0, 2: 0, 3: 0, 4: 0},
        "total_lesions": len(lesions),
        "lesions_by_type": {},
        "affected_teeth": [],
    }

    # Count teeth by quadrant
    for tooth in teeth:
        fdi = tooth["tooth_id"]
        if fdi and len(fdi) >= 1:
            quadrant = int(fdi[0])
            if quadrant in summary["teeth_by_quadrant"]:
                summary["teeth_by_quadrant"][quadrant] += 1

    # Count lesions by type
    for lesion in lesions:
        ltype = lesion["lesion_type"]
        summary["lesions_by_type"][ltype] = summary["lesions_by_type"].get(ltype, 0) + 1
        if lesion.get("tooth_id"):
            summary["affected_teeth"].append(lesion["tooth_id"])

    summary["affected_teeth"] = list(set(summary["affected_teeth"]))

    return summary


# ============ API Endpoints ============

@router.post("/analyze", response_model=AnalysisResult)
async def analyze_opg(
    file: UploadFile = File(...),
    include_overlay: bool = True,
    include_masks: bool = False,
    confidence_threshold: float = 0.5,
):
    """
    Analyze OPG/panoramic X-ray image

    Returns:
    - Tooth detections with FDI numbering
    - Lesion detections (caries, periapical, impacted)
    - Summary statistics
    - Optional annotated overlay image
    """
    # Read and decode image
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # Generate unique image ID
    image_id = f"opg_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(contents) % 10000:04d}"

    try:
        # Load model and run inference
        model = load_model()
        results = model(image, conf=confidence_threshold)

        teeth = []
        lesions = []

        for result in results:
            boxes = result.boxes

            for i in range(len(boxes)):
                class_id = int(boxes.cls[i])
                confidence = float(boxes.conf[i])
                bbox = boxes.xyxy[i].tolist()

                # Determine if tooth or lesion
                fdi = class_id_to_fdi(class_id)
                if fdi:
                    teeth.append({
                        "tooth_id": fdi,
                        "tooth_name": FDI_TOOTH_NAMES.get(fdi, f"Tooth {fdi}"),
                        "tooth_type": get_tooth_type(fdi),
                        "bbox": bbox,
                        "confidence": confidence,
                    })
                else:
                    lesion_type = class_id_to_lesion(class_id)
                    if lesion_type:
                        lesions.append({
                            "lesion_type": lesion_type,
                            "tooth_id": None,  # TODO: Associate with nearest tooth
                            "bbox": bbox,
                            "confidence": confidence,
                        })

        # Generate summary
        summary = generate_summary(teeth, lesions)

        # Generate overlay if requested
        overlay_base64 = None
        if include_overlay:
            overlay = generate_overlay(image, teeth, lesions)
            overlay_base64 = image_to_base64(overlay)

        return AnalysisResult(
            image_id=image_id,
            timestamp=datetime.now().isoformat(),
            teeth=[ToothDetection(**t) for t in teeth],
            lesions=[LesionDetection(**l) for l in lesions],
            summary=summary,
            overlay_image=overlay_base64,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/health")
async def health_check():
    """Check dental AI service health"""
    model_status = "available" if TOOTH_MODEL_PATH.exists() else "not_trained"

    return {
        "status": "healthy",
        "model_status": model_status,
        "model_path": str(TOOTH_MODEL_PATH),
        "supported_tasks": [
            "tooth_detection",
            "fdi_numbering",
            "pathology_detection",
        ],
        "supported_pathologies": list(LESION_TYPES.keys()),
    }


@router.get("/classes")
async def list_classes():
    """List all detection classes"""
    return {
        "teeth": FDI_TOOTH_NAMES,
        "tooth_types": TOOTH_TYPES,
        "lesions": {k: {"id": v["id"]} for k, v in LESION_TYPES.items()},
    }


@router.post("/batch-analyze")
async def batch_analyze(
    files: List[UploadFile] = File(...),
    background_tasks: BackgroundTasks = None,
):
    """
    Analyze multiple OPG images (batch processing)

    Returns job ID for async processing
    """
    # TODO: Implement batch processing with background tasks
    job_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    return {
        "job_id": job_id,
        "status": "queued",
        "total_images": len(files),
        "message": "Batch processing started. Use /batch-status/{job_id} to check progress."
    }


@router.get("/model/info")
async def model_info():
    """Get information about the loaded model"""
    if not TOOTH_MODEL_PATH.exists():
        return {
            "status": "not_trained",
            "message": "Model has not been trained yet. Run training pipeline first."
        }

    try:
        from ultralytics import YOLO
        model = YOLO(str(TOOTH_MODEL_PATH))

        return {
            "status": "available",
            "model_path": str(TOOTH_MODEL_PATH),
            "model_type": "YOLOv8",
            "num_classes": len(model.names) if hasattr(model, 'names') else "unknown",
            "input_size": 1024,
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
        }
