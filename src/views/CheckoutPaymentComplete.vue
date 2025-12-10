<template>
  <div class="paymentCompleted">
    <base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
    <div class="paymentCompleted__wrapper">
      <svg-icon icon-id="correct-icon" icon-viewbox="0 0 72 72"></svg-icon>
      <div class="paymentCompleted__wrapper--text">
        <h1 class="main-title">Payment Completed</h1>
        <p>
          Thank you! Your payment has been processed, Details of your order are
          included below...
        </p>
      </div>
      <div class="card">
        <div class="card__body grid" data-grid-item-width="1/3">
          <div class="item">
            <p>#{{ orderData.number }}</p>
            <span>Order Number</span>
          </div>
          <div class="item">
            <p>{{ orderData.date_placed.split("T")[0] }}</p>
            <span>Ordered date</span>
          </div>
          <div class="item">
            <p>
              <money-format
                :value="Number(orderData.total_excl_tax)"
                :locale="`en`"
                :currency-code="userProfile.default_currency"
                :subunits-value="false"
                :hide-subunits="false"
              >
              </money-format>
            </p>
            <span>Total Amount</span>
          </div>
          <div class="item">
            <p>Credit or Debit Cards</p>
            <span>Payment Type</span>
          </div>
        </div>
      </div>
      <h2>You can start with one of your purchased services</h2>
      <div class="contentBox">
        <div
          class="serviceRow"
          v-for="(item, index) in orderLines"
          :key="index"
          @click.prevent="openProduct(index)"
        >
          <div
            class="serviceRow__image"
            v-if="item.product_obj.product_class == 'online-ai-service'"
          >
            <img
              v-if="item && item.product_obj.parent_obj.images.length > 0"
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
              v-if="item && item.product_obj.images.length > 0"
              :src="item.product_obj.images[0].original"
              alt=""
              class="img-fluid"
            />
          </div>
          <div class="serviceRow__title">
            <span v-if="item.product_obj.product_class == 'online-ai-service'">
              {{ item.product_obj.parent_obj.title }} -
              {{ item.product_obj.title }}
            </span>
            <span v-if="item.product_obj.product_class != 'online-ai-service'">
              {{ item.product_obj.title }}
            </span>
            <!-- <div class="serviceRow__cases" v-if="item.remaining">
							<div class="serviceRow__cases--progress">
								<b-progress
									:value="item.value"
									:max="item.max"
								></b-progress>
							</div>
							<div
								class="
									d-flex
									justify-content-between
									align-items-center
								"
							>
								<div class="serviceRow__cases--remaining">
									<span>{{ item.case }} </span
									>{{ item.remainingCase }}
									<svg-icon
										v-b-tooltip.hover
										title="cases remaining"
										icon-id="info-circle"
										icon-viewbox="0 0 24 24"
									></svg-icon>
								</div>
								<div class="serviceRow__cases--duration">
									{{ item.duration }}
								</div>
							</div>
						</div> -->
            <!-- <div class="serviceRow__details" v-if="item.seeMore">
							<a href="#" class="viewMore"
								>{{ item.detail }}
								<font-awesome-icon :icon="['fa', 'angle-right']"
							/></a>
						</div> -->
          </div>
          <!-- <div class="serviceRow__link">
						<a href="#" v-if="item.showBtn" class="btn btn-default">{{
							item.link
						}}</a>
					</div> -->
        </div>
      </div>
      <div class="paymentCompleted__proceed">
        <router-link
          :to="{
            name: 'Shop',
            params: {
              lang: $i18n.locale,
              page: '1',
            },
          }"
          class="btn btn-secondary orange"
        >
          Continue Shopping
        </router-link>
        <router-link
          :to="{
            name: 'My Order',
            params: {
              lang: $i18n.locale,
              page: '1',
            },
          }"
          class="viewMore"
        >
          See Order Details
          <font-awesome-icon :icon="['fa', 'angle-right']" />
        </router-link>
      </div>
    </div>
  </div>
</template>
<script>
// [*] Import UI Components
import BaseBreadCrumb from "@/common/components/base/BaseBreadCrumb.vue";
import MoneyFormat from "vue-money-format";
import Services from "@/components/service/Services.vue";

// [*] Import Breadcrumbs
import { checkoutPaymentCompleteBreadCrumbs } from "@/common/constant/breadCrumbs";

