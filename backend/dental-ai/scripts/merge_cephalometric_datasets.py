#!/usr/bin/env python3
"""
Merge Cephalometric Datasets for Training

Combines ISBI 2015, Aariz, and CL-Detection 2024 datasets into a unified
training dataset with consistent landmark format.

Usage:
    python merge_cephalometric_datasets.py --common    # Only 19 common landmarks
    python merge_cephalometric_datasets.py --all       # All 49 landmarks (sparse)
"""

import os
import sys
import argparse
import shutil
import json
import yaml
from pathlib import Path
from PIL import Image
import numpy as np

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))
from cephalometric_landmark_schema import (
    ISBI_TO_UNIFIED,
    AARIZ_TO_UNIFIED,
    CL_DETECTION_TO_UNIFIED,
    get_unified_landmark_name,
    get_common_landmarks,
    NUM_UNIFIED_LANDMARKS,
)

BASE_DIR = Path(__file__).parent.parent
DATASETS_DIR = BASE_DIR / "datasets"
OUTPUT_DIR = DATASETS_DIR / "cephalometric_unified"


def parse_isbi_annotation(txt_path: Path) -> list:
    """Parse ISBI 2015 annotation file (x,y per line)"""
    landmarks = []
    with open(txt_path, 'r') as f:
        for i, line in enumerate(f):
            parts = line.strip().split(',')
            if len(parts) >= 2:
                x, y = float(parts[0]), float(parts[1])
                landmarks.append({
                    "original_id": i,
                    "x": x,
                    "y": y,
                    "unified_id": ISBI_TO_UNIFIED.get(i),
                })
    return landmarks


def parse_aariz_annotation(txt_path: Path) -> list:
    """Parse Aariz/CEPHA29 annotation file"""
    landmarks = []
    with open(txt_path, 'r') as f:
        for i, line in enumerate(f):
            parts = line.strip().split()
            if len(parts) >= 2:
                x, y = float(parts[0]), float(parts[1])
                landmarks.append({
                    "original_id": i,
                    "x": x,
                    "y": y,
                    "unified_id": AARIZ_TO_UNIFIED.get(i),
                })
    return landmarks


def parse_cl_detection_annotation(json_path: Path) -> list:
    """Parse CL-Detection 2024 JSON annotation"""
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    landmarks = []
    for i, point in enumerate(data.get("landmarks", [])):
        x, y = point.get("x", 0), point.get("y", 0)
        landmarks.append({
            "original_id": i,
            "x": x,
            "y": y,
            "unified_id": CL_DETECTION_TO_UNIFIED.get(i),
        })
    return landmarks


def convert_to_unified_format(landmarks: list, img_width: int, img_height: int, 
                              use_common_only: bool = True) -> dict:
    """
    Convert landmarks to unified format.
    
    Returns dict with:
    - normalized coordinates (0-1 range)
    - unified landmark IDs
    """
    common = get_common_landmarks() if use_common_only else list(range(NUM_UNIFIED_LANDMARKS))
    
    result = {
        "image_width": img_width,
        "image_height": img_height,
        "landmarks": {}
    }
    
    for lm in landmarks:
        unified_id = lm.get("unified_id")
        if unified_id is not None and unified_id in common:
            result["landmarks"][unified_id] = {
                "name": get_unified_landmark_name(unified_id),
                "x": lm["x"] / img_width,  # Normalize
                "y": lm["y"] / img_height,
                "x_abs": lm["x"],
                "y_abs": lm["y"],
            }
    
    return result


