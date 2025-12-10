#!/usr/bin/env python3
"""
Dental AI Dataset Download Scripts
Downloads and organizes datasets for OPG/panoramic AI training:
- DENTEX (Zenodo/Kaggle)
- OdontoAI (GitHub)
- Pediatric Caries (Nature/Kaggle)
- Mendeley Panoramic (Mendeley Data)
"""

import os
import sys
import subprocess
import zipfile
import tarfile
import shutil
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
DATASETS_DIR = BASE_DIR / "datasets"


def ensure_dir(path: Path) -> Path:
    """Create directory if it doesn't exist"""
    path.mkdir(parents=True, exist_ok=True)
    return path


def run_cmd(cmd: list, cwd: Path = None) -> bool:
    """Run a command and return success status"""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False


def download_dentex():
    """
    Download DENTEX dataset from Kaggle
    Requires: kaggle CLI configured with API key
    
    Dataset structure:
    - training_data/quadrant/
    - training_data/quadrant_enumeration/
    - training_data/quadrant_enumeration_disease/
    - unlabeled/
    """
    print("\n" + "="*60)
    print("Downloading DENTEX Dataset")
    print("="*60)
    
    output_dir = ensure_dir(DATASETS_DIR / "dentex")
    
    # Check if kaggle is installed
    try:
        subprocess.run(["kaggle", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: Kaggle CLI not found.")
        print("Install with: pip install kaggle")
        print("Then configure: https://www.kaggle.com/docs/api")
        return False
    
    # Download from Kaggle
    cmd = [
        "kaggle", "datasets", "download", "-d",
        "truthisneverlinear/dentex-challenge-2023",
        "-p", str(output_dir),
        "--unzip"
    ]
    
    if run_cmd(cmd, cwd=output_dir):
        print(f"✅ DENTEX downloaded to {output_dir}")
        return True
    else:
        print("❌ DENTEX download failed")
        print("\nAlternative: Download manually from:")
        print("  https://zenodo.org/records/7812323")
        print("  https://www.kaggle.com/datasets/truthisneverlinear/dentex-challenge-2023")
        return False


def download_odontoai():
    """
    Download OdontoAI Open Panoramic Radiographs from GitHub
    
    Dataset: 4000 panoramic images (2000 labeled)
    Annotations: JSON with bounding boxes for 52 tooth types
    """
    print("\n" + "="*60)
    print("Downloading OdontoAI Open Panoramic Radiographs")
    print("="*60)
    
    output_dir = ensure_dir(DATASETS_DIR / "odontoai")
    repo_url = "https://github.com/IvisionLab/OdontoAI-Open-Panoramic-Radiographs.git"
    
    # Clone the repository
    if (output_dir / "README.md").exists():
        print("OdontoAI already downloaded, skipping...")
        return True
    
    cmd = ["git", "clone", "--depth", "1", repo_url, str(output_dir)]
    
    if run_cmd(cmd):
        print(f"✅ OdontoAI downloaded to {output_dir}")
        print("\nNote: Follow instructions in README.md to download actual images")
        print("Images may require registration on the OdontoAI platform")
        return True
    else:
        print("❌ OdontoAI download failed")
        return False


def download_pediatric_caries():
    """
    Download Children's Dental Panoramic Radiographs Dataset
    
    Source: Nature Scientific Data / Kaggle
    Contains: 106 pediatric patients with caries segmentation masks
    """
    print("\n" + "="*60)
    print("Downloading Pediatric Caries Dataset")
    print("="*60)
    
    output_dir = ensure_dir(DATASETS_DIR / "pediatric-caries")
    
    # Try Kaggle first
    try:
        subprocess.run(["kaggle", "--version"], check=True, capture_output=True)
        
        # The dataset is hosted on Kaggle by luanhui
        cmd = [
            "kaggle", "datasets", "download", "-d",
            "luanhui/childrens-dental-panoramic-radiographs-dataset",
            "-p", str(output_dir),
            "--unzip"
        ]
        
        if run_cmd(cmd, cwd=output_dir):
            print(f"✅ Pediatric Caries downloaded to {output_dir}")
            return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    print("❌ Pediatric Caries download failed")
    print("\nManual download options:")
    print("  1. Kaggle: https://www.kaggle.com/datasets/luanhui/childrens-dental-panoramic-radiographs-dataset")
    print("  2. Figshare: https://figshare.com (search 'Children dental panoramic')")
    print("  3. Nature: https://www.nature.com/articles/s41597-023-02237-5")
    return False


def download_mendeley():
    """
    Download Panoramic Dental X-ray Dataset from Mendeley Data
    
    Contains:
    - 107 images with tooth instance segmentation
    - 60 images with tooth class annotations (8 classes)
    - 54 high-resolution radiographs
    """
    print("\n" + "="*60)
    print("Downloading Mendeley Panoramic Dataset")
    print("="*60)
    
    output_dir = ensure_dir(DATASETS_DIR / "mendeley")
    
    print("Mendeley Data requires manual download with registration.")
    print("\nDownload from:")
    print("  https://data.mendeley.com/datasets/73n3kz2k4k")
    print(f"\nExtract to: {output_dir}")
    
    return False


def download_kaggle_caries():
    """
    Download Panoramic Dental Dataset (Caries Segmentation)
    """
    print("\n" + "="*60)
    print("Downloading Kaggle Caries Segmentation Dataset")
    print("="*60)
    
    output_dir = ensure_dir(DATASETS_DIR / "kaggle-caries")
    
    try:
        subprocess.run(["kaggle", "--version"], check=True, capture_output=True)
        
        cmd = [
            "kaggle", "datasets", "download", "-d",
            "thunderpede/panoramic-dental-dataset",
            "-p", str(output_dir),
            "--unzip"
        ]
        
        if run_cmd(cmd, cwd=output_dir):
            print(f"✅ Kaggle Caries downloaded to {output_dir}")
            return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    print("❌ Kaggle Caries download failed")
    print("\nManual download:")
    print("  https://www.kaggle.com/datasets/thunderpede/panoramic-dental-dataset")
    return False


def clone_model_repos():
    """
    Clone model repositories for reference/backbone
    """
    print("\n" + "="*60)
    print("Cloning Model Repositories")
    print("="*60)
    
    models_dir = BASE_DIR / "models"
    
    repos = [
        ("simurgailab", "https://github.com/simurgailab/tooth-detection-and-numbering-in-panoramic-radiographs.git"),
        ("dental-disease-detection", "https://github.com/Loki-Silvres/Dental-Disease-Detection.git"),
        ("detectron2-dental", "https://github.com/arpsn123/Dental-X-RAY-Image-Detection-and-Instance-Segmentation.git"),
        ("unet-teeth", "https://github.com/SerdarHelli/Segmentation-of-Teeth-in-Panoramic-X-ray-Image-Using-U-Net.git"),
    ]
    
    for name, url in repos:
        repo_dir = models_dir / name
        if repo_dir.exists():
            print(f"  {name} already exists, skipping...")
            continue
        
        ensure_dir(repo_dir)
        cmd = ["git", "clone", "--depth", "1", url, str(repo_dir)]
        
        if run_cmd(cmd):
            print(f"  ✅ {name} cloned")
        else:
            print(f"  ❌ {name} failed")


def main():
    """Main entry point"""
    print("="*60)
    print("Dental AI Dataset Downloader")
    print("="*60)
    print(f"Base directory: {BASE_DIR}")
    print(f"Datasets directory: {DATASETS_DIR}")
    
    # Ensure base directories exist
    ensure_dir(DATASETS_DIR)
    ensure_dir(BASE_DIR / "models")
    
    # Parse arguments
    if len(sys.argv) > 1:
        dataset = sys.argv[1].lower()
        if dataset == "dentex":
            download_dentex()
        elif dataset == "odontoai":
            download_odontoai()
        elif dataset == "pediatric":
            download_pediatric_caries()
        elif dataset == "mendeley":
            download_mendeley()
        elif dataset == "caries":
            download_kaggle_caries()
        elif dataset == "models":
            clone_model_repos()
        elif dataset == "all":
            download_dentex()
            download_odontoai()
            download_pediatric_caries()
            download_kaggle_caries()
            clone_model_repos()
        else:
            print(f"Unknown dataset: {dataset}")
            print("Options: dentex, odontoai, pediatric, mendeley, caries, models, all")
    else:
        print("\nUsage: python download_datasets.py <dataset>")
        print("\nAvailable datasets:")
        print("  dentex     - DENTEX Challenge 2023 (Kaggle)")
        print("  odontoai   - OdontoAI Open Panoramic Radiographs (GitHub)")
        print("  pediatric  - Children's Dental Caries (Kaggle)")
        print("  mendeley   - Mendeley Panoramic Dataset (requires manual)")
        print("  caries     - Kaggle Caries Segmentation")
        print("  models     - Clone model repositories")
        print("  all        - Download all available datasets")
        print("\nExample: python download_datasets.py dentex")


if __name__ == "__main__":
    main()
