import { CheckoutService } from '@/common/api_services/checkout';
import { COMMON_MUTATIONS } from '@/store/modules/common/actions'
import { SERVICE_ACTIONS } from '@/store/modules/service/actions';
import { USER_ACTIONS } from '@/store/modules/user/actions';
import { CART_ACTIONS } from '@/store/modules/cart/actions';


import { CHECKOUT, CHECKOUT_ACTIONS, CHECKOUT_MUTATIONS } from '@/store/modules/checkout/actions';

const state = {
    checkout: {},
    shippingMethods: null,
    countries: [],
    billingAddress: null,
    shippingAddress: null,
    orderData: null,
    orderLines: [],
    selectedAiPricePlan: null,
    countryShippingCost: null,
    digitalOrderData: null,
}

const getters = {
    checkout: state => state.checkout,
    shippingMethods: state => state.shippingMethods,
    countries: state => state.countries,
    shippingAddress: state => state.shippingAddress,
    billingAddress: state => state.billingAddress,
    orderData: state => state.orderData,
    orderLines: state => state.orderLines,
    selectedAiPricePlan: state => state.selectedAiPricePlan,
    countryShippingCost: state => state.countryShippingCost,
    digitalOrderData: state => state.digitalOrderData,
}

const mutations = {
    [CHECKOUT_MUTATIONS.SET_COUNTRIES]: (state, data) => {
        state.countries = data;
    },
    [CHECKOUT_MUTATIONS.SET_SHIPPING_METHODS]: (state, data) => {
        state.shippingMethods = data;
    },
    [CHECKOUT_MUTATIONS.SET_SHIPING_ADDRESS]: (state, data) => {
        state.shippingAddress = data;
    },
    [CHECKOUT_MUTATIONS.SET_BILLING_ADDRESS]: (state, data) => {
        state.billingAddress = data;
    },
    [CHECKOUT_MUTATIONS.SET_ORDER_DATA]: (state, data) => {
        state.orderData = data;
    },
    [CHECKOUT_MUTATIONS.SET_ORDER_LINE]: (state, data) => {
        state.orderLines = [...data];
    },
    [CHECKOUT_MUTATIONS.SET_DIGITAL_ORDER_DATA]: (state, data) => {
        state.digitalOrderData = data;
    },
    [CHECKOUT_MUTATIONS.FULFILL_PAYMENT_INTENT]: (state, resp) => {
        state.orderData = resp.data;
    },
}

const actions = {
    [CHECKOUT_ACTIONS.GET_COUNTRIES]: ({ commit }, payload) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...")
        return CheckoutService.get_countries(payload)
            .then(resp => {
                commit(CHECKOUT_MUTATIONS.SET_COUNTRIES, resp.data.results)
                commit(COMMON_MUTATIONS.SET_SUCCESS)
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Get Countries")
            })
    },
    [CHECKOUT_ACTIONS.GET_SHIPPING_METHODS]: ({ commit }, payload) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...")
        return CheckoutService.post_shipping(payload.shipping)
            .then(resp => {
                commit(CHECKOUT_MUTATIONS.SET_SHIPPING_METHODS, resp.data)
                commit(CHECKOUT_MUTATIONS.SET_SHIPING_ADDRESS, payload.shipping)
                commit(CHECKOUT_MUTATIONS.SET_BILLING_ADDRESS, payload.billing)
                commit(COMMON_MUTATIONS.SET_SUCCESS)
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Post Shipping Checkout")
            })
    },
    [CHECKOUT_ACTIONS.PLACE_ORDER]: ({ commit, dispatch, state }, payload) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...");
        return CheckoutService.placeOrder(payload)
            .then(async  resp => {
                payload.paymentMethod == "stripe"
                    ? dispatch(CHECKOUT_ACTIONS.FULFILL_PAYMENT_INTENT, payload)
                    : commit(CHECKOUT_MUTATIONS.SET_ORDER_DATA, resp.data);

                // When start new digital service
                if(state.digitalOrderData) {
                    dispatch(SERVICE_ACTIONS.ADD_SERVICE, {
                        "product": state.digitalOrderData.product.id,
				        "patient": state.digitalOrderData.patient.id,
				        "order_line": resp.data.lines_id[0],
                        "service_data": {
                            ...state.digitalOrderData,
                            'created': Date.now().toString(),
						    'files_status': 'waiting'
                        }
                    })
                }
                return CheckoutService.getOrderLines(resp.data.lines)
            })
            .then((lines) => {
                commit(CHECKOUT_MUTATIONS.SET_ORDER_LINE, [...lines.data.results])
                dispatch(CART_ACTIONS.GET_CART, {})
                dispatch(CART_ACTIONS.CLEAR_COUPON_DATA, {})
                dispatch(USER_ACTIONS.GET_USER, {})
                commit(COMMON_MUTATIONS.SET_SUCCESS)
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Place Order")
            })
    },
    [CHECKOUT_ACTIONS.LOAD_DIGITAL_ORDER_DATA]: ({ commit, dispatch, state }, payload) => {
        commit(COMMON_MUTATIONS.SET_LOADING, "Loading ...");
        commit(CHECKOUT_MUTATIONS.SET_DIGITAL_ORDER_DATA, payload);
        commit(COMMON_MUTATIONS.SET_SUCCESS);
    },
    [CHECKOUT_ACTIONS.FULFILL_PAYMENT_INTENT]: ({ commit }, payload) => {
        return CheckoutService.fulfillPaymentIntent(payload.paymentIntentId, {shippingAddress: payload.shipping_address})
            .then(resp => {
                commit(CHECKOUT.FULFILL_PAYMENT_INTENT, resp);
                commit(CHECKOUT_MUTATIONS.SET_ORDER_DATA, resp.data);
            })
            .catch(() => {
                commit(COMMON_MUTATIONS.SET_ERROR, "[ERROR] Fulfill Payment Intent")
            })
    },
}

export default {
    state,
    getters,
    mutations,
    actions,
}
