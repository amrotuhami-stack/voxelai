import { Loading } from 'notiflix'

import { COMMON_MUTATIONS, COMMON_ACTIONS } from '@/store/modules/common/actions'

var loader_svg = require('@/assets/images/LogoV.png');
//var loader_svg_2 = require('@/assets/images/svg/loader.svg')

Loading.init({
    customSvgUrl: loader_svg,
    svgSize: '135px',
    backgroundColor: '#ffffff',
    messageFontSize: '0px',
})

const state = {
    loading: {
        value: false,
        messege: "",
    },
    uploadProgress: {
        target: "",
        value: 0,
    },
    error: {
        value: false,
        messege: "",
    },
    overlay: false,
    activeOrderCount: 0,
    serviceCount: 0,
    myOrdersCount: 0,
    myPatientCount: 0,
    productsCount: 0,
}

const getters = {
    loading: state => state.loading,
    error: state => state.error,
    overlay: state => state.overlay,
    activeOrderCount: state => state.activeOrderCount,
    serviceCount: state => state.serviceCount,
    myOrdersCount: state => state.myOrdersCount,
    myPatientCount: state => state.myPatientCount,
    productsCount: state => state.productsCount,
    uploadProgress: state => state.uploadProgress,
}

const mutations = {
    [COMMON_MUTATIONS.SET_LOADING]: (state, data) => {
        state.loading = {value: true, messege: data}
    },
    [COMMON_MUTATIONS.SET_UPLOAD_PROGRESS]: (state, data) => {
        state.uploadProgress = data
    },
    [COMMON_MUTATIONS.SET_OVERLAY]: (state) => {
        state.overlay = true
    },
    [COMMON_MUTATIONS.CLOSE_OVERLAY]: (state) => {
        state.overlay = false
    },
    [COMMON_MUTATIONS.SET_SUCCESS]: (state, count) => {
        state.loading = {value: false, messege: ""}
        state.error =   {value: false, messege: ""}
        //state.overlay = false
        if(count != undefined){
            if(count.type == 'active-orders')
                state.activeOrderCount = count.value
            else if  (count.type == 'services')
                state.serviceCount = count.value
            else if  (count.type == 'patients')
                state.myPatientCount = count.value
            else if  (count.type == 'products')
                state.productsCount = count.value
            else
                state.myOrdersCount = count.value
        }
    },
    [COMMON_MUTATIONS.SET_ERROR]: (state, messege) => {
        state.loading = {value: false, messege: "", overlay: false}
        state.error = {value: true, messege: messege}
        
    },
    [COMMON_MUTATIONS.SPLASH_SCREEN_START]: () => {
        Loading.custom('Loading...', { customSvgUrl: loader_svg })
    },
    [COMMON_MUTATIONS.SPLASH_SCREEN_END]: () => {
        Loading.remove()
    },
}

const actions = {
    [COMMON_ACTIONS.SHOW_SPLASH_SCREEN]: ({commit}) => {
        commit(COMMON_MUTATIONS.SPLASH_SCREEN_START)
    },
    [COMMON_ACTIONS.HIDE_SPLASH_SCREEN]: ({commit}) => {
        commit(COMMON_MUTATIONS.SPLASH_SCREEN_END)
    },
    [COMMON_ACTIONS.CLOSE_OVERLAY]: ({commit}) => {
        commit(COMMON_MUTATIONS.CLOSE_OVERLAY)
    },
}

export default {
    state,
    getters,
    mutations,
    actions,
}
