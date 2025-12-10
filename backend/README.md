# Voxel3Di Backend API

FastAPI backend for orchestrating 3D Slicer processing jobs.

## Features

- **Job Orchestration**: Manages communication between Voxel3di and 3D Slicer
- **REST API**: Clean endpoints for segmentation, model generation, and panoramic reconstruction
- **CORS Support**: Configured for VoxelApp and Voxel3di frontends
- **Health Checks**: Monitor backend and Slicer server status

## Endpoints

### Main Endpoints
- `GET /` - API information
- `GET /health` - Backend health check
- `GET /docs` - Interactive API documentation (Swagger UI)

### Slicer Processing
- `POST /process/slicer/segment` - Trigger CBCT segmentation
- `POST /process/slicer/model` - Generate 3D model (STL/GLB)
- `POST /process/slicer/panoramic` - Generate panoramic reconstruction
- `GET /process/slicer/health` - Check Slicer server status

## Usage

### Build and Run

```bash
cd backend
docker compose up -d
```

### Test API

```bash
# Health check
curl http://localhost:8001/health

# Trigger segmentation
curl -X POST http://localhost:8001/process/slicer/segment \
  -H "Content-Type: application/json" \
  -d '{
    "studyInstanceUID": "1.2.3.4.5",
    "seriesInstanceUID": "1.2.3.4.5.6"
  }'
```

### API Documentation

Visit http://localhost:8001/docs for interactive API documentation.

## Development

### Local Development (without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload --port 8001
```

### Environment Variables

- `SLICER_HOST` - Slicer server hostname (default: `slicer`)
- `SLICER_PORT` - Slicer server port (default: `5005`)
- `ORTHANC_URL` - Orthanc PACS URL (default: `http://orthanc:8042`)

## Integration

The backend integrates with:
- **3D Slicer Server** (port 5005) - Processing engine
- **Orthanc PACS** (port 8042) - DICOM storage
- **Voxel3di Viewer** (port 3000) - Frontend client
- **VoxelApp** (port 8082) - Main application

## Architecture

```
Voxel3di → Backend API → 3D Slicer → Orthanc
             (8001)        (5005)      (8042)
```

## Next Steps

1. Start Slicer server first
2. Start backend
3. Configure Voxel3di extension to call backend endpoints
4. Test end-to-end workflow
