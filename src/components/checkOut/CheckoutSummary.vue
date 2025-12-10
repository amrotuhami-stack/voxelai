<template>
	<div class="totalSummary">
		<div class="card" v-if="cart && userProfile">
			<div class="card__head">Summary</div>
			<div class="card__body">
				<div class="totalSummary__item" v-if="shippingMethod">
					<p>Shipping: </p>
					<p>
						<money-format :value="Number(shippingMethod.price.excl_tax)"
							:locale='`en`'
							:currency-code='userProfile.default_currency'
							:subunits-value=false
							:hide-subunits=false>
						</money-format>
					</p>
				</div>
				<div class="totalSummary__item divider" v-if="shippingMethod">
					<p>Shipping incl. VAT:</p>
					<p>
						<money-format :value="Number(shippingMethod.price.incl_tax)"
							:locale='`en`'
							:currency-code='userProfile.default_currency'
							:subunits-value=false
							:hide-subunits=false>
						</money-format>
					</p>
				</div>
				<div class="totalSummary__item" v-if="shippingMethod">
					<p>Total exc. VAT:</p>
					<p>
						<money-format :value="Number(cart.total_excl_tax)"
							:locale='`en`'
							:currency-code='userProfile.default_currency'
							:subunits-value=false
							:hide-subunits=false>
						</money-format>
					</p>
				</div>
				<div class="totalSummary__item" v-if="shippingMethod">
					<p>VAT:</p>
					<p>
						<money-format :value="Number(shippingMethod.total_tax_of_products)"
							:locale='`en`'
							:currency-code='userProfile.default_currency'
							:subunits-value=false
							:hide-subunits=false>
						</money-format>
					</p>
				</div>
				<div class="totalSummary__item divider" v-if="shippingMethod">
					<p>Total inc. VAT:</p>
					<p>
						<money-format :value="Number(cart.total_excl_tax) + Number(shippingMethod.total_tax_of_products)"
							:locale='`en`'
							:currency-code='userProfile.default_currency' 
							:subunits-value=false
							:hide-subunits=false>
						</money-format>
					</p>
				</div>
				<div class="totalSummary__item--total">
					<p>Total:</p>
					<div class="total__price">
						<money-format :value="Number(basket_total)"
							:locale='`en`'
							:currency-code='userProfile.default_currency'
							:subunits-value=false
							:hide-subunits=false>
						</money-format>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { mapGetters } from 'vuex';


import MoneyFormat from 'vue-money-format';

export default {
	data(){
		return {
			basket_total: null,
			shippingMethod: null,
		}
	},
	components: {
		MoneyFormat,
	},
	computed: {
		...mapGetters(['userProfile', 'cart', 'shippingMethods', 'selectedAiPricePlan']),
    },
	mounted(){
		if ( this.userProfile && this.cart ) {
			this.basket_total = this.cart.total_excl_tax;
			if(this.shippingMethods && this.shippingMethods.length > 0) {
				this.shippingMethod = this.shippingMethods[0];
				this.basket_total = Number(this.cart.total_excl_tax) + Number(this.shippingMethods[0].total_tax_of_products) + Number(this.shippingMethods[0].price.incl_tax);
			};
		}
	},
	watch:{
		shippingMethods(){
			if ( this.userProfile && this.cart ) {
				this.basket_total = this.cart.total_excl_tax;
				if(this.shippingMethods && this.shippingMethods.length > 0) {
					this.shippingMethod = this.shippingMethods[0];
					this.basket_total = Number(this.cart.total_excl_tax) + Number(this.shippingMethods[0].total_tax_of_products) + Number(this.shippingMethods[0].price.incl_tax);
				};
			}
		},
		cart() {
			if ( this.userProfile && this.cart ) {
				this.basket_total = this.cart.total_excl_tax;
				if(this.shippingMethods && this.shippingMethods.length > 0) {
					this.shippingMethod = this.shippingMethods[0];
					this.basket_total = Number(this.cart.total_excl_tax) + Number(this.shippingMethods[0].total_tax_of_products) + Number(this.shippingMethods[0].price.incl_tax);
				};
			}
		}
	},
};
</script>

<style lang="scss" scoped>
.totalSummary {
	.card__head {
		padding: rem(27px) rem(24px);
	}

	.divider {
		border-bottom: 1px solid var(--borderColor);
		margin-bottom: rem(12px);
	}

	.totalSummary__item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		p:nth-child(2) {
			color: #000 !important;
			font-size: rem(20px) !important;
			@media screen and (max-width:1199px) and (min-width:992px){
				font-size:rem(18px) !important;
			}
		}
		p {
			font-size: rem(14px);
			color: var(--textSecondary);
			margin-bottom: rem(16px);
			padding-right:5px;
		}
		&--total {
			display: flex;
			align-items: center;
			justify-content: space-between;
			padding-top: rem(4px);
			p {
				font-weight: 500;
				font-size: rem(20px);
				color: #171716;
				margin-bottom: 0;
				@media screen and (max-width:1025px) and (min-width:992px){
					font-size:rem(18px);
				}
			}
			.total__price {
				font-size: rem(24px);
				color: #171716;
				font-weight: 500;
				@media screen and (max-width:1025px) and (min-width:992px){
					font-size:rem(20px);
				}
			}
		}
	}
	
}
</style>
