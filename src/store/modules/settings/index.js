import { SettingService } from '@/common/api_services/settings'
import { SETTINGS } from '@/store/modules/settings/actions'

import { COMMON_MUTATIONS } from '@/store/modules/common/actions'

const state = {
    navMenu: {},
    footerSettings: {},
    socialSettings: {},
    country: {},
}

const getters = {
    navMenu: state => state.navMenu,
    footerSettings: state => state.footerSettings,
    socialSettings: state => state.socialSettings,
    country: state => state.country,
}

const mutations = {
    [SETTINGS.SET_NAV_MENU]: (state, resp) => {
        state.navMenu = resp.data
    },
    [SETTINGS.SET_FOOTER]: (state, resp) => {
        state.footerSettings = resp.data
    },
    [SETTINGS.SET_SOCIAL]: (state, resp) => {
        state.socialSettings = resp.data
    },
    [SETTINGS.GET_SOCIAL]: (state, resp) => {
        state.country = resp.data
    },
}

const actions = {
    [SETTINGS.GET_NAV_MENU]: ({ commit }, payload) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...")
        SettingService.getNavMenu(payload)
            .then(resp => {
                commit(SETTINGS.SET_NAV_MENU, resp)
                commit(COMMON_MUTATIONS.SET_SUCCESS)
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] GET NAV MENU")
            })
    },
    [SETTINGS.GET_FOOTER]: ({ commit }, payload) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...")
        SettingService.getFooterSettings(payload)
            .then(resp => {
                commit(SETTINGS.SET_FOOTER, resp)
                commit(COMMON_MUTATIONS.SET_SUCCESS)
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] GET Footer Settings")
            })
    },
    [SETTINGS.GET_SOCIAL]: ({ commit }, payload) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...")
        SettingService.getSocialSettings(payload)
            .then(resp => {
                commit(SETTINGS.SET_SOCIAL, resp)
                commit(COMMON_MUTATIONS.SET_SUCCESS)
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Get Social Settings")
            })
    },
    [SETTINGS.GET_COUNTRY]: ({ commit }, payload) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...")
        SettingService.getCountry(payload)
            .then(resp => {
                commit(SETTINGS.GET_SOCIAL, resp)
                commit(COMMON_MUTATIONS.SET_SUCCESS)
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Get Country")
            })
    },
}
export default {
    state,
    getters,
    mutations,
    actions,
}
