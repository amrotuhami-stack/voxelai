<template>
  <div>
    <!-- choose pricing plan -->
    <div class="row justify-content-center">
      <div class="col-md-4 col-sm-6 mb-2"
        v-for="(content, i) in item.product_obj.siblings" :key="i"
      >
        <div
          class="card paymentPlan__item"
          :class="content.id == item.product_obj.id ? 'selected' : ''"
          @click.prevent="updatePricePlan((oldProductUrl = item.product_obj.url),(newProductUrl = content.url), (lineId = item.id))"
        >
          <div v-if="content.id == item.product_obj.id" :class="'selected__label'">
            selected
          </div> 
          <div class="card__body">
            <div class="paymentPlan__item--image">
              <svg-icon
                fill="currentColor"
                :icon-viewbox="'0 0 42 54'"
                :icon-id="'documentIcon'"
              ></svg-icon>
            </div>
            <div class="paymentPlan__item--title">
              {{ content.title }}
            </div>
            <div class="paymentPlan__item--price">
              <money-format
                :value="Number(content.price_availability.price.excl_tax)"
                :locale="`en`"
                :currency-code="userProfile.default_currency"
                :subunits-value="false"
                :hide-subunits="false"
              >
              </money-format>
            </div>
            <div class="paymentPlan__item--subtitle">
              {{ content.subscription_size }} Cases
            </div>
            <div class="paymentPlan__item--duration">
              {{ content.subscription_duration_m }} Months Access
            </div>
            <a href="#" class="btn btn-secondary"
              @click.prevent="updatePricePlan((oldProductUrl = item.product_obj.url),(newProductUrl = content.url), (lineId = item.id))"
              >Go {{ content.title }}</a
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// [*] Import UI Components .
import MoneyFormat from 'vue-money-format';
// [*] Vuex State Getter And Action Helper
import { BasketHelper } from "@/common/crud-helpers/basket";
import { mapGetters } from "vuex";

export default {
  props: {
    cartLineId: String,
    next: Function,
  },
  components: {
    MoneyFormat,
  },
  data() {
    return {
    };
  },
  computed: {
    ...mapGetters(["cartLines", "userProfile", "loading"]),
    item() {
        return this.cartLines.filter((item) => item.id == this.cartLineId)[0];
    },
  },
  methods: {
    updatePricePlan(oldProductUrl, newProductUrl, lineId) {
      if (oldProductUrl != newProductUrl) {
        BasketHelper.replaceCartItem({
          basket_id: this.userProfile.basket.id,
          id: lineId,
          oldProductUrl: oldProductUrl,
          newProductUrl: newProductUrl,
        });
      }
      this.next()
    },
  },
};
</script>


<style lang="scss"  scoped>
.paymentPlan__item {
  cursor: pointer;
  transition: 0.4s ease all;
  $self: &;
  @media screen and (max-width: 767px) {
    margin-bottom: rem(20px);
  }
  @media screen and (max-width: 575px) {
    max-width: 350px;
    margin: auto auto rem(20px) auto;
  }
  &.selected {
    position: relative;
    border: 1px solid #f7c0b7;
    overflow: unset;
    .selected__label {
      display: block;
      color: #ea5a43;
      text-transform: uppercase;
      font-weight: 500;
      font-size: rem(12px);
      letter-spacing: 1px;
      position: absolute;
      padding: rem(10px) rem(12px);
      width: 135px;
      border: 2px solid #f7c0b7;
      border-radius: 6px;
      text-align: center;
      left: 50%;
      transform: translateX(-50%);
      top: -15px;
      background: #fdefed;
    }
  }
  &.popular {
    position: relative;
    border: 1px solid #e9e9e9;
    overflow: unset;
    .popular__label {
      display: block;
      color: #8e8e8e;
      text-transform: uppercase;
      font-weight: 500;
      font-size: rem(12px);
      letter-spacing: 1px;
      position: absolute;
      padding: rem(10px) rem(12px);
      width: 135px;
      border: 2px solid #f7c0b7;
      border-radius: 6px;
      text-align: center;
      left: 50%;
      transform: translateX(-50%);
      top: -15px;
    }
  }
  .card__body {
    padding: rem(32px);
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    @media screen and (max-width: 1199px) and (min-width: 992px) {
      padding-left: rem(20px);
      padding-right: rem(20px);
    }
  }
  &--image {
    margin-top: rem(24px);
    position: relative;
    svg {
      position: static !important;
      fill: #fff;
      color: #e9e9e9;
      width: 38px !important;
      height: 100% !important;
      transition: 0.4s ease all;
    }
  }
  &--title {
    // margin-top: rem(25px);
    text-transform: uppercase;
    font-size: rem(20px);
    color: var(--default);
  }
  &--price {
    color: var(--textPrimary);
    margin-top: rem(16px);
    font-size: rem(24px);
    font-weight: 500;
  }
  &--subtitle {
    position: relative;
    color: #ea5a43;
    font-size: rem(16px);
    margin-top: rem(24px);
    padding-bottom: rem(16px);
    &::before {
      content: "";
      position: absolute;
      height: 1px;
      width: 180px;
      background: #eeeded;
      left: -40px;
      bottom: 0;
    }
  }
  &--duration {
    margin-top: rem(16px);
    margin-bottom: rem(24px);
    font-size: rem(14px);
    color: var(--textSecondary);
  }
  .btn {
    padding: rem(14px) rem(46px);
    @media screen and (max-width: 575px) {
      width: 100%;
    }
  }
  &.active {
    border-color: var(--primary);
    #{ $self }--image {
      svg {
        color: var(--primary);
      }
    }
    .btn {
      background: var(--primary);
      color: #fff;
      &:hover {
        opacity: 0.7;
      }
    }
  }
}
</style>