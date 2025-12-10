import { ServiceService } from "@/common/api_services/service";
import { COMMON_MUTATIONS } from "@/store/modules/common/actions";

import {
  SERVICE_MUTATIONS,
  SERVICE_ACTIONS,
} from "@/store/modules/service/actions";

const state = {
  activeOrderLine: [],
  orderLine: {},
  patients: [],
  patientAiServices: [],
  serviceList: [],
  serviceDetail: null,
  doctors: [],
  filter: {},
};

const getters = {
  activeOrderLine: (state) => state.activeOrderLine,
  orderLine: (state) => state.orderLine,
  patients: (state) => state.patients,
  patientAiServices: (state) => state.patientAiServices,
  serviceList: (state) => state.serviceList,
  serviceDetail: (state) => state.serviceDetail,
  doctors: (state) => state.doctors,
  filter: (state) => state.filter,
};

const mutations = {
  [SERVICE_MUTATIONS.SET_ACTIVE_ORDER_LINES]: (state, data) => {
    state.activeOrderLine = data;
  },
  [SERVICE_MUTATIONS.SET_ACTIVE_ORDER_LINE]: (state, data) => {
    state.orderLine = data;
  },
  [SERVICE_MUTATIONS.SET_PATIENTS]: (state, data) => {
    state.patients = data;
  },
  [SERVICE_MUTATIONS.SET_PATIENT_AI_SERVICES]: (state, data) => {
    state.patientAiServices = data;
  },
  [SERVICE_MUTATIONS.SET_SERVICES]: (state, data) => {
    state.serviceList = data;
  },
  [SERVICE_MUTATIONS.SET_SERVICE_DETAIL]: (state, data) => {
    state.serviceDetail = data;
  },
  [SERVICE_MUTATIONS.SET_DOCTORS]: (state, data) => {
    state.doctors = data;
  },
  [SERVICE_MUTATIONS.SET_FILTER]: (state, data) => {
    state.filter = data;
  },
};

