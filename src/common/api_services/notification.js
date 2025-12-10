import { ApiService } from '@/common/api_services'

export const NotificationService = {
    getNotification(params) {
        return ApiService.query('notification/notifications/', { params })
    },
    getNotificationCount(params) {
        return ApiService.query('notification/new-notifications/', { params })
    },
    seenNotification() {
        return ApiService.post('notification/seen/')
    },
}
