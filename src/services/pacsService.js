/**
 * PACS Service - DICOMweb API Client
 * 
 * Provides methods to interact with dcm4chee PACS server using DICOMweb standards:
 * - QIDO-RS: Query for studies, series, instances
 * - WADO-RS: Retrieve DICOM objects
 * - STOW-RS: Store DICOM files
 */

import axios from 'axios';

const DEFAULT_PACS_URL = "http://127.0.0.1:8043";
const DEFAULT_DICOM_WEB_ROOT = "http://127.0.0.1:8043/dicom-web";
const DEFAULT_VOXEL3DI_URL = "http://127.0.0.1:8042";

const PACS_URL = process.env.VUE_APP_PACS_URL || DEFAULT_PACS_URL;
const DICOMWEB_ROOT = process.env.VUE_APP_DICOM_WEB_ROOT || DEFAULT_DICOM_WEB_ROOT;

// Create axios instance with default config
const pacsClient = axios.create({
    baseURL: DICOMWEB_ROOT,
    headers: {
        'Accept': 'application/dicom+json',
        'Content-Type': 'application/dicom+json',
        'Authorization': 'Basic ' + btoa('orthanc:orthanc'),
    },
    withCredentials: false
});

// Add request interceptor for authentication if needed
pacsClient.interceptors.request.use(
    (config) => {
        // Add auth token if available
        const token = localStorage.getItem('pacs_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Add response interceptor for error handling
pacsClient.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error('PACS API Error:', error.response?.data || error.message);
        return Promise.reject(error);
    }
);

/**
 * QIDO-RS: Query for Studies
 * @param {Object} params - Query parameters (PatientName, PatientID, StudyDate, etc.)
 * @returns {Promise<Array>} Array of study objects
 */
export async function queryStudies(params = {}) {
    try {
        const queryParams = new URLSearchParams();

        // Add common DICOM query parameters
        if (params.PatientName) queryParams.append('PatientName', params.PatientName);
        if (params.PatientID) queryParams.append('PatientID', params.PatientID);
        if (params.StudyDate) queryParams.append('StudyDate', params.StudyDate);
        if (params.StudyDescription) queryParams.append('StudyDescription', params.StudyDescription);
        if (params.AccessionNumber) queryParams.append('AccessionNumber', params.AccessionNumber);

        // Always include these fields in response
        queryParams.append('includefield', 'all');

        const response = await pacsClient.get(`/studies?${queryParams.toString()}`);
        return response.data;
    } catch (error) {
        console.error('Error querying studies:', error);
        throw error;
    }
}

/**
 * QIDO-RS: Query for Series in a Study
 * @param {string} studyUID - Study Instance UID
 * @returns {Promise<Array>} Array of series objects
 */
export async function querySeries(studyUID) {
    try {
        const response = await pacsClient.get(`/studies/${studyUID}/series?includefield=all`);
        return response.data;
    } catch (error) {
        console.error('Error querying series:', error);
        throw error;
    }
}

/**
 * QIDO-RS: Query for Instances in a Series
 * @param {string} studyUID - Study Instance UID
 * @param {string} seriesUID - Series Instance UID
 * @returns {Promise<Array>} Array of instance objects
 */
export async function queryInstances(studyUID, seriesUID) {
    try {
        const response = await pacsClient.get(
            `/studies/${studyUID}/series/${seriesUID}/instances?includefield=all`
        );
        return response.data;
    } catch (error) {
        console.error('Error querying instances:', error);
        throw error;
    }
}

/**
 * WADO-RS: Retrieve Study Metadata
 * @param {string} studyUID - Study Instance UID
 * @returns {Promise<Object>} Study metadata
 */
export async function getStudyMetadata(studyUID) {
    try {
        const response = await pacsClient.get(`/studies/${studyUID}/metadata`);
        return response.data;
    } catch (error) {
        console.error('Error retrieving study metadata:', error);
        throw error;
    }
}

/**
 * WADO-RS: Retrieve Instance (DICOM file)
 * @param {string} studyUID - Study Instance UID
 * @param {string} seriesUID - Series Instance UID
 * @param {string} instanceUID - SOP Instance UID
 * @returns {Promise<Blob>} DICOM file as blob
 */
export async function getInstance(studyUID, seriesUID, instanceUID) {
    try {
        const response = await pacsClient.get(
            `/studies/${studyUID}/series/${seriesUID}/instances/${instanceUID}`,
            {
                headers: {
                    'Accept': 'application/dicom'
                },
                responseType: 'blob'
            }
        );
        return response.data;
    } catch (error) {
        console.error('Error retrieving instance:', error);
        throw error;
    }
}

/**
 * WADO-RS: Retrieve Rendered Frame (JPEG/PNG)
 * @param {string} studyUID - Study Instance UID
 * @param {string} seriesUID - Series Instance UID
 * @param {string} instanceUID - SOP Instance UID
 * @param {number} frameNumber - Frame number (1-based)
 * @returns {Promise<Blob>} Rendered image as blob
 */
export async function getRenderedFrame(studyUID, seriesUID, instanceUID, frameNumber = 1) {
    try {
        const response = await pacsClient.get(
            `/studies/${studyUID}/series/${seriesUID}/instances/${instanceUID}/frames/${frameNumber}/rendered`,
            {
                headers: {
                    'Accept': 'image/jpeg'
                },
                responseType: 'blob'
            }
        );
        return response.data;
    } catch (error) {
        console.error('Error retrieving rendered frame:', error);
        throw error;
    }
}

/**
 * STOW-RS: Store DICOM File
 * @param {File} file - DICOM file to upload
 * @param {Function} onProgress - Progress callback (optional)
 * @returns {Promise<Object>} Upload response
 */
export async function storeDicomFile(file, onProgress = null) {
    try {
        // Read file as ArrayBuffer
        const arrayBuffer = await file.arrayBuffer();

        // Generate boundary for multipart/related
        const boundary = `----DICOMwebBoundary${Date.now()}`;

        // Create multipart body manually
        const encoder = new TextEncoder();
        const parts = [];

        // Add boundary and headers for DICOM part
        parts.push(encoder.encode(`--${boundary}\r\n`));
        parts.push(encoder.encode(`Content-Type: application/dicom\r\n`));
        parts.push(encoder.encode(`\r\n`));

        // Add DICOM file data
        parts.push(new Uint8Array(arrayBuffer));

        // Add closing boundary
        parts.push(encoder.encode(`\r\n--${boundary}--\r\n`));

        // Combine all parts into single blob
        const blob = new Blob(parts);

        const config = {
            headers: {
                'Content-Type': `multipart/related; type="application/dicom"; boundary=${boundary}`,
                'Accept': 'application/dicom+json'
            }
        };

        if (onProgress) {
            config.onUploadProgress = (progressEvent) => {
                const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                onProgress(percentCompleted);
            };
        }

        const response = await pacsClient.post('/studies', blob, config);
        return response.data;
    } catch (error) {
        console.error('Error storing DICOM file:', error);
        console.error('Error details:', error.response?.data);
        throw error;
    }
}

/**
 * @param {FileList|Array<File>} files - DICOM files to upload
 * @param {Function} onProgress - Progress callback (optional)
 * @returns {Promise<Array>} Array of upload responses
 */
/**
* Store DICOM files to PACS (Orthanc /instances)
* @param {Array<File>} files - Array of DICOM files to upload
* @param {Function} onProgress - Progress callback (percent)
* @returns {Promise<Object>} - Upload result
*/
export async function storeDicomFiles(files, onProgress) {
    try {
        const url = `${PACS_URL}/instances`;
        const results = [];
        let totalSize = 0;
        let uploadedSize = 0;

        files.forEach((file) => {
            totalSize += file.size;
        });

        for (const file of files) {
            try {
                // Read file as ArrayBuffer
                const fileData = await file.arrayBuffer();

                await axios.post(url, fileData, {
                    headers: {
                        "Content-Type": "application/dicom",
                        Authorization: "Basic " + btoa("orthanc:orthanc"),
                    },
                    onUploadProgress: (progressEvent) => {
                        const currentFileProgress = progressEvent.loaded;
                        const totalProgress = Math.round(
                            ((uploadedSize + currentFileProgress) * 100) / totalSize
                        );
                        if (onProgress) onProgress(totalProgress);
                    },
                });
                results.push({
                    name: file.name,
                    success: true,
                });
            } catch (error) {
                console.error(`Error uploading file ${file.name}:`, error);
                results.push({
                    name: file.name,
                    success: false,
                    error: error.message,
                });
            }
            uploadedSize += file.size;
        }

        return results;
    } catch (error) {
        console.error("Error storing DICOM files:", error);
        throw error;
    }
}

/**
 * Delete Study
 * @param {string} studyUID - Study Instance UID
 * @returns {Promise<void>}
 */
export async function deleteStudy(studyUID) {
    try {
        await pacsClient.delete(`/studies/${studyUID}`);
    } catch (error) {
        console.error('Error deleting study:', error);
        throw error;
    }
}

/**
 * Get PACS Server Status
 * @returns {Promise<Object>} Server status
 */
export async function getServerStatus() {
    try {
        const response = await axios.get(`${PACS_URL}/dcm4chee-arc/monitor/status`);
        return response.data;
    } catch (error) {
        console.error('Error getting server status:', error);
        throw error;
    }
}

/**
 * Build Voxel3di Viewer URL for a study
 * @param {string} studyUID - Study Instance UID
 * @returns {string} Voxel3di viewer URL
 */
export function buildVoxel3diViewerUrl(studyUID) {
    const voxel3diUrl = process.env.VUE_APP_VOXEL3DI_URL || 'http://127.0.0.1:3000';
    const viewerPath = process.env.VUE_APP_VOXEL3DI_VIEWER_PATH || '/viewer';

    // Build DICOMweb data source URL
    const dataSourceUrl = encodeURIComponent(DICOMWEB_ROOT);

    return `${voxel3diUrl}${viewerPath}?StudyInstanceUIDs=${studyUID}&url=${dataSourceUrl}`;
}

export default {
    queryStudies,
    querySeries,
    queryInstances,
    getStudyMetadata,
    getInstance,
    getRenderedFrame,
    storeDicomFile,
    storeDicomFiles,
    deleteStudy,
    getServerStatus,
    buildVoxel3diViewerUrl
};
