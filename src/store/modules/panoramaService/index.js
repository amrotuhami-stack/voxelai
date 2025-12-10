import { PanoramaService } from "@/common/api_services/panoramaService";
import {
  UPDATE_PANORAMA_SERVICE,
  ADD_PANORAMA_SERVICE_FILE,
  UPDATE_PANORAMA_SERVICE_FILE,
  DELETE_PANORAMA_SERVICE_FILE,
  START_PANORAMA_ANALYSIS,
  START_LOCAL_AI_ANALYSIS,
} from "@/store/modules/panoramaService/actions";

import {
  SET_IMAGE_UPLOADED_PERCENTAGE,
  SET_IMAGE_ANALYZING_PERCENTAGE,
} from "@/store/modules/panoramaService/mutations";
import { SERVICE_STATUS } from "@/utils/constants";
import { SERVICE_MUTATIONS } from "@/store/modules/service/actions";
import { DentalAIService } from "@/services/dentalAIService";

const updateUploadFilePercentage = (store, progressEvent) => {
  const uploadedPercentage = Math.round(
    (progressEvent.loaded / progressEvent.total) * 100
  );
  if (uploadedPercentage < 100) {
    store.commit(SET_IMAGE_UPLOADED_PERCENTAGE, uploadedPercentage);
  }
};

const state = {
  fileUploadedPercentage: 0,
  isUploading: false,
  fileAnalyzedPercentage: 0,
  isAnalyzing: false,
  aiServiceStatus: null,
};

const getters = {};

const mutations = {
  [SET_IMAGE_UPLOADED_PERCENTAGE]: (state, percentage) => {
    state.fileUploadedPercentage = percentage;
    if (percentage == 100) {
      state.isUploading = false;
    } else {
      state.isUploading = true;
    }
  },
  [SET_IMAGE_ANALYZING_PERCENTAGE]: (state, percentage) => {
    state.fileAnalyzedPercentage = percentage;
    if (percentage == 100) {
      state.isAnalyzing = false;
    } else {
      state.isAnalyzing = true;
    }
  },
  SET_AI_SERVICE_STATUS: (state, status) => {
    state.aiServiceStatus = status;
  },
};
const actions = {
  [UPDATE_PANORAMA_SERVICE]: ({ commit }, payload) => {
    return new Promise((resolve, reject) => {
      PanoramaService.updateService(payload)
        .then((resp) => {
          commit(SERVICE_MUTATIONS.SET_SERVICE_DETAIL, resp.data);
          resolve(resp);
        })
        .catch((error) => {
          console.error(error);
          reject(error);
        });
    });
  },
  [ADD_PANORAMA_SERVICE_FILE]: ({ commit, dispatch }, payload) => {
    const { width, height, ...restData } = payload;

    return new Promise((resolve, reject) => {
      PanoramaService.addServiceFile(restData, updateUploadFilePercentage)
        .then((resp) => {
          const updatedServiceData = {
            service_data: {
              imageDimensions: {
                width: width,
                height: height,
              },
            },
            serviceId: payload.serviceId,
          };
          dispatch(UPDATE_PANORAMA_SERVICE, updatedServiceData).then(() => {
            commit(SET_IMAGE_UPLOADED_PERCENTAGE, 100);
            resolve(resp);
          });
        })
        .catch((error) => {
          console.error(error);
          reject(error);
        });
    });
  },
  [UPDATE_PANORAMA_SERVICE_FILE]: ({ commit }, payload) => {
    return new Promise((resolve, reject) => {
      PanoramaService.updateServiceFile(payload, updateUploadFilePercentage)
        .then((resp) => {
          const updatedServiceData = {
            service_data: {
              imageDimensions: {
                width: width,
                height: height,
              },
            },
            serviceId: payload.serviceId,
          };
          dispatch(UPDATE_PANORAMA_SERVICE, updatedServiceData);
          resolve(resp);
        })
        .catch((error) => {
          console.error(error);
          reject(error);
        });
    });
  },
  [DELETE_PANORAMA_SERVICE_FILE]: ({ commit }, payload) => {
    return new Promise((resolve, reject) => {
      PanoramaService.deleteServiceFile(payload)
        .then((resp) => {
          resolve(resp);
        })
        .catch((error) => {
          console.error(error);
          reject(error);
        });
    });
  },
  [START_PANORAMA_ANALYSIS]: ({ commit, dispatch, state }, payload) => {
    const { ...restData } = payload;

    return new Promise((resolve, reject) => {
      const form = {
        request_data: {
          scan_image: payload.imageUrl,
        },
        response_data: {},
        service: payload.serviceId,
      };

      commit(SET_IMAGE_ANALYZING_PERCENTAGE, 50);

      PanoramaService.startAnalysis(form)
        .then((resp) => {
          commit(SET_IMAGE_ANALYZING_PERCENTAGE, 90);
          const updatedServiceData = {
            service_data: {
              ...payload.service.service_data,
              points: resp.data.response_data.data,
              original_points: resp.data.response_data.data,
            },
            status: SERVICE_STATUS.TEETH_NUMBERING_VALIDATION.title,
            serviceId: payload.serviceId,
          };

          dispatch(UPDATE_PANORAMA_SERVICE, updatedServiceData).then(() => {
            commit(SET_IMAGE_ANALYZING_PERCENTAGE, 100);
            resolve(resp);
          });
        })
        .catch((error) => {
          console.error(error);
          reject(error);
        });
    });
  },
  /**
   * Start analysis using local AI backend (trained YOLOv8 model)
   * This uses our dental-ai service running on localhost:8000
   */
  [START_LOCAL_AI_ANALYSIS]: async ({ commit, dispatch }, payload) => {
    const { imageFile, service, serviceId } = payload;

    commit(SET_IMAGE_ANALYZING_PERCENTAGE, 10);

    try {
      // Call local AI API
      const aiResults = await DentalAIService.analyzeOPG(imageFile, {
        includeOverlay: true,
        includeMasks: false,
        confidenceThreshold: 0.5,
        onUploadProgress: (progressEvent) => {
          const progress = Math.round(
            (progressEvent.loaded / progressEvent.total) * 30
          );
          commit(SET_IMAGE_ANALYZING_PERCENTAGE, 10 + progress);
        },
      });

      commit(SET_IMAGE_ANALYZING_PERCENTAGE, 70);

      // Format results for the teeth numbering modal
      const formattedData = DentalAIService.formatForTeethNumbering(aiResults);

      commit(SET_IMAGE_ANALYZING_PERCENTAGE, 90);

      // Update service with AI results
      const updatedServiceData = {
        service_data: {
          ...service.service_data,
          points: formattedData.points,
          original_points: formattedData.points,
          imageDimensions: formattedData.imageDimensions,
          aiSummary: formattedData.summary,
          aiImageId: aiResults.image_id,
        },
        status: SERVICE_STATUS.TEETH_NUMBERING_VALIDATION.title,
        serviceId: serviceId,
      };

      await dispatch(UPDATE_PANORAMA_SERVICE, updatedServiceData);
      commit(SET_IMAGE_ANALYZING_PERCENTAGE, 100);

      return aiResults;
    } catch (error) {
      console.error("Local AI analysis failed:", error);
      commit(SET_IMAGE_ANALYZING_PERCENTAGE, 0);
      throw error;
    }
  },
};

export default {
  state,
  getters,
  mutations,
  actions,
};

