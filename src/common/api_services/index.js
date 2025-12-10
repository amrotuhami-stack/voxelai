import { apiBase, fileUploadURL } from "@/conf";
import axios from "axios";
import Vue from "vue";
import VueAxios from "vue-axios";

Vue.use(VueAxios, axios);
Vue.axios.defaults.baseURL = apiBase();

export const ApiService = {
  init() {},

  query(resource, params) {
    return Vue.axios.get(resource, params);
  },

  queryByURL(url) {
    return axios.get(url);
  },

  get(resource, pk = "") {
    return Vue.axios.get(`${resource}/${pk}/`);
  },

  post(resource, params, config = {}) {
    return Vue.axios.post(`${resource}`, params, config);
  },

  file(resource, params) {
    let formData = new FormData();
    formData.append("file", params.file);
    return Vue.axios.post(`${resource}`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  djfile(formData) {
    return Vue.axios.post(`${fileUploadURL()}`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  update(resource, pk, params) {
    return Vue.axios.patch(`${resource}/${pk}/`, params);
  },

  put(resource, params, config = {}) {
    return Vue.axios.put(`${resource}`, params, config);
  },

  delete(resource) {
    return Vue.axios.delete(resource);
  },
};

export default ApiService;
