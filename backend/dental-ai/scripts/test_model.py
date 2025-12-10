#!/usr/bin/env python3
"""
Test the trained YOLOv8 dental model on sample images
"""

from ultralytics import YOLO
from pathlib import Path
import os

def main():
    # Paths
    BASE_DIR = Path(__file__).parent.parent

    # Use the best model from V2 training (mAP50 = 0.761)
    MODEL_PATH = BASE_DIR / "models" / "yolov8" / "dental_unified_v2" / "weights" / "best.pt"

    # Get sample images from validation set
    VAL_IMAGES = BASE_DIR / "datasets" / "unified" / "images" / "val"
    OUTPUT_DIR = BASE_DIR / "test_results"

    print("=" * 60)
    print("Testing Dental AI YOLOv8 Model")
    print("=" * 60)
    print(f"Model: {MODEL_PATH}")
    print(f"Images: {VAL_IMAGES}")
    print(f"Output: {OUTPUT_DIR}")
    print()

    # Load model
    print("Loading model...")
    model = YOLO(str(MODEL_PATH))

    # Get first 5 validation images
    image_files = list(VAL_IMAGES.glob("*.png"))[:5]
    if not image_files:
        image_files = list(VAL_IMAGES.glob("*.jpg"))[:5]

    print(f"Found {len(image_files)} test images")

    # Run inference
    print("\nRunning inference...")
    results = model.predict(
        source=[str(f) for f in image_files],
        save=True,
        project=str(OUTPUT_DIR),
        name="predictions",
        exist_ok=True,
        conf=0.25,  # Confidence threshold
        iou=0.45,   # NMS IoU threshold
    )

    # Print results
    print("\n" + "=" * 60)
    print("Detection Results")
    print("=" * 60)

    for i, result in enumerate(results):
        print(f"\nImage {i+1}: {Path(result.path).name}")
        boxes = result.boxes
        print(f"  Detections: {len(boxes)}")

        if len(boxes) > 0:
            # Get class names and confidences
            for j, box in enumerate(boxes[:10]):  # Show first 10 detections
                cls_id = int(box.cls[0])
                cls_name = model.names[cls_id]
                conf = float(box.conf[0])
                print(f"    - {cls_name}: {conf:.2%}")

    print("\n" + "=" * 60)
    print(f"Results saved to: {OUTPUT_DIR}/predictions")
    print("=" * 60)


if __name__ == "__main__":
    main()
