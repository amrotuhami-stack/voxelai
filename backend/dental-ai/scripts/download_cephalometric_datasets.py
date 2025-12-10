#!/usr/bin/env python3
"""
Download and prepare cephalometric landmark detection datasets

Datasets:
1. ISBI 2015 - 400 images, 19 landmarks (already downloaded by user)
2. Aariz/CEPHA29 - 1000 images, 29 landmarks (Figshare)
3. CL-Detection 2024 - ~700 images, 53 landmarks (Zenodo)

Usage:
    python download_cephalometric_datasets.py --all
    python download_cephalometric_datasets.py --aariz
    python download_cephalometric_datasets.py --cl-detection
"""

import os
import sys
import argparse
import requests
import zipfile
from pathlib import Path
from tqdm import tqdm
import shutil

BASE_DIR = Path(__file__).parent.parent
DATASETS_DIR = BASE_DIR / "datasets" / "cephalometric"

# Dataset URLs and info
DATASETS = {
    "aariz": {
        "name": "Aariz (CEPHA29)",
        "description": "1000 LCRs with 29 landmarks from 7 imaging devices",
        "landmarks": 29,
        "images": 1000,
        # Figshare hosted - need browser download
        "url": "https://figshare.com/articles/dataset/Aariz_A_Benchmark_Dataset_for_Automatic_Cephalometric_Landmark_Detection_and_CVM_Stage_Classification/25171188",
        "manual_download": True,
        "instructions": """
Manual Download Required:
1. Go to: https://figshare.com/articles/dataset/Aariz_A_Benchmark_Dataset_for_Automatic_Cephalometric_Landmark_Detection_and_CVM_Stage_Classification/25171188
2. Click "Download all" button
3. Extract to: datasets/cephalometric/aariz/
"""
    },
    "cl-detection-2024": {
        "name": "CL-Detection 2024",
        "description": "~700 images with 53 landmarks from MICCAI challenge",
        "landmarks": 53,
        "images": 700,
        "url": "https://zenodo.org/records/12609878/files/CL-Detection2024_Training_and_Validation.zip?download=1",
        "manual_download": False,
    },
    "isbi2015": {
        "name": "ISBI 2015",
        "description": "400 images with 19 landmarks (classic benchmark)",
        "landmarks": 19,
        "images": 400,
        "url": "https://figshare.com/s/37ec464af8e81ae6ebbf",
        "manual_download": True,
        "instructions": """
Manual Download Required:
1. Go to: https://figshare.com/s/37ec464af8e81ae6ebbf
2. Download the files
3. Extract to: datasets/isbi2015/
"""
    }
}


def download_file(url: str, dest_path: Path, desc: str = "Downloading"):
    """Download file with progress bar"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(dest_path, 'wb') as f:
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=desc) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
    
    return dest_path


def download_cl_detection_2024():
    """Download CL-Detection 2024 dataset from Zenodo"""
    print("\n📥 Downloading CL-Detection 2024 dataset...")
    
    dest_dir = DATASETS_DIR / "cl-detection-2024"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    zip_path = dest_dir / "cl_detection_2024.zip"
    
    if zip_path.exists():
        print(f"  ⚠️ ZIP already exists: {zip_path}")
    else:
        url = DATASETS["cl-detection-2024"]["url"]
        print(f"  Downloading from Zenodo (~1GB)...")
        download_file(url, zip_path, "CL-Detection 2024")
    
    # Extract
    print("  📦 Extracting...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest_dir)
    
    print(f"  ✅ CL-Detection 2024 downloaded to: {dest_dir}")
    return dest_dir


def check_isbi2015():
    """Check if ISBI 2015 is available"""
    isbi_dir = BASE_DIR / "datasets" / "isbi2015"
    
    if isbi_dir.exists():
        images = list(isbi_dir.glob("**/*.bmp"))
        annotations = list(isbi_dir.glob("**/*.txt"))
        print(f"\n✅ ISBI 2015 found: {len(images)} images, {len(annotations)} annotations")
        return True
    else:
        print(f"\n❌ ISBI 2015 not found at: {isbi_dir}")
        print(DATASETS["isbi2015"]["instructions"])
        return False


def check_aariz():
    """Check if Aariz dataset is available"""
    aariz_dir = DATASETS_DIR / "aariz"
    
    if aariz_dir.exists() and any(aariz_dir.iterdir()):
        images = list(aariz_dir.glob("**/*.jpg")) + list(aariz_dir.glob("**/*.png")) + list(aariz_dir.glob("**/*.bmp"))
        print(f"\n✅ Aariz dataset found: {len(images)} images")
        return True
    else:
        print(f"\n❌ Aariz dataset not found at: {aariz_dir}")
        print(DATASETS["aariz"]["instructions"])
        return False


def list_datasets():
    """List all available datasets"""
    print("\n" + "="*60)
    print("CEPHALOMETRIC LANDMARK DETECTION DATASETS")
    print("="*60)
    
    for key, info in DATASETS.items():
        print(f"\n📁 {info['name']}")
        print(f"   Description: {info['description']}")
        print(f"   Landmarks: {info['landmarks']}")
        print(f"   Images: {info['images']}")
        print(f"   Auto-download: {'No' if info.get('manual_download') else 'Yes'}")
    
    print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(description="Download cephalometric datasets")
    parser.add_argument("--all", action="store_true", help="Download all available datasets")
    parser.add_argument("--aariz", action="store_true", help="Download Aariz dataset")
    parser.add_argument("--cl-detection", action="store_true", help="Download CL-Detection 2024")
    parser.add_argument("--list", action="store_true", help="List all datasets")
    parser.add_argument("--check", action="store_true", help="Check which datasets are available")
    
    args = parser.parse_args()
    
    if args.list:
        list_datasets()
        return
    
    if args.check:
        print("\n🔍 Checking available datasets...")
        check_isbi2015()
        check_aariz()
        
        cl_det_dir = DATASETS_DIR / "cl-detection-2024"
        if cl_det_dir.exists():
            print(f"\n✅ CL-Detection 2024 found at: {cl_det_dir}")
        else:
            print(f"\n❌ CL-Detection 2024 not found")
        return
    
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)
    
    if args.cl_detection or args.all:
        download_cl_detection_2024()
    
    if args.aariz or args.all:
        if not check_aariz():
            print("\n⚠️ Aariz requires manual download from Figshare")
            print(DATASETS["aariz"]["instructions"])
    
    if args.all:
        check_isbi2015()
    
    print("\n✅ Dataset download complete!")
    print("\nNext steps:")
    print("1. Run: python merge_cephalometric_datasets.py")
    print("2. Start training with CEPHMark-Net")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        list_datasets()
        print("\nUsage examples:")
        print("  python download_cephalometric_datasets.py --check")
        print("  python download_cephalometric_datasets.py --cl-detection")
        print("  python download_cephalometric_datasets.py --all")
    else:
        main()
