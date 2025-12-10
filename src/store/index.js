import Vue from "vue";
import Vuex from "vuex";

import settings from "@/store/modules/settings/index";
import catalogue from "@/store/modules/catalogue/index";
import cart from "@/store/modules/cart/index";
import checkout from "@/store/modules/checkout/index";
import users from "@/store/modules/user/index";
import service from "@/store/modules/service/index";
import common from "@/store/modules/common/index";
import panoramaService from "@/store/modules/panoramaService/index";

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== "production";

export default new Vuex.Store({
  modules: {
    settings,
    common,
    // notification,
    catalogue,
    cart,
    checkout,
    users,
    service,
    panoramaService,
  },
  strict: debug,
});
