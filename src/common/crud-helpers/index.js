import store from '@/store'
export const ApiServiceHelper = {
    execAction(action, params) {
        return store.dispatch(action, params)
    },
}
export default ApiServiceHelper
