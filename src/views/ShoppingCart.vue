<template>
  <div class="shoppingCart">
    <!-- <base-offer-notifications /> -->
    <base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
    <h1 class="main-title">Shopping Cart</h1>
    <div class="shoppingCartWrapper">
      <div class="shoppingCart__left">
        <div class="tableDesktop">
          <div class="table" v-if="onlineAiServiceCartItem.length > 0">
            <div class="table__head">
              <div class="table__row">
                <div class="table__row--cell">Product</div>
                <div class="table__row--cell" data-width="40">Pricing Plan</div>
                <div class="table__row--cell" data-width="10">Actions</div>
              </div>
            </div>
            <div
              class="table__body cartItem"
              style="border: none"
              v-if="onlineAiServiceCartItem.length > 0"
            >
              <div
                class="table__row"
                v-for="(item, i) in onlineAiServiceCartItem"
                :key="i"
              >
                <div class="table__row--cell">
                  <product
                    :product="item.product_obj"
                    :showAmount="false"
                    :showOptions="true"
                    :cartLine="item"
                    :basketId="item.basket_id"
                  />
                </div>
                <div class="table__row--cell" data-width="40">
                  <div class="pricingPlan">
                    <div class="pricingPlan__plan">
                      {{ item.product_obj.title }}
                      <p>
                        {{ item.product_obj.subscription_duration_m }} Months Access
                      </p>
                    </div>
                    <div class="pricingPlan__price">
                      <money-format
                        :value="
                          Number(
                            item.product_obj.price_availability.price.excl_tax
                          )
                        "
                        :locale="`en`"
                        :currency-code="userProfile.default_currency"
                        :subunits-value="false"
                        :hide-subunits="false"
                      >
                      </money-format>
                      <p>
                        {{ item.product_obj.subscription_size }} Cases
                      </p>
                    </div>
                    <div class="pricingPlan__change">
                      <router-link to="" v-b-modal="`pricing-plan-${item.id}`">
                        Change
                      </router-link>
                    </div>
                  </div>
                </div>
                <div class="table__row--cell" data-width="10" @click.prevent="removeFromCart(item.id)">
                  <div class="actions">
                    <svg-icon
                      icon-id="cross-icon"
                      icon-viewBox="0 0 12 12"
                    ></svg-icon>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="table" v-if="cartItem.length > 0">
						<div class="table__head">
							<div class="table__row">
								<div class="table__row--cell">Product</div>
								<div class="table__row--cell" data-width="10">
									Price
								</div>
								<div class="table__row--cell" data-width="20">
									Quantity
								</div>
								<div class="table__row--cell" data-width="10">
									Total
								</div>
								<div class="table__row--cell" data-width="10">
									Actions
								</div>
							</div>
						</div>
						<div class="table__body cartItem" style="border: none; ">
								<cart-item v-for="(item, i) in cartItem" :key="i" :cart="item"/>
						</div>
					</div>
        </div>

        <div class="tableResponsive">
          <div class="table" v-if="onlineAiServiceCartItem.length > 0">
            <div class="table__body cartItem">
              <div
                class="table__row"
                v-for="(item, i) in onlineAiServiceCartItem"
                :key="i"
              >
                <div class="table__row--cell">
                  <product
                    :product="item.product_obj"
                    :showAmount="false"
                    :showOptions="true"
                    :cartLine="item"
                    :basketId="item.basket_id"
                  />
                </div>
                <div class="table__row--cell justify-content-between">
                  <div class="pricingPlan">
                    <div class="pricingPlan__plan">
                      {{ item.product_obj.title }}
                      <p>
                        {{ item.product_obj.subscription_duration_m }} Months
                        Access
                      </p>
                    </div>
                    <div class="pricingPlan__price">
                      <money-format
                        :value="
                          Number(
                            item.product_obj.price_availability.price.excl_tax
                          )
                        "
                        :locale="`en`"
                        :currency-code="userProfile.default_currency"
                        :subunits-value="false"
                        :hide-subunits="false"
                      >
                      </money-format>
                      <p>
                        {{ item.product_obj.subscription_size }} Cases
                      </p>
                    </div>
                    <div class="pricingPlan__change">
                      <router-link to="" v-b-modal="`pricing-plan-${item.id}`">
                        Change
                      </router-link>
                    </div>
                  </div>
                  <a href="#" class="remove-cart" @click.prevent="removeFromCart(item.id)"> Remove from cart </a>
                </div>
              </div>
            </div>
          </div>
          <div class="table">
						<div class="table__body">
							<cart-item v-for="(item, index) in cartItem" :key="index" :cart="item"/>
						</div>
					</div>
        </div>
      </div>
      <div class="shoppingCart__right">
        <sub-total></sub-total>
      </div>
    </div>
    <div class="productDetail__relatedProducts">
      <related-product-slider></related-product-slider>
    </div>
    <!-- The modal -->
    <b-modal
      class="pricingModal"
      :id="`pricing-plan-${item.id}`"
      center
      size="xl"
      v-for="(item, i) in onlineAiServiceCartItem"
      :key="i"
    >
      <div class="modal-title">Choose Pricing Plan</div>
      <p class="mb-40">Here are the offers created for you.</p>

      <!-- choose pricing plan -->
      <div class="row justify-content-center">
        <div
          class="col-md-4 col-sm-6 mb-4"
          v-for="(content, i) in item.product_obj.siblings"
          :key="i"
        >
          <div
            class="card paymentPlan__item"
            :class="content.most_popular == true ? 'popular' : ''"
          >
            <div v-if="content.most_popular" class="popular__label">
              most popular
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
              <a
                href="#"
                class="btn btn-secondary"
                @click.prevent="
                  updatePricePlan(
                    (oldProductUrl = item.product_obj.url),
                    (newProductUrl = content.url),
                    (lineId = item.id)
                  )
                "
                >Go {{ content.title }}</a
              >
            </div>
          </div>
        </div>
      </div>
    </b-modal>
  </div>
