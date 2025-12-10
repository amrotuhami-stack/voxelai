#!/usr/bin/env python3
"""
Convert DENTEX annotations to YOLO format for training

DENTEX format:
- category_id_1: Quadrant (0-3 = Quadrants 1-4)
- category_id_2: Tooth position (0-7 = Positions 1-8)
- category_id_3: Diagnosis (0=Impacted, 1=Caries, 2=Periapical, 3=Deep Caries)

YOLO format:
- class_id x_center y_center width height (normalized 0-1)
"""

import json
import shutil
from pathlib import Path
import yaml
import random

# Paths
BASE_DIR = Path(__file__).parent.parent
DENTEX_DIR = BASE_DIR / "datasets" / "dentex" / "training_data"
OUTPUT_DIR = BASE_DIR / "datasets" / "dentex_yolo"

# DENTEX category mappings
QUADRANT_MAP = {0: 1, 1: 2, 2: 3, 3: 4}  # category_id to FDI quadrant
POSITION_MAP = {i: i + 1 for i in range(8)}  # category_id to FDI position
DIAGNOSIS_MAP = {
    0: "impacted",
    1: "caries",
    2: "periapical_lesion",
    3: "deep_caries",
}


def create_yolo_dataset():
    """Convert DENTEX to YOLO format"""
    print("="*60)
    print("Converting DENTEX to YOLO format")
    print("="*60)
    
    # Create output directories
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "images" / "train").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "images" / "val").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "labels" / "train").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "labels" / "val").mkdir(parents=True, exist_ok=True)
    
    # Build class list: 32 tooth classes + 4 pathology classes
    classes = []
    fdi_to_class = {}
    
    # Tooth classes (FDI numbering: 11-18, 21-28, 31-38, 41-48)
    for q in [1, 2, 3, 4]:
        for t in range(1, 9):
            fdi = f"{q}{t}"
            fdi_to_class[fdi] = len(classes)
            classes.append(f"tooth_{fdi}")
    
    # Pathology classes
    pathology_to_class = {
        "impacted": len(classes),
        "caries": len(classes) + 1,
        "periapical_lesion": len(classes) + 2,
        "deep_caries": len(classes) + 3,
    }
    classes.extend(["impacted", "caries", "periapical_lesion", "deep_caries"])
    
    print(f"Total classes: {len(classes)}")
    print(f"  Tooth classes: 32 (FDI 11-48)")
    print(f"  Pathology classes: 4")
    
    # Process quadrant-enumeration-disease (best annotations)
    disease_dir = DENTEX_DIR / "quadrant-enumeration-disease"
    if not disease_dir.exists():
        print(f"ERROR: {disease_dir} not found")
        return None
    
    anno_file = disease_dir / "train_quadrant_enumeration_disease.json"
    if not anno_file.exists():
        print(f"ERROR: Annotation file not found: {anno_file}")
        return None
    
    with open(anno_file, "r") as f:
        data = json.load(f)
    
    images = {img["id"]: img for img in data.get("images", [])}
    annotations = data.get("annotations", [])
    
    print(f"\nFound {len(images)} images and {len(annotations)} annotations")
    
    # Group annotations by image
    anno_by_image = {}
    for anno in annotations:
        img_id = anno["image_id"]
        if img_id not in anno_by_image:
            anno_by_image[img_id] = []
        anno_by_image[img_id].append(anno)
    
    # Split 80/20 train/val
    image_ids = list(images.keys())
    random.seed(42)
    random.shuffle(image_ids)
    split_idx = int(len(image_ids) * 0.8)
    train_ids = set(image_ids[:split_idx])
    val_ids = set(image_ids[split_idx:])
    
    print(f"Train: {len(train_ids)} images, Val: {len(val_ids)} images")
    
    total_tooth_annos = 0
    total_disease_annos = 0
    
    for img_id, img_info in images.items():
        split = "train" if img_id in train_ids else "val"
        
        # Find and copy image
        img_name = img_info.get("file_name", f"train_{img_id}.png")
        src_img = disease_dir / "xrays" / img_name
        
        if not src_img.exists():
            # Try alternative naming
            src_img = disease_dir / "xrays" / f"train_{img_id}.png"
        
        if not src_img.exists():
            continue
        
        dst_img = OUTPUT_DIR / "images" / split / img_name
        if not dst_img.exists():
            shutil.copy(src_img, dst_img)
        
        # Get image dimensions
        img_w = img_info.get("width", 2943)  # Default DENTEX width
        img_h = img_info.get("height", 1435)  # Default DENTEX height
        
        # Convert annotations
        yolo_labels = []
        
        for anno in anno_by_image.get(img_id, []):
            bbox = anno.get("bbox", [])
            if len(bbox) != 4:
                continue
            
            x, y, w, h = bbox
            
            # Normalize to YOLO format
            x_center = (x + w / 2) / img_w
            y_center = (y + h / 2) / img_h
            w_norm = w / img_w
            h_norm = h / img_h
            
            # Clamp values to valid range
            x_center = max(0, min(1, x_center))
            y_center = max(0, min(1, y_center))
            w_norm = max(0, min(1, w_norm))
            h_norm = max(0, min(1, h_norm))
            
            # Get quadrant and position for FDI number
            quadrant_idx = anno.get("category_id_1")
            position_idx = anno.get("category_id_2")
            diagnosis_idx = anno.get("category_id_3")
            
            if quadrant_idx is not None and position_idx is not None:
                quadrant = QUADRANT_MAP.get(quadrant_idx)
                position = POSITION_MAP.get(position_idx)
                
                if quadrant and position:
                    fdi = f"{quadrant}{position}"
                    if fdi in fdi_to_class:
                        class_id = fdi_to_class[fdi]
                        yolo_labels.append(f"{class_id} {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}")
                        total_tooth_annos += 1
            
            # Also add disease annotation if present (not "normal" = not 0-indexed diagnosis)
            if diagnosis_idx is not None and diagnosis_idx in DIAGNOSIS_MAP:
                diagnosis = DIAGNOSIS_MAP[diagnosis_idx]
                if diagnosis in pathology_to_class:
                    class_id = pathology_to_class[diagnosis]
                    yolo_labels.append(f"{class_id} {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}")
                    total_disease_annos += 1
        
        # Write label file
        label_name = Path(img_name).stem + ".txt"
        label_file = OUTPUT_DIR / "labels" / split / label_name
        with open(label_file, "w") as f:
            f.write("\n".join(yolo_labels))
    
    print(f"\nConverted:")
    print(f"  Tooth annotations: {total_tooth_annos}")
    print(f"  Disease annotations: {total_disease_annos}")
    
    # Create dataset YAML
    yaml_content = {
        "path": str(OUTPUT_DIR.absolute()),
        "train": "images/train",
        "val": "images/val",
        "nc": len(classes),
        "names": classes,
    }
    
    yaml_path = OUTPUT_DIR / "dataset.yaml"
    with open(yaml_path, "w") as f:
        yaml.dump(yaml_content, f, default_flow_style=False)
    
    print(f"\nDataset YAML saved to: {yaml_path}")
    
    # Also save class mapping for reference
    class_mapping = {
        "fdi_to_class": fdi_to_class,
        "pathology_to_class": pathology_to_class,
        "classes": classes,
    }
    with open(OUTPUT_DIR / "class_mapping.json", "w") as f:
        json.dump(class_mapping, f, indent=2)
    
    return yaml_path


if __name__ == "__main__":
    create_yolo_dataset()
