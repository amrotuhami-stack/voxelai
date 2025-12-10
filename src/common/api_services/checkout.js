import { ApiService } from '@/common/api_services'


export const CheckoutService = {
    post(params) {
        return ApiService.post('shop/checkout/', { params })
    },
    post_shipping(params) {
        return ApiService.post('shop/basket/shipping-methods/', params)
    },
    get_countries(params) {
        return ApiService.query('shipping/country/?page=1&page_size=1000', )
    },
    placeOrder(params){
        return ApiService.post('shop/checkout/', params)
    },
    getOrderLines(url){
        return ApiService.queryByURL(url)
    },
    fulfillPaymentIntent(paymentIntentId, params){
        return ApiService.post(`fulfill-payment-intent/${paymentIntentId}/`, params)
    },
    getCountryShippingCost(){
        return ApiService.query('shipping/country-shipping-cost/', )
    },
}
