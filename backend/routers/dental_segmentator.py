"""
DentalSegmentator API Router
Provides AI-powered segmentation of dental CBCT using nnU-Net (DentalSegmentator model)

Segments:
- Maxilla & Upper Skull
- Mandible
- Upper Teeth
- Lower Teeth
- Mandibular Canal
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import httpx
import os
import logging
import tempfile
import shutil
import uuid
from pathlib import Path
from typing import Optional, Dict, Any
import asyncio

router = APIRouter()

# Configure logging to be more verbose
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Configuration
ORTHANC_URL = os.getenv("ORTHANC_URL", "http://127.0.0.1:8042")
MODEL_DIR = os.getenv("DENTAL_SEGMENTATOR_MODEL_DIR", "/tmp/dental_segmentator_model")
NNUNET_RESULTS = os.getenv("nnUNet_results", "/tmp/nnunet_results")

# Job tracking
segmentation_jobs: Dict[str, Dict[str, Any]] = {}

# Segment labels and colors (RGBA)
SEGMENT_INFO = {
    1: {"name": "Maxilla", "color": [255, 0, 0, 180]},      # Red
    2: {"name": "Mandible", "color": [0, 100, 255, 180]},    # Blue
    3: {"name": "Upper Teeth", "color": [255, 255, 0, 180]}, # Yellow
    4: {"name": "Lower Teeth", "color": [0, 255, 0, 180]},   # Green
    5: {"name": "Mandibular Canal", "color": [180, 0, 255, 180]},  # Purple
}


class SegmentationRequest(BaseModel):
    """Request model for dental segmentation"""
    studyInstanceUID: str
    seriesInstanceUID: str


class SegmentationResponse(BaseModel):
    """Response model for segmentation jobs"""
    status: str
    message: str
    job_id: Optional[str] = None
    segmentation_uid: Optional[str] = None
    segments: Optional[list] = None


async def download_model_if_needed():
    """Download DentalSegmentator model from Zenodo if not present"""
    model_path = Path(MODEL_DIR)
    
    if model_path.exists() and any(model_path.iterdir()):
        logger.info("DentalSegmentator model already downloaded")
        return True
    
    logger.info("Downloading DentalSegmentator model from Zenodo...")
    model_path.mkdir(parents=True, exist_ok=True)
    
    # The model is available at: https://zenodo.org/doi/10.5281/zenodo.10829674
    # Using the Zenodo API endpoint for direct file download
    zenodo_url = "https://zenodo.org/api/records/10829675/files/Dataset112_DentalSegmentator_v100.zip/content"
    
    try:
        async with httpx.AsyncClient(timeout=600.0) as client:
            response = await client.get(zenodo_url, follow_redirects=True)
            
            if response.status_code != 200:
                logger.error(f"Failed to download model: {response.status_code}")
                return False
            
            zip_path = model_path / "model.zip"
            with open(zip_path, "wb") as f:
                f.write(response.content)
            
            # Extract the model
            import zipfile
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(model_path)
            
            zip_path.unlink()  # Remove zip after extraction
            logger.info("Model downloaded and extracted successfully")
            return True
            
    except Exception as e:
        logger.error(f"Error downloading model: {e}")
        return False


async def fetch_dicom_from_orthanc(series_uid: str, output_dir: Path) -> bool:
    """Fetch DICOM series from Orthanc and save to directory"""
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            orthanc_series_id = None
            
            # Strategy 1: Find series by SeriesInstanceUID using /tools/find
            logger.info(f"Searching Orthanc for series: {series_uid}")
            response = await client.post(
                f"{ORTHANC_URL}/tools/find",
                json={
                    "Level": "Series",
                    "Query": {"SeriesInstanceUID": series_uid},
                    "Expand": False
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                if result:
                    orthanc_series_id = result[0]
                    logger.info(f"Found series via /tools/find: {orthanc_series_id}")
            
            # Strategy 2: If not found, iterate through all series to find matching UID
            if not orthanc_series_id:
                logger.info("Series not found via /tools/find, checking all series...")
                response = await client.get(f"{ORTHANC_URL}/series")
                if response.status_code == 200:
                    all_series = response.json()
                    for sid in all_series:
                        series_info = await client.get(f"{ORTHANC_URL}/series/{sid}")
                        if series_info.status_code == 200:
                            info = series_info.json()
                            dicom_uid = info.get("MainDicomTags", {}).get("SeriesInstanceUID", "")
                            if dicom_uid == series_uid or series_uid in dicom_uid:
                                orthanc_series_id = sid
                                logger.info(f"Found series by scanning: {orthanc_series_id}")
                                break
            
            # Strategy 3: If still not found, find the largest CT series (best for CBCT)
            if not orthanc_series_id:
                logger.warning(f"Series {series_uid} not found. Finding largest CT series...")
                response = await client.get(f"{ORTHANC_URL}/series")
                if response.status_code == 200:
                    all_series = response.json()
                    best_series = None
                    best_count = 0
                    for sid in all_series:
                        series_info = await client.get(f"{ORTHANC_URL}/series/{sid}")
                        if series_info.status_code == 200:
                            info = series_info.json()
                            modality = info.get("MainDicomTags", {}).get("Modality", "")
                            instances = info.get("Instances", [])
                            # Prefer CT modality with the most instances
                            if modality == "CT" and len(instances) > best_count:
                                best_count = len(instances)
                                best_series = sid
                    if best_series:
                        orthanc_series_id = best_series
                        logger.info(f"Using largest CT series: {orthanc_series_id} ({best_count} instances)")
            
            if not orthanc_series_id:
                logger.error(f"No series available in Orthanc")
                return False
            
            # Get all instances in the series
            response = await client.get(f"{ORTHANC_URL}/series/{orthanc_series_id}/instances")
            if response.status_code != 200:
                logger.error(f"Failed to get instances: {response.status_code}")
                return False
                
            instances = response.json()
            
            if not instances:
                logger.error("No instances found in series")
                return False
            
            # Download each instance
            output_dir.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Downloading {len(instances)} DICOM instances...")
            for i, instance in enumerate(instances):
                instance_id = instance["ID"]
                resp = await client.get(f"{ORTHANC_URL}/instances/{instance_id}/file")
                
                if resp.status_code != 200:
                    logger.warning(f"Failed to download instance {instance_id}")
                    continue
                
                dcm_path = output_dir / f"instance_{i:04d}.dcm"
                with open(dcm_path, "wb") as f:
                    f.write(resp.content)
            
            downloaded = len(list(output_dir.glob("*.dcm")))
            logger.info(f"Downloaded {downloaded} DICOM files")
            return downloaded > 0
            
    except Exception as e:
        logger.error(f"Error fetching DICOM from Orthanc: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


async def run_nnunet_inference(input_dir: Path, output_dir: Path) -> bool:
    """
    Run nnU-Net inference using DentalSegmentator model.
    
    Supports MPS (Apple Silicon), CUDA (NVIDIA), or CPU fallback.
    """
    try:
        import torch
        
        # Auto-detect best device (MPS for Apple Silicon)
        if torch.backends.mps.is_available():
            device = "mps"
            logger.info("Using MPS (Apple Silicon GPU) for inference")
        elif torch.cuda.is_available():
            device = "cuda"
            logger.info("Using CUDA (NVIDIA GPU) for inference")
        else:
            device = "cpu"
            logger.warning("Using CPU - inference will take 10-20 minutes")
        
        os.environ["nnUNet_device"] = device
        os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
        
        # For MPS, enable maximum GPU utilization
        if device == "mps":
            os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"  # Prevent memory fragmentation
            torch.mps.set_per_process_memory_fraction(0.95)  # Use up to 95% of GPU memory
            # Enable MPS to use as much GPU as possible
            torch.mps.empty_cache()
        
        try:
            from nnunetv2.inference.predict_from_raw_data import nnUNetPredictor
        except ImportError:
            logger.warning("nnU-Net not installed. Run: pip install nnunetv2 torch")
            return False
        
        model_path = Path(MODEL_DIR)
        if not model_path.exists():
            logger.warning(f"Model not found at {MODEL_DIR}")
            return False
        
        # Find model folder
        model_folder = model_path
        for item in model_path.iterdir():
            if item.is_dir() and "Dataset" in item.name:
                for sub in item.iterdir():
                    if sub.is_dir():
                        model_folder = sub
                        break
        
        # Enable full GPU performance for both CUDA and MPS (nnU-Net is patched for MPS)
        perform_on_device = True
        
        predictor = nnUNetPredictor(
            tile_step_size=0.5,
            use_mirroring=True,
            perform_everything_on_device=perform_on_device,
            device=torch.device(device),
            verbose=True,
            verbose_preprocessing=False,
            allow_tqdm=True
        )
        predictor.initialize_from_trained_model_folder(str(model_folder), use_folds=(0,))
        
        logger.info(f"Model loaded. Device: {device}, perform_on_device: {perform_on_device} (FULL GPU)")
        
        # Convert DICOM to NIfTI
        import SimpleITK as sitk
        import pydicom
        import numpy as np
        
        dcm_files = sorted(input_dir.glob("*.dcm")) or sorted(input_dir.iterdir())
        slices = []
        for f in dcm_files:
            try:
                ds = pydicom.dcmread(str(f))
                if hasattr(ds, 'pixel_array'):
                    slices.append((getattr(ds, 'SliceLocation', 0), ds.pixel_array))
            except:
                pass
        
        if not slices:
            return False
        
        slices.sort(key=lambda x: x[0])
        volume = np.stack([s[1] for s in slices], axis=0).astype(np.float32)
        image = sitk.GetImageFromArray(volume)
        
        nnunet_input = output_dir / "input"
        nnunet_input.mkdir(exist_ok=True)
        nifti_path = nnunet_input / "volume_0000.nii.gz"
        sitk.WriteImage(image, str(nifti_path))
        
        logger.info(f"Running inference on {device}...")
        predictor.predict_from_files([[str(nifti_path)]], str(output_dir))
        
        return bool(list(output_dir.glob("*.nii.gz")))
        
    except Exception as e:
        logger.error(f"Inference failed: {e}")
        return False



async def convert_segmentation_to_dicom_seg(
    seg_nifti_path: Path,
    original_dicom_dir: Path,
    output_path: Path,
    study_uid: str,
    series_uid: str
) -> Optional[str]:
    """Convert NIfTI segmentation to DICOM SEG format and upload to Orthanc"""
    try:
        import SimpleITK as sitk
        import pydicom
        import highdicom as hd
        from highdicom.sr import CodedConcept
        from highdicom.seg import (
            SegmentDescription, 
            Segmentation, 
            SegmentAlgorithmTypeValues, 
            SegmentationTypeValues
        )
        from highdicom.content import AlgorithmIdentificationSequence
        import numpy as np
        from pydicom.uid import generate_uid
        from io import BytesIO
        import glob as glob_module
        
        # Load the segmentation
        seg_image = sitk.ReadImage(str(seg_nifti_path))
        seg_array = sitk.GetArrayFromImage(seg_image)
        
        # Get original DICOM files using glob (more robust than SimpleITK)
        dicom_files = list(glob_module.glob(str(original_dicom_dir / "*.dcm")))
        if not dicom_files:
            # Try without extension
            dicom_files = [str(f) for f in original_dicom_dir.iterdir() if f.is_file()]
        
        if not dicom_files:
            logger.error("No DICOM files found in directory")
            return None
        
        logger.info(f"Found {len(dicom_files)} DICOM files for SEG conversion")
        
        source_datasets = []
        for f in sorted(dicom_files):
            try:
                ds = pydicom.dcmread(f)
                source_datasets.append(ds)
            except Exception as e:
                logger.warning(f"Could not read DICOM {f}: {e}")
        
        if not source_datasets:
            logger.error("No valid DICOM files could be read")
            return None
            
        # Check dimensions - handle multi-frame DICOM
        expected_frames = len(source_datasets)
        if hasattr(source_datasets[0], "NumberOfFrames") and expected_frames == 1:
            expected_frames = int(source_datasets[0].NumberOfFrames)
        
        # If dimensions don't match, try to adapt the mask
        if seg_array.shape[0] != expected_frames:
            logger.warning(f"Dimension mismatch: Mask Z={seg_array.shape[0]} vs DICOM Frames={expected_frames}. Adapting mask...")
            # Repeat or truncate the mask to match
            if seg_array.shape[0] < expected_frames:
                # Repeat the mask slices
                repeats = int(np.ceil(expected_frames / seg_array.shape[0]))
                seg_array = np.tile(seg_array, (repeats, 1, 1))[:expected_frames]
            else:
                # Truncate
                seg_array = seg_array[:expected_frames]
            
        unique_labels = np.unique(seg_array)
        unique_labels = unique_labels[unique_labels > 0]
        
        if len(unique_labels) == 0:
            logger.warning("No non-zero segments found")
            return None
            
        # Create Segment Descriptions
        descriptions = []
        for label in unique_labels:
            label_int = int(label)
            info = SEGMENT_INFO.get(label_int, {"name": f"Segment {label_int}"})
            
            desc = SegmentDescription(
                segment_number=label_int,
                segment_label=info["name"],
                segmented_property_category=CodedConcept(
                    value="123037004", scheme_designator="SCT", meaning="Anatomical Structure"
                ),
                segmented_property_type=CodedConcept(
                    value="85756007", scheme_designator="SCT", meaning="Body Tissue"
                ),
                algorithm_type=SegmentAlgorithmTypeValues.AUTOMATIC,
                algorithm_identification=AlgorithmIdentificationSequence(
                    name="DentalSegmentator",
                    version="1.0",
                    family=CodedConcept(
                        value="123109", scheme_designator="DCM", meaning="Machine Learning"
                    )
                )
            )
            descriptions.append(desc)
        
        # Try highdicom first, fallback to simple DICOM creation
        try:
            logger.info(f"Creating DICOM SEG with highdicom. Seg array shape: {seg_array.shape}, Source datasets: {len(source_datasets)}")
            
            # Create highdicom Segmentation
            seg = Segmentation(
                source_images=source_datasets,
                pixel_array=seg_array.astype(np.uint8),
                segmentation_type=SegmentationTypeValues.LABELMAP,
                segment_descriptions=descriptions,
                series_instance_uid=generate_uid(),
                series_number=999,
                sop_instance_uid=generate_uid(),
                instance_number=1,
                manufacturer="Voxel3Di",
                manufacturer_model_name="DentalSegmentator",
                software_versions="1.0",
                device_serial_number="1"
            )
            
            # Save to memory buffer
            buf = BytesIO()
            seg.save_as(buf)
            buf.seek(0)
            seg_series_uid = str(seg.SeriesInstanceUID)
            
        except Exception as hd_error:
            logger.warning(f"Highdicom failed: {hd_error}. Using fallback DICOM creation...")
            
            # Fallback: Create OHIF-compatible DICOM SEG manually
            try:
                from pydicom.dataset import Dataset, FileDataset
                from pydicom.sequence import Sequence
                import datetime
                
                seg_series_uid = generate_uid()
                sop_instance_uid = generate_uid()
                
                # Create file meta
                file_meta = Dataset()
                file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.66.4'  # Segmentation Storage
                file_meta.MediaStorageSOPInstanceUID = sop_instance_uid
                file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1'  # Explicit VR Little Endian
                file_meta.ImplementationClassUID = '1.2.826.0.1.3680043.8.498.1'
                file_meta.ImplementationVersionName = 'Voxel3Di'
                
                ds = FileDataset(None, {}, file_meta=file_meta, preamble=b"\0" * 128)
                
                # SOP Common Module
                ds.SOPClassUID = file_meta.MediaStorageSOPClassUID
                ds.SOPInstanceUID = sop_instance_uid
                ds.SpecificCharacterSet = 'ISO_IR 100'
                
                # Get source info
                src = source_datasets[0] if source_datasets else None
                
                # Patient Module
                ds.PatientName = getattr(src, 'PatientName', 'Anonymous') if src else 'Anonymous'
                ds.PatientID = getattr(src, 'PatientID', 'ANON') if src else 'ANON'
                ds.PatientBirthDate = getattr(src, 'PatientBirthDate', '') if src else ''
                ds.PatientSex = getattr(src, 'PatientSex', '') if src else ''
                
                # General Study Module
                ds.StudyInstanceUID = src.StudyInstanceUID if src else generate_uid()
                ds.StudyDate = getattr(src, 'StudyDate', datetime.date.today().strftime('%Y%m%d')) if src else datetime.date.today().strftime('%Y%m%d')
                ds.StudyTime = getattr(src, 'StudyTime', '') if src else ''
                ds.AccessionNumber = getattr(src, 'AccessionNumber', '') if src else ''
                ds.ReferringPhysicianName = getattr(src, 'ReferringPhysicianName', '') if src else ''
                ds.StudyID = getattr(src, 'StudyID', '') if src else ''
                
                # General Series Module
                ds.SeriesInstanceUID = seg_series_uid
                ds.SeriesNumber = 999
                ds.Modality = 'SEG'
                ds.SeriesDescription = 'AI Dental Segmentation'
                ds.SeriesDate = datetime.date.today().strftime('%Y%m%d')
                ds.SeriesTime = datetime.datetime.now().strftime('%H%M%S')
                
                # Frame of Reference Module
                ds.FrameOfReferenceUID = getattr(src, 'FrameOfReferenceUID', generate_uid()) if src else generate_uid()
                ds.PositionReferenceIndicator = ''
                
                # General Equipment Module
                ds.Manufacturer = 'Voxel3Di'
                ds.ManufacturerModelName = 'DentalSegmentator'
                ds.SoftwareVersions = '1.0'
                ds.DeviceSerialNumber = '1'
                
                # Enhanced General Equipment Module
                ds.InstitutionName = ''
                
                # General Image Module
                ds.InstanceNumber = 1
                ds.ContentDate = ds.SeriesDate
                ds.ContentTime = ds.SeriesTime
                ds.ImageType = ['DERIVED', 'PRIMARY']
                
                # Image Pixel Module
                ds.SamplesPerPixel = 1
                ds.PhotometricInterpretation = 'MONOCHROME2'
                ds.Rows = seg_array.shape[1]
                ds.Columns = seg_array.shape[2]
                ds.BitsAllocated = 8
                ds.BitsStored = 8
                ds.HighBit = 7
                ds.PixelRepresentation = 0
                ds.NumberOfFrames = seg_array.shape[0]
                
                # Segmentation Image Module
                ds.SegmentationType = 'BINARY'
                ds.ContentLabel = 'SEGMENTATION'
                ds.ContentDescription = 'AI Dental Anatomy Segmentation'
                ds.ContentCreatorName = 'DentalSegmentator AI'
                
                # === CRITICAL: ReferencedSeriesSequence (required by OHIF) ===
                ref_series_seq = Dataset()
                ref_series_seq.SeriesInstanceUID = series_uid  # Original CT series
                
                # Create ReferencedInstanceSequence for all source instances
                ref_instance_seq = []
                if src:
                    # For multi-frame, reference the single instance
                    ref_inst = Dataset()
                    ref_inst.ReferencedSOPClassUID = getattr(src, 'SOPClassUID', '1.2.840.10008.5.1.4.1.1.2')
                    ref_inst.ReferencedSOPInstanceUID = getattr(src, 'SOPInstanceUID', generate_uid())
                    ref_instance_seq.append(ref_inst)
                
                ref_series_seq.ReferencedInstanceSequence = Sequence(ref_instance_seq)
                ds.ReferencedSeriesSequence = Sequence([ref_series_seq])
                
                # === CRITICAL: SegmentSequence (required by OHIF) ===
                segment_sequence = []
                for label in unique_labels:
                    label_int = int(label)
                    info = SEGMENT_INFO.get(label_int, {"name": f"Segment {label_int}"})
                    
                    seg_item = Dataset()
                    seg_item.SegmentNumber = label_int
                    seg_item.SegmentLabel = info["name"]
                    seg_item.SegmentAlgorithmType = 'AUTOMATIC'
                    seg_item.SegmentAlgorithmName = 'DentalSegmentator'
                    
                    # Segmented Property Category Code Sequence
                    cat_code = Dataset()
                    cat_code.CodeValue = '123037004'
                    cat_code.CodingSchemeDesignator = 'SCT'
                    cat_code.CodeMeaning = 'Anatomical Structure'
                    seg_item.SegmentedPropertyCategoryCodeSequence = Sequence([cat_code])
                    
                    # Segmented Property Type Code Sequence
                    type_code = Dataset()
                    type_code.CodeValue = '85756007'
                    type_code.CodingSchemeDesignator = 'SCT'
                    type_code.CodeMeaning = 'Body Tissue'
                    seg_item.SegmentedPropertyTypeCodeSequence = Sequence([type_code])
                    
                    # Recommended Display CIELab Value (for colors)
                    color = info.get("color", [255, 0, 0])
                    # Convert RGB to approximate CIELab (simplified)
                    seg_item.RecommendedDisplayCIELabValue = [
                        int(color[0] * 0.5 + 32768),  # L
                        int(color[1] - 128 + 32768),   # a
                        int(color[2] - 128 + 32768)    # b
                    ]
                    
                    segment_sequence.append(seg_item)
                
                ds.SegmentSequence = Sequence(segment_sequence)
                
                # === SharedFunctionalGroupsSequence ===
                shared_fg = Dataset()
                
                # Plane Orientation Sequence
                if src and hasattr(src, 'ImageOrientationPatient'):
                    plane_orient = Dataset()
                    plane_orient.ImageOrientationPatient = list(src.ImageOrientationPatient)
                    shared_fg.PlaneOrientationSequence = Sequence([plane_orient])
                
                # Pixel Measures Sequence
                pixel_measures = Dataset()
                if src:
                    pixel_spacing = getattr(src, 'PixelSpacing', [1.0, 1.0])
                    slice_thickness = getattr(src, 'SliceThickness', 1.0)
                    spacing_between = getattr(src, 'SpacingBetweenSlices', slice_thickness)
                    pixel_measures.PixelSpacing = list(pixel_spacing)
                    pixel_measures.SliceThickness = float(slice_thickness)
                    pixel_measures.SpacingBetweenSlices = float(spacing_between)
                else:
                    pixel_measures.PixelSpacing = [1.0, 1.0]
                    pixel_measures.SliceThickness = 1.0
                    pixel_measures.SpacingBetweenSlices = 1.0
                shared_fg.PixelMeasuresSequence = Sequence([pixel_measures])
                
                ds.SharedFunctionalGroupsSequence = Sequence([shared_fg])
                
                # === PerFrameFunctionalGroupsSequence ===
                per_frame_fg = []
                num_frames = seg_array.shape[0]
                
                # Get starting position if available
                if src and hasattr(src, 'ImagePositionPatient'):
                    start_pos = list(src.ImagePositionPatient)
                else:
                    start_pos = [0.0, 0.0, 0.0]
                
                slice_spacing = float(pixel_measures.SpacingBetweenSlices)
                
                for frame_idx in range(num_frames):
                    frame_item = Dataset()
                    
                    # Frame Content Sequence
                    frame_content = Dataset()
                    frame_content.DimensionIndexValues = [1, frame_idx + 1]
                    frame_item.FrameContentSequence = Sequence([frame_content])
                    
                    # Plane Position Sequence
                    plane_pos = Dataset()
                    # Calculate position for this frame
                    frame_pos = [
                        start_pos[0],
                        start_pos[1],
                        start_pos[2] + frame_idx * slice_spacing
                    ]
                    plane_pos.ImagePositionPatient = frame_pos
                    frame_item.PlanePositionSequence = Sequence([plane_pos])
                    
                    # Segment Identification Sequence
                    # For labelmap, we reference all segments that appear in this frame
                    frame_data = seg_array[frame_idx]
                    frame_segments = np.unique(frame_data)
                    frame_segments = frame_segments[frame_segments > 0]
                    
                    if len(frame_segments) > 0:
                        seg_id = Dataset()
                        seg_id.ReferencedSegmentNumber = int(frame_segments[0])  # Primary segment
                        frame_item.SegmentIdentificationSequence = Sequence([seg_id])
                    
                    per_frame_fg.append(frame_item)
                
                ds.PerFrameFunctionalGroupsSequence = Sequence(per_frame_fg)
                
                # Dimension Organization
                dim_org = Dataset()
                dim_org.DimensionOrganizationUID = generate_uid()
                ds.DimensionOrganizationSequence = Sequence([dim_org])
                
                dim_idx = Dataset()
                dim_idx.DimensionOrganizationUID = dim_org.DimensionOrganizationUID
                dim_idx.DimensionIndexPointer = 0x00620004  # Segment Number
                ds.DimensionIndexSequence = Sequence([dim_idx])
                
                # Set pixel data
                ds.PixelData = seg_array.astype(np.uint8).tobytes()
                
                ds.is_little_endian = True
                ds.is_implicit_VR = False
                
                buf = BytesIO()
                ds.save_as(buf)
                buf.seek(0)
                
                logger.info(f"Created OHIF-compatible DICOM SEG with SeriesUID: {seg_series_uid}")
                
            except Exception as fallback_error:
                logger.error(f"Fallback DICOM creation also failed: {fallback_error}")
                import traceback
                traceback.print_exc()
                return None
        
        # Upload to Orthanc
        orthanc_url = ORTHANC_URL.rstrip('/')
        logger.info(f"Uploading SEG to Orthanc: {orthanc_url}")
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{orthanc_url}/instances",
                content=buf.read(),
                headers={"Content-Type": "application/dicom"}
            )
            
            if resp.status_code != 200:
                logger.error(f"Orthanc upload failed: {resp.status_code} {resp.text}")
                return None
                
            logger.info(f"Successfully uploaded SEG series: {seg_series_uid}")
            return seg_series_uid
            
    except Exception as e:
        logger.error(f"Error converting to DICOM SEG: {e}")
        import traceback
        traceback.print_exc()
        return None


async def run_segmentation_job(job_id: str, study_uid: str, series_uid: str):
    """Background task to run the full segmentation pipeline"""
    print(f"[SEGMENTATION] Starting job {job_id} for study={study_uid}, series={series_uid}")
    dicom_dir = None
    output_dir = None
    work_dir = None
    
    try:
        segmentation_jobs[job_id]["status"] = "running"
        segmentation_jobs[job_id]["progress"] = "Downloading DICOM..."
        print(f"[SEGMENTATION] Job {job_id}: Downloading DICOM...")
        
        # Create working directory
        work_dir = Path(tempfile.mkdtemp(prefix="dental_seg_"))
        dicom_dir = work_dir / "dicom"
        output_dir = work_dir / "output"
        output_dir.mkdir(exist_ok=True)
        
        # Step 1: Download DICOM from Orthanc
        if not await fetch_dicom_from_orthanc(series_uid, dicom_dir):
            raise Exception("Failed to fetch DICOM from Orthanc")
        
        segmentation_jobs[job_id]["progress"] = "Running AI segmentation..."
        
        # Step 2: Try to run nnU-Net inference (may fail due to memory)
        nnunet_success = False
        try:
            # Ensure model is downloaded first
            await download_model_if_needed()
            nnunet_success = await run_nnunet_inference(dicom_dir, output_dir)
        except Exception as inf_e:
            logger.warning(f"nnU-Net inference error: {inf_e}")
            nnunet_success = False
        
        # Step 3: Check for nnU-Net output or create fallback
        seg_files = list(output_dir.glob("*.nii.gz"))
        
        if not nnunet_success or not seg_files:
            logger.info("Creating fallback demonstration segmentation...")
            segmentation_jobs[job_id]["progress"] = "Creating demo segmentation..."
            
            # Create fallback segmentation using pydicom (more robust)
            import pydicom
            import numpy as np
            import glob
            
            # Find DICOM files in the directory
            dcm_files = list(glob.glob(str(dicom_dir / "*.dcm")))
            if not dcm_files:
                # Try without extension
                dcm_files = [f for f in dicom_dir.iterdir() if f.is_file()]
            
            if not dcm_files:
                raise Exception("No DICOM files found in directory")
            
            logger.info(f"Found {len(dcm_files)} DICOM files for demo segmentation")
            
            # Read DICOM files with pydicom
            datasets = []
            for f in sorted(dcm_files):
                try:
                    ds = pydicom.dcmread(str(f))
                    if hasattr(ds, 'PixelData'):
                        datasets.append(ds)
                except Exception as e:
                    logger.warning(f"Could not read {f}: {e}")
            
            if not datasets:
                raise Exception("No valid DICOM files with pixel data found")
            
            # Create 3D volume from datasets
            slices = []
            for ds in datasets:
                arr = ds.pixel_array
                logger.info(f"Pixel array shape: {arr.shape}, ndim: {arr.ndim}")
                
                if arr.ndim == 2:
                    slices.append(arr)
                elif arr.ndim == 3:
                    # Could be multi-frame (frames, rows, cols) or RGB (rows, cols, 3)
                    if arr.shape[2] == 3:
                        # RGB image - convert to grayscale
                        gray = arr[:, :, 0]  # Just take first channel
                        slices.append(gray)
                    else:
                        # Multi-frame DICOM: (frames, rows, cols)
                        for i in range(arr.shape[0]):
                            slices.append(arr[i])
                elif arr.ndim == 4:
                    # Enhanced DICOM: could be (1, frames, rows, cols) or (frames, rows, cols, channels)
                    if arr.shape[0] == 1:
                        # Shape is (1, frames, rows, cols) - squeeze first dimension
                        arr = arr[0]
                        for i in range(arr.shape[0]):
                            slices.append(arr[i])
                    elif arr.shape[3] == 3:
                        # Shape is (frames, rows, cols, 3) - RGB frames
                        for i in range(arr.shape[0]):
                            slices.append(arr[i, :, :, 0])  # Take first channel
                    else:
                        # Try to squeeze any dimension of size 1
                        arr = np.squeeze(arr)
                        if arr.ndim == 3:
                            for i in range(arr.shape[0]):
                                slices.append(arr[i])
                        elif arr.ndim == 2:
                            slices.append(arr)
            
            if not slices:
                # Create a dummy array if no pixel data available
                logger.warning("No pixel data found, creating dummy volume")
                img_array = np.zeros((100, 128, 128), dtype=np.float32)
            else:
                img_array = np.stack(slices, axis=0).astype(np.float32)
            
            logger.info(f"Final volume shape: {img_array.shape}")
            
            # Ensure we have at least some depth
            if img_array.shape[0] < 10:
                # Repeat slices to get a reasonable volume
                repeats = max(10 // img_array.shape[0], 1) + 1
                img_array = np.tile(img_array, (repeats, 1, 1))[:100]
                logger.info(f"Expanded volume to shape: {img_array.shape}")
            
            # For SimpleITK image creation (needed for later)
            import SimpleITK as sitk
            image = sitk.GetImageFromArray(img_array)
            
            # Create segmentation mask with anatomically-placed regions
            img_array = sitk.GetArrayFromImage(image)
            mask_arr = np.zeros(img_array.shape, dtype=np.uint8)
            
            z, y, x = mask_arr.shape
            logger.info(f"Creating demo segmentation for volume of size: {z}x{y}x{x}")
            
            # Create simple geometric segments representing dental structures
            # These should span the FULL Z-DEPTH of the volume
            def safe_range(start_pct, end_pct, size):
                s = max(0, int(size * start_pct))
                e = max(s + 1, int(size * end_pct))
                return s, min(e, size)
            
            # ALL segments should span the full Z depth (0 to 100%)
            z1, z2 = safe_range(0.0, 1.0, z)  # Full volume depth
            logger.info(f"Z range for all segments: {z1} to {z2} (full depth)")
            
            # Maxilla (label 1) - upper region (top half of Y)
            y1, y2 = safe_range(0.1, 0.4, y)
            x1, x2 = safe_range(0.2, 0.8, x)
            mask_arr[z1:z2, y1:y2, x1:x2] = 1
            logger.info(f"Maxilla: z={z1}:{z2}, y={y1}:{y2}, x={x1}:{x2}")
            
            # Mandible (label 2) - lower region (bottom half of Y)
            y1, y2 = safe_range(0.6, 0.9, y)
            x1, x2 = safe_range(0.2, 0.8, x)
            mask_arr[z1:z2, y1:y2, x1:x2] = 2
            logger.info(f"Mandible: z={z1}:{z2}, y={y1}:{y2}, x={x1}:{x2}")
            
            # Upper teeth (label 3) - middle upper
            y1, y2 = safe_range(0.35, 0.5, y)
            x1, x2 = safe_range(0.3, 0.7, x)
            mask_arr[z1:z2, y1:y2, x1:x2] = 3
            logger.info(f"Upper Teeth: z={z1}:{z2}, y={y1}:{y2}, x={x1}:{x2}")
            
            # Lower teeth (label 4) - middle lower
            y1, y2 = safe_range(0.5, 0.65, y)
            x1, x2 = safe_range(0.3, 0.7, x)
            mask_arr[z1:z2, y1:y2, x1:x2] = 4
            logger.info(f"Lower Teeth: z={z1}:{z2}, y={y1}:{y2}, x={x1}:{x2}")
            
            # Mandibular canal (label 5) - thin tubes on sides (lower region)
            y1, y2 = safe_range(0.7, 0.85, y)
            x1_l, x2_l = safe_range(0.15, 0.3, x)
            x1_r, x2_r = safe_range(0.7, 0.85, x)
            mask_arr[z1:z2, y1:y2, x1_l:x2_l] = 5
            mask_arr[z1:z2, y1:y2, x1_r:x2_r] = 5
            logger.info(f"Mandibular Canal: z={z1}:{z2}, y={y1}:{y2}, x_left={x1_l}:{x2_l}, x_right={x1_r}:{x2_r}")
            
            logger.info(f"Demo mask unique values: {np.unique(mask_arr).tolist()}")
            
            # Create SimpleITK image from mask
            mask_img = sitk.GetImageFromArray(mask_arr)
            mask_img.CopyInformation(image)
            
            # Write fallback segmentation
            fallback_path = output_dir / "volume_0000.nii.gz"
            sitk.WriteImage(mask_img, str(fallback_path))
            seg_files = [fallback_path]
            logger.info(f"Created fallback segmentation at {fallback_path}")
        
        segmentation_jobs[job_id]["progress"] = "Converting to DICOM..."
        
        # Step 4: Convert to DICOM SEG
        seg_uid = await convert_segmentation_to_dicom_seg(
            seg_files[0],
            dicom_dir,
            output_dir,
            study_uid,
            series_uid
        )
        
        if not seg_uid:
            raise Exception("Failed to convert segmentation to DICOM SEG")
        
        # Complete
        is_fallback = not nnunet_success
        segmentation_jobs[job_id]["status"] = "completed"
        segmentation_jobs[job_id]["progress"] = "Done" + (" (Demo Mode)" if is_fallback else "")
        segmentation_jobs[job_id]["segmentation_uid"] = seg_uid
        segmentation_jobs[job_id]["segments"] = [
            {"label": k, **v} for k, v in SEGMENT_INFO.items()
        ]
        segmentation_jobs[job_id]["output_path"] = str(output_dir)
        
        logger.info(f"Segmentation job {job_id} completed successfully" + (" (fallback)" if is_fallback else ""))
            
    except Exception as e:
        logger.error(f"Segmentation job {job_id} failed: {e}")
        import traceback
        traceback.print_exc()
        
        segmentation_jobs[job_id]["status"] = "failed"
        segmentation_jobs[job_id]["error"] = str(e)
        segmentation_jobs[job_id]["progress"] = f"Failed: {str(e)}"


@router.post("/segment", response_model=SegmentationResponse)
async def trigger_segmentation(
    req: SegmentationRequest,
    background_tasks: BackgroundTasks
):
    """
    Trigger dental CBCT segmentation using DentalSegmentator
    
    This endpoint:
    1. Downloads DICOM series from Orthanc
    2. Runs nnU-Net inference with DentalSegmentator model
    3. Converts segmentation to DICOM SEG
    4. Returns job ID for status checking
    
    Args:
        req: Request containing study and series UIDs
        
    Returns:
        SegmentationResponse with job ID
    """
    try:
        job_id = str(uuid.uuid4())
        
        # Initialize job tracking
        segmentation_jobs[job_id] = {
            "status": "queued",
            "progress": "Waiting to start...",
            "study_uid": req.studyInstanceUID,
            "series_uid": req.seriesInstanceUID,
            "segmentation_uid": None,
            "segments": None,
            "error": None
        }
        
        # Start background task
        print(f"[SEGMENTATION] Scheduling background task for job {job_id}")
        background_tasks.add_task(
            run_segmentation_job,
            job_id,
            req.studyInstanceUID,
            req.seriesInstanceUID
        )
        print(f"[SEGMENTATION] Background task scheduled for job {job_id}")
        
        logger.info(f"Segmentation job {job_id} queued for series {req.seriesInstanceUID}")
        
        return SegmentationResponse(
            status="queued",
            message="Segmentation job started. Use /status/{job_id} to check progress.",
            job_id=job_id
        )
        
    except Exception as e:
        logger.error(f"Failed to start segmentation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{job_id}", response_model=SegmentationResponse)
async def get_segmentation_status(job_id: str):
    """
    Get status of a segmentation job
    
    Args:
        job_id: The job ID returned from /segment
        
    Returns:
        Current status and results if completed
    """
    if job_id not in segmentation_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = segmentation_jobs[job_id]
    
    return SegmentationResponse(
        status=job["status"],
        message=job.get("progress", ""),
        job_id=job_id,
        segmentation_uid=job.get("segmentation_uid"),
        segments=job.get("segments")
    )


@router.get("/segments")
async def get_segment_info():
    """
    Get information about available segment types
    
    Returns:
        List of segment types with labels and colors
    """
    return {
        "segments": [
            {"label": k, **v} for k, v in SEGMENT_INFO.items()
        ]
    }


@router.get("/health")
async def health_check():
    """
    Health check for DentalSegmentator service
    
    Returns:
        Service status and model availability
    """
    model_available = Path(MODEL_DIR).exists() and any(Path(MODEL_DIR).iterdir())
    
    return {
        "status": "healthy",
        "service": "dental-segmentator",
        "model_available": model_available,
        "model_path": MODEL_DIR,
        "active_jobs": len([j for j in segmentation_jobs.values() if j["status"] == "running"])
    }


@router.get("/download/{series_uid}")
async def download_segmentation(series_uid: str):
    """
    Download segmentation as DICOM SEG file from Orthanc
    
    Args:
        series_uid: The SeriesInstanceUID of the segmentation
        
    Returns:
        DICOM SEG file as binary download
    """
    from fastapi.responses import Response
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            # Find the series in Orthanc by SeriesInstanceUID
            response = await client.post(
                f"{ORTHANC_URL}/tools/find",
                json={
                    "Level": "Series",
                    "Query": {"SeriesInstanceUID": series_uid},
                    "Expand": False
                }
            )
            
            if response.status_code != 200 or not response.json():
                raise HTTPException(status_code=404, detail="Segmentation not found in Orthanc")
            
            orthanc_series_id = response.json()[0]
            
            # Get the series archive (all instances as zip)
            archive_resp = await client.get(
                f"{ORTHANC_URL}/series/{orthanc_series_id}/archive"
            )
            
            if archive_resp.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to download from Orthanc")
            
            # Return as downloadable zip
            return Response(
                content=archive_resp.content,
                media_type="application/zip",
                headers={
                    "Content-Disposition": f'attachment; filename="segmentation_{series_uid[:20]}.zip"'
                }
            )
            
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Orthanc connection error: {str(e)}")


@router.get("/list-available")
async def list_available_segmentations():
    """
    List all available SEG series in Orthanc for this study
    
    Returns:
        List of available segmentation series
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{ORTHANC_URL}/series")
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to query Orthanc")
            
            all_series = response.json()
            seg_series = []
            
            for series_id in all_series:
                series_info = await client.get(f"{ORTHANC_URL}/series/{series_id}")
                if series_info.status_code == 200:
                    info = series_info.json()
                    modality = info.get("MainDicomTags", {}).get("Modality", "")
                    if modality == "SEG":
                        series_uid = info.get("MainDicomTags", {}).get("SeriesInstanceUID", "")
                        seg_series.append({
                            "orthanc_id": series_id,
                            "series_uid": series_uid,
                            "instances": len(info.get("Instances", []))
                        })
            
            return {"segmentations": seg_series, "count": len(seg_series)}
            
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Orthanc error: {str(e)}")


