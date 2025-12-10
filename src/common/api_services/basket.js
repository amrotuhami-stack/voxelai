import { ApiService } from '@/common/api_services'

export const BasketService = {
    query(params) {
        return ApiService.query('shop/basket/', { params })
    },
    lines(url, params) {
        return ApiService.query(url, { params })
    },
    updateLineQty(params){
        let payload = {
            "quantity": params.quantity,
          };
        return ApiService.update(`shop/baskets/${params.basket_id}/lines`, params.lineId, payload)
    },
    updateCartLineAttr(params){
        let payload = {
            "value": params.value,
            "option": params.option,
            "quantity": params.quantity || 1
        };
        return ApiService.update(`shop/baskets/${params.basket_id}/lines/${params.lineId}/lineattributes`, params.attrId, payload)
    },
    addLineAttribute(params){
        let payload = {
            "value": params.value,
            "option": params.option
        };
        return ApiService.post(`shop/baskets/${params.basket_id}/lines/${params.lineId}/lineattributes/`, payload)
    },
    add(params){
        return ApiService.post('shop/basket/add-product.json', params )
    },
    remove(params){
        return ApiService.delete(`shop/baskets/${params.basket_id}/lines/${params.id}/` )
    },
    addVoucher(params){
        return ApiService.post('shop/basket/add-voucher/', params )
    },
}
