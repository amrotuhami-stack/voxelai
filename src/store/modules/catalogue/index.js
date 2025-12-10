import { CatalogueService } from '@/common/api_services/catalogue'
import { COMMON_MUTATIONS } from '@/store/modules/common/actions'
import { CATALOGUE, CATALOGUE_ACTIONS, CATALOGUE_MUTATIONS } from '@/store/modules/catalogue/actions'
import { ListGroupPlugin } from 'bootstrap-vue'

const state = {
    productList: [],
    allFacetData: {},
    productDetail: {},
    relatedProducts: [],
}

const getters = {
    productList: state => state.productList,
    allFacetData: state => state.allFacetData,
    productDetail: state => state.productDetail,
    relatedProducts: state => state.relatedProducts,
}

const mutations = {
    [CATALOGUE_MUTATIONS.SET_PRODUCTS]: (state, data) => {
        state.productList = data;
    },
    [CATALOGUE_MUTATIONS.SET_FACET_DATA]: (state, data) => {
        state.allFacetData = data;
    },
    [CATALOGUE_MUTATIONS.SET_PRODUCT_DETAILS]: (state, data) => {
        state.productDetail = data
    },
    [CATALOGUE_MUTATIONS.SET_RELATED_PRODUCTS]: (state, data) => {
        state.relatedProducts = data
    },
}

const actions = {
    [CATALOGUE_ACTIONS.GET_PRODUCTS]: ({ commit }, payload) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...");
        return CatalogueService.query(payload)
            .then(resp => {
                commit(CATALOGUE_MUTATIONS.SET_PRODUCTS, resp.data.results)
                commit(CATALOGUE_MUTATIONS.SET_FACET_DATA, resp.data.facet_data)
                commit(COMMON_MUTATIONS.SET_SUCCESS, {'type': 'products', 'value': resp.data.count})
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Get Products")
            })
    },
    [CATALOGUE_ACTIONS.GET_PRODUCT_DETAILS]: ({ commit, dispatch, state }, payload) => {
        return CatalogueService.get(payload.id)
            .then(resp => {
                commit(CATALOGUE_MUTATIONS.SET_PRODUCT_DETAILS, resp.data)
                commit(COMMON_MUTATIONS.SET_SUCCESS)
                if(resp.data.recommended_products.length > 0) {
                    dispatch(CATALOGUE_ACTIONS.GET_RELATED_PRODUCTS, resp.data.recommended_products)
                }
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Get Catalogue Detail")
            })
    },
    [CATALOGUE_ACTIONS.APPLY_FILTER]: ({ commit }, url) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...");
        return CatalogueService.queryByURL(url)
            .then(resp => {
                commit(CATALOGUE_MUTATIONS.SET_PRODUCTS, resp.data.results)
                commit(COMMON_MUTATIONS.SET_SUCCESS)
            })
            .catch((err) => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Apply Products Filter")
            })
    },
    [CATALOGUE_ACTIONS.GET_RELATED_PRODUCTS]: ({ commit, dispatch, state }, payload) => {
        return CatalogueService.queryAllByURL(payload)
            .then(resp => {
                commit(CATALOGUE_MUTATIONS.SET_RELATED_PRODUCTS, resp)
                commit(COMMON_MUTATIONS.SET_SUCCESS)
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Get Related Products")
            })
    },
}

export default {
    state,
    getters,
    mutations,
    actions,
}