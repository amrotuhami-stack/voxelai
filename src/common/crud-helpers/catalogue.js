import { ApiServiceHelper } from '.'
import { CATALOGUE_ACTIONS } from '@/store/modules/catalogue/actions'


export const CatalogueHelper = {
    getProducts(params) {
        return ApiServiceHelper.execAction(CATALOGUE_ACTIONS.GET_PRODUCTS, params)
    },
    applyFilter(url) {
        return ApiServiceHelper.execAction(CATALOGUE_ACTIONS.APPLY_FILTER, url)
    },
    getProductDetail(params) {
        return ApiServiceHelper.execAction(CATALOGUE_ACTIONS.GET_PRODUCT_DETAILS, params)
    },
    getRelatedProducts(params) {
        return  ApiServiceHelper.execAction(CATALOGUE_ACTIONS.GET_RELATED_PRODUCTS, params)
    }
}