def process_isbi2015(output_dir: Path, use_common_only: bool = True):
    """Process ISBI 2015 dataset"""
    isbi_dir = DATASETS_DIR / "isbi2015"
    
    if not isbi_dir.exists():
        print("❌ ISBI 2015 not found")
        return []
    
    print("\n📁 Processing ISBI 2015...")
    
    samples = []
    
    # Process training, test1, test2
    splits = {
        "Training": "train",
        "Test1": "val",
        "Test2": "test"
    }
    
    raw_dir = isbi_dir / "RawImage"
    anno_dir = isbi_dir / "AnnotationsByMD"
    
    # Use senior orthodontist annotations
    senior_dir = anno_dir / "400_senior"
    if not senior_dir.exists():
        senior_dir = list(anno_dir.glob("*senior*"))[0] if any(anno_dir.glob("*senior*")) else anno_dir
    
    for split_name, split_type in [("TrainingData", "train"), ("Test1Data", "val"), ("Test2Data", "test")]:
        split_dir = raw_dir / split_name
        if not split_dir.exists():
            continue
        
        images = list(split_dir.glob("*.bmp"))
        print(f"  Found {len(images)} images in {split_name}")
        
        for img_path in images:
            # Find corresponding annotation
            img_name = img_path.stem  # e.g., "001"
            anno_path = senior_dir / f"{img_name}.txt"
            
            if not anno_path.exists():
                continue
            
            # Get image dimensions
            with Image.open(img_path) as img:
                width, height = img.size
            
            # Parse landmarks
            landmarks = parse_isbi_annotation(anno_path)
            unified = convert_to_unified_format(landmarks, width, height, use_common_only)
            
            # Copy image
            dest_img_dir = output_dir / "images" / split_type
            dest_img_dir.mkdir(parents=True, exist_ok=True)
            dest_img = dest_img_dir / f"isbi_{img_name}.png"
            
            # Convert BMP to PNG (handle truncated images)
            try:
                from PIL import ImageFile
                ImageFile.LOAD_TRUNCATED_IMAGES = True
                with Image.open(img_path) as img:
                    img.save(dest_img, "PNG")
            except Exception as e:
                print(f"    ⚠️ Skipping {img_name}: {e}")
                continue
            
            # Save annotation
            dest_anno_dir = output_dir / "annotations" / split_type
            dest_anno_dir.mkdir(parents=True, exist_ok=True)
            dest_anno = dest_anno_dir / f"isbi_{img_name}.json"
            
            with open(dest_anno, 'w') as f:
                json.dump(unified, f, indent=2)
            
            samples.append({
                "image": str(dest_img.relative_to(output_dir)),
                "annotation": str(dest_anno.relative_to(output_dir)),
                "split": split_type,
                "source": "isbi2015",
            })
    
    print(f"  ✅ Processed {len(samples)} samples from ISBI 2015")
    return samples


def process_aariz(output_dir: Path, use_common_only: bool = True):
    """Process Aariz/CEPHA29 dataset"""
    aariz_dir = DATASETS_DIR / "cephalometric" / "aariz"
    
    if not aariz_dir.exists():
        print("❌ Aariz dataset not found")
        return []
    
    # Check if data folders exist
    if not (aariz_dir / "train").exists():
        print("❌ Aariz dataset folders not found (train/valid/test)")
        return []
    
    print("\n📁 Processing Aariz dataset...")
    
    # Aariz landmark name to unified ID mapping
    AARIZ_NAME_TO_UNIFIED = {
        "Sella": 0,
        "Nasion": 1,
        "Orbitale": 2,
        "Porion": 3,
        "A-point": 4,
        "B-point": 5,
        "Pogonion": 6,
        "Menton": 7,
        "Gnathion": 8,
        "Gonion": 9,
        "Articulare": 10,
        "Anterior Nasal Spine": 12,
        "Posterior Nasal Spine": 13,
        "Upper Incisor Tip": 17,
        "Lower Incisor Tip": 19,
        "Subnasale": 31,
        "Labrale superius": 32,  # Upper Lip
        "Labrale inferius": 33,  # Lower Lip
        "Soft Tissue Pogonion": 34,
        "Pronasale": 29,
        "Soft Tissue Nasion": 27,
        "Condylion": 16,
        "Upper Incisor Apex": 18,
        "Lower Incisor Apex": 20,
        "Upper Molar Cusp Tip": 25,
        "Lower Molar Cusp Tip": 26,
    }
    
    samples = []
    
    for split_name, split_type in [("train", "train"), ("valid", "val"), ("test", "test")]:
        split_dir = aariz_dir / split_name
        if not split_dir.exists():
            continue
        
        img_dir = split_dir / "Cephalograms"
        anno_dir = split_dir / "Annotations" / "Cephalometric Landmarks" / "Senior Orthodontists"
        
        if not img_dir.exists() or not anno_dir.exists():
            print(f"  ⚠️ Skipping {split_name}: directories not found")
            continue
        
        images = list(img_dir.glob("*.png")) + list(img_dir.glob("*.jpg"))
        print(f"  Found {len(images)} images in {split_name}")
        
        for img_path in images:
            img_id = img_path.stem
            anno_path = anno_dir / f"{img_id}.json"
            
            if not anno_path.exists():
                continue
            
            # Parse Aariz JSON annotation
            try:
                with open(anno_path, 'r') as f:
                    data = json.load(f)
                
                # Get image dimensions
                from PIL import ImageFile
                ImageFile.LOAD_TRUNCATED_IMAGES = True
                with Image.open(img_path) as img:
                    width, height = img.size
                
                # Parse landmarks
                landmarks = []
                for lm in data.get("landmarks", []):
                    title = lm.get("title", "")
                    value = lm.get("value", {})
                    x, y = value.get("x", 0), value.get("y", 0)
                    unified_id = AARIZ_NAME_TO_UNIFIED.get(title)
                    
                    landmarks.append({
                        "original_title": title,
                        "x": x,
                        "y": y,
                        "unified_id": unified_id,
                    })
                
                # Convert to unified format
                unified = convert_to_unified_format(landmarks, width, height, use_common_only)
                
                # Copy image
                dest_img_dir = output_dir / "images" / split_type
                dest_img_dir.mkdir(parents=True, exist_ok=True)
                dest_img = dest_img_dir / f"aariz_{img_id}.png"
                
                with Image.open(img_path) as img:
                    img.save(dest_img, "PNG")
                
                # Save annotation
                dest_anno_dir = output_dir / "annotations" / split_type
                dest_anno_dir.mkdir(parents=True, exist_ok=True)
                dest_anno = dest_anno_dir / f"aariz_{img_id}.json"
                
                with open(dest_anno, 'w') as f:
                    json.dump(unified, f, indent=2)
                
                samples.append({
                    "image": str(dest_img.relative_to(output_dir)),
                    "annotation": str(dest_anno.relative_to(output_dir)),
                    "split": split_type,
                    "source": "aariz",
                })
            except Exception as e:
                print(f"    ⚠️ Error processing {img_id}: {e}")
                continue
    
    print(f"  ✅ Processed {len(samples)} samples from Aariz")
    return samples


