# Dental AI Module

AI-powered dental image analysis for OPG/Panoramic X-rays.

## Features

- **Tooth Detection**: Detect all teeth in panoramic X-rays
- **FDI Numbering**: Automatic tooth numbering using Fédération Dentaire Internationale system
- **Pathology Detection**: Detect caries, periapical lesions, and impacted teeth
- **Instance Segmentation**: Pixel-level tooth segmentation masks

## Directory Structure

```
dental-ai/
├── datasets/
│   ├── dentex/         # DENTEX Challenge dataset (10GB)
│   ├── odontoai/       # OdontoAI Open Panoramic dataset
│   ├── pediatric-caries/
│   └── unified/        # Combined dataset in COCO format
├── models/
│   ├── dentex-repo/    # Official DENTEX code
│   ├── simurgailab/    # Tooth numbering reference
│   ├── yolov8/         # Trained YOLOv8 models
│   └── combined/       # Multi-task models
└── scripts/
    ├── download_datasets.py  # Dataset download utilities
    ├── label_schema.py       # Unified FDI + lesion schema
    └── train_yolov8.py       # YOLOv8 training pipeline
```

## Quick Start

### 1. Setup Kaggle (for downloading datasets)

```bash
pip install kaggle
# Configure API: https://www.kaggle.com/docs/api
```

### 2. Download Datasets

```bash
# Download DENTEX from Zenodo (automatic)
cd backend/dental-ai
curl -L -o datasets/dentex/dentex_dataset.zip "https://zenodo.org/records/7812323/files/training_data.zip?download=1"
unzip datasets/dentex/dentex_dataset.zip -d datasets/dentex/

# Or use the download script (requires Kaggle API)
python scripts/download_datasets.py dentex
```

### 3. Prepare Dataset for Training

```bash
python scripts/train_yolov8.py prepare
```

### 4. Train Model

```bash
python scripts/train_yolov8.py train
```

### 5. Start API

```bash
cd backend
uvicorn main:app --reload --port 8000
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/dental-ai/analyze` | POST | Analyze single OPG image |
| `/api/dental-ai/health` | GET | Service health check |
| `/api/dental-ai/classes` | GET | List detection classes |
| `/api/dental-ai/model/info` | GET | Get model information |

## Training Data

### DENTEX (Primary)
- 705 annotated panoramic X-rays
- Annotations: quadrant, tooth enumeration (FDI), diagnosis
- Pathologies: caries, deep caries, periapical lesion, impacted

### OdontoAI (Supplementary)
- 4,000 panoramic X-rays (2,000 labeled)
- 52 tooth categories + restorations

## Model Architecture

- **Backbone**: YOLOv8m-seg (medium variant with segmentation)
- **Input Size**: 1024x1024
- **Classes**: 32 tooth classes + 4 pathology classes = 36 total
- **Output**: Bounding boxes + instance masks + class labels

## FDI Tooth Numbering

```
        Upper Right (1)    Upper Left (2)
           18-11              21-28
        ─────────────────────────────
        Lower Right (4)    Lower Left (3)  
           48-41              31-38
```

## Integration with Voxel Vue App

The API integrates with the Vue frontend through:
1. Upload OPG via `/api/dental-ai/analyze`
2. Receive JSON with teeth + lesions + overlay image
3. Display interactive tooth chart with findings
4. Generate PDF reports

## License

Research use only. Datasets have their own licenses:
- DENTEX: CC-BY-NC-SA
- OdontoAI: Academic use
