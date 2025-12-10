
import Keycloak from 'keycloak-js'

const options = {
  pkceMethod: process.env.VUE_APP_KEYCLOAK_PKCE_METHOD,
  url: process.env.VUE_APP_KEYCLOAK_URL,
  realm: process.env.VUE_APP_KEYCLOAK_REALM,
  clientId: process.env.VUE_APP_KEYCLOAK_CLIENT_ID,
  //onLoad: process.env.VUE_APP_KEYCLOAK_ON_LOAD
  onLoad: 'check-sso',
  silentCheckSsoRedirectUri: `${process.env.BASE_URL}/silent-check-sso.html`,
}

const _keycloak = Keycloak(options)

const Plugin = {
  install: (Vue, options) => {
    // 1. add global property
    Vue.keycloak = _keycloak

    // 2. add global method ....
    Vue.listenToTokenRefresh = function (ms) {
      setInterval(() => {
        _keycloak.updateToken(70).then(() => {}).catch((e) => {
          console.log('Failed to refresh token: ', e);
        });
      }, ms)
    }

    // 3. add an instance property
    Vue.prototype.$keycloak = _keycloak
  }
}

export default Plugin