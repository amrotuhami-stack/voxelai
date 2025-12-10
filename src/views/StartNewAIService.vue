<template>
	<div class="cephService">
		<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
		<div>
			<h1 class="main-title">Start New AI Service</h1>
			<div class="row">
				<div class="col-lg-9">
					<div class="contentBox" v-if="productDetail && item">
						<div class="serviceRow">
							<div class="serviceRow__image" v-if="item.product_obj.product_class == 'online-ai-service'">
								<img v-if="item.product_obj.images.length > 0"
									:src="item.product_obj.images[0].original"
									alt=""
									class="img-fluid"
								/>
							</div>
							<div class="serviceRow__title" v-if="item.product_obj.product_class == 'online-ai-service'">
								<span>
									{{ item.product_obj.parent_obj.title }} - {{ item.product_obj.title }} 
								</span>
							</div>
						</div>
					</div>
					<div class="contentBox" v-else>
						<div class="serviceRow">
							<div class="serviceRow__image p-0">
								<b-skeleton animation="fade" width="100%" height="100px" class="skelton"></b-skeleton>
							</div>
							<div class="serviceRow__title"> 
								<b-skeleton animation="fade" width="50%" height="25px" class="skelton"></b-skeleton>
								<div class="serviceRow__details serviceData">
									<b-skeleton animation="fade" width="20%" height="25px" class="skelton"></b-skeleton>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div class="row" v-if="!item">
				<div style="margin-top: 35px;" v-for="(_, index) in 5" :key="index">
					<b-skeleton animation="fade" width="5%" height="30px" class="skelton"></b-skeleton>
					<b-skeleton animation="fade" width="50%" height="35px" class="skelton mt-2"></b-skeleton>
					<b-skeleton animation="fade" width="20%" height="30px" class="skelton mt-2"></b-skeleton>
				</div>
			</div>
			<div class="caseSteps accordion" v-if="item">
				<!-- 1 -->
				<div class="caseSteps__item">
					<div class="caseSteps__item--head" role="tab">
						<a href="javascript:void(0)" v-b-toggle.PricingPlan0>
							<span class="counter">STEP 01</span>Choose Pricing Plan
						</a>
					</div>
					<b-collapse
						id="PricingPlan0"
						invisible
						accordion="inner-accordion"
						role="tabpanel"
						v-model="collapseStates[0]"
					>
						<div class="caseSteps__item--body">
							<div class="row">
								<div class="col-lg-9">
									<div class="caseSteps__item--subtitle">
										<p>
											Here are the offers created for you.
										</p>
									</div>
								</div>
							</div>
							<div class="row">
								<div class="col-lg-9">
									<pricing-plans :cartLineId="String(item.id)" :next="priceingPlanSelected"></pricing-plans>
								</div>
							</div>
						</div>
					</b-collapse>
				</div>
				<!-- 1 -->
				<!-- 2 -->
				<div class="caseSteps__item">
					<div class="caseSteps__item--head" role="tab">
						<a href="javascript:void(0)" v-b-toggle.PricingPlan1>
							<span class="counter">STEP 02</span>Billing Account - CheckOut
						</a>
					</div>
					<b-collapse
						id="PricingPlan1"
						invisible
						accordion="inner-accordion"
						role="tabpanel"
						v-model="collapseStates[1]"
					>
						<div class="caseSteps__item--body">
							<div class="row">
								<div class="col-lg-9">
									<div class="caseSteps__item--subtitle">
										<p>
											Add your billing and shipping address
										</p>
									</div>
								</div>
							</div>
							<div class="row">
								<div class="col-lg-12">
									<checkout />
								</div>
							</div>
						</div>
					</b-collapse>
				</div>
				<!-- 2 -->
				<!-- 3 -->
				<div class="caseSteps__item">
					<div class="caseSteps__item--head" role="tab">
						<a href="javascript:void(0)">
							<span class="counter">STEP 03</span>Confirm Order and Pay
						</a>
					</div>
					<b-collapse
						id="PricingPlan2"
						invisible
						accordion="inner-accordion"
						role="tabpanel"
						v-model="collapseStates[2]"
					>
						<div class="caseSteps__item--body">
							<div class="row">
								<div class="col-lg-9">
									<div class="caseSteps__item--subtitle">
										<p>
											Choose your payment method and pay
										</p>
									</div>
								</div>
							</div>
							<div class="row" v-if="shippingMethods">
								<div class="col-lg-12">
									<confirm-payment />
								</div>
							</div>
						</div>
					</b-collapse>
				</div>
				<!-- 3 -->
			</div>
		</div>
	</div>
</template>

<script>
// [*] Import UI Components .
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import MoneyFormat from 'vue-money-format';
import PricingPlans from "@/components/NewAISteps/pricingPlans.vue"
import Checkout from "@/components/NewAISteps/checkout.vue"
import ConfirmPayment from '../components/NewAISteps/confirmPayment.vue';

