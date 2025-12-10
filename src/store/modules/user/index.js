import { UsersService } from '@/common/api_services/users'
import { ApiService } from '@/common/api_services/index'
import { COMMON_MUTATIONS } from '@/store/modules/common/actions'

import { USER_ACTIONS, USER_MUTATIONS } from '@/store/modules/user/actions'


import Messenger from '../../../common/firebase/messenger'


const state = {
    userProfile: null,
    userProfileChanged: false,
    invalidPhoneNumber: "",
    myOrders: [],
}

const getters = {
    userProfile: state => state.userProfile,
    userProfileChanged: state => state.userProfileChanged,
    myOrders: state => state.myOrders,
    invalidPhoneNumber: state => state.invalidPhoneNumber,
}

const mutations = {
    [USER_MUTATIONS.SET_USER]: (state, data) => {
        state.invalidPhoneNumber = ""
        state.userProfile = { ...state.userProfile, ...data }
    },
    [USER_MUTATIONS.SET_PROFILE_CHANGED]: (state, flag) => {
        state.userProfileChanged = flag
    },
    [USER_MUTATIONS.INVALID_PHONE_NUMBER]: (state, flag) => {
        state.invalidPhoneNumber = flag
    },
    [USER_MUTATIONS.SET_MY_ORDERS]: (state, data) => {
        state.myOrders = data
    },
}

const actions = {
    // Users entity actions
    [USER_ACTIONS.GET_USER]: ({ commit }, payload) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...")
        return UsersService.getUserProfile(payload)
            .then(async resp => {
                // IF user is internal doctor ...
                let userProfile = {...resp.data}
                if(resp.data.is_internal_doctor) {
                    let counters = await UsersService.getInternalDoctorDashboardCounter()
                    userProfile = {...resp.data, dashboard: {...counters.data}}
                }

                commit(COMMON_MUTATIONS.SET_SUCCESS)
                commit(USER_MUTATIONS.SET_PROFILE_CHANGED, false)

                if(!userProfile.shipping_country || !userProfile.shipping_city || !userProfile.shipping_address)
                    commit(USER_MUTATIONS.SET_USER, {...userProfile, differentShippingAddress: false})
                else
                    commit(USER_MUTATIONS.SET_USER, userProfile)

                
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Get User Profile")
            })
    },

    [USER_ACTIONS.UPDATE_USER]: ({ commit }, payload) => {
        commit(USER_MUTATIONS.SET_PROFILE_CHANGED, true)
        commit(USER_MUTATIONS.SET_USER, payload)
    },

    [USER_ACTIONS.SAVE_USER_CHANGES]: ({ commit }, payload) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...")
        return UsersService.updateUserProfile(state.userProfile)
            .then(resp => {
                commit(COMMON_MUTATIONS.SET_SUCCESS)
                commit(USER_MUTATIONS.SET_PROFILE_CHANGED, false)
                if(!resp.data.shipping_country || !resp.data.shipping_city || !resp.data.shipping_address)
                    commit(USER_MUTATIONS.SET_USER, {...resp.data, differentShippingAddress: false})
                else
                    commit(USER_MUTATIONS.SET_USER, resp.data)
            })
            .catch((error) => {
                if(error.response.data.billing_phone_number) {
                    commit(USER_MUTATIONS.INVALID_PHONE_NUMBER, "billing")
                }
                if(error.response.data.phone_number) {
                    commit(USER_MUTATIONS.INVALID_PHONE_NUMBER, "personal")
                }
                if(error.response.data.shipping_phone_number) {
                    commit(USER_MUTATIONS.INVALID_PHONE_NUMBER, "shipping")
                }
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Update User Profile")
            })
    },
    [USER_ACTIONS.UPDATE_PROFILE_IMAGE]: ({ commit, dispatch, state }, payload) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...")
        let formData = new FormData();
        formData.append("file", payload);
        return ApiService.djfile(formData)
            .then((resp) => {
                return UsersService.updateUserProfile({
                    ...state.userProfile,
                    "photo": {
                        "path": resp.data.path,
                        "filename": resp.data.filename,
                    }
                })
            })
            .then(resp => {
                commit(COMMON_MUTATIONS.SET_SUCCESS)
                commit(USER_MUTATIONS.SET_PROFILE_CHANGED, false)
                dispatch(USER_ACTIONS.GET_USER, {})
            })
            .catch((error) => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Update User Profile Image")
            });
    },
    [USER_ACTIONS.RESET_USER_IMAGE]: ({ commit, dispatch, state }, payload) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...")
        return UsersService.updateUserProfile({...state.userProfile, photo: null})
            .then(resp => {
                commit(COMMON_MUTATIONS.SET_SUCCESS)
                commit(USER_MUTATIONS.SET_PROFILE_CHANGED, false)
                dispatch(USER_ACTIONS.GET_USER, {})
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Update User Profile")
            })
    },
    [USER_ACTIONS.GET_MY_ORDERS]: ({ commit }, payload) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...")
        return UsersService.getMyOrders(payload)
            .then(resp => {
                commit(COMMON_MUTATIONS.SET_SUCCESS, {'type': 'my-orders', 'value': resp.data.count})
                commit(USER_MUTATIONS.SET_MY_ORDERS, resp.data.results)
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Get My ORDERS")
            })
    },
    [USER_ACTIONS.GET_ORDER_LINES]: ({ commit }, payload) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...")
        return UsersService.getOrderLines(payload.url)
            .then(resp => {
                commit(COMMON_MUTATIONS.SET_SUCCESS)
                return resp.data
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Get My ORDERS")
            })
    },
}

export default {
    state,
    getters,
    mutations,
    actions,
}
