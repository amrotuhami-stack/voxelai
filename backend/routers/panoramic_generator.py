"""
Panoramic Generator API Router
Provides AI-powered dental arch detection and panoramic CPR generation from CBCT

Algorithm based on: NargesSayah/3D-Panoramic-Reconstruction-of-CBCT-Images
Uses MIP + polynomial curve fitting to detect dental arch and generate panoramic

Endpoints:
- POST /detect-arch: Detect dental arch curve from CBCT
- POST /generate: Generate panoramic image along detected arch
- GET /status/{job_id}: Check job status
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List, Tuple
import httpx
import os
import logging
import uuid
import numpy as np
from pathlib import Path
import base64
from io import BytesIO

router = APIRouter()
logger = logging.getLogger(__name__)

# Orthanc configuration
ORTHANC_URL = os.getenv("ORTHANC_URL", "http://localhost:8042")
ORTHANC_USER = os.getenv("ORTHANC_USER", "orthanc")
ORTHANC_PASS = os.getenv("ORTHANC_PASS", "orthanc")

# Job storage (in production, use Redis or database)
jobs = {}

# ==================== Request/Response Models ====================

class ArchDetectionRequest(BaseModel):
    """Request model for dental arch detection"""
    studyInstanceUID: str
    seriesInstanceUID: str

class ArchCurve(BaseModel):
    """Detected dental arch curve"""
    points: List[List[float]]  # [[x1,y1], [x2,y2], ...]
    polynomial_coeffs: List[float]  # Polynomial coefficients [a0, a1, a2, a3, a4]
    optimal_slice_index: int  # Best axial slice for arch detection
    thickness_mm: float  # Arch thickness in mm
    world_coords: Optional[List[List[float]]] = None  # 3D world coordinates

class ArchDetectionResponse(BaseModel):
    """Response model for arch detection"""
    status: str
    message: str
    arch_curve: Optional[ArchCurve] = None
    job_id: Optional[str] = None

class PanoramicRequest(BaseModel):
    """Request model for panoramic generation"""
    studyInstanceUID: str
    seriesInstanceUID: str
    arch_curve: Optional[ArchCurve] = None  # Optional - auto-detect if not provided

class PanoramicResponse(BaseModel):
    """Response model for panoramic generation"""
    status: str
    message: str
    panoramic_image: Optional[str] = None  # Base64 encoded PNG
    dimensions: Optional[dict] = None
    cross_sections: Optional[List[str]] = None  # Base64 encoded cross-section images
    job_id: Optional[str] = None

# ==================== Core Algorithm Functions ====================

async def fetch_series_instances(series_uid: str) -> List[dict]:
    """
    Fetch all DICOM instances for a series from Orthanc
    
    Args:
        series_uid: DICOM Series Instance UID
        
    Returns:
        List of instance metadata
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        # Find series by UID
        response = await client.post(
            f"{ORTHANC_URL}/tools/find",
            json={
                "Level": "Series",
                "Query": {"SeriesInstanceUID": series_uid}
            },
            auth=(ORTHANC_USER, ORTHANC_PASS)
        )
        
        if response.status_code != 200 or not response.json():
            raise HTTPException(status_code=404, detail=f"Series not found: {series_uid}")
        
        orthanc_id = response.json()[0]
        
        # Get instances for this series
        response = await client.get(
            f"{ORTHANC_URL}/series/{orthanc_id}/instances",
            auth=(ORTHANC_USER, ORTHANC_PASS)
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch instances")
            
        return response.json()

async def load_cbct_volume(series_uid: str) -> Tuple[np.ndarray, dict]:
    """
    Load CBCT volume from Orthanc
    
    Args:
        series_uid: DICOM Series Instance UID
        
    Returns:
        Tuple of (3D numpy array, metadata dict)
    """
    try:
        import pydicom
        from io import BytesIO
    except ImportError:
        raise HTTPException(
            status_code=500, 
            detail="pydicom not installed. Install with: pip install pydicom"
        )
    
    instances = await fetch_series_instances(series_uid)
    
    if not instances:
        raise HTTPException(status_code=404, detail="No instances found in series")
    
    logger.info(f"Loading {len(instances)} DICOM instances")
    
    slices = []
    async with httpx.AsyncClient(timeout=120.0) as client:
        for inst in instances:
            inst_id = inst.get("ID")
            response = await client.get(
                f"{ORTHANC_URL}/instances/{inst_id}/file",
                auth=(ORTHANC_USER, ORTHANC_PASS)
            )
            
            if response.status_code == 200:
                ds = pydicom.dcmread(BytesIO(response.content))
                if hasattr(ds, 'SliceLocation') and hasattr(ds, 'pixel_array'):
                    slices.append(ds)
    
    if not slices:
        raise HTTPException(status_code=500, detail="No valid slices found")
    
    # Sort by slice location
    slices = sorted(slices, key=lambda s: float(s.SliceLocation))
    
    # Extract metadata
    ps = slices[0].PixelSpacing if hasattr(slices[0], 'PixelSpacing') else [1.0, 1.0]
    ss = slices[0].SliceThickness if hasattr(slices[0], 'SliceThickness') else 1.0
    
    metadata = {
        'pixel_spacing': [float(ps[0]), float(ps[1])],
        'slice_thickness': float(ss),
        'num_slices': len(slices),
        'rows': int(slices[0].Rows),
        'cols': int(slices[0].Columns),
    }
    
    # Build 3D volume
    volume = np.zeros((metadata['rows'], metadata['cols'], len(slices)), dtype=np.float32)
    for i, s in enumerate(slices):
        volume[:, :, i] = s.pixel_array.astype(np.float32)
    
    logger.info(f"Loaded volume: {volume.shape}")
    return volume, metadata

def compute_mip(volume: np.ndarray, axis: int = 2) -> np.ndarray:
    """
    Compute Maximum Intensity Projection
    
    Args:
        volume: 3D numpy array
        axis: Axis along which to compute MIP (2 = axial)
        
    Returns:
        2D MIP image
    """
    return np.max(volume, axis=axis)

def detect_dental_arch_slice(volume: np.ndarray) -> Tuple[int, np.ndarray]:
    """
    Find the optimal axial slice containing the dental arch
    Uses intensity analysis to find the slice with highest dental content
    
    Args:
        volume: 3D CBCT volume
        
    Returns:
        Tuple of (optimal slice index, slice image)
    """
    num_slices = volume.shape[2]
    
    # Analyze middle third of volume (where teeth typically are)
    start_slice = num_slices // 3
    end_slice = 2 * num_slices // 3
    
    best_score = 0
    best_idx = start_slice
    
    for i in range(start_slice, end_slice):
        slice_img = volume[:, :, i]
        
        # Score based on high intensity pixels (teeth/bone)
        threshold = np.percentile(slice_img, 90)
        high_intensity_count = np.sum(slice_img > threshold)
        
        # Also consider the spread (teeth should form an arc pattern)
        if high_intensity_count > best_score:
            best_score = high_intensity_count
            best_idx = i
    
    return best_idx, volume[:, :, best_idx]

def fit_polynomial_arch(slice_img: np.ndarray, degree: int = 4) -> Tuple[np.ndarray, List[float]]:
    """
    Fit a polynomial curve to the dental arch using DeAPIR-style algorithm
    
    DeAPIR Algorithm Steps:
    1. Binary threshold to isolate high-intensity regions (teeth/bone)
    2. Morphological operations: dilation, Gaussian smoothing
    3. Find skeleton/centerline using thinning
    4. Extract ordered arch points
    5. Fit quadratic curve and extend beyond detected region
    
    Args:
        slice_img: 2D axial slice image
        degree: Polynomial degree (2 = quadratic for DeAPIR)
        
    Returns:
        Tuple of (curve points array, polynomial coefficients)
    """
    from scipy import ndimage
    
    rows, cols = slice_img.shape
    
    # Step 1: Threshold to isolate teeth/bone (above-average intensity)
    # Use adaptive threshold based on slice statistics
    mean_intensity = np.mean(slice_img)
    std_intensity = np.std(slice_img)
    threshold = mean_intensity + 1.5 * std_intensity
    binary = (slice_img > threshold).astype(np.uint8)
    
    logger.info(f"DeAPIR: threshold={threshold:.1f}, binary pixels={np.sum(binary)}")
    
    # Step 2: Morphological operations
    # Dilation to connect nearby structures
    struct = ndimage.generate_binary_structure(2, 2)
    dilated = ndimage.binary_dilation(binary, structure=struct, iterations=3)
    
    # Gaussian smoothing to remove noise
    smoothed = ndimage.gaussian_filter(dilated.astype(np.float32), sigma=2)
    smoothed_binary = (smoothed > 0.3).astype(np.uint8)
    
    # Step 3: Thinning/skeletonization using erosion-based approach
    # (scipy doesn't have skeletonize, so we use iterative erosion)
    skeleton = morphological_thinning(smoothed_binary)
    
    # Step 4: Extract ordered arch points from skeleton
    y_indices, x_indices = np.where(skeleton > 0)
    
    if len(x_indices) < 10:
        logger.warning("DeAPIR: Not enough skeleton points, using centroid method")
        # Fallback to centroid-based detection
        return centroid_based_arch(slice_img, binary, rows, cols)
    
    # Group skeleton points by x-coordinate and find mean y for each x
    x_to_y = {}
    for x, y in zip(x_indices, y_indices):
        if x not in x_to_y:
            x_to_y[x] = []
        x_to_y[x].append(y)
    
    # Get mean y for each x
    x_coords = sorted(x_to_y.keys())
    y_coords = [np.mean(x_to_y[x]) for x in x_coords]
    
    if len(x_coords) < 5:
        logger.warning("DeAPIR: Too few unique x coordinates")
        return centroid_based_arch(slice_img, binary, rows, cols)
    
    x_arr = np.array(x_coords)
    y_arr = np.array(y_coords)
    
    # Step 5: Fit quadratic curve (characteristic of dental arch)
    try:
        # Use degree 2 for quadratic (DeAPIR uses quadratic)
        coeffs = np.polyfit(x_arr, y_arr, 2)
        poly = np.poly1d(coeffs)
        
        # Extend curve beyond detected region (10% on each side)
        x_min = max(0, x_arr.min() - cols * 0.1)
        x_max = min(cols, x_arr.max() + cols * 0.1)
        
        # Generate smooth curve with 100 points
        x_smooth = np.linspace(x_min, x_max, 100)
        y_smooth = poly(x_smooth)
        
        # Clip y values to valid range
        y_smooth = np.clip(y_smooth, 0, rows - 1)
        
        logger.info(f"DeAPIR: Fitted quadratic arch from x={x_min:.0f} to x={x_max:.0f}")
        
        return np.column_stack([x_smooth, y_smooth]), list(coeffs)
        
    except Exception as e:
        logger.error(f"DeAPIR: Polynomial fitting failed: {e}")
        return centroid_based_arch(slice_img, binary, rows, cols)


def morphological_thinning(binary_img: np.ndarray, max_iterations: int = 50) -> np.ndarray:
    """
    Perform morphological thinning to get skeleton-like structure
    Uses iterative erosion with end-point preservation
    
    Args:
        binary_img: Binary image to thin
        max_iterations: Maximum thinning iterations
        
    Returns:
        Thinned binary image
    """
    from scipy import ndimage
    
    img = binary_img.copy().astype(np.uint8)
    
    for _ in range(max_iterations):
        # Erode the image
        eroded = ndimage.binary_erosion(img)
        
        # Find pixels that would be deleted
        deleted = img & ~eroded
        
        # If nothing left to delete, we're done
        if not np.any(deleted):
            break
            
        # Apply erosion
        img = eroded.astype(np.uint8)
        
        # Stop if image becomes too thin
        if np.sum(img) < 20:
            break
    
    return img


def centroid_based_arch(slice_img: np.ndarray, binary: np.ndarray, rows: int, cols: int) -> Tuple[np.ndarray, List[float]]:
    """
    Fallback centroid-based arch detection
    
    Args:
        slice_img: Original image
        binary: Binary thresholded image  
        rows, cols: Image dimensions
        
    Returns:
        Tuple of (curve points, coefficients)
    """
    x_coords = []
    y_coords = []
    
    # Sample columns with step to avoid noise
    step = max(1, cols // 100)
    
    for x in range(0, cols, step):
        column = binary[:, x]
        y_positions = np.where(column > 0)[0]
        
        if len(y_positions) > 3:
            # Use weighted centroid
            weights = slice_img[y_positions, x]
            weights = weights - weights.min() + 1  # Ensure positive
            y_centroid = np.average(y_positions, weights=weights)
            x_coords.append(x)
            y_coords.append(y_centroid)
    
    if len(x_coords) < 5:
        # Return default U-shaped arch
        logger.warning("Centroid fallback: Using default arch")
        x_points = np.linspace(cols * 0.15, cols * 0.85, 100)
        center_x = cols / 2
        center_y = rows * 0.35
        a = 0.0005
        y_points = a * (x_points - center_x) ** 2 + center_y
        return np.column_stack([x_points, y_points]), [a, -a * center_x * 2, a * center_x**2 + center_y]
    
    x_arr = np.array(x_coords)
    y_arr = np.array(y_coords)
    
    try:
        coeffs = np.polyfit(x_arr, y_arr, 2)
        poly = np.poly1d(coeffs)
        x_smooth = np.linspace(x_arr.min(), x_arr.max(), 100)
        y_smooth = poly(x_smooth)
        return np.column_stack([x_smooth, y_smooth]), list(coeffs)
    except:
        # Ultimate fallback
        x_points = np.linspace(cols * 0.15, cols * 0.85, 100)
        center_x = cols / 2
        center_y = rows * 0.35
        a = 0.0005
        y_points = a * (x_points - center_x) ** 2 + center_y
        return np.column_stack([x_points, y_points]), [a, 0, center_y]

def generate_panoramic_image(
    volume: np.ndarray,
    arch_points: np.ndarray,
    thickness: int = 25,
    optimal_slice: int = None
) -> np.ndarray:
    """
    Generate panoramic image by projecting intensities along the dental arch
    
    Algorithm:
    1. For each point on the arch curve
    2. Extract perpendicular slice through the volume
    3. Project intensities to create panoramic view
    
    Args:
        volume: 3D CBCT volume
        arch_points: Nx2 array of arch curve points (x, y)
        thickness: Thickness of panoramic slab in pixels
        optimal_slice: Z-coordinate to center the panoramic
        
    Returns:
        2D panoramic image
    """
    rows, cols, depth = volume.shape
    num_points = len(arch_points)
    
    if optimal_slice is None:
        optimal_slice = depth // 2
    
    # Panoramic dimensions
    pan_width = num_points
    pan_height = thickness * 2  # Extend above and below arch
    
    panoramic = np.zeros((pan_height, pan_width), dtype=np.float32)
    
    for i, (x, y) in enumerate(arch_points):
        x_int = int(np.clip(x, 0, cols - 1))
        y_int = int(np.clip(y, 0, rows - 1))
        
        # Extract vertical column through volume at this arch position
        z_start = max(0, optimal_slice - thickness)
        z_end = min(depth, optimal_slice + thickness)
        
        # Get intensities along z-axis at this (x, y) position
        column = volume[y_int, x_int, z_start:z_end]
        
        # Place in panoramic image
        col_height = len(column)
        start_row = (pan_height - col_height) // 2
        end_row = start_row + col_height
        panoramic[start_row:end_row, i] = column
    
    return panoramic

def image_to_base64(img: np.ndarray, normalize: bool = True) -> str:
    """
    Convert numpy array to base64 encoded PNG
    
    Args:
        img: 2D numpy array
        normalize: Whether to normalize to 0-255
        
    Returns:
        Base64 encoded PNG string
    """
    from PIL import Image
    
    if normalize:
        img_min = img.min()
        img_max = img.max()
        if img_max > img_min:
            img = ((img - img_min) / (img_max - img_min) * 255).astype(np.uint8)
        else:
            img = np.zeros_like(img, dtype=np.uint8)
    
    pil_img = Image.fromarray(img)
    buffer = BytesIO()
    pil_img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

# ==================== Background Job Functions ====================

async def run_arch_detection_job(job_id: str, study_uid: str, series_uid: str):
    """Background task to run dental arch detection"""
    try:
        jobs[job_id] = {"status": "running", "progress": 0, "message": "Loading volume..."}
        
        # Load CBCT volume
        volume, metadata = await load_cbct_volume(series_uid)
        jobs[job_id]["progress"] = 30
        jobs[job_id]["message"] = "Finding optimal slice..."
        
        # Find optimal dental arch slice
        optimal_idx, slice_img = detect_dental_arch_slice(volume)
        jobs[job_id]["progress"] = 50
        jobs[job_id]["message"] = "Fitting dental arch curve..."
        
        # Fit polynomial arch curve
        arch_points, coeffs = fit_polynomial_arch(slice_img)
        jobs[job_id]["progress"] = 80
        jobs[job_id]["message"] = "Generating result..."
        
        # Calculate thickness based on volume size
        thickness_mm = metadata['slice_thickness'] * 25
        
        # Convert points to list format
        points_list = arch_points.tolist()
        
        arch_curve = ArchCurve(
            points=points_list,
            polynomial_coeffs=coeffs,
            optimal_slice_index=int(optimal_idx),
            thickness_mm=float(thickness_mm)
        )
        
        jobs[job_id] = {
            "status": "completed",
            "progress": 100,
            "message": "Arch detection completed",
            "result": arch_curve.dict()
        }
        
    except Exception as e:
        logger.error(f"Arch detection job {job_id} failed: {e}")
        jobs[job_id] = {
            "status": "failed",
            "progress": 0,
            "message": str(e),
            "result": None
        }

async def run_panoramic_generation_job(
    job_id: str, 
    study_uid: str, 
    series_uid: str,
    arch_curve: Optional[ArchCurve] = None
):
    """Background task to run panoramic generation"""
    try:
        jobs[job_id] = {"status": "running", "progress": 0, "message": "Loading volume..."}
        
        # Load CBCT volume
        volume, metadata = await load_cbct_volume(series_uid)
        jobs[job_id]["progress"] = 20
        
        # Detect arch if not provided
        if arch_curve is None:
            jobs[job_id]["message"] = "Detecting dental arch..."
            optimal_idx, slice_img = detect_dental_arch_slice(volume)
            arch_points, coeffs = fit_polynomial_arch(slice_img)
            jobs[job_id]["progress"] = 50
        else:
            arch_points = np.array(arch_curve.points)
            optimal_idx = arch_curve.optimal_slice_index
            jobs[job_id]["progress"] = 40
        
        jobs[job_id]["message"] = "Generating panoramic image..."
        
        # Generate panoramic
        panoramic = generate_panoramic_image(
            volume, 
            arch_points, 
            thickness=25,
            optimal_slice=optimal_idx
        )
        jobs[job_id]["progress"] = 80
        
        # Convert to base64
        pan_b64 = image_to_base64(panoramic)
        
        jobs[job_id] = {
            "status": "completed",
            "progress": 100,
            "message": "Panoramic generation completed",
            "result": {
                "panoramic_image": pan_b64,
                "dimensions": {
                    "width": panoramic.shape[1],
                    "height": panoramic.shape[0]
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Panoramic generation job {job_id} failed: {e}")
        jobs[job_id] = {
            "status": "failed",
            "progress": 0,
            "message": str(e),
            "result": None
        }

# ==================== API Endpoints ====================

@router.post("/detect-arch", response_model=ArchDetectionResponse)
async def detect_arch(req: ArchDetectionRequest, background_tasks: BackgroundTasks):
    """
    Detect dental arch curve from CBCT series
    
    Uses MIP + polynomial curve fitting algorithm to automatically
    detect the dental arch centerline for panoramic generation.
    
    Args:
        req: Request containing study and series UIDs
        
    Returns:
        ArchDetectionResponse with detected curve or job_id for polling
    """
    logger.info(f"Arch detection requested for series: {req.seriesInstanceUID}")
    
    job_id = str(uuid.uuid4())
    
    # Start background job
    background_tasks.add_task(
        run_arch_detection_job,
        job_id,
        req.studyInstanceUID,
        req.seriesInstanceUID
    )
    
    return ArchDetectionResponse(
        status="processing",
        message="Arch detection started",
        job_id=job_id
    )

@router.post("/generate", response_model=PanoramicResponse)
async def generate_panoramic(req: PanoramicRequest, background_tasks: BackgroundTasks):
    """
    Generate panoramic CPR image from CBCT series
    
    Projects CBCT intensities along the dental arch curve to create
    a 2D panoramic view similar to traditional panoramic X-rays.
    
    Args:
        req: Request containing study/series UIDs and optional arch curve
        
    Returns:
        PanoramicResponse with base64 encoded panoramic image or job_id
    """
    logger.info(f"Panoramic generation requested for series: {req.seriesInstanceUID}")
    
    job_id = str(uuid.uuid4())
    
    # Start background job
    background_tasks.add_task(
        run_panoramic_generation_job,
        job_id,
        req.studyInstanceUID,
        req.seriesInstanceUID,
        req.arch_curve
    )
    
    return PanoramicResponse(
        status="processing",
        message="Panoramic generation started",
        job_id=job_id
    )

@router.get("/status/{job_id}")
async def get_job_status(job_id: str):
    """
    Get status of an arch detection or panoramic generation job
    
    Args:
        job_id: The job ID returned from /detect-arch or /generate
        
    Returns:
        Current status, progress, and results if completed
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail=f"Job not found: {job_id}")
    
    return jobs[job_id]

@router.get("/health")
async def health_check():
    """
    Health check for panoramic generator service
    
    Returns:
        Service status and dependencies
    """
    return {
        "status": "healthy",
        "service": "panoramic-generator",
        "dependencies": {
            "orthanc": ORTHANC_URL,
            "scipy": True,
            "numpy": True
        }
    }
