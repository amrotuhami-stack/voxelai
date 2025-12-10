#!/usr/bin/env python3
"""
Merge multiple dental datasets into unified YOLO format

Combines:
1. DENTEX (705 images, 36 classes: 32 teeth + 4 pathologies)
2. UFBA-425 (1,384 images, 32 tooth classes)

Output: Unified dataset with 36 classes for training
"""

import os
import shutil
import json
from pathlib import Path
import yaml
import random

BASE_DIR = Path(__file__).parent.parent
DATASETS_DIR = BASE_DIR / "datasets"
OUTPUT_DIR = DATASETS_DIR / "unified"


def merge_datasets():
    """Merge DENTEX and UFBA-425 into unified dataset"""
    print("="*60)
    print("Merging Dental Datasets")
    print("="*60)
    
    # Create output directories
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "images" / "train").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "images" / "val").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "labels" / "train").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "labels" / "val").mkdir(parents=True, exist_ok=True)
    
    # Define unified class list (36 classes)
    # 0-31: FDI teeth (11-18, 21-28, 31-38, 41-48)
    # 32-35: Pathologies (impacted, caries, periapical_lesion, deep_caries)
    
    # FDI to class ID mapping
    fdi_to_class = {}
    classes = []
    
    for q in [1, 2, 3, 4]:
        for t in range(1, 9):
            fdi = f"{q}{t}"
            fdi_to_class[fdi] = len(classes)
            classes.append(f"tooth_{fdi}")
    
    # Pathologies
    pathologies = ["impacted", "caries", "periapical_lesion", "deep_caries"]
    for p in pathologies:
        classes.append(p)
    
    print(f"Unified classes: {len(classes)}")
    
    total_train = 0
    total_val = 0
    
    # ===== Process DENTEX =====
    dentex_dir = DATASETS_DIR / "dentex_yolo"
    if dentex_dir.exists():
        print("\n[1] Processing DENTEX...")
        
        for split in ["train", "val"]:
            src_images = dentex_dir / "images" / split
            src_labels = dentex_dir / "labels" / split
            
            if not src_images.exists():
                continue
            
            for img_file in src_images.glob("*.png"):
                # Copy image with prefix
                dst_name = f"dentex_{img_file.name}"
                dst_img = OUTPUT_DIR / "images" / split / dst_name
                
                if not dst_img.exists():
                    shutil.copy(img_file, dst_img)
                
                # Copy label (class IDs already match)
                label_file = src_labels / (img_file.stem + ".txt")
                if label_file.exists():
                    dst_label = OUTPUT_DIR / "labels" / split / (dst_img.stem + ".txt")
                    shutil.copy(label_file, dst_label)
                
                if split == "train":
                    total_train += 1
                else:
                    total_val += 1
        
        print(f"  Added {total_train} train, {total_val} val from DENTEX")
    
    # ===== Process UFBA-425 =====
    ufba_dir = DATASETS_DIR / "ufba-425" / "Dataset" / "yolo_train_dataset"
    if ufba_dir.exists():
        print("\n[2] Processing UFBA-425...")
        
        # UFBA class names are FDI numbers directly
        ufba_classes = ['11', '12', '13', '14', '15', '16', '17', '18',
                        '21', '22', '23', '24', '25', '26', '27', '28',
                        '31', '32', '33', '34', '35', '36', '37', '38',
                        '41', '42', '43', '44', '45', '46', '47', '48']
        
        # Map UFBA class IDs to unified class IDs
        ufba_to_unified = {}
        for ufba_id, fdi in enumerate(ufba_classes):
            if fdi in fdi_to_class:
                ufba_to_unified[ufba_id] = fdi_to_class[fdi]
        
        ufba_train = 0
        ufba_val = 0
        
        for split_name, src_dir in [("train", "train"), ("val", "valid")]:
            src_images = ufba_dir / src_dir / "images"
            src_labels = ufba_dir / src_dir / "labels"
            
            if not src_images.exists():
                continue
            
            for img_file in src_images.glob("*"):
                if img_file.suffix.lower() not in ['.jpg', '.jpeg', '.png']:
                    continue
                
                # Copy image with prefix
                dst_name = f"ufba_{img_file.name}"
                dst_img = OUTPUT_DIR / "images" / split_name / dst_name
                
                if not dst_img.exists():
                    shutil.copy(img_file, dst_img)
                
                # Convert and copy label
                label_file = src_labels / (img_file.stem + ".txt")
                if label_file.exists():
                    with open(label_file, "r") as f:
                        lines = f.readlines()
                    
                    # Convert class IDs
                    converted_lines = []
                    for line in lines:
                        parts = line.strip().split()
                        if len(parts) >= 5:
                            old_id = int(parts[0])
                            if old_id in ufba_to_unified:
                                parts[0] = str(ufba_to_unified[old_id])
                                converted_lines.append(" ".join(parts))
                    
                    dst_label = OUTPUT_DIR / "labels" / split_name / (dst_img.stem + ".txt")
                    with open(dst_label, "w") as f:
                        f.write("\n".join(converted_lines))
                
                if split_name == "train":
                    ufba_train += 1
                else:
                    ufba_val += 1
        
        total_train += ufba_train
        total_val += ufba_val
        print(f"  Added {ufba_train} train, {ufba_val} val from UFBA-425")
    
    # ===== Create dataset YAML =====
    print("\n[3] Creating dataset YAML...")
    
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
    
    # Save class mapping
    class_mapping = {
        "fdi_to_class": fdi_to_class,
        "classes": classes,
        "sources": {
            "dentex": "705 images, 36 classes (teeth + pathologies)",
            "ufba_425": "1384 images, 32 tooth classes",
        }
    }
    with open(OUTPUT_DIR / "class_mapping.json", "w") as f:
        json.dump(class_mapping, f, indent=2)
    
    print(f"\n" + "="*60)
    print("MERGE COMPLETE")
    print("="*60)
    print(f"Total train images: {total_train}")
    print(f"Total val images: {total_val}")
    print(f"Total classes: {len(classes)}")
    print(f"Dataset YAML: {yaml_path}")
    
    return yaml_path


if __name__ == "__main__":
    merge_datasets()
