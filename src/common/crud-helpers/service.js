import { ApiServiceHelper } from '.'
import { SERVICE_ACTIONS } from '@/store/modules/service/actions'

export const ServiceHelper = {
    getPatients(params) {
        return ApiServiceHelper.execAction(SERVICE_ACTIONS.GET_PATIENTS, params)
    },
    addPatients(params){
        return ApiServiceHelper.execAction(SERVICE_ACTIONS.ADD_PATIENTS, params)
    },
    searchPatient(params) {
        return ApiServiceHelper.execAction(SERVICE_ACTIONS.SEARCH_PATIENTS, params)
    },
    addService(params){
        return ApiServiceHelper.execAction(SERVICE_ACTIONS.ADD_SERVICE, params)
    },
    getServices(params){
        return ApiServiceHelper.execAction(SERVICE_ACTIONS.GET_SERVICES, params)
    },
    filterServices(params){
        return ApiServiceHelper.execAction(SERVICE_ACTIONS.FILTER_SERVICES, params)
    },
    getServiceDetail(pk){
        return ApiServiceHelper.execAction(SERVICE_ACTIONS.GET_SERVICE_DETAIL, pk)
    },
    closeService(params){
        return ApiServiceHelper.execAction(SERVICE_ACTIONS.CLOSE_SERVICE, params)
    },
    getActiveOrderLines(params){
        return ApiServiceHelper.execAction(SERVICE_ACTIONS.GET_ACTIVE_ORDER_LINES, params)
    },
    getActiveOrderLine(pk){
        return ApiServiceHelper.execAction(SERVICE_ACTIONS.GET_ACTIVE_ORDER_LINE, pk)
    },
    getPatientAiServices(params){
        return ApiServiceHelper.execAction(SERVICE_ACTIONS.GET_PATIENT_AI_SERVICES, params)
    },
    updateServiceData(params) {
        return ApiServiceHelper.execAction(SERVICE_ACTIONS.UPDATE_SERVICE, params)
    },
    pushTempFile(params) {
        return ApiServiceHelper.execAction(SERVICE_ACTIONS.PUSH_TEMP_FILE, params)
    },
    pushServiceFile(params) {
        return ApiServiceHelper.execAction(SERVICE_ACTIONS.ADD_SERVICE_FILE, params)
    },
    getFileSignture(params) {
        return ApiServiceHelper.execAction(SERVICE_ACTIONS.GET_FILE_SIGNTURE, params)
    },
    submitPhaseFields(params) {
        return ApiServiceHelper.execAction(SERVICE_ACTIONS.SUBMIT_PHASE_FIELDS, params)
    },
    updatePhaseStatus(params) {
        return ApiServiceHelper.execAction(SERVICE_ACTIONS.UPDATE_PHASE_STATUS, params)
    },
    getDoctors(params) {
        return ApiServiceHelper.execAction(SERVICE_ACTIONS.GET_DOCTORS, params)
    },
}
