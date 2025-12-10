#!/usr/bin/env python3
"""
YOLOv8 Training Pipeline for Dental OPG Analysis
Trains on DENTEX dataset for:
- Tooth detection with FDI numbering
- Pathology detection (caries, periapical, impacted)
"""

import os
import json
import shutil
from pathlib import Path
from ultralytics import YOLO
import yaml

# Configuration
BASE_DIR = Path(__file__).parent.parent
DATASETS_DIR = BASE_DIR / "datasets"
MODELS_DIR = BASE_DIR / "models"

# DENTEX dataset structure
DENTEX_DIR = DATASETS_DIR / "dentex"

# Training configuration
TRAIN_CONFIG = {
    "batch_size": 8,
    "epochs": 100,
    "imgsz": 1024,
    "device": "mps",  # Apple Silicon GPU
    "patience": 20,
    "save_period": 10,
}


def prepare_dentex_for_yolo():
    """
    Convert DENTEX annotations to YOLO format
    
    DENTEX format: COCO-style JSON with quadrant/enumeration/diagnosis
    YOLO format: txt files with class_id x_center y_center width height
    """
    print("="*60)
    print("Preparing DENTEX dataset for YOLO training")
    print("="*60)
    
    # Check if DENTEX data exists
    dentex_training = DENTEX_DIR / "training_data"
    if not dentex_training.exists():
        print(f"DENTEX training data not found at {dentex_training}")
        print("Please download and extract the dataset first")
        return None
    
    # Create YOLO dataset structure
    yolo_dataset = DATASETS_DIR / "dentex_yolo"
    yolo_dataset.mkdir(exist_ok=True)
    (yolo_dataset / "images" / "train").mkdir(parents=True, exist_ok=True)
    (yolo_dataset / "images" / "val").mkdir(parents=True, exist_ok=True)
    (yolo_dataset / "labels" / "train").mkdir(parents=True, exist_ok=True)
    (yolo_dataset / "labels" / "val").mkdir(parents=True, exist_ok=True)
    
    # Class mapping: quadrant + enumeration = FDI number
    # For YOLO, we need integer class IDs
    # Classes 0-31: permanent teeth (11-18, 21-28, 31-38, 41-48)
    # Classes 32-35: pathologies (caries, deep_caries, periapical, impacted)
    
    classes = []
    fdi_to_class = {}
    
    # Permanent teeth (32 classes)
    for q in [1, 2, 3, 4]:
        for t in range(1, 9):
            fdi = f"{q}{t}"
            class_id = len(classes)
            fdi_to_class[fdi] = class_id
            classes.append(f"tooth_{fdi}")
    
    # Pathologies (4 classes)
    pathologies = ["Caries", "Deep Caries", "Periapical Lesion", "Impacted"]
    pathology_to_class = {}
    for p in pathologies:
        class_id = len(classes)
        pathology_to_class[p.lower().replace(" ", "_")] = class_id
        classes.append(p.lower().replace(" ", "_"))
    
    print(f"Total classes: {len(classes)}")
    print(f"Tooth classes: 32 (FDI 11-48)")
    print(f"Pathology classes: 4")
    
    # Process each DENTEX subset
    subsets = [
        "quadrant-enumeration-train",
        "quadrant-enumeration-disease",
    ]
    
    total_images = 0
    total_annotations = 0
    
    for subset in subsets:
        subset_dir = dentex_training / subset
        if not subset_dir.exists():
            print(f"Subset not found: {subset}")
            continue
        
        # Find annotation file
        anno_file = subset_dir / "annotations.json"
        if not anno_file.exists():
            # Try xray_v2.json
            anno_file = subset_dir / "xray_v2.json"
        if not anno_file.exists():
            print(f"No annotation file found in {subset}")
            continue
        
        print(f"\nProcessing: {subset}")
        
        with open(anno_file, "r") as f:
            data = json.load(f)
        
        images = {img["id"]: img for img in data.get("images", [])}
        annotations = data.get("annotations", [])
        
        # Split 80/20 train/val
        image_ids = list(images.keys())
        split_idx = int(len(image_ids) * 0.8)
        train_ids = set(image_ids[:split_idx])
        val_ids = set(image_ids[split_idx:])
        
        # Group annotations by image
        anno_by_image = {}
        for anno in annotations:
            img_id = anno["image_id"]
            if img_id not in anno_by_image:
                anno_by_image[img_id] = []
            anno_by_image[img_id].append(anno)
        
        for img_id, img_info in images.items():
            split = "train" if img_id in train_ids else "val"
            
            # Copy image
            src_img = subset_dir / img_info["file_name"]
            if not src_img.exists():
                src_img = subset_dir / "images" / img_info["file_name"]
            if not src_img.exists():
                continue
            
            dst_img = yolo_dataset / "images" / split / img_info["file_name"]
            if not dst_img.exists():
                shutil.copy(src_img, dst_img)
            
            total_images += 1
            
            # Convert annotations to YOLO format
            img_w, img_h = img_info.get("width", 2048), img_info.get("height", 1024)
            yolo_labels = []
            
            for anno in anno_by_image.get(img_id, []):
                bbox = anno.get("bbox", [])
                if len(bbox) != 4:
                    continue
                
                # COCO format: [x_min, y_min, width, height]
                x_min, y_min, w, h = bbox
                
                # Convert to YOLO format: [x_center, y_center, width, height] (normalized)
                x_center = (x_min + w / 2) / img_w
                y_center = (y_min + h / 2) / img_h
                w_norm = w / img_w
                h_norm = h / img_h
                
                # Determine class ID
                category_id = anno.get("category_id")
                category_name = anno.get("category_name", "")
                
                # Try to get FDI number from category
                fdi = None
                if "quadrant" in anno and "enumeration" in anno:
                    fdi = f"{anno['quadrant']}{anno['enumeration']}"
                
                if fdi and fdi in fdi_to_class:
                    class_id = fdi_to_class[fdi]
                elif category_name.lower() in pathology_to_class:
                    class_id = pathology_to_class[category_name.lower()]
                else:
                    continue  # Skip unknown classes
                
                yolo_labels.append(f"{class_id} {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}")
                total_annotations += 1
            
            # Write label file
            label_file = yolo_dataset / "labels" / split / (Path(img_info["file_name"]).stem + ".txt")
            with open(label_file, "w") as f:
                f.write("\n".join(yolo_labels))
    
    print(f"\nTotal images: {total_images}")
    print(f"Total annotations: {total_annotations}")
    
    # Create dataset YAML
    yaml_content = {
        "path": str(yolo_dataset),
        "train": "images/train",
        "val": "images/val",
        "names": {i: name for i, name in enumerate(classes)},
    }
    
    yaml_path = yolo_dataset / "dataset.yaml"
    with open(yaml_path, "w") as f:
        yaml.dump(yaml_content, f, default_flow_style=False)
    
    print(f"\nDataset YAML saved to: {yaml_path}")
    
    return yaml_path


