
import { NotificationService } from '@/common/api_services/notification'
import { NOTIFICATION } from '@/store/actions/notification'
import { FETCH_SUCCESS, FETCH_ERROR } from '@/store/common'

// import { NotificationHelper } from '@/common/crud-helpers/notification'
// import notification from '@/store/modules/notification'
// import { SOCKET_MUTATIONS } from '@/store/actions/notification'

const state = {
    notificationList: [],
    notificationCount: 0,
}

const getters = {
    notificationList: state => state.notificationList,
    notificationCount: state => state.notificationCount,
}

const mutations = {
    [NOTIFICATION.SET_LIST]: (state, resp) => {
        state.notificationList = resp.data
    },
    [NOTIFICATION.SET_LIST_COUNT]: (state, resp) => {
        state.notificationCount = resp.data.count
    },
}

const actions = {
    [NOTIFICATION.LIST]: ({ commit }, payload) => {
        return NotificationService.getNotification(payload)
            .then(resp => {
                commit(NOTIFICATION.SET_LIST, resp)
                commit(FETCH_SUCCESS)
            })
            .catch(() => {
                commit(FETCH_ERROR)
            })
    },
    [NOTIFICATION.LIST_COUNT]: ({ commit }, payload) => {
        return NotificationService.getNotificationCount(payload)
            .then(resp => {
                commit(NOTIFICATION.SET_LIST_COUNT, resp)
                commit(FETCH_SUCCESS)
            })
            .catch(() => {
                commit(FETCH_ERROR)
            })
    },
    [NOTIFICATION.SEEN]: ({ commit }, payload) => {
        return NotificationService.seenNotification(payload)
            .then(() => {
                commit(FETCH_SUCCESS)
            })
            .catch(() => {
                commit(FETCH_ERROR)
            })
    },
}

export default {
    state,
    getters,
    mutations,
    actions,
}
