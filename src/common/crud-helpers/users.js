import { USER_ACTIONS } from '@/store/modules/user/actions'

import { ApiServiceHelper } from '../crud-helpers'
export const UsersHelper = {
    getUserProfile(params) {
        return ApiServiceHelper.execAction(USER_ACTIONS.GET_USER, params)
    },
    updateUserProfile(params) {
        return ApiServiceHelper.execAction(USER_ACTIONS.UPDATE_USER, params)
    },
    updateUserProfileImage(params) {
        return ApiServiceHelper.execAction(USER_ACTIONS.UPDATE_PROFILE_IMAGE, params)
    },
    resetUserProfileImage(params) {
        return ApiServiceHelper.execAction(USER_ACTIONS.RESET_USER_IMAGE, params)
    },
    saveUserProfile() {
        return ApiServiceHelper.execAction(USER_ACTIONS.SAVE_USER_CHANGES)
    },
    cancelUserProfileChange() {
        return this.getUserProfile()
    },
    getMyOrders(params) {
        return ApiServiceHelper.execAction(USER_ACTIONS.GET_MY_ORDERS, params)
    },
    getOrderLines(params) {
        return ApiServiceHelper.execAction(USER_ACTIONS.GET_ORDER_LINES, params)
    },
}