// [*] Import Breadcrumbs
import { startNewAIServiceBreadCrumbs } from "@/common/constant/breadCrumbs"


// [*] Vuex State Getter And Action Helper
import { CatalogueHelper } from '@/common/crud-helpers/catalogue';
import { BasketHelper } from '@/common/crud-helpers/basket';
import { mapGetters } from 'vuex';



export default {
	components: {
		BaseBreadCrumb,
		MoneyFormat,
		PricingPlans,
		Checkout,
		ConfirmPayment,
	},
	props: {
		productId: String,
	},
	computed: {
		...mapGetters(['userProfile', 'productDetail', 'cartLines', 'shippingMethods']),
	},
	data() {
		return {
			breadCrumbsItems: [...startNewAIServiceBreadCrumbs],
			collapseStates: [true, false, false],
			item: null,

			firstRender: false,
		};
	},
	mounted(){
		this.getProductDetail();
	},
	created() {
		this.firstRender = true
	},
	watch: {
		productDetail(){
			if (this.productDetail) BasketHelper.getCart();
		},
		cartLines(){
			if(!this.productDetail) return
			if (this.firstRender && this.cartLines.length == 0 ){
				this.addToCart(this.productDetail.add_cart_url, this.productDetail.product_options)
			}
			else {
				let index = this.cartLines.findIndex((item) => item.product_obj.parent_obj && item.product_obj.parent_obj.id == this.productId)
				if(this.firstRender && index === -1) {
					this.addToCart(this.productDetail.add_cart_url, this.productDetail.product_options)
				}
				else {
					this.item = this.cartLines[index]
				}
			}
		},
		shippingMethods() {
			if(this.shippingMethods.length > 0) {
				this.collapseStates = [false, false, true]
			}
		}
    },

	methods: {
		getProductDetail (){
			CatalogueHelper.getProductDetail({id: Number(this.productId)})
		},
		addToCart: function(url, options){
			let params = { "quantity": 1, "url": url }
			if (options.length > 0 ) params["options"] = options.map(item => ({"option": item.url, "value": 0}))
			BasketHelper.addCart(params)
		},
		priceingPlanSelected: function() {
			this.collapseStates =  [false, true, false]
		},
	},
};
</script>

<style lang="scss" scoped>
.cephService {
	::v-deep.paymentPlan {
		&__item {
			&--image {
				margin-top: 0;
				margin-bottom: rem(20px);
			}
		}
	}
	.paymentMethod {
		h3 {
			font-size: rem(16px);
			font-weight: 400;
			color: var(--default);
			margin-bottom: rem(16px);
		}
		&__serviceTrems {
			display: flex;
			align-items: center;
			justify-content: space-between;
			@media screen and (max-width: 991px) {
				flex-direction: column;
			}
			p {
				font-size: rem(12px);
				font-weight: 400;
				letter-spacing: 1px;
				a {
					font-weight: 500;
					color: var(--primary);
				}
				svg {
					width: 24px;
					height: 24px;
					margin-right: rem(8px);
				}
			}
		}
		&__checkOutproceed {
			@include flex(center, space-between);
			p {
				margin-bottom: 0;
				span {
					color: #000000;
					font-weight: 500;
				}
			}
		}
		::v-deep {
			.totalSummary {
				.card {
					margin-bottom: rem(25px);
					&__body {
						padding-left: rem(20px);
						padding-right: rem(20px);
						@media screen and (max-width: 1199px) and (min-width: 992px) {
							padding-left: rem(10px);
							padding-right: rem(10px);
						}
					}
				}
			}
		}
		.orderDetail {
			border: 1px solid #a8d5ee;
			border-radius: 6px;
			padding: rem(16px);
			overflow: hidden;
			&__name {
				font-size: rem(20px);
				font-weight: 400;
				color: var(--default);
				margin-bottom: rem(10px);
			}
			&__duration {
				font-size: rem(14px);
				font-weight: 400;
				line-height: 1;
				color: var(--textSecondary);
				margin: 0;
			}
			&__info {
				padding-top: rem(28px);
				h4 {
					font-size: rem(16px);
					font-weight: 500;
					color: var(--textPrimary);
					line-height: 1;
				}
				&--case {
					padding-top: rem(6px);
					@include flex(center, space-between);
					font-size: rem(14px);
					color: var(--orange);
					font-weight: normal;
					a {
						font-weight: 500;
						color: var(--primary);
						@media screen and (max-width: 1300px) and (min-width: 992px) {
							display: block;
							padding-top: rem(12px);
						}
						&:hover {
							text-decoration: underline;
						}
					}
				}
			}
		}
	}
}
</style>
