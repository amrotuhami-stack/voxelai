#!/usr/bin/env python3
"""
Start YOLOv8 Dental AI Training
Run this script to train the model on the unified dataset
"""

from ultralytics import YOLO
from pathlib import Path

def main():
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    DATASET_YAML = BASE_DIR / "datasets" / "unified" / "dataset.yaml"
    OUTPUT_DIR = BASE_DIR / "models" / "yolov8"

    print("=" * 60)
    print("Starting Dental AI YOLOv8 Training")
    print("=" * 60)
    print(f"Dataset: {DATASET_YAML}")
    print(f"Output: {OUTPUT_DIR}")
    print()

    # Continue training from epoch 38 checkpoint with extended epochs
    LAST_CHECKPOINT = OUTPUT_DIR / "dental_unified_v2" / "weights" / "last.pt"

    print(f"Loading checkpoint: {LAST_CHECKPOINT}")
    model = YOLO(str(LAST_CHECKPOINT))

    # Start new training session from pretrained checkpoint
    # Model weights are already trained for 38 epochs, continue for 112 more
    results = model.train(
        data=str(DATASET_YAML),
        epochs=112,         # 150 - 38 = 112 more epochs
        imgsz=1024,
        batch=8,
        device="cuda",
        patience=25,
        save_period=10,
        workers=8,
        cache="ram",
        project=str(OUTPUT_DIR),
        name="dental_unified_v3",   # New name to avoid conflicts
        exist_ok=True,
        amp=True,
    )

    print("\n" + "=" * 60)
    print("Training Complete!")
    print("=" * 60)
    print(f"Best model: {results.save_dir}/weights/best.pt")


if __name__ == "__main__":
    main()
