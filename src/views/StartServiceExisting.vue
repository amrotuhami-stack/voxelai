<template>
  <div class="service">
    <!-- <base-offer-notifications /> -->
    <base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
    <h1 class="main-title">Start Service</h1>
    <p>
      <span>Choose</span> a service form Shop or <span>Continue</span> with your
      recent purchased services.
    </p>
    <div class="container">
      <router-link
        class="linkBox viewMore"
        :to="{ name: 'Shop', params: { lang: $i18n.locale } }"
      >
        <p>Choose a service from Shop</p>
        <font-awesome-icon :icon="['fa', 'angle-right']" />
      </router-link>
      <h2>Or start with one of your purchased Services</h2>
      <div class="contentBox" v-if="!activeOrderLines">
        <div class="serviceRow" v-for="(_, index) in 5" :key="index">
          <b-skeleton
            animation="wave"
            width="100%"
            height="100px"
            class="skelton"
          ></b-skeleton>
        </div>
      </div>
      <div class="contentBox" v-else>
        <div
          class="serviceRow"
          v-for="(item, index) in activeOrderLines"
          :key="index"
        >
          <div
            class="serviceRow__image"
            v-if="item.product_obj.product_class == 'online-ai-service'"
          >
            <img
              v-if="
                item &&
                item.product_obj.parent_id &&
                item.product_obj.parent_obj.images &&
                item.product_obj.parent_obj.images.length > 0
              "
              :src="item.product_obj.parent_obj.images[0].original"
              alt=""
              class="img-fluid"
            />
          </div>
          <div
            class="serviceRow__image"
            v-if="item.product_obj.product_class != 'online-ai-service'"
          >
            <img
              v-if="
                item &&
                item.product_obj.images &&
                item.product_obj.images.length > 0
              "
              :src="item.product_obj.images[0].original"
              alt=""
              class="img-fluid"
            />
          </div>
          <div class="serviceRow__title">
            <span
              v-if="
                item.product_obj.product_class == 'online-ai-service' &&
                item.product_obj &&
                item.product_obj.parent_obj
              "
            >
              {{ item.product_obj.parent_obj.title }} -
              {{ item.product_obj.title }}
            </span>
            <span v-if="item.product_obj.product_class != 'online-ai-service'">
              {{ item.product_obj.title }}
            </span>
            <div
              class="serviceRow__cases"
              v-if="item.product_obj.product_class == 'online-ai-service'"
            >
              <div class="serviceRow__cases--progress">
                <b-progress
                  :value="item.used_cases"
                  :max="item.product_obj.subscription_size"
                ></b-progress>
              </div>
              <div class="d-flex justify-content-between align-items-center">
                <div class="serviceRow__cases--remaining">
                  <span
                    v-html="
                      item.product_obj.subscription_size - item.used_cases < 0
                        ? 0
                        : item.product_obj.subscription_size - item.used_cases
                    "
                  ></span>
                  cases remaining
                  <svg-icon
                    v-b-tooltip.hover
                    title="cases remaining"
                    icon-id="info-circle"
                    icon-viewbox="0 0 24 24"
                  ></svg-icon>
                </div>
                <div class="serviceRow__cases--duration">
                  {{ item.date_placed | formatDate }}
                </div>
              </div>
            </div>
            <div
              class="serviceRow__details"
              v-if="item.product_obj.product_class != 'online-ai-service'"
            >
              <router-link
                class="viewMore"
                :to="{
                  name: 'My Order',
                  params: { lang: $i18n.locale, page: '1' },
                }"
              >
                See Order Details
                <font-awesome-icon :icon="['fa', 'angle-right']" />
              </router-link>
              <div class="row">
                <div class="col-lg-3">
                  <div class="item">
                    <p>{{ formatId(item.id) }}</p>
                    <span>Order ID</span>
                  </div>
                </div>
                <div class="col-lg-5">
                  <div class="item">
                    <p>{{ item.date_placed | formatDate }}</p>
                    <span>Placed Date</span>
                  </div>
                </div>
                <div class="col-lg-4">
                  <div class="item">
                    <p>{{ item.price_excl_tax }}</p>
                    <span>Price</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div
            class="serviceRow__link"
            v-if="
              item.product_obj.product_class == 'online-ai-service' &&
              item.product_obj.parent_obj.title == 'AI Cephalometric Analysis'
            "
          >
            <router-link
              class="btn btn-default"
              :to="{
                name: 'Start New Ceph Service analysis',
                params: {
                  lang: $i18n.locale,
                  type: 'order',
                  id: String(item.id),
                },
              }"
            >
              {{
                item.product_obj.subscription_size - item.used_cases > 0
                  ? "Start"
                  : "View Result"
              }}
            </router-link>
          </div>
          <div
            class="serviceRow__link"
            v-if="
              item.product_obj.product_class == 'online-ai-service' &&
              item.product_obj.parent_obj.title == 'Pan Ai'
            "
          >
            <router-link
              class="btn btn-default"
              :to="{
                name: 'Start New Panoramic Service analysis',
                params: {
                  lang: $i18n.locale,
                  type: 'order',
                  id: String(item.id),
                  patient: '#',
                },
              }"
            >
              {{
                item.product_obj.subscription_size - item.used_cases > 0
                  ? "Start"
                  : "View Result"
              }}
            </router-link>
          </div>
          <div
            class="serviceRow__link"
            v-if="
              item.product_obj.product_class != 'online-ai-service' &&
              item.product_obj.case_definitions.length > 0
            "
          >
            <router-link
              class="btn btn-secondary grey"
              :to="{
                name: 'continue-service-flow',
                params: {
                  lang: $i18n.locale,
                  type: 'order',
                  index: String(item.id),
                },
              }"
            >
              Continue
            </router-link>
          </div>
        </div>
      </div>
      <base-pagination
        path="/start-service-existing/page="
        :itemPerPage="5"
        :count="activeOrderCount"
      />
    </div>
  </div>
