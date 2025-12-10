import { ApiServiceHelper } from '.'
import { CHECKOUT, CHECKOUT_ACTIONS } from '@/store/modules/checkout/actions'


export const CheckoutHelper = {
    getCountries(params) {
        return ApiServiceHelper.execAction(CHECKOUT_ACTIONS.GET_COUNTRIES, params)
    },
    getShippingMethods(params) {
        return ApiServiceHelper.execAction(CHECKOUT_ACTIONS.GET_SHIPPING_METHODS, params)
    },
    placeOrder(params){
        return ApiServiceHelper.execAction(CHECKOUT_ACTIONS.PLACE_ORDER, params)
    },
    loadDigitalProductData(params) {
        return ApiServiceHelper.execAction(CHECKOUT_ACTIONS.LOAD_DIGITAL_ORDER_DATA, params)
    },
    ////////////////////////////////////////////////////////////////////////////
    postCheckout(params) {
        return ApiServiceHelper.execAction(CHECKOUT.POST_CHECKOUT, params)
    },
    fulfillPaymentIntend(paymentIntentId){
        return ApiServiceHelper.execAction(CHECKOUT.FULFILL_PAYMENT_INTENT, paymentIntentId)
    },
    getCountryShippingCost() {
        return ApiServiceHelper.execAction(CHECKOUT.GET_COUNTRY_SHIPING_COST)
    },
}