def train_tooth_detection(dataset_yaml: Path = None):
    """Train YOLOv8 for tooth detection with FDI numbering"""
    print("\n" + "="*60)
    print("Training YOLOv8 for Tooth Detection")
    print("="*60)
    
    if dataset_yaml is None:
        dataset_yaml = DATASETS_DIR / "dentex_yolo" / "dataset.yaml"
    
    if not dataset_yaml.exists():
        print(f"Dataset YAML not found: {dataset_yaml}")
        print("Run prepare_dentex_for_yolo() first")
        return None
    
    # Load YOLOv8 model (medium size for balance of speed/accuracy)
    model = YOLO("yolov8m-seg.pt")  # Segmentation variant
    
    # Train
    results = model.train(
        data=str(dataset_yaml),
        epochs=TRAIN_CONFIG["epochs"],
        imgsz=TRAIN_CONFIG["imgsz"],
        batch=TRAIN_CONFIG["batch_size"],
        device=TRAIN_CONFIG["device"],
        patience=TRAIN_CONFIG["patience"],
        save_period=TRAIN_CONFIG["save_period"],
        project=str(MODELS_DIR / "yolov8"),
        name="tooth_detection",
        exist_ok=True,
    )
    
    print("\nTraining completed!")
    print(f"Best model saved to: {results.save_dir}/weights/best.pt")
    
    return results


def validate_model(model_path: str = None):
    """Validate trained model"""
    if model_path is None:
        model_path = MODELS_DIR / "yolov8" / "tooth_detection" / "weights" / "best.pt"
    
    if not Path(model_path).exists():
        print(f"Model not found: {model_path}")
        return None
    
    model = YOLO(model_path)
    
    # Validate on validation set
    results = model.val(
        data=str(DATASETS_DIR / "dentex_yolo" / "dataset.yaml"),
        imgsz=TRAIN_CONFIG["imgsz"],
    )
    
    print("\nValidation Results:")
    print(f"  mAP50: {results.box.map50:.4f}")
    print(f"  mAP50-95: {results.box.map:.4f}")
    
    return results


def export_model(model_path: str = None, format: str = "onnx"):
    """Export model for deployment"""
    if model_path is None:
        model_path = MODELS_DIR / "yolov8" / "tooth_detection" / "weights" / "best.pt"
    
    model = YOLO(model_path)
    
    # Export to ONNX for deployment
    model.export(format=format, imgsz=TRAIN_CONFIG["imgsz"])
    
    print(f"\nModel exported to {format} format")


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python train_yolov8.py <command>")
        print("\nCommands:")
        print("  prepare   - Prepare DENTEX dataset for YOLO training")
        print("  train     - Train YOLOv8 tooth detection model")
        print("  validate  - Validate trained model")
        print("  export    - Export model for deployment (ONNX)")
        print("  all       - Run full pipeline")
        return
    
    command = sys.argv[1].lower()
    
    if command == "prepare":
        prepare_dentex_for_yolo()
    elif command == "train":
        train_tooth_detection()
    elif command == "validate":
        validate_model()
    elif command == "export":
        export_model()
    elif command == "all":
        yaml_path = prepare_dentex_for_yolo()
        if yaml_path:
            train_tooth_detection(yaml_path)
            validate_model()
            export_model()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
