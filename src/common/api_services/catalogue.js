import { ApiService } from '@/common/api_services'

export const CatalogueService = {
    query(params) {
        let page = 'page' in params ? params.page : '1'
        let pageSize = 'page' in params ? '100' : '1000'
        return ApiService.query(`shop/products/?page=${page}&page_size=${pageSize}`, { params })
    },
    queryByURL(url) {
        return ApiService.queryByURL(url)
    },
    get(pk) {
        return ApiService.get('shop/products', pk)
    },
    async queryAllByURL(list) {
        let items = []
        try {
            for(var i = 0; i < list.length; i++) {
                let result = await ApiService.queryByURL(list[i])
                items.push(result.data)
            }
            return items
        }
        catch(error) {
            throw error
        }
    },
}
