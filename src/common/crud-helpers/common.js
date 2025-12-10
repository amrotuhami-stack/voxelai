import { ApiServiceHelper } from '../crud-helpers'
import {COMMON_ACTIONS } from '@/store/modules/common/actions'


export const CommonHelper = {
    showSplashScreen(params) {
        return ApiServiceHelper.execAction(COMMON_ACTIONS.SHOW_SPLASH_SCREEN, params)
    },
    hideSplashScreen(params) {
        return ApiServiceHelper.execAction(COMMON_ACTIONS.HIDE_SPLASH_SCREEN, params)
    },
    closeOverLay(params) {
        return ApiServiceHelper.execAction(COMMON_ACTIONS.CLOSE_OVERLAY, params)
    },
}