</template>

<script>
// [*] Import UI Components .
import BaseBreadCrumb from "@/common/components/base/BaseBreadCrumb.vue";
import BaseOfferNotifications from "@/common/components/base/BaseOfferNotifications.vue";
import BaseTouchSpin from "../common/components/base/BaseTouchSpin.vue";
import RelatedProductSlider from "@/components/productDetails/RelatedProductSlider.vue";
import CartItem from "@/components/cart/CartItem.vue";
import SubTotal from "@/components/cart/SubTotal.vue";
import PaymentPlanItem from "@/components/PaymentPlanItem.vue";
import Product from "@/components/cart/partials/Product.vue";
import MoneyFormat from "vue-money-format";

// [*] Import Breadcrumbs
import { shopingCartBreadCrumbs } from "@/common/constant/breadCrumbs";

// [*] Vuex State Getter And Action Helper
import { BasketHelper } from "@/common/crud-helpers/basket";
import { CatalogueHelper } from "@/common/crud-helpers/catalogue";
import { mapGetters } from "vuex";

export default {
  components: {
    BaseBreadCrumb,
    BaseOfferNotifications,
    BaseTouchSpin,
    RelatedProductSlider,
    CartItem,
    SubTotal,
    PaymentPlanItem,
    Product,
    MoneyFormat,
  },
  data() {
    return {
      breadCrumbsItems: [...shopingCartBreadCrumbs],
    };
  },
  computed: {
    ...mapGetters(["cartLines", "userProfile", "loading"]),
    onlineAiServiceCartItem() {
      return this.cartLines.filter(function (item) {
        return item.product_obj.product_class == "online-ai-service";
      });
    },
    cartItem() {
      return this.cartLines.filter(function (item) {
        return item.product_obj.product_class != "online-ai-service";
      });
    },
  },
  watch: {
    cartLines() {
      if (this.cartLines.length == 0) {
        this.$router.push({ name: "empty-shopping-cart" });
      }
      else {
        let relatedProducts = []
        this.cartLines.forEach((item) => {
          if(item.product_obj.product_class == "online-ai-service") {
            relatedProducts = [...relatedProducts, ...item.product_obj.parent_obj.recommended_products]
          }
          else {
            relatedProducts = [...relatedProducts, ...item.product_obj.recommended_products]
          }
        })
        CatalogueHelper.getRelatedProducts(relatedProducts)
      }
    },
  },
  methods: {
    updatePricePlan(oldProductUrl, newProductUrl, lineId) {
      this.$bvModal.hide(`pricing-plan-${lineId}`);
      if (oldProductUrl != newProductUrl) {
        BasketHelper.replaceCartItem({
		  basket_id: this.userProfile.basket.id,
		  id: lineId,
          oldProductUrl: oldProductUrl,
          newProductUrl: newProductUrl,
        });
      }
    },
	removeFromCart: function(line_id){
		let params = { basket_id: this.userProfile.basket.id, id: line_id, };
		BasketHelper.removeCart(params);
	}
  },
};
</script>

