import { ApiService } from '@/common/api_services'
export const UsersService = {
    getUserProfile() {
        return ApiService.query('users/profile/')
    },
    query(params) {
        return ApiService.query('users/users/', { params })
    },
    get(username) {
        return ApiService.get('users/users', username)
    },
    updateUserProfile(params) {
        let id = params.basket.owner.split('/')[8];
        return ApiService.put(`users/profile/${id}/`, params)
    },
    getMyOrders(params) {
        let page = 'page' in params ? params.page : '1'
        let pageSize = 'page' in params ? '10' : '1000'
        return ApiService.query(`shop/orders/?page=${page}&page_size=${pageSize}`)
    },
    getOrderLines(url) {
        return ApiService.queryByURL(url + '?page=1&page_size=1000')
    },
    getInternalDoctorDashboardCounter() {
        return ApiService.query('customer/service-counter/')
    },
}
