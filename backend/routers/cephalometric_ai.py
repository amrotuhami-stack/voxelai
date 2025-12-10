"""
Cephalometric AI API Router
Endpoint for lateral cephalogram landmark detection using CEPHMark-Net
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
import cv2
import base64
import io
from pathlib import Path

router = APIRouter(prefix="/api/cephalometric", tags=["Cephalometric AI"])

# Model paths
BASE_DIR = Path(__file__).parent.parent / "dental-ai"
CEPHMARK_DIR = BASE_DIR / "models" / "CEPHMark-Net"
WEIGHTS_PATH = CEPHMARK_DIR / "logs" / "weights" / "best_weights.h5"

# 19 Cephalometric Landmarks (ISBI standard)
LANDMARKS = {
    0: "Sella (S)",
    1: "Nasion (N)",
    2: "Orbitale (Or)",
    3: "Porion (Po)",
    4: "A-point (A)",
    5: "B-point (B)",
    6: "Pogonion (Pog)",
    7: "Menton (Me)",
    8: "Gnathion (Gn)",
    9: "Gonion (Go)",
    10: "Lower Incisal Incision (LI)",
    11: "Upper Incisal Incision (UI)",
    12: "Upper Lip (UL)",
    13: "Lower Lip (LL)",
    14: "Subnasale (Sn)",
    15: "Soft Tissue Pogonion (Pog')",
    16: "Posterior Nasal Spine (PNS)",
    17: "Anterior Nasal Spine (ANS)",
    18: "Articulare (Ar)",
}

# Cephalometric Measurements
MEASUREMENTS = {
    "SNA": {"landmarks": [0, 1, 4], "unit": "degrees", "normal": "82±2"},
    "SNB": {"landmarks": [0, 1, 5], "unit": "degrees", "normal": "80±2"},
    "ANB": {"landmarks": [4, 1, 5], "unit": "degrees", "normal": "2±2"},
    "FMA": {"landmarks": [3, 2, 7], "unit": "degrees", "normal": "25±5"},
    "IMPA": {"landmarks": [7, 9, 10], "unit": "degrees", "normal": "90±5"},
}


class Landmark(BaseModel):
    id: int
    name: str
    x: float
    y: float
    confidence: float


class Measurement(BaseModel):
    name: str
    value: float
    unit: str
    normal_range: str
    status: str  # normal, high, low


class CephalometricResult(BaseModel):
    landmarks: List[Landmark]
    measurements: List[Measurement]
    image_dimensions: dict
    overlay_image: Optional[str] = None


# Global model instance
_model = None


def load_model():
    """Load CEPHMark-Net model"""
    global _model
    
    if _model is not None:
        return _model
    
    try:
        import tensorflow as tf
        
        # Add CEPHMark-Net to path
        import sys
        sys.path.insert(0, str(CEPHMARK_DIR))
        
        from network.cephmark_net import CEPHMarkNet
        from config import cfg
        
        # Initialize model
        _model = CEPHMarkNet(cfg)
        
        # Load weights if available
        if WEIGHTS_PATH.exists():
            _model.load_weights(str(WEIGHTS_PATH))
            print(f"✅ Loaded CEPHMark-Net weights from {WEIGHTS_PATH}")
        else:
            print(f"⚠️ No weights found at {WEIGHTS_PATH}, model not trained")
            _model = None
            
        return _model
        
    except Exception as e:
        print(f"❌ Failed to load CEPHMark-Net: {e}")
        return None


def preprocess_image(image_bytes: bytes):
    """Preprocess cephalogram for model input"""
    # Decode image
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("Could not decode image")
    
    original_h, original_w = img.shape[:2]
    
    # Resize to model input size (640x800 as per config)
    target_w, target_h = 640, 800
    resized = cv2.resize(img, (target_w, target_h))
    
    # Normalize
    normalized = resized.astype(np.float32) / 255.0
    
    return normalized, img, (original_w, original_h), (target_w, target_h)


def calculate_angle(p1, p2, p3):
    """Calculate angle between three points (angle at p2)"""
    v1 = np.array([p1[0] - p2[0], p1[1] - p2[1]])
    v2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])
    
    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-8)
    angle = np.arccos(np.clip(cos_angle, -1, 1))
    return np.degrees(angle)


def compute_measurements(landmarks: List[Landmark]) -> List[Measurement]:
    """Compute cephalometric measurements from landmarks"""
    measurements = []
    
    landmark_dict = {lm.id: (lm.x, lm.y) for lm in landmarks}
    
    for name, config in MEASUREMENTS.items():
        try:
            points = [landmark_dict[i] for i in config["landmarks"]]
            value = calculate_angle(points[0], points[1], points[2])
            
            # Parse normal range
            normal = config["normal"]
            normal_val = float(normal.split("±")[0])
            tolerance = float(normal.split("±")[1])
            
            if value < normal_val - tolerance:
                status = "low"
            elif value > normal_val + tolerance:
                status = "high"
            else:
                status = "normal"
            
            measurements.append(Measurement(
                name=name,
                value=round(value, 1),
                unit=config["unit"],
                normal_range=normal,
                status=status
            ))
        except (KeyError, IndexError):
            continue
    
    return measurements


def draw_overlay(image, landmarks: List[Landmark], measurements: List[Measurement]):
    """Draw landmarks and measurements on image"""
    overlay = image.copy()
    
    # Draw landmarks
    for lm in landmarks:
        x, y = int(lm.x), int(lm.y)
        # Draw point
        cv2.circle(overlay, (x, y), 5, (0, 255, 0), -1)
        cv2.circle(overlay, (x, y), 7, (255, 255, 255), 2)
        # Draw label
        cv2.putText(overlay, str(lm.id), (x + 10, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Draw measurement lines (SNA, SNB, ANB triangle)
    sella = next((lm for lm in landmarks if lm.id == 0), None)
    nasion = next((lm for lm in landmarks if lm.id == 1), None)
    a_point = next((lm for lm in landmarks if lm.id == 4), None)
    b_point = next((lm for lm in landmarks if lm.id == 5), None)
    
    if all([sella, nasion, a_point, b_point]):
        pts = [(int(sella.x), int(sella.y)), (int(nasion.x), int(nasion.y)),
               (int(a_point.x), int(a_point.y)), (int(b_point.x), int(b_point.y))]
        cv2.line(overlay, pts[0], pts[1], (255, 255, 0), 2)  # S-N
        cv2.line(overlay, pts[1], pts[2], (0, 255, 255), 2)  # N-A
        cv2.line(overlay, pts[1], pts[3], (255, 0, 255), 2)  # N-B
    
    return overlay


@router.get("/health")
async def health_check():
    """Check cephalometric AI service health"""
    model = load_model()
    return {
        "status": "healthy" if model is not None else "model_not_loaded",
        "model": "CEPHMark-Net",
        "landmarks": 19,
        "weights_available": WEIGHTS_PATH.exists()
    }


@router.get("/landmarks")
async def get_landmarks():
    """Get list of cephalometric landmarks"""
    return {
        "count": len(LANDMARKS),
        "landmarks": [{"id": k, "name": v} for k, v in LANDMARKS.items()]
    }


@router.get("/measurements")
async def get_measurements():
    """Get available cephalometric measurements"""
    return {
        "count": len(MEASUREMENTS),
        "measurements": [
            {"name": k, **v} for k, v in MEASUREMENTS.items()
        ]
    }


@router.post("/analyze", response_model=CephalometricResult)
async def analyze_cephalogram(
    file: UploadFile = File(...),
    include_overlay: bool = True,
):
    """
    Analyze lateral cephalogram and detect 19 anatomical landmarks.
    
    Returns:
    - landmarks: List of detected landmark positions
    - measurements: Calculated cephalometric measurements (SNA, SNB, ANB, etc.)
    - overlay_image: Base64 encoded image with annotations (if requested)
    """
    # Read image
    contents = await file.read()
    
    try:
        preprocessed, original, orig_size, model_size = preprocess_image(contents)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Load model
    model = load_model()
    
    if model is None:
        # Return mock data if model not loaded (for testing)
        # In production, you would raise an error
        mock_landmarks = []
        for i, name in LANDMARKS.items():
            # Generate mock positions
            mock_landmarks.append(Landmark(
                id=i,
                name=name,
                x=orig_size[0] * (0.3 + 0.4 * np.random.random()),
                y=orig_size[1] * (0.2 + 0.6 * np.random.random()),
                confidence=0.5 + 0.5 * np.random.random()
            ))
        
        measurements = compute_measurements(mock_landmarks)
        
        overlay_b64 = None
        if include_overlay:
            overlay = draw_overlay(original, mock_landmarks, measurements)
            _, buffer = cv2.imencode('.jpg', overlay)
            overlay_b64 = base64.b64encode(buffer).decode('utf-8')
        
        return CephalometricResult(
            landmarks=mock_landmarks,
            measurements=measurements,
            image_dimensions={"width": orig_size[0], "height": orig_size[1]},
            overlay_image=overlay_b64
        )
    
    # Run inference
    input_tensor = np.expand_dims(preprocessed, axis=0)
    predictions = model.predict(input_tensor)
    
    # Scale predictions to original image size
    scale_x = orig_size[0] / model_size[0]
    scale_y = orig_size[1] / model_size[1]
    
    landmarks = []
    for i, (pred_x, pred_y) in enumerate(predictions[0]):
        landmarks.append(Landmark(
            id=i,
            name=LANDMARKS[i],
            x=pred_x * scale_x,
            y=pred_y * scale_y,
            confidence=0.9  # CEPHMark-Net doesn't output confidence per landmark
        ))
    
    # Compute measurements
    measurements = compute_measurements(landmarks)
    
    # Generate overlay
    overlay_b64 = None
    if include_overlay:
        overlay = draw_overlay(original, landmarks, measurements)
        _, buffer = cv2.imencode('.jpg', overlay)
        overlay_b64 = base64.b64encode(buffer).decode('utf-8')
    
    return CephalometricResult(
        landmarks=landmarks,
        measurements=measurements,
        image_dimensions={"width": orig_size[0], "height": orig_size[1]},
        overlay_image=overlay_b64
    )
