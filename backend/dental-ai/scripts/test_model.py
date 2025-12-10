#!/usr/bin/env python3
"""
Test the trained dental AI model on sample X-rays

Usage:
    python test_model.py                     # Test on random sample from dataset
    python test_model.py /path/to/image.jpg  # Test on specific image
"""

import sys
from pathlib import Path
from ultralytics import YOLO
import cv2
import numpy as np

# Paths
BASE_DIR = Path(__file__).parent.parent
MODEL_PATH = BASE_DIR / "models" / "yolov8" / "dental_unified" / "weights" / "best.pt"
SAMPLE_DIR = BASE_DIR / "datasets" / "unified" / "images" / "val"
OUTPUT_DIR = BASE_DIR / "test_results"

# FDI tooth names for display
FDI_NAMES = {
    11: "UR1", 12: "UR2", 13: "UR3", 14: "UR4", 15: "UR5", 16: "UR6", 17: "UR7", 18: "UR8",
    21: "UL1", 22: "UL2", 23: "UL3", 24: "UL4", 25: "UL5", 26: "UL6", 27: "UL7", 28: "UL8",
    31: "LL1", 32: "LL2", 33: "LL3", 34: "LL4", 35: "LL5", 36: "LL6", 37: "LL7", 38: "LL8",
    41: "LR1", 42: "LR2", 43: "LR3", 44: "LR4", 45: "LR5", 46: "LR6", 47: "LR7", 48: "LR8",
}

PATHOLOGY_NAMES = {
    32: "impacted",
    33: "caries", 
    34: "periapical",
    35: "deep_caries",
}


def test_model(image_path=None, conf_threshold=0.25):
    """Run inference on an image and save results"""
    
    print("="*60)
    print("DENTAL AI MODEL TEST")
    print("="*60)
    
    # Check model exists
    if not MODEL_PATH.exists():
        print(f"❌ Model not found at: {MODEL_PATH}")
        print("Please train the model first or provide a valid model path.")
        return None
    
    print(f"✅ Loading model: {MODEL_PATH}")
    model = YOLO(str(MODEL_PATH))
    
    # Get image path
    if image_path:
        img_path = Path(image_path)
        if not img_path.exists():
            print(f"❌ Image not found: {img_path}")
            return None
    else:
        # Pick a random sample from validation set
        if SAMPLE_DIR.exists():
            samples = list(SAMPLE_DIR.glob("*.png")) + list(SAMPLE_DIR.glob("*.jpg"))
            if samples:
                import random
                img_path = random.choice(samples)
                print(f"📷 Using random sample: {img_path.name}")
            else:
                print(f"❌ No images found in {SAMPLE_DIR}")
                return None
        else:
            print(f"❌ Sample directory not found: {SAMPLE_DIR}")
            return None
    
    print(f"\n📷 Running inference on: {img_path}")
    
    # Run inference
    results = model(str(img_path), conf=conf_threshold, verbose=False)
    result = results[0]
    
    # Parse detections
    boxes = result.boxes
    print(f"\n🦷 Found {len(boxes)} detections:")
    print("-" * 50)
    
    teeth_detected = []
    pathologies_detected = []
    
    for i, box in enumerate(boxes):
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        
        # Determine if tooth or pathology
        if cls_id < 32:
            # Tooth: class 0-31 maps to FDI 11-48
            quadrant = (cls_id // 8) + 1
            position = (cls_id % 8) + 1
            fdi = quadrant * 10 + position
            name = FDI_NAMES.get(fdi, f"tooth_{fdi}")
            teeth_detected.append({
                'fdi': fdi,
                'name': name,
                'conf': conf,
                'bbox': [x1, y1, x2, y2]
            })
            print(f"  🦷 Tooth {fdi} ({name}): {conf:.2%}")
        else:
            # Pathology
            pathology_name = PATHOLOGY_NAMES.get(cls_id, f"pathology_{cls_id}")
            pathologies_detected.append({
                'type': pathology_name,
                'conf': conf,
                'bbox': [x1, y1, x2, y2]
            })
            print(f"  ⚠️  {pathology_name}: {conf:.2%}")
    
    print("-" * 50)
    print(f"\n📊 Summary:")
    print(f"   Teeth detected: {len(teeth_detected)}")
    print(f"   Pathologies: {len(pathologies_detected)}")
    
    # Save annotated image
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / f"result_{img_path.stem}.jpg"
    
    # Get annotated image
    annotated = result.plot()
    cv2.imwrite(str(output_path), annotated)
    print(f"\n💾 Saved annotated image: {output_path}")
    
    return {
        'image': str(img_path),
        'teeth': teeth_detected,
        'pathologies': pathologies_detected,
        'output_image': str(output_path)
    }


if __name__ == "__main__":
    image_path = sys.argv[1] if len(sys.argv) > 1 else None
    result = test_model(image_path)
    
    if result:
        print("\n✅ Test complete!")
        print(f"   View result: open {result['output_image']}")
