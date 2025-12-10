import { ApiService } from "@/common/api_services";

import store from "@/store";

export const PanoramaService = {
  updateService(payload) {
    const { serviceId, ...data } = payload;
    return ApiService.put(`customer/service/${serviceId}/`, data);
  },
  addServiceFile(payload, onUploadProgress) {
    const form = new FormData();
    form.append("file", payload.file);
    form.append("name", payload.fileName);
    form.append("service", payload.serviceId);

    return ApiService.post(`customer/service-file/`, form, {
      onUploadProgress: function (progressEvent) {
        onUploadProgress(store, progressEvent);
      },
    });
  },
  updateServiceFile(payload, onUploadProgress) {
    const form = new FormData();
    form.append("file", payload.file);
    form.append("name", payload.fileName);
    form.append("service", payload.serviceId);

    return ApiService.put(`customer/service-file/${payload.fileId}/`, form, {
      onUploadProgress: function (progressEvent) {
        onUploadProgress(store, progressEvent);
      },
    });
  },
  deleteServiceFile(payload) {
    return ApiService.delete(`customer/service-file/${payload.fileId}/`);
  },
  startAnalysis(payload) {
    return ApiService.post(`customer/panorama-ai/`, payload);
  },
};