const actions = {
  [SERVICE_ACTIONS.GET_ACTIVE_ORDER_LINES]: ({ commit }, payload) => {
    commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...");
    return ServiceService.getActiveOrderLines(payload)
      .then((resp) => {
        commit(SERVICE_MUTATIONS.SET_ACTIVE_ORDER_LINES, resp.data.results);
        commit(COMMON_MUTATIONS.SET_SUCCESS, {
          type: "active-orders",
          value: resp.data.count,
        });
      })
      .catch(() => {
        commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Get Active Order Line");
      });
  },
  [SERVICE_ACTIONS.GET_ACTIVE_ORDER_LINE]: ({ commit }, pk) => {
    commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...");
    return ServiceService.getActiveOrderLine(pk)
      .then((resp) => {
        commit(SERVICE_MUTATIONS.SET_ACTIVE_ORDER_LINE, resp.data);
        commit(COMMON_MUTATIONS.SET_SUCCESS);
      })
      .catch(() => {
        commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Get Active Order Line");
      });
  },
  [SERVICE_ACTIONS.GET_PATIENTS]: ({ commit }, payload) => {
    commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...");
    return ServiceService.query(payload)
      .then((resp) => {
        commit(SERVICE_MUTATIONS.SET_PATIENTS, resp.data.results);
        commit(COMMON_MUTATIONS.SET_SUCCESS, {
          type: "patients",
          value: resp.data.count,
        });
      })
      .catch(() => {
        commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Query Patients");
      });
  },
  [SERVICE_ACTIONS.SEARCH_PATIENTS]: ({ commit }, payload) => {
    commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...");
    return ServiceService.search(payload)
      .then((resp) => {
        return resp.data.results
      })
      .catch(() => {
        commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Search Patients");
      });
  },
  [SERVICE_ACTIONS.ADD_PATIENTS]: ({ commit, dispatch, state }, payload) => {
    commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...");
    return ServiceService.addPatient(payload)
      .then(async (resp) => {
        commit(COMMON_MUTATIONS.SET_SUCCESS);
        // This line should be removed after review
        await dispatch(SERVICE_ACTIONS.GET_PATIENTS, {});
        return resp.data;
      })
      .catch(() => {
        commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Add Patient");
      });
  },
  [SERVICE_ACTIONS.GET_PATIENT_AI_SERVICES]: ({ commit }, payload) => {
    commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...");
    return ServiceService.getPatientAiService(payload)
      .then((resp) => {
        commit(SERVICE_MUTATIONS.SET_PATIENT_AI_SERVICES, resp.data);
        commit(COMMON_MUTATIONS.SET_SUCCESS);
        return resp.data;
      })
      .catch(() => {
        commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Get Patient AI Service");
      });
  },
  [SERVICE_ACTIONS.GET_SERVICES]: ({ commit, dispatch, state }, payload) => {
    commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...");

    if(state.filter != {}) {
      return dispatch(SERVICE_ACTIONS.FILTER_SERVICES, {...payload, ...state.filter})
    }
    return ServiceService.getServices(payload)
      .then((resp) => {
        commit(SERVICE_MUTATIONS.SET_SERVICES, resp.data.results);
        commit(COMMON_MUTATIONS.SET_SUCCESS, {
          type: "services",
          value: resp.data.count,
        });
      })
      .catch(() => {
        commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Get Service");
      });
  },
  [SERVICE_ACTIONS.FILTER_SERVICES]: ({ commit }, payload) => {
    commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...");
    commit(SERVICE_MUTATIONS.SET_FILTER, payload);
    return ServiceService.filterServices(payload)
      .then((resp) => {
        commit(SERVICE_MUTATIONS.SET_SERVICES, resp.data.results);
        commit(COMMON_MUTATIONS.SET_SUCCESS, {
          type: "services",
          value: resp.data.count,
        });
      })
      .catch(() => {
        commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Get Service");
      });
  },
  [SERVICE_ACTIONS.ADD_SERVICE]: ({ commit, dispatch, state }, payload) => {
    commit(COMMON_MUTATIONS.SET_LOADING, "add-service");

    return ServiceService.addService(payload).then(async resp => {

      if(payload.service_data && payload.service_data.files.length) {
        commit(COMMON_MUTATIONS.SET_OVERLAY);
        await payload.service_data.files.forEach(async (file, index) => {
          let data = await dispatch(SERVICE_ACTIONS.ADD_SERVICE_FILE, {
            ...file,
            'service': resp.data.id,
            'files': [],
          })
          payload.service_data.files[index] = {...file, ...data, value: data.file}
          let updated = await dispatch(SERVICE_ACTIONS.UPDATE_SERVICE, {
            serviceId: resp.data.id,
            service_data: {
              ...payload.service_data,
              'modified': Date.now().toString(),
              'files_status': 'waiting'
            },
          })
          if(updated &&  index == payload.service_data.files.length - 1) 
            commit(COMMON_MUTATIONS.CLOSE_OVERLAY);
        })
      }

      commit(SERVICE_MUTATIONS.SET_SERVICE_DETAIL, resp.data)
      commit(COMMON_MUTATIONS.SET_SUCCESS)
      return resp.data.id
    })
    .catch(() => {
        commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Add Service")
    })
  },
    [SERVICE_ACTIONS.UPDATE_SERVICE]: ({ commit, dispatch, state }, payload) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...");
        return ServiceService.updateService(payload)
            .then(resp => {
                commit(COMMON_MUTATIONS.SET_SUCCESS)
                dispatch(SERVICE_ACTIONS.GET_SERVICES, {})
                commit(SERVICE_MUTATIONS.SET_SERVICE_DETAIL, resp.data)
                return true
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Add Service")
            })
    },
    [SERVICE_ACTIONS.GET_SERVICE_DETAIL]: ({ commit }, pk) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...");
        return ServiceService.getServiceDetail(pk)
            .then(resp => {
                commit(SERVICE_MUTATIONS.SET_SERVICE_DETAIL, resp.data)
                commit(COMMON_MUTATIONS.SET_SUCCESS)
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Get Service Detail")
            })
    },
    [SERVICE_ACTIONS.CLOSE_SERVICE]: ({ commit, dispatch, state }, payload) => {
      commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...");
      return ServiceService.closeService(payload)
          .then(resp => {
              commit(COMMON_MUTATIONS.SET_SUCCESS)
              dispatch(SERVICE_ACTIONS.GET_SERVICES, {})
              return true
          })
          .catch(() => {
              commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Close Service")
          })
  },
    [SERVICE_ACTIONS.PUSH_TEMP_FILE]: ({ commit, dispatch, state }, payload) => {
      commit(COMMON_MUTATIONS.SET_LOADING, "Loading" + payload.name);

      const form = new FormData();
      form.append("file", payload.value);

      return ServiceService.pushTempFile(form, {
        onUploadProgress: (progressEvent) => {
          commit(COMMON_MUTATIONS.SET_UPLOAD_PROGRESS, {
            target: payload.name,
            value: progressEvent.loaded
          });
        }
      })
      .then((resp) => {
        commit(COMMON_MUTATIONS.SET_SUCCESS);
        return resp.data;
      })
      .catch(() => {
        commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Push Temp File");
      });
    },
    [SERVICE_ACTIONS.ADD_SERVICE_FILE]: ({ commit, dispatch, state }, payload) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading" + payload.name);

        const form = new FormData();
        form.append("file_obj", payload.temp_file_id);
        form.append("name", payload.name);
        form.append("service", payload.service);

        let fileExist = payload.files.findIndex(
          (file) => file.name == payload.name
        );
        if (fileExist != -1) {
          return ServiceService.putServiceFile(form, payload.files[fileExist].id)
            .then((resp) => {
              commit(COMMON_MUTATIONS.SET_SUCCESS);
              return resp.data;
            })
            .catch(() => {
              commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Update Service File");
            });
        } else {
          return ServiceService.addServiceFile(form)
            .then((resp) => {
              commit(COMMON_MUTATIONS.SET_SUCCESS);
              return resp.data;
            })
            .catch(() => {
              commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Add Service File");
            });
        }
  },
  [SERVICE_ACTIONS.GET_FILE_SIGNTURE]: ({ commit }, payload) => {
    commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...");
    return ServiceService.getServiceSigntureFile(payload)
      .then((resp) => {
        commit(COMMON_MUTATIONS.SET_SUCCESS);
        return resp.data;
      })
      .catch(() => {
        commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Get Service");
      });
  },
  [SERVICE_ACTIONS.SUBMIT_PHASE_FIELDS]: ({ commit, dispatch, state }, payload) => {
    commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...");
    return ServiceService.submitPhaseFields(payload)
      .then((resp) => {
        commit(COMMON_MUTATIONS.SET_SUCCESS);
        dispatch(SERVICE_ACTIONS.GET_SERVICE_DETAIL, payload.serviceId);
      })
      .catch(() => {
        commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Add Service");
      });
  },
  [SERVICE_ACTIONS.UPDATE_PHASE_STATUS]: ({ commit, dispatch, state },payload) => {
    commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...");
    return ServiceService.updateServicePhaseStatus(payload)
      .then((resp) => {
        commit(COMMON_MUTATIONS.SET_SUCCESS);
        dispatch(SERVICE_ACTIONS.GET_SERVICE_DETAIL, resp.data.service);
      })
      .catch(() => {
        commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Update Service Phase Status");
      });
  },
};

export default {
  state,
  getters,
  mutations,
  actions,
};