<style lang="scss">
.cartItem {
  padding-bottom: rem(15px);
  .btn-secondary {
    filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
  }
  .table {
    &__row {
      &:hover {
        background-color: transparent !important;
        .table__row--cell {
          &:first-child {
            text-decoration: none !important;
          }
        }
      }
    }
  }
}
</style>
<style lang="scss" scoped>
.shoppingCart {
  .shoppingCartWrapper {
    display: flex;
    @media screen and (max-width: 991px) {
      flex-direction: column-reverse;
    }
  }
  &__left {
    flex: 1;
    margin-right: rem(20px);
    margin-bottom: rem(50px);
    @media screen and (max-width: 1200px) {
      margin-right: rem(10px);
    }
    @media screen and (max-width: 991px) {
      margin-right: rem(0px);
    }
    .cartItem {
      .table__row {
        padding: 5px;
      }
    }
  }
  &__right {
    max-width: 350px;
    flex: 0 0 350px;
    @media screen and (max-width: 1600px) {
      max-width: 300px;
      flex: 0 0 300px;
    }
    @media screen and (max-width: 1200px) {
      max-width: 250px;
      flex: 0 0 250px;
    }
    @media screen and (max-width: 991px) {
      max-width: 100%;
      flex: 0 0 100%;
      margin-bottom: rem(30px);
    }
  }
  .cartItem {
    &__product {
      display: flex;
      align-items: center;
      font-size: rem(20px);
      color: var(--textPrimary) !important;
      &--image {
        flex: 0 0 118px;
        max-width: 118px;
        margin-right: rem(5px);
        img {
          background: #f5f5f5;
          padding: rem(7px) 0;
          border-radius: 6px;
          width: 115px;
        }
      }
    }
    svg {
      height: 12px;
      width: 12px;
      &:hover {
        opacity: 0.7;
        cursor: pointer;
      }
    }
    .btn-secondary {
      @media screen and (min-width: 1201px) {
        padding-left: rem(70px);
        padding-right: rem(70px);
      }
    }
    .table {
      &__row {
        &--cell {
          padding-top: rem(15px);
          padding-bottom: rem(15px);
          text-decoration: none !important;
          .actions {
            display: flex;
            justify-content: center;
            align-items: center;
          }
        }
        &:hover {
          background: transparent;
        }
      }
    }
  }
  .table {
    .pricingPlan {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border: 2px solid #a8d5ee;
      border-radius: 6px;
      padding: rem(24px) rem(20px);
      @media screen and (max-width: 1200px) {
        padding: rem(18px) rem(12px);
      }
      > div {
        &:not(:last-child) {
          padding-right: rem(10px);
          @media screen and (max-width: 1200px) {
            padding-right: rem(5px);
          }
        }
      }
      p {
        line-height: 1;
        margin-bottom: 0;
        font-size: rem(14px);
        margin-top: 5px;
      }
      &__plan {
        font-size: rem(20px);
        text-transform: uppercase;
        color: var(--default);
      }
      &__price {
        font-size: rem(20px);
        color: var(--textPrimary);
        font-weight: 500;
        p {
          color: var(--secondary);
        }
      }
      &__change {
        a {
          color: var(--primary);
          font-size: rem(14px);
          font-weight: 500;
          &:hover {
            color: var(--secondary);
          }
        }
      }
    }
  }
}

@media screen and (min-width: 992px) {
  ::v-deep .hideDesktop {
    display: none;
  }
}

@media screen and (max-width: 991px) {
  ::v-deep .showDesktop {
    display: none;
  }
  ::v-deep .hideDesktop {
    display: block;
    &.cartItem__price {
      display: flex;
    }
    &.checkbox {
      flex: 0 0 100%;
      margin: 8px 0;
    }
  }
}

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
  &.popular {
    position: relative;
    border: 1px solid #f7c0b7;
    overflow: unset;
    .popular__label {
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