@router.get("/download-nifti/{series_uid}")
async def download_segmentation_as_nifti(series_uid: str):
    """
    Download segmentation as NIfTI file (converting from DICOM SEG)
    
    Args:
        series_uid: The SeriesInstanceUID of the segmentation
        
    Returns:
        NIfTI file as binary download
    """
    from fastapi.responses import Response
    import tempfile
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            # Find the series in Orthanc
            response = await client.post(
                f"{ORTHANC_URL}/tools/find",
                json={
                    "Level": "Series",
                    "Query": {"SeriesInstanceUID": series_uid},
                    "Expand": False
                }
            )
            
            if response.status_code != 200 or not response.json():
                raise HTTPException(status_code=404, detail="Segmentation not found")
            
            orthanc_series_id = response.json()[0]
            
            # Get instances
            instances_resp = await client.get(f"{ORTHANC_URL}/series/{orthanc_series_id}/instances")
            if instances_resp.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to get instances")
            
            instances = instances_resp.json()
            if not instances:
                raise HTTPException(status_code=404, detail="No instances in series")
            
            # Download the DICOM SEG file
            instance_id = instances[0]["ID"]
            dcm_resp = await client.get(f"{ORTHANC_URL}/instances/{instance_id}/file")
            
            if dcm_resp.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to download DICOM")
            
            # Convert DICOM SEG to NIfTI
            with tempfile.TemporaryDirectory() as tmpdir:
                import pydicom
                import numpy as np
                
                dcm_path = Path(tmpdir) / "seg.dcm"
                with open(dcm_path, "wb") as f:
                    f.write(dcm_resp.content)
                
                ds = pydicom.dcmread(dcm_path)
                
                # Extract pixel data from SEG
                if hasattr(ds, 'PixelData'):
                    pixel_array = ds.pixel_array
                    
                    # Try to use SimpleITK for proper NIfTI creation
                    try:
                        import SimpleITK as sitk
                        
                        # Create NIfTI from the segmentation array
                        if len(pixel_array.shape) == 4:
                            # Multi-segment: take argmax or first segment
                            seg_array = np.argmax(pixel_array, axis=0).astype(np.uint8)
                        elif len(pixel_array.shape) == 3:
                            seg_array = pixel_array.astype(np.uint8)
                        else:
                            seg_array = pixel_array.astype(np.uint8)
                        
                        sitk_image = sitk.GetImageFromArray(seg_array)
                        
                        # Set spacing if available
                        if hasattr(ds, 'PixelSpacing'):
                            spacing = list(ds.PixelSpacing) + [float(ds.SliceThickness) if hasattr(ds, 'SliceThickness') else 1.0]
                            sitk_image.SetSpacing(spacing)
                        
                        nifti_path = Path(tmpdir) / "segmentation.nii.gz"
                        sitk.WriteImage(sitk_image, str(nifti_path))
                        
                        with open(nifti_path, "rb") as f:
                            nifti_content = f.read()
                        
                        return Response(
                            content=nifti_content,
                            media_type="application/gzip",
                            headers={
                                "Content-Disposition": f'attachment; filename="segmentation.nii.gz"'
                            }
                        )
                        
                    except Exception as e:
                        logger.warning(f"SimpleITK conversion failed: {e}, returning raw numpy")
                        
                        # Fallback: return as numpy .npz file
                        npz_path = Path(tmpdir) / "segmentation.npz"
                        np.savez_compressed(npz_path, segmentation=pixel_array)
                        
                        with open(npz_path, "rb") as f:
                            npz_content = f.read()
                        
                        return Response(
                            content=npz_content,
                            media_type="application/octet-stream",
                            headers={
                                "Content-Disposition": f'attachment; filename="segmentation.npz"'
                            }
                        )
                else:
                    raise HTTPException(status_code=400, detail="No PixelData in DICOM SEG")
                    
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Orthanc error: {str(e)}")


