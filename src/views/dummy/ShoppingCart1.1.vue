<template>
	<div class="shoppingCart">
		<base-offer-notifications />
		<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
		<h1 class="main-title">Shopping Cart</h1>
		<div class="shoppingCartWrapper">
			<div class="shoppingCart__left">
				<div class="table">
					<div class="table__head">
						<div class="table__row">
							<div class="table__row--cell">Product</div>
							<div class="table__row--cell" data-width="48">
								Pricing Plan
							</div>
							<div class="table__row--cell" data-width="10">
								&nbsp;
							</div>
						</div>
					</div>
					<div class="table__body cartItem">
						<div class="table__row">
							<div class="table__row--cell">
								<div class="cartItem__product">
									<div class="cartItem__product--image">
										<img
											src="@/assets/images/shoppingCart/mobile.png"
											alt=""
											class="img-fluid"
										/>
									</div>
									<div>Cephalometric<br />Analysis</div>
								</div>
							</div>
							<div class="table__row--cell" data-width="48">
								<div class="pricingPlan">
									<div class="pricingPlan__plan">
										PRO
										<p>6 Months Access</p>
									</div>
									<div class="pricingPlan__price">
										$236.00
										<p>15 Cases a Month</p>
									</div>
									<div class="pricingPlan__change">
										<router-link to="">Change</router-link>
									</div>
								</div>
							</div>
							<div class="table__row--cell" data-width="10">
								<svg-icon
									icon-id="cross-icon"
									icon-viewBox="0 0 12 12"
								></svg-icon>
							</div>
						</div>
					</div>
				</div>
				<div class="table">
					<div class="table__head">
						<div class="table__row">
							<div class="table__row--cell">Product</div>
							<div class="table__row--cell" data-width="15">
								Price
							</div>
							<div class="table__row--cell" data-width="28">
								Quantity
							</div>
							<div class="table__row--cell" data-width="15">
								Total
							</div>
							<div class="table__row--cell" data-width="5">
								&nbsp;
							</div>
						</div>
					</div>
					<!-- <cart-item /> -->
				</div>
			</div>
			<div class="shoppingCart__right">
				<sub-total></sub-total>
			</div>
		</div>
		<div class="productDetail__relatedProducts">
			<related-product-slider></related-product-slider>
		</div>
	</div>
</template>

<script>
import BaseOfferNotifications from '@/common/components/base/BaseOfferNotifications.vue';
import BaseTouchSpin from '../../common/components/base/BaseTouchSpin.vue';
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import { shopingCartBreadCrumbs } from "@/common/constant/breadCrumbs"
import RelatedProductSlider from '@/components/productDetails/RelatedProductSlider.vue';
import CartItem from '@/components/cart/CartItem.vue';
import SubTotal from '@/components/shoppingCart/SubTotal.vue';
import PaymentPlanItem from '@/components/PaymentPlanItem.vue';
export default {
	components: {
		BaseBreadCrumb,
		BaseOfferNotifications,
		BaseTouchSpin,
		RelatedProductSlider,
		CartItem,
		SubTotal,
		PaymentPlanItem,
	},
	data() {
		return {
			breadCrumbsItems: [...shopingCartBreadCrumbs],
			cardContent: [
				{
					index: 0,
					iconId: 'documentIcon',
					viewBox: '0 0 42 54',
					title: 'Basic',
					price: '$236.00',
					subtitle: '15 Cases a Month',
					duration: '6 Months Access',
				},
				{
					index: 1,
					popular: true,
					iconId: 'documentIcon',
					viewBox: '0 0 42 54',
					title: 'Pro',
					price: '$236.00',
					subtitle: '15 Cases a Month',
					duration: '6 Months Access',
				},
				{
					index: 2,
					iconId: 'documentIcon',
					viewBox: '0 0 42 54',
					title: 'Elite',
					price: '$236.00',
					subtitle: '15 Cases a Month',
					duration: '6 Months Access',
				},
			],
		};
	},
};
</script>

<style lang="scss" scoped>
.shoppingCart {
	.shoppingCartWrapper {
		display: flex;
	}
	&__left {
		flex: 1;
		margin-right: rem(20px);
		margin-bottom: rem(50px);
	}
	&__right {
		max-width: 300px;
		flex: 0 0 300px;
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
			padding-left: rem(70px);
			padding-right: rem(70px);
		}
		.table {
			&__row {
				&--cell {
					padding-top: rem(15px);
					padding-bottom: rem(15px);
					text-decoration: none !important;
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
			> div {
				&:not(:last-child) {
					padding-right: rem(10px);
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
</style>
