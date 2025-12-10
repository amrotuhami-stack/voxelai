<template>
	<div>
		<div class="card">
			<div class="card__head">Subtotal</div>
			<div class="card__body">
				<div class="itemPrice" v-if="cart && userProfile && !loading.value">
					<money-format :value="Number(cart.total_excl_tax)"
						:locale='`en`'
						:currency-code='userProfile.default_currency'
						:subunits-value=false
						:hide-subunits=false>
					</money-format>
					<p v-if="cart.total_excl_tax != cart.total_excl_tax_excl_discounts">
						<money-format :value="Number(cart.total_excl_tax_excl_discounts)"
							:locale='`en`'
							:currency-code='userProfile.default_currency'
							:subunits-value=false
							:hide-subunits=false>
						</money-format>
					</p>
				</div>
				<div v-if="loading.value" style="text-align: center;margin-bottom: 20px;">
					<font-awesome-icon id="spinner" class="spinner" icon="spinner" size="3x" spin  />
				</div>
				<router-link class="btn btn-primary full" :class="hideCheckoutButton ? 'd-none' : ''"
					:to="{name: 'CheckOut', params: { lang: $i18n.locale,},}"
				>Proceed to Checkout</router-link>
				<div class="couponWrapper">
					<div class="Coupon">
						<input
							type="text"
							class="form-control"
							placeholder="Enter Coupon"
							v-model="code"
						/>
						<button type="button" class="btn btn-secondary" @click.prevent="applyCoupon">
							Apply
						</button>
					</div>
					<ul class="CouponApplied list-unstyled" v-if="coupon.name">
						<li>
							<!-- <span class="icon">
								<svg-icon
									icon-id="cross-icon"
									icon-viewBox="0 0 12 12"
								></svg-icon>
							</span> -->
							<p>VOXEL Coupon ({{coupon.code }})</p>
							<span>Applied</span>
						</li>
					</ul>
					<ul class="CouponApplied list-unstyled" v-if="(coupon == false)">
						<li>
							<!-- <span class="icon">
								<svg-icon
									icon-id="cross-icon"
									icon-viewBox="0 0 12 12"
								></svg-icon>
							</span> -->
							<p>Coupon Code</p>
							<span style="color: red;">Invalid</span>
						</li>
					</ul>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
// [*] Vuex State Getter And Action Helper
import { mapGetters } from 'vuex';

// [*] Import UI Components .
import MoneyFormat from 'vue-money-format';

import { BasketHelper } from '@/common/crud-helpers/basket';

export default {
	props: {
		hideCheckoutButton: {
			type: Boolean,
			default: false,
		},
	},
	components: { MoneyFormat },
	data(){
		return {
			code: "",
		}
	},
	computed: {
		...mapGetters(['userProfile', 'loading', 'cart', 'coupon']),
    },
	watch: {
		coupon() {
			if(this.coupon.name) 
				this.code = ""
			
		}
	},
	methods: {
		applyCoupon() {
			BasketHelper.addCartCoupon({'vouchercode': this.code});
		}
	}
};
</script>

<style lang="scss" scoped>
.card {
	&__head {
		padding: rem(27px) rem(24px);
	}
	.itemPrice {
		font-size: rem(32px);
		color: var(--textPrimary);
		font-weight: 500;
		margin-bottom: rem(16px);
		@media screen and (max-width:1025px) and (min-width:992px){
			font-size:rem(26px);
		}
		@media screen and (max-width:767px){
			font-size:rem(26px);
		}
		p {
			text-decoration-line: line-through;
			color: #8e8e8e;
			margin-bottom: 7px;
			line-height: 1;
			font-weight: 400;
			margin-top: rem(10px);
		}
	}
	.Coupon {
		display: flex;
		justify-content: space-between;
		margin-top: rem(16px);
		.form-control {
			background: transparent;
			border-radius: 8px;
			height: 41px;
			border: 1px solid #c9c9c9;
			color: #8e8e8e;
			font-size: rem(14px);
			margin-right: rem(10px);
			padding-left: rem(18px);
			padding-top: rem(12px);
			&::placeholder {
				color: #8e8e8e !important;
				font-size: rem(14px);
				display: block !important;
				opacity: 1 !important;
				font-weight: 400;
			}
		}
		.btn {
			height: 41px;
			padding: rem(15px);
			font-size: rem(14px);
		}
		@media screen and (max-width:1199px) and (min-width:992px){
			flex-direction: column;
			.btn{
				margin-top:rem(6px);
				width: 80px;
			}
		}
	}
	.CouponApplied {
		padding-top: rem(12px);
		padding-left: 6px;
		color: var(--textPrimary);
		font-size: rem(12px);
		letter-spacing: 1px;
		margin: 0;
		li {
			display: flex;
			align-items: center;
			svg {
				width: 12px;
				height: 12px;
			}
			span {
				color: #00966d;
				&.icon {
					cursor: pointer;
					&:hover {
						opacity: 0.7;
					}
				}
			}
			p {
				color: var(--textPrimary);
				font-size: rem(12px);
				line-height: 1;
				margin: 0 7px;
			}
		}
	}
	@media screen and (max-width:1199px) and (min-width:992px){
		&__body{
			padding-left:rem(8px);
			padding-right:rem(8px);
		}
	}
	@media screen and (max-width:991px){
		border:0;
		border-radius: 0;
		max-width:400px;
		margin:auto;
		margin-top:rem(20px);
		&__head{
			background: transparent;
			padding:rem(16px) 0;
		}
		&__body{
			padding-left:0;
			padding-right:0;
		}
	}
}
</style>
