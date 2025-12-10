import { NOTIFICATION } from '@/store/modules/notification/actions'

import { ApiServiceHelper } from '../crud-helpers'

export const NotificationHelper = {
    getNotification(params) {
        return ApiServiceHelper.execAction(NOTIFICATION.LIST, params)
    },
    getNotificationCount(params) {
        return ApiServiceHelper.execAction(NOTIFICATION.LIST_COUNT, params)
    },
    seenNotification() {
        return ApiServiceHelper.execAction(NOTIFICATION.SEEN)
    },
}
