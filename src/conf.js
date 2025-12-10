const API_BASE = process.env.VUE_APP_VOXEL_API_BASE || 'http://localhost:8003'
const VUE_APP_WS_NOTIFICATIONS = process.env.VUE_APP_WS_NOTIFICATIONS
const VUE_APP_WS_CHAT = process.env.VUE_APP_WS_CHAT
const VUE_APP_WS_SENTRY = process.env.VUE_APP_WS_SENTRY
const VUE_APP_STRIPE_PUBLISHABLE_KEY = process.env.VUE_APP_STRIPE_PUBLISHABLE_KEY || "pk_live_51JwQOTBwDLpn2SCRGfBZJVkTjqR3VCaBxXXhu4ROO1PkDwBAqzC0SxYBCHOxmVgUFTWQSR69TJel3FqlI9rKSzgw00rXMBA2yO";

let apiBase = function() {
    return API_BASE + '/en/api/v1/'
}

let backendBase = function() {
    return API_BASE
}

let fileUploadURL = function() {
    return '/hcfljiqzeb/'
}

let stripeApiKey = function() {
    return VUE_APP_STRIPE_PUBLISHABLE_KEY
}
export {
    apiBase,
    backendBase,
    fileUploadURL,
    API_BASE,
    VUE_APP_WS_NOTIFICATIONS,
    VUE_APP_WS_CHAT,
    VUE_APP_WS_SENTRY,
    VUE_APP_STRIPE_PUBLISHABLE_KEY,
    stripeApiKey
}
