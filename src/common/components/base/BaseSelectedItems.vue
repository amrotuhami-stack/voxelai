<template>
	<div>
		<b-dropdown>
			<div class="cartItems">
				<base-inner-scrollbar height="350px">
					<div
						class="cartItems__products"
						v-for="(item) in cartItem"
						:key="item.url"
					>
						<product  :product="item.product_obj" :showAmount="true" :showOptions="false" :cartLine="item" :basketId="item.basket_id" />
						<span class="cartItems__products--close" @click.prevent="remove(item.id)">
							<svg-icon
								icon-id="cross-icon"
								icon-viewBox="0 0 12 12"
							></svg-icon>
						</span> 
					</div>
				</base-inner-scrollbar>
				<div class="cartItems__Total">
					Total excl. VAT:&nbsp; <money-format :value="Number(cart.total_excl_tax)"
						:locale='`en`'
						:currency-code="userProfile.default_currency"
						:subunits-value=false
						:hide-subunits=false>
					</money-format>
					<span ref="remmove" v-if="cart.total_excl_tax != cart.total_excl_tax_excl_discounts">
						<money-format :value="Number(cart.total_excl_tax_excl_discounts)"
							:locale='`en`'
							:currency-code="userProfile.default_currency"
							:subunits-value=false
							:hide-subunits=false>
						</money-format>
					</span>
					<div class="button-row" >
						<router-link class="btn btn-primary full"
							:to="{
								name: 'shopping-cart',
								params: {
									lang: $i18n.locale,
								},
							}"
							>Go to Cart</router-link
						>
					</div>
				</div>
			</div>
			<!-- <div style="text-align: center; margin: 20px;"> 
				<font-awesome-icon icon="spinner" size="3x" spin />
				<div style="text-align: center">  <p>Loading</p> </div>
			</div> !-->
		</b-dropdown>
	</div>
</template>

<script>
// [*] Import UI Compnents ...
import Product from '../../../components/cart/partials/Product.vue';
import MoneyFormat from 'vue-money-format';

// [*] Import vuex state and helpers
import { mapGetters } from 'vuex';
import { BasketHelper } from '@/common/crud-helpers/basket';


export default {
	components: { Product, MoneyFormat },
	props: { cartItem: Array, cart: Object },
	computed: {
		...mapGetters(['userProfile']),
    },
	methods: {
		remove(line_id) {
			let params = { basket_id: this.userProfile.basket.id, id: line_id, };
			BasketHelper.removeCart(params);
		}
  	},
};
</script>
<style lang="scss">
.cartItems {
	box-shadow: 0px 4px 25px rgba(107, 107, 107, 0.03);
	background: rgba(247, 247, 247, 0.3);
	&__products {
		display: flex;
		justify-content: space-between;
		padding-right: rem(24px);
		&--close {
			margin-top: rem(25px);
			// position: absolute;
			// right: 20px;
			// top: 25px;
			svg {
				width: 12px;
				height: 12px;
				opacity: 0.5;
			}
			&:hover {
				svg {
					opacity: 0.9;
				}
			}
		}
	}

	.cartItemsWrapper {
		box-shadow: 0px 4px 25px rgba(107, 107, 107, 0.03);
		background: rgba(247, 247, 247, 0.3);
	}
	.cartItem {
		&__product {
			display: flex;
			align-items: center;
			position: relative;
			padding: 0 rem(15px);
			padding-right: rem(42px);
			flex-wrap: nowrap;
			&:not(:last-child) {
				margin-bottom: rem(20px);
			}
			&--image {
				flex: 0 0 96px;
				max-width: 96px;
				background: var(--imageBg);
				text-align: center;
				padding-top: 7px;
				padding-bottom: 7px;
				border-radius: 6px;
				margin-right: 12px;
			}
			&--title {
				font-size: rem(14px);
				font-weight: 400;
				margin-bottom: rem(10px) !important;
				max-width: 100%;
				flex: 1;
				padding-right: 10px;
				@include truncate(1);
			}
			&--price {
				font-size: rem(16px);
				font-weight: 500;
				span {
					font-size: rem(14px);
					display: inline-block;
					color: #8e8e8e;
					margin-left: 10px;
					text-decoration: line-through;
					font-weight: 400;
				}
			}
		}
	}
	&__item {
		display: flex;
		align-items: center;
		position: relative;
		background: rgba(247, 247, 247, 0.3);

		&--detail {
			p {
				line-height: 1;
				color: var(--textPrimary);
				margin: 0;
				&:not(:last-child) {
					margin-bottom: rem(15px);
				}
			}

			&--price {
				font-size: rem(16px);
				font-weight: 500;
				span {
					font-size: rem(14px);
					display: inline-block;
					color: #8e8e8e;
					margin-left: 10px;
					text-decoration: line-through;
					font-weight: 400;
				}
			}
		}
	}
	&__Total {
		font-size: rem(20px);
		color: var(--textPrimary);
		font-weight: 500;
		padding: rem(15px);
		padding-top: rem(22px);
		margin-top: rem(20px);
		background: #fff;
		box-shadow: 0 -5px 5px -5px rgba(107, 107, 107, 0.24);
		display: flex;
		span {
			font-size: rem(16px);
			font-weight: 400;
			color: #8e8e8e;
			display: inline-block;
			text-decoration: line-through;
			margin-left: 10px;
		}
		.button-row {
			margin-top: rem(20px);
		}
	}
}
</style>
<style lang="scss" scoped>
::v-deep {
	.dropdown {
		box-shadow: none !important;
		.dropdown-toggle {
			width: 24px;
			height: 24px;
			background: transparent !important;
			background-color: transparent !important;
			padding:0 !important;
			&:hover,
			&:focus {
				background: transparent !important;
				background-color: transparent !important;
			}
			&::after {
				display: none;
			}
		}
		.dropdown-menu {
			width: 415px;
			padding: 0;
			padding-top: rem(15px);
			padding-right: 2px;
			border-radius: 10px !important;
			box-shadow: 0px 4px 25px rgba(107, 107, 107, 0.08);
			right: 0;
			margin-top:rem(20px);
			@media screen and (max-width: 991px) {
				width: 350px;
			}
			@media screen and (max-width: 575px) {
				width: 320px;
			}
			.button-row {
				.btn {
					background-color: var(--secondary) !important;
					color: #ffffff !important;
					border: 2px solid var(--secondary);
					@include flex(center, center);
					height: 52px;
					padding: rem(16px);
					border-radius: 8px;
					&:hover {
						background-color: #fff !important;
						color: var(--secondary) !important;
					}
				}
			}
		}
		.scrollbar-wrap .scrollbar-y {
			width: 0.4em;
		}
		&.show {
			.btn {
				background: transparent !important;
				background-color: transparent !important;
			}
		}
	}
}
</style>
