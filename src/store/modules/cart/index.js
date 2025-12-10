import { BasketService } from '@/common/api_services/basket'
import { COMMON_MUTATIONS } from '@/store/modules/common/actions'
import { CART_ACTIONS, CART_MUTATIONS } from '@/store/modules/cart/actions'
import { USER_ACTIONS } from '@/store/modules/user/actions'


const state = {
    cart: {},
    cartLines: [],
    coupon: {},
}

const getters = {
    cart: state => state.cart,
    cartLines: state => state.cartLines,
    coupon: state => state.coupon,
}

const mutations = {
    [CART_MUTATIONS.SET_CART]: (state, data) => {
        state.cart = data
    },
    [CART_MUTATIONS.SET_CART_LINES]: (state, data) => {
        state.cartLines = data
    },
    [CART_MUTATIONS.SET_COUPON]: (state, data) => {
        state.coupon = data
    },
}

const actions = {
    [CART_ACTIONS.GET_CART]: ({ commit }, payload) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...")
        return BasketService.query(payload)
            .then(resp => {
                commit(CART_MUTATIONS.SET_CART, resp.data)
                return BasketService.lines(resp.data.lines, {})
            })
            .then(resp => {
                commit(COMMON_MUTATIONS.SET_SUCCESS)
                commit(CART_MUTATIONS.SET_CART_LINES, resp.data.results)
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Get Cart")
            })
    },
    [CART_ACTIONS.ADD_TO_CART]: ({ commit, dispatch, state }, payload) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...")
        console.log('ADD_TO_CART action called with payload:', payload)
        return BasketService.add(payload).then(resp => {
            console.log('ADD_TO_CART success response:', resp)
            commit(COMMON_MUTATIONS.SET_SUCCESS)
            dispatch(CART_ACTIONS.GET_CART, {})
            dispatch(USER_ACTIONS.GET_USER, {})
            return resp
        })
        .catch((err) => {
            console.error('ADD_TO_CART error:', err)
            if (err.response) {
                console.error('Error response data:', err.response.data)
                console.error('Error response status:', err.response.status)
            }
            commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Add To Cart")
            throw err
        })
    },
    [CART_ACTIONS.REMOVE_FROM_CART]: ({ commit, dispatch, state }, params) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...")
        return BasketService.remove(params)
            .then(resp => {
                commit(COMMON_MUTATIONS.SET_SUCCESS)
                dispatch(CART_ACTIONS.GET_CART, {})
                dispatch(USER_ACTIONS.GET_USER, {})
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Remove Basket Service")
            })
    },
    [CART_ACTIONS.REPLACE_CART_ITEM]: ({ commit, dispatch, state }, params) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...")
        return BasketService.remove(params)
            .then(resp => {
                commit(COMMON_MUTATIONS.SET_SUCCESS)
                dispatch(CART_ACTIONS.ADD_TO_CART, {"quantity": 1,"url": params.newProductUrl})
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Replace Cart Item")
            })
    },
    [CART_ACTIONS.UPDTAE_CART_LINE_ATTRIBUTE]: ({ commit, dispatch, state }, params) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...")
        return BasketService.updateCartLineAttr(params)
            .then(resp => {
                commit(COMMON_MUTATIONS.SET_SUCCESS)
                dispatch(CART_ACTIONS.GET_CART, {})
                dispatch(USER_ACTIONS.GET_USER, {})
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Update Cart Line Attribute")
            })
    },
    [CART_ACTIONS.ADD_LINE_ATTRIBUTE]: ({ commit, dispatch, state }, params) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...")
        return BasketService.addLineAttribute(params)
            .then(resp => {
                commit(COMMON_MUTATIONS.SET_SUCCESS)
                return resp
            })
            .catch((err) => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Add Line Attribute")
                throw err
            })
    },
    [CART_ACTIONS.UPDTAE_CART_LINE_QUANTITY]: ({ commit, dispatch, state }, params) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...")
        return BasketService.updateLineQty(params)
            .then(resp => {
                commit(COMMON_MUTATIONS.SET_SUCCESS)
                dispatch(CART_ACTIONS.GET_CART, {})
                dispatch(USER_ACTIONS.GET_USER, {})
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Update Cart Qty")
            })
    },
    [CART_ACTIONS.ADD_COUPON_TO_CART]: ({ commit, dispatch, state }, payload) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...")
        commit(CART_MUTATIONS.SET_COUPON, {})
        return BasketService.addVoucher(payload).then(resp => {
            commit(COMMON_MUTATIONS.SET_SUCCESS)
            commit(CART_MUTATIONS.SET_COUPON, resp.data)
            dispatch(CART_ACTIONS.GET_CART, {})
            dispatch(USER_ACTIONS.GET_USER, {})
        })
        .catch((err) => {
            commit(CART_MUTATIONS.SET_COUPON, false)
            commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Add Cart Coupon")
        })
    },
    [CART_ACTIONS.CLEAR_COUPON_DATA]: ({ commit, dispatch, state }, payload) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...")
        commit(CART_MUTATIONS.SET_COUPON, {})
        
    },
}

export default {
    state,
    getters,
    mutations,
    actions,
}

/*
*/


/*
/*
[CATALOGUE.ADD_CART]: (state, payload) => {
        if ( payload.productListIndex ){
            state.productList.results[payload.productListIndex]["cartadded"] = true;
        };
    },
    [CATALOGUE.REMOVE_CART]: (state, payload) => {
       
    },
    [CATALOGUE.GET_CART]: (state, resp) => {
        state.cart = resp.data
    },
    [CATALOGUE.CART_LINES]: (state, resp) => {
        state.cartLines = resp.data;
    },
    [CATALOGUE.REPLACE_CART_ITEM]: (state, resp) => {
        
    },
    [CATALOGUE.UPDATE_CART_QTY]: (state, resp) => {
        // state.loadingCart = false;
    },
    [CATALOGUE.UPDATE_CART_LINE_ATTR]: (state, resp) => {
        
    },*/
    /*

    
    
    [CATALOGUE.GET_CART]: ({ commit }, payload) => {
        return BasketService.query(payload)
            .then(resp => {
                commit(CATALOGUE.GET_CART, resp)
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Get Cart")
            })
    },
    [CATALOGUE.CART_LINES]: ({ commit }, payload) => {
        return BasketService.lines(store.getters.userProfile.basket.lines, {})
            .then(resp => {
                commit(CATALOGUE.CART_LINES, resp)
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Cart Lines")
            })
    },
    [CATALOGUE.UPDATE_CART_QTY]: ({ commit }, params) => {
        state.loadingCart = true;
        return BasketService.updateLineQty(params)
            .then(resp => {
                store.dispatch(USER_ACTIONS.GET_USER, {});
                store.dispatch(CATALOGUE.CART_LINES);
                commit(CATALOGUE.UPDATE_CART_QTY, resp);
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Update Cart Qty")
            })
    },
    [CATALOGUE.UPDATE_CART_LINE_ATTR]: ({ commit }, params) => {
        state.loadingCart = true;
        return BasketService.updateCartLineAttr(params)
            .then(resp => {
                store.dispatch(USER_ACTIONS.GET_USER, {})
                commit(CATALOGUE.UPDATE_CART_LINE_ATTR, resp);
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Update Cart Line ATTR")
            })
    },
    */