</template>

<script>
// [*] Import UI Components
import BaseBreadCrumb from "@/common/components/base/BaseBreadCrumb.vue";
import BaseOfferNotifications from "@/common/components/base/BaseOfferNotifications.vue";
import BasePagination from "@/common/components/base/BasePagination.vue";

// [*] Import Breadcrumbs
import { startServiceExistingBreadCrumbs } from "@/common/constant/breadCrumbs";

// [*] Vuex State Getter And Action Helper
import { formatIds } from "@/common/helpers/index";
import { ServiceHelper } from "@/common/crud-helpers/service";
import { mapGetters } from "vuex";

export default {
  props: {
    page: String,
  },
  components: {
    BaseBreadCrumb,
    BaseOfferNotifications,
    BasePagination,
  },
  data() {
    return {
      breadCrumbsItems: [...startServiceExistingBreadCrumbs],
      activeOrderLines: null,
    };
  },
  mounted() {
    ServiceHelper.getActiveOrderLines({ page: this.page });
  },
  computed: {
    ...mapGetters(["serviceList", "activeOrderLine", "activeOrderCount"]),
  },
  watch: {
    activeOrderLine() {
      this.activeOrderLines = this.activeOrderLine.filter(
        (line) =>
          line.product_obj.product_class == "online-ai-service" ||
          line.product_obj.product_class == "digital-service"
      );
    },
    page() {
      ServiceHelper.getActiveOrderLines({ page: this.page });
    },
  },
  methods: {
    formatId(id) {
      return "#" + formatIds(id);
    },
  },
};
</script>

<style lang="scss" scoped>
.service {
  h1 {
    margin-bottom: rem(8px);
  }
  h2 {
    font-size: rem(20px);
    font-weight: 400;
    margin-bottom: rem(16px);
  }
  p {
    margin-bottom: rem(32px);
    span {
      font-weight: 500;
    }
  }
  .viewMore {
    &:hover {
      svg {
        transform: translate(7px, 0px);
        color: #f7c0b7;
      }
    }
  }
  .contentBox {
    @media screen and (max-width: 991px) {
      border: 0;
      padding: 0;
    }
  }
}
</style>
