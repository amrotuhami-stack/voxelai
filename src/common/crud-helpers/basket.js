import { ApiServiceHelper } from '.'
import { CART_ACTIONS } from '@/store/modules/cart/actions'


export const BasketHelper = {
    getCart(params) {
        return ApiServiceHelper.execAction(CART_ACTIONS.GET_CART, params)
    },
    addCart(params) {
        return ApiServiceHelper.execAction(CART_ACTIONS.ADD_TO_CART, params)
    },
    removeCart(params) {
        return ApiServiceHelper.execAction(CART_ACTIONS.REMOVE_FROM_CART, params)
    },
    replaceCartItem(params) {
        return ApiServiceHelper.execAction(CART_ACTIONS.REPLACE_CART_ITEM, params)
    },
    updateCartQty(params){
        return ApiServiceHelper.execAction(CART_ACTIONS.UPDTAE_CART_LINE_QUANTITY, params)
    },
    updateCartLineAttr(params){
        return ApiServiceHelper.execAction(CART_ACTIONS.UPDTAE_CART_LINE_ATTRIBUTE, params)
    },
    addCartCoupon(params){
        return ApiServiceHelper.execAction(CART_ACTIONS.ADD_COUPON_TO_CART, params)
    },
    clearCartCoupon(params){
        return ApiServiceHelper.execAction(CART_ACTIONS.CLEAR_COUPON_DATA, params)
    }
}
