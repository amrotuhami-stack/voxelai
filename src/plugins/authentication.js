import Vue from 'vue';
import axios from "axios";
let instance;

const BASE = `${process.env.VUE_APP_VOXEL_API_BASE}/en/o/`;



function generateRandomBytes(length) {
  const randomArray = new Uint8Array(length);
  window.crypto.getRandomValues(randomArray);
  return randomArray;
}

// Function to encode bytes to base64url
function base64urlEncode(buffer) {
  return btoa(String.fromCharCode.apply(null, buffer))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
}

function setCookie(cname, cvalue, expire) {
  const d = new Date();
  d.setTime(d.getTime() + expire);
  let expires = "expires=" + d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
function getCookie(cname) {
  let decodedCookie = decodeURIComponent(document.cookie);
  let cArray = decodedCookie.split(';');
  for(let item of cArray) {
    if(item.split('=')[0].trim() == cname) {
      return item.split('=')[1];
    }
  }
  return false;
}
function eraseCookie(name) {
  document.cookie = name + "=" + null + ";" + "expires=" + null + ";path=/";
}

export const useAuth = (configs) => {
  instance = new Vue({
    data() {
      return {
        isAuthenticated: false,
        error: null,
        code: null,
        code_challenge: null,
      };
    },
    created() {
      window.onload = function () {
        if (window.location.search.includes('code=')) {
          instance.code = window.location.search.split('code=')[1];
          instance.obtainAccessToken()
        }
      };
    },
    methods: {
      isUserAuth: (callback) => {
        let token = getCookie('token_obj');
        if(!token) callback(false)
        callback(JSON.parse(token));
      },
      logUserOut: () => {
        eraseCookie('token_obj');
        window.location.replace(`${process.env.VUE_APP_VOXEL_API_BASE}/en/accounts/logout/?next=/`);
      },
      tryToLogin:(options) => {
        // Save Target Route
        //setCookie('target_route', JSON.stringify({to: window.location.href}), (1 * 24 * 60 * 60 * 1000));
        localStorage.setItem('target_route', window.location.href)

        // Generate 32 random bytes
        const randomBytes = generateRandomBytes(32);

        // Convert random bytes to base64url encoding
        let codeVerifier = base64urlEncode(randomBytes);

        // Remove trailing '=' characters
        codeVerifier = codeVerifier.replace(/=+$/, '');

        // Hash the code verifier using SHA-256
        const hashBuffer = crypto.subtle.digest('SHA-256', new TextEncoder().encode(codeVerifier));
        hashBuffer.then(hashArray => {
          const codeVerifierHash = new Uint8Array(hashArray);
          // Convert hashed code verifier to base64url encoding
          const codeChallenge = base64urlEncode(codeVerifierHash);
          instance.code_challenge = codeChallenge;

          setCookie('verifier_code', codeVerifier, (7 * 24 * 60 * 60 * 1000));

          if (window.location.search.includes('code=')) return;
          const uri = `${BASE}authorize/?client_id=${configs.client_id}&redirect_uri=${window.location.origin}/&response_type=code&code_challenge=${instance.code_challenge}&code_challenge_method=S256`;
          window.location.replace(uri);
        });
      },
      obtainAccessToken: () => {
        let verifier_code = getCookie('verifier_code')
        let target_route = localStorage.getItem('target_route')
        const params = new URLSearchParams();
        params.append('grant_type', configs.grant_type);
        params.append('code', instance.code);
        params.append('redirect_uri', `${window.location.origin}/`);
        params.append('client_id', configs.client_id);
        params.append('code_verifier', verifier_code);
        axios.post(`${BASE}token/`, params, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            "Accept": "/"
          }
        })
        .then(function (response) {
          setCookie('token_obj', JSON.stringify(response.data), response.data.expires_in * 1000)
          eraseCookie(verifier_code);
          localStorage.removeItem('target_route');

          if(target_route == `${window.location.origin}/`) {
            return window.location.replace(`${window.location.origin}/dashboard/page=1`);
          }
          window.location.replace(target_route);
        })
        .catch(function (error) {
          console.log(error);
          eraseCookie(verifier_code)
        });
      },
    }
  });
  return instance
};

let configs = {
  client_id: process.env.VUE_APP_AUTH_CLIENT_ID,
  grant_type: process.env.VUE_APP_AUTH_GRANT_TYPE,
}

const AuthService = useAuth(configs);

const AuthenticationPlugin = {
  install(Vue, options) {
    // Add global property
    Vue.auth = AuthService
    // Add an instance property
    Vue.prototype.$auth = AuthService
  },
};

export default AuthenticationPlugin