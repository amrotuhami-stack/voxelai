import { ApiService } from '@/common/api_services'
export const SettingService = {
    getNavMenu(params) {
        return ApiService.query('settings/nav-menu/', { params })
    },
    getFooterSettings(params) {
        return ApiService.query('settings/footer-setting/', { params })
    },
    getSocialSettings(params) {
        return ApiService.query('settings/social-setting/', { params })
    },
    getCountry(params) {
        return ApiService.query('settings/country/', { params })
    },
}