// [*] Vuex State Getter And Action Helper
import { mapGetters } from "vuex";
import { ServiceHelper } from "@/common/crud-helpers/service";

export default {
  components: {
    BaseBreadCrumb,
    Services,
    MoneyFormat,
  },

  data() {
    return {
      breadCrumbsItems: [...checkoutPaymentCompleteBreadCrumbs],
    };
  },
  mounted() {
    if (!this.orderData) {
      this.$router.push({
        name: "Shop",
        params: { lang: $i18n.locale, page: "1" },
      });
    }
  },
  created() {
    ServiceHelper.getActiveOrderLines({ page: "1" });
  },
  computed: {
    ...mapGetters([
      "userProfile",
      "orderData",
      "orderLines",
      "activeOrderLine",
    ]),
  },
  methods: {
    openProduct(index) {
      let orderLine = this.activeOrderLine.find(
        (line) => line.id == this.orderData.lines_id[index]
      );
      if (orderLine == null || orderLine == undefined) return;
      if (
        orderLine.product_obj.product_class == "online-ai-service" &&
        orderLine.product_obj.parent_obj.title == "AI Cephalometric Analysis"
      ) {
        this.$router.push({
          name: "Start New Ceph Service analysis",
          params: {
            lang: this.$i18n.locale,
            type: "order",
            id: String(orderLine.id),
            patient: "#",
          },
        });
      } else if (
        orderLine.product_obj.product_class == "online-ai-service" &&
        orderLine.product_obj.parent_obj.title == "Pan Ai"
      ) {
        this.$router.push({
          name: "Start New Panoramic Service analysis",
          params: {
            lang: this.$i18n.locale,
            type: "order",
            id: String(orderLine.id),
            patient: "#",
          },
        });
      } else {
        this.$router.push({
          name: "continue-service-flow",
          params: {
            lang: this.$i18n.locale,
            type: "order",
            index: String(orderLine.id),
          },
        });
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.paymentCompleted {
  &__wrapper {
    margin-top: rem(48px);
    max-width: 840px;
    margin-left: auto;
    margin-right: auto;
    text-align: center;
    @media screen and (max-width: 991px) {
      .contentBox {
        border: 0;
        padding: 0;
      }
    }
    svg {
      height: 72px;
      width: 72px;
      display: block;
      margin-left: auto;
      margin-right: auto;
    }
    &--text {
      max-width: 392px;
      margin-left: auto;
      margin-right: auto;
      h1 {
        margin-top: rem(24px);
      }
      p {
        color: var(--default);
      }
    }
    .card__body {
      padding: rem(28px) rem(74px);
      @media screen and (max-width: 767px) {
        padding: 16px;
      }
      &.grid {
        grid-template-columns: 93px 91px 90px 1fr;
        grid-gap: 86px;
        @media screen and (max-width: 1200px) {
          grid-gap: 50px;
        }
        @media screen and (max-width: 767px) {
          grid-template-columns: unset;
          grid-gap: unset;
        }
      }
      .item {
        text-align: left;
        @media screen and (max-width: 767px) {
          text-align: center;
          display: flex;
          flex-direction: row-reverse;
          width: 100%;
          justify-content: space-between;
          &:not(:last-child) {
            margin-bottom: 12px;
          }
        }
        p {
          margin-bottom: rem(5px);
          color: #171716;
          font-size: rem(16px);
          @media screen and (max-width: 767px) {
            margin-bottom: rem(0px);
          }
        }
        span {
          font-size: rem(14px);
          color: var(--textSecondary);
        }
      }
    }
    h2 {
      margin-top: rem(32px);
      margin-bottom: rem(24px);
      font-size: rem(20px);
    }
  }
  &__proceed {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: rem(40px);
    @media screen and (max-width: 991px) {
    }
    @media screen and (max-width: 767px) {
      flex-direction: column;
      justify-content: center;
    }
    .btn {
      padding-right: rem(75px);
      padding-left: rem(75px);
    }
    a {
      display: flex;
      align-items: center;
      justify-content: space-between;
      @media screen and (max-width: 767px) {
        margin-top: 15px;
      }
      svg {
        margin-left: rem(10px);
        height: 16px;
        width: 16px;
      }
      &.viewMore {
        &:hover {
          svg {
            transform: translate(7px, 0px);
          }
        }
      }
    }
  }
}
</style>
