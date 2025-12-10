/**
 * Dental AI Service
 * Integrates Vue frontend with Python backend AI API for:
 * - Tooth detection with FDI numbering
 * - Pathology detection (caries, periapical, impacted)
 * - HITL corrections
 */

import axios from 'axios';

// Backend API base URL
const API_BASE = process.env.VUE_APP_BACKEND_URL || 'http://localhost:8000';
const DENTAL_AI_API = `${API_BASE}/api/dental-ai`;

/**
 * Dental AI API Service
 */
export const DentalAIService = {
    /**
     * Analyze an OPG/panoramic X-ray image
     * @param {File} imageFile - The image file to analyze
     * @param {Object} options - Analysis options
     * @returns {Promise<Object>} Analysis results with teeth and lesions
     */
    async analyzeOPG(imageFile, options = {}) {
        const formData = new FormData();
        formData.append('file', imageFile);

        const params = new URLSearchParams({
            include_overlay: options.includeOverlay ?? true,
            include_masks: options.includeMasks ?? false,
            confidence_threshold: options.confidenceThreshold ?? 0.5,
        });

        try {
            const response = await axios.post(
                `${DENTAL_AI_API}/analyze?${params.toString()}`,
                formData,
                {
                    headers: { 'Content-Type': 'multipart/form-data' },
                    onUploadProgress: options.onUploadProgress,
                }
            );
            return response.data;
        } catch (error) {
            console.error('Dental AI analysis failed:', error);
            throw error;
        }
    },

    /**
     * Convert AI results to Vue component format
     * @param {Object} aiResults - Raw API response
     * @returns {Object} Formatted data for teethNumberingModal
     */
    formatForTeethNumbering(aiResults) {
        const points = [];

        // Convert tooth detections to component format
        if (aiResults.teeth) {
            aiResults.teeth.forEach((tooth) => {
                points.push({
                    classes: parseInt(tooth.tooth_id),
                    scores: tooth.confidence,
                    pred_boxes: tooth.bbox, // [x1, y1, x2, y2]
                    tooth_type: tooth.tooth_type,
                    lesions: [],
                });
            });
        }

        // Associate lesions with nearest teeth
        if (aiResults.lesions) {
            aiResults.lesions.forEach((lesion) => {
                // Find nearest tooth by bbox center distance
                const lesionCenter = {
                    x: (lesion.bbox[0] + lesion.bbox[2]) / 2,
                    y: (lesion.bbox[1] + lesion.bbox[3]) / 2,
                };

                let nearestTooth = null;
                let minDistance = Infinity;

                points.forEach((point) => {
                    const toothCenter = {
                        x: (point.pred_boxes[0] + point.pred_boxes[2]) / 2,
                        y: (point.pred_boxes[1] + point.pred_boxes[3]) / 2,
                    };
                    const distance = Math.sqrt(
                        Math.pow(lesionCenter.x - toothCenter.x, 2) +
                        Math.pow(lesionCenter.y - toothCenter.y, 2)
                    );
                    if (distance < minDistance) {
                        minDistance = distance;
                        nearestTooth = point;
                    }
                });

                if (nearestTooth) {
                    nearestTooth.lesions.push({
                        type: lesion.lesion_type,
                        confidence: lesion.confidence,
                        severity: lesion.severity,
                    });
                }
            });
        }

        return {
            points,
            imageDimensions: aiResults.imageDimensions || { width: 2943, height: 1435 },
            overlayImage: aiResults.overlay_image,
            summary: aiResults.summary,
        };
    },

    /**
     * Check AI service health
     * @returns {Promise<Object>} Health status
     */
    async checkHealth() {
        try {
            const response = await axios.get(`${DENTAL_AI_API}/health`);
            return response.data;
        } catch (error) {
            return { status: 'offline', error: error.message };
        }
    },

    /**
     * Get available detection classes
     * @returns {Promise<Object>} Class definitions
     */
    async getClasses() {
        try {
            const response = await axios.get(`${DENTAL_AI_API}/classes`);
            return response.data;
        } catch (error) {
            console.error('Failed to get classes:', error);
            throw error;
        }
    },

    /**
     * Get model information
     * @returns {Promise<Object>} Model info
     */
    async getModelInfo() {
        try {
            const response = await axios.get(`${DENTAL_AI_API}/model/info`);
            return response.data;
        } catch (error) {
            return { status: 'unavailable', error: error.message };
        }
    },

    /**
     * Send HITL corrections back to improve model
     * @param {string} imageId - Original image ID
     * @param {Array} corrections - Array of tooth corrections
     * @returns {Promise<Object>} Submission result
     */
    async submitCorrections(imageId, corrections) {
        try {
            const response = await axios.post(`${DENTAL_AI_API}/corrections`, {
                image_id: imageId,
                corrections: corrections.map((c) => ({
                    original_tooth_id: c.originalToothId,
                    corrected_tooth_id: c.correctedToothId,
                    action: c.action, // 'change', 'remove', 'add'
                    bbox: c.bbox,
                })),
            });
            return response.data;
        } catch (error) {
            console.error('Failed to submit corrections:', error);
            // Don't throw - corrections are optional and shouldn't block user
            return { status: 'failed', error: error.message };
        }
    },
};

/**
 * FDI Numbering Constants
 */
export const FDI_TEETH = {
    // Upper Right (Quadrant 1)
    11: 'Upper Right Central Incisor',
    12: 'Upper Right Lateral Incisor',
    13: 'Upper Right Canine',
    14: 'Upper Right First Premolar',
    15: 'Upper Right Second Premolar',
    16: 'Upper Right First Molar',
    17: 'Upper Right Second Molar',
    18: 'Upper Right Third Molar',
    // Upper Left (Quadrant 2)
    21: 'Upper Left Central Incisor',
    22: 'Upper Left Lateral Incisor',
    23: 'Upper Left Canine',
    24: 'Upper Left First Premolar',
    25: 'Upper Left Second Premolar',
    26: 'Upper Left First Molar',
    27: 'Upper Left Second Molar',
    28: 'Upper Left Third Molar',
    // Lower Left (Quadrant 3)
    31: 'Lower Left Central Incisor',
    32: 'Lower Left Lateral Incisor',
    33: 'Lower Left Canine',
    34: 'Lower Left First Premolar',
    35: 'Lower Left Second Premolar',
    36: 'Lower Left First Molar',
    37: 'Lower Left Second Molar',
    38: 'Lower Left Third Molar',
    // Lower Right (Quadrant 4)
    41: 'Lower Right Central Incisor',
    42: 'Lower Right Lateral Incisor',
    43: 'Lower Right Canine',
    44: 'Lower Right First Premolar',
    45: 'Lower Right Second Premolar',
    46: 'Lower Right First Molar',
    47: 'Lower Right Second Molar',
    48: 'Lower Right Third Molar',
};

/**
 * Lesion Types
 */
export const LESION_TYPES = {
    caries: { id: 1, label: 'Caries', color: '#FF0000' },
    deep_caries: { id: 2, label: 'Deep Caries', color: '#CC0000' },
    periapical_lesion: { id: 3, label: 'Periapical Lesion', color: '#FFA500' },
    impacted: { id: 4, label: 'Impacted', color: '#800080' },
};

export default DentalAIService;
