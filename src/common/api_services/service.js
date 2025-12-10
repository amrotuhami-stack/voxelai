import { ApiService } from '@/common/api_services'

export const ServiceService = {
    query(params) {
        let page = 'page' in params ? params.page : '1'
        let pageSize = 'page' in params ? '10' : '1000'
        return ApiService.query(`customer/patient/?page=${page}&page_size=${pageSize}`, params)
    },
    search(params) {
        return ApiService.query(`customer/patient/?name=${params.name}`, params)
    },
    addPatient(params) {
        return ApiService.post('customer/patient/', params)
    },
    addService(params) {
        return ApiService.post('customer/service/', params)
    },
    updateService(params) {
        return ApiService.put(`customer/service/${params.serviceId}/`, params)
    },
    getServices(params) {
        let page = 'page' in params ? params.page : '1'
        let pageSize = 'page' in params ? '10' : '100'
        return ApiService.query(`customer/service/?page=${page}&page_size=${pageSize}`, params)
    },
    filterServices(params) {
        let page = 'page' in params ? params.page : '1'
        let pageSize = 'page' in params ? '10' : '10'

        return ApiService.query(`customer/service/?search=${params.search ?? ''}&fulfillment_status=${params.fulfillment_status ?? ''}&service_date=${params.service_date ?? ''}&patient=${params.patient ?? ''}&owner=${params.owner ?? ''}&page=${page}&page_size=${pageSize}`, {})
    },
    getServiceDetail(pk) {
        return ApiService.query(`customer/service/${pk}/`)
    },
    closeService(params) {
        return ApiService.put(`/customer/service/${params.id}/close-service/`, params)
    },
    getActiveOrderLines(params) {
        let page = 'page' in params ? params.page : '1'
        let pageSize = 'page' in params ? '5' : '1000'
        return ApiService.query(`order/order-lines-active/?page=${page}&page_size=${pageSize}`, params)
    },
    getActiveOrderLine(pk) {
        return ApiService.query(`order/order-lines-active/${pk}/`)
    },
    getPatientAiService(params) {
        return ApiService.query(`customer/service/patient-product-service/?product_id=${params.product_id}&patient_id=${params.patient_id}`)
    },
    pushTempFile(form, config) {
        return ApiService.post('hcfljiqzeb/', form, config)
    },
    addServiceFile(form) {
        return ApiService.post('customer/service-file/', form)
    },
    putServiceFile(form, fileId) {
        return ApiService.put(`customer/service-file/${fileId}/`, form)
    },
    getServiceSigntureFile(params) {
        return ApiService.query(`customer/service-file/${params.fileId}/`, params)
    },
    submitPhaseFields(params) {
        return ApiService.post(`customer/service/${params.serviceId}/post-service-phase/`, params)
    },
    updateServicePhaseStatus(params) {
        return ApiService.post(`customer/service/${params.serviceId}/update-service-phase-status/`, params)
    },
    getAllDoctors(params) {
        let page = 'page' in params ? params.page : '1'
        let pageSize = 'page' in params ? '10' : '100'
        return ApiService.query(`users/doctors/?page=${page}&page_size=${pageSize}`, params)
    },
}



        /* Service Id, "id",
        "owner__first_name",
        "owner__last_name",
        "owner__name",
        "product__upc",
        "product__title",
        "patient__first_name",
        "patient__last_name",
        "order_line__order__number"

        under_processing = "under_processing"
    fulfilled = "fulfilled"
    rejected = "rejected
        */ 