def process_cl_detection(output_dir: Path, use_common_only: bool = True):
    """Process CL-Detection 2024 dataset"""
    cl_dir = DATASETS_DIR / "cephalometric" / "cl-detection-2024"
    
    if not cl_dir.exists() or not any(cl_dir.iterdir()):
        print("❌ CL-Detection 2024 not found")
        return []
    
    print("\n📁 Processing CL-Detection 2024...")
    # Implementation for JSON format...
    samples = []
    print(f"  ✅ Processed {len(samples)} samples from CL-Detection 2024")
    return samples


def create_dataset_yaml(output_dir: Path, num_landmarks: int):
    """Create dataset.yaml for training"""
    yaml_content = {
        "path": str(output_dir),
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
        "nc": num_landmarks,
        "names": {
            i: get_unified_landmark_name(i) 
            for i in get_common_landmarks()
        }
    }
    
    yaml_path = output_dir / "dataset.yaml"
    with open(yaml_path, 'w') as f:
        yaml.dump(yaml_content, f, default_flow_style=False)
    
    print(f"\n✅ Created dataset.yaml with {num_landmarks} landmarks")
    return yaml_path


def main():
    parser = argparse.ArgumentParser(description="Merge cephalometric datasets")
    parser.add_argument("--common", action="store_true", 
                        help="Use only 19 common landmarks (recommended for training)")
    parser.add_argument("--all", action="store_true",
                        help="Use all 49 landmarks (sparse, advanced)")
    parser.add_argument("--output", type=str, default=None,
                        help="Output directory")
    
    args = parser.parse_args()
    
    use_common_only = not args.all
    num_landmarks = 19 if use_common_only else 49
    
    output_dir = Path(args.output) if args.output else OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("="*60)
    print("MERGING CEPHALOMETRIC DATASETS")
    print("="*60)
    print(f"\nOutput: {output_dir}")
    print(f"Landmarks: {num_landmarks} ({'common' if use_common_only else 'all'})")
    
    all_samples = []
    
    # Process each dataset
    all_samples.extend(process_isbi2015(output_dir, use_common_only))
    all_samples.extend(process_aariz(output_dir, use_common_only))
    all_samples.extend(process_cl_detection(output_dir, use_common_only))
    
    # Save manifest
    manifest_path = output_dir / "manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump({
            "total_samples": len(all_samples),
            "num_landmarks": num_landmarks,
            "use_common_only": use_common_only,
            "samples": all_samples,
        }, f, indent=2)
    
    # Create dataset.yaml
    create_dataset_yaml(output_dir, num_landmarks)
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    sources = {}
    splits = {}
    for s in all_samples:
        sources[s["source"]] = sources.get(s["source"], 0) + 1
        splits[s["split"]] = splits.get(s["split"], 0) + 1
    
    print(f"\nTotal samples: {len(all_samples)}")
    print("\nBy source:")
    for src, count in sources.items():
        print(f"  {src}: {count}")
    
    print("\nBy split:")
    for split, count in splits.items():
        print(f"  {split}: {count}")
    
    print(f"\n✅ Merged dataset saved to: {output_dir}")
    print("\nNext: Train CEPHMark-Net with this dataset")


if __name__ == "__main__":
    main()