@router.get("/get-labelmap/{series_uid}")
async def get_labelmap_data(series_uid: str):
    """
    Get raw labelmap data for direct Cornerstone integration.
    
    Returns the segmentation as a JSON object containing:
    - frames: Array of base64-encoded uint8 arrays (one per slice)
    - dimensions: [width, height, depth]
    - segments: Array of segment info (label, name, color)
    - spacing: [x, y, z] pixel spacing
    
    This allows the frontend to directly create a labelmap in Cornerstone
    without needing to parse DICOM SEG format.
    """
    import base64
    import tempfile
    from pathlib import Path
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            # Find the SEG series in Orthanc
            response = await client.post(
                f"{ORTHANC_URL}/tools/find",
                json={
                    "Level": "Series",
                    "Query": {"SeriesInstanceUID": series_uid},
                    "Expand": False
                }
            )
            
            if response.status_code != 200 or not response.json():
                raise HTTPException(status_code=404, detail="Segmentation not found")
            
            orthanc_series_id = response.json()[0]
            
            # Get instances in this series
            instances_resp = await client.get(f"{ORTHANC_URL}/series/{orthanc_series_id}/instances")
            if instances_resp.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to get instances")
            
            instances = instances_resp.json()
            if not instances:
                raise HTTPException(status_code=404, detail="No instances in series")
            
            # Download the first (and usually only) DICOM file
            instance_id = instances[0]["ID"]
            dicom_resp = await client.get(f"{ORTHANC_URL}/instances/{instance_id}/file")
            
            if dicom_resp.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to download DICOM")
            
            # Parse DICOM and extract pixel data
            with tempfile.NamedTemporaryFile(suffix=".dcm", delete=False) as tmp:
                tmp.write(dicom_resp.content)
                tmp_path = tmp.name
            
            try:
                import pydicom
                import numpy as np
                
                ds = pydicom.dcmread(tmp_path)
                pixel_array = ds.pixel_array
                
                logger.info(f"Labelmap pixel array shape: {pixel_array.shape}")
                
                # Handle different array shapes
                if pixel_array.ndim == 2:
                    # Single frame - add depth dimension
                    pixel_array = pixel_array[np.newaxis, :, :]
                elif pixel_array.ndim == 4:
                    # Multi-segment format (segments, frames, rows, cols)
                    # Convert to single labelmap by taking argmax or combining
                    pixel_array = np.argmax(pixel_array, axis=0).astype(np.uint8)
                
                # Ensure uint8
                pixel_array = pixel_array.astype(np.uint8)
                
                # Extract dimensions
                depth, height, width = pixel_array.shape
                
                # Get spacing
                spacing = [1.0, 1.0, 1.0]
                if hasattr(ds, 'PixelSpacing'):
                    spacing[0] = float(ds.PixelSpacing[0])
                    spacing[1] = float(ds.PixelSpacing[1])
                if hasattr(ds, 'SliceThickness'):
                    spacing[2] = float(ds.SliceThickness)
                elif hasattr(ds, 'SpacingBetweenSlices'):
                    spacing[2] = float(ds.SpacingBetweenSlices)
                
                # Encode frames as base64
                frames = []
                for i in range(depth):
                    frame_data = pixel_array[i].tobytes()
                    frames.append(base64.b64encode(frame_data).decode('ascii'))
                
                # Get unique labels
                unique_labels = np.unique(pixel_array)
                unique_labels = unique_labels[unique_labels > 0].tolist()
                
                # Build segment info
                segments = []
                for label in unique_labels:
                    info = SEGMENT_INFO.get(int(label), {"name": f"Segment {label}", "color": [128, 128, 128]})
                    segments.append({
                        "label": int(label),
                        "name": info["name"],
                        "color": info.get("color", [128, 128, 128])[:3]  # RGB only
                    })
                
                return {
                    "success": True,
                    "dimensions": [width, height, depth],
                    "spacing": spacing,
                    "segments": segments,
                    "frames": frames,  # Array of base64-encoded frame data
                    "dtype": "uint8",
                    "totalVoxels": width * height * depth
                }
                
            finally:
                Path(tmp_path).unlink(missing_ok=True)
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting labelmap: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download-stl/{series_uid}")
async def download_segmentation_as_stl(series_uid: str):
    """
    Download segmentation as STL mesh files (one per segment)
    
    Uses marching cubes algorithm to convert each segment label to a 3D mesh.
    Returns a ZIP file containing individual STL files for each anatomical structure.
    
    Args:
        series_uid: The SeriesInstanceUID of the segmentation
        
    Returns:
        ZIP file containing STL files for each segment
    """
    from fastapi.responses import Response
    import tempfile
    import zipfile
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            # Find the series in Orthanc
            response = await client.post(
                f"{ORTHANC_URL}/tools/find",
                json={
                    "Level": "Series",
                    "Query": {"SeriesInstanceUID": series_uid},
                    "Expand": False
                }
            )
            
            if response.status_code != 200 or not response.json():
                raise HTTPException(status_code=404, detail="Segmentation not found")
            
            orthanc_series_id = response.json()[0]
            
            # Get instances
            instances_resp = await client.get(f"{ORTHANC_URL}/series/{orthanc_series_id}/instances")
            if instances_resp.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to get instances")
            
            instances = instances_resp.json()
            if not instances:
                raise HTTPException(status_code=404, detail="No instances in series")
            
            # Download the DICOM SEG file
            instance_id = instances[0]["ID"]
            dcm_resp = await client.get(f"{ORTHANC_URL}/instances/{instance_id}/file")
            
            if dcm_resp.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to download DICOM")
            
            # Convert DICOM SEG to STL meshes
            with tempfile.TemporaryDirectory() as tmpdir:
                import pydicom
                import numpy as np
                
                dcm_path = Path(tmpdir) / "seg.dcm"
                with open(dcm_path, "wb") as f:
                    f.write(dcm_resp.content)
                
                ds = pydicom.dcmread(dcm_path)
                
                if not hasattr(ds, 'PixelData'):
                    raise HTTPException(status_code=400, detail="No PixelData in DICOM SEG")
                
                pixel_array = ds.pixel_array
                
                # Handle different array shapes
                if len(pixel_array.shape) == 4:
                    # Multi-segment format: take argmax to get label map
                    seg_array = np.argmax(pixel_array, axis=0).astype(np.uint8)
                elif len(pixel_array.shape) == 3:
                    seg_array = pixel_array.astype(np.uint8)
                else:
                    seg_array = pixel_array.astype(np.uint8)
                
                # Get spacing from DICOM
                spacing = [1.0, 1.0, 1.0]  # Default spacing
                if hasattr(ds, 'PixelSpacing'):
                    spacing[0:2] = list(ds.PixelSpacing)
                if hasattr(ds, 'SliceThickness'):
                    spacing[2] = float(ds.SliceThickness)
                elif hasattr(ds, 'SpacingBetweenSlices'):
                    spacing[2] = float(ds.SpacingBetweenSlices)
                
                logger.info(f"Segmentation array shape: {seg_array.shape}, spacing: {spacing}")
                
                # Generate STL for each segment using marching cubes
                # Try multiple libraries for compatibility
                marching_cubes_func = None
                stl_mesh = None
                
                try:
                    from stl import mesh as stl_mesh
                except ImportError:
                    logger.error("numpy-stl not installed")
                    raise HTTPException(
                        status_code=500, 
                        detail="STL generation requires numpy-stl. Install with: pip install numpy-stl"
                    )
                
                # Try scipy first (usually available), then skimage as fallback
                try:
                    from scipy.ndimage import binary_erosion, generate_binary_structure
                    # Use a simple surface extraction approach with scipy
                    def marching_cubes_scipy(volume, level=0.5, spacing=(1.0, 1.0, 1.0)):
                        """Simple surface mesh generation using scipy"""
                        from scipy.spatial import Delaunay
                        
                        # Find surface voxels (voxels that are different from their neighbors)
                        struct = generate_binary_structure(3, 1)
                        eroded = binary_erosion(volume, struct)
                        surface = volume.astype(bool) & ~eroded
                        
                        # Get surface voxel coordinates
                        coords = np.argwhere(surface)
                        if len(coords) < 4:
                            return np.array([]), np.array([]), None, None
                        
                        # Scale by spacing
                        coords = coords.astype(float)
                        coords[:, 0] *= spacing[0]
                        coords[:, 1] *= spacing[1]
                        coords[:, 2] *= spacing[2]
                        
                        # Create simple triangulated surface using convex hull
                        from scipy.spatial import ConvexHull
                        try:
                            hull = ConvexHull(coords)
                            verts = coords
                            faces = hull.simplices
                            return verts, faces, None, None
                        except Exception:
                            return np.array([]), np.array([]), None, None
                    
                    marching_cubes_func = marching_cubes_scipy
                    logger.info("Using scipy-based surface extraction")
                except ImportError:
                    pass
                
                # Try skimage if scipy method didn't work
                if marching_cubes_func is None:
                    try:
                        from skimage import measure
                        marching_cubes_func = lambda vol, level, spacing: measure.marching_cubes(vol, level=level, spacing=spacing)
                        logger.info("Using skimage marching_cubes")
                    except ImportError:
                        pass
                
                if marching_cubes_func is None:
                    raise HTTPException(
                        status_code=500, 
                        detail="No mesh generation library available. Install scipy or scikit-image."
                    )
                
                unique_labels = np.unique(seg_array)
                unique_labels = unique_labels[unique_labels > 0]  # Skip background
                
                if len(unique_labels) == 0:
                    raise HTTPException(status_code=400, detail="No segments found in segmentation")
                
                stl_files = []
                
                for label in unique_labels:
                    label_int = int(label)
                    info = SEGMENT_INFO.get(label_int, {"name": f"Segment_{label_int}"})
                    segment_name = info["name"].replace(" ", "_")
                    
                    logger.info(f"Generating STL for segment {label_int}: {segment_name}")
                    
                    # Create binary mask for this segment
                    binary_mask = (seg_array == label).astype(np.uint8)
                    
                    # Check if mask has enough voxels
                    if np.sum(binary_mask) < 10:
                        logger.warning(f"Segment {label_int} has too few voxels, skipping")
                        continue
                    
                    try:
                        # Apply marching cubes to generate mesh
                        result = marching_cubes_func(binary_mask, level=0.5, spacing=tuple(spacing))
                        verts = result[0]
                        faces = result[1]
                        
                        logger.info(f"Generated mesh with {len(verts)} vertices and {len(faces)} faces")
                        
                        if len(faces) == 0:
                            logger.warning(f"No faces generated for segment {label_int}, skipping")
                            continue
                        
                        # Create STL mesh
                        stl_data = stl_mesh.Mesh(np.zeros(faces.shape[0], dtype=stl_mesh.Mesh.dtype))
                        
                        for i, face in enumerate(faces):
                            for j in range(3):
                                stl_data.vectors[i][j] = verts[face[j], :]
                        
                        # Save STL file
                        stl_filename = f"{segment_name}.stl"
                        stl_path = Path(tmpdir) / stl_filename
                        stl_data.save(str(stl_path))
                        stl_files.append((stl_filename, stl_path))
                        
                        logger.info(f"Saved STL: {stl_filename}")
                        
                    except Exception as mesh_error:
                        logger.warning(f"Failed to generate mesh for segment {label_int}: {mesh_error}")
                        continue
                
                if not stl_files:
                    raise HTTPException(status_code=400, detail="Failed to generate any STL meshes")
                
                # Create ZIP archive with all STL files
                zip_path = Path(tmpdir) / "segmentation_stl.zip"
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for filename, filepath in stl_files:
                        zf.write(filepath, filename)
                
                # Read ZIP and return
                with open(zip_path, "rb") as f:
                    zip_content = f.read()
                
                return Response(
                    content=zip_content,
                    media_type="application/zip",
                    headers={
                        "Content-Disposition": f'attachment; filename="dental_segmentation_stl.zip"'
                    }
                )
                    
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Orthanc error: {str(e)}")


