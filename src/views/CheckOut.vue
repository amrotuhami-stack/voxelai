<template>
	<div class="checkOut">
		<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
		<h1 class="main-title">Shoping Cart - Checkout</h1>
		<div class="d-flex">
			<div class="checkOut__left">
					<billing-address :countries="listOfcountries" :validation="billingShippingFormValidationChange"></billing-address>
					<shipping-address :countries="listOfcountries" :validation="billingShippingFormValidationChange"></shipping-address>
					<div class="inline-btns-wrapper stack-on-sm" v-if="userProfile">
						<button @click="checkout" v-if="!userProfileChanged" :class="`${billingShippingAddressFormValid ?  'btn btn-primary' : 'btn btn-primary disabled'}`">
							Checkout
						</button>
						<button @click="saveUserProfileChanges" v-if="userProfileChanged" :class="`${billingShippingAddressFormValid ?  'btn btn-primary' : 'btn btn-primary disabled'}`">
							Save Address
						</button>
						<router-link class="btn btn-secondary grey" :to="{ name: 'shopping-cart', params: { lang: $i18n.locale }}">
							Back to Cart
						</router-link>
					</div>
			</div>
			<div class="checkOut__right">
				<checkout-summary />
				<checkout-details class="mt-4" />
			</div>
		</div>
	</div>
</template>
<script>
// [*] Import UI Components
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import PersonalInfo from '@/components/accountSettings/PersonalInfo.vue';
import BillingAddress from '@/components/accountSettings/BillingAddress.vue';
import ShippingAddress from '@/components/accountSettings/ShippingAddress.vue';
import CheckoutSummary from '@/components/checkOut/CheckoutSummary.vue';
import CheckoutDetails from '@/components/checkOut/CheckoutDetails.vue';

// [*] Import Breadcrumbs
import { checkoutBreadCrumbs } from "@/common/constant/breadCrumbs"
import { EMPTY_CART_SCREEN } from "@/router/index"

// [*] Vuex State Getter And Action Helper
import { CheckoutHelper } from '@/common/crud-helpers/checkout';
import { BasketHelper } from '@/common/crud-helpers/basket'
import { UsersHelper } from '@/common/crud-helpers/users';
import { mapGetters } from 'vuex';

export default {
	components: {
		BaseBreadCrumb,
		PersonalInfo,
		BillingAddress,
		ShippingAddress,
		CheckoutSummary,
		CheckoutDetails,
	},

	data() {
		return {
			breadCrumbsItems: [...checkoutBreadCrumbs],
			listOfcountries: [],
			billingShippingAddressFormValid: true,
		};
	},
	mounted() {
		
		UsersHelper.getUserProfile()
		CheckoutHelper.getCountries({});
	},
	created() {
		
	},
	computed: {
		...mapGetters(['userProfile', 'cart', 'userProfileChanged', 'countries', 'cartLines', 'shippingAddress', 'billingAddress', 'shippingMethods']),
    },
	watch: {
		countries(){
			this.listOfcountries = this.countries.map(country => ({
				value: country.iso_3166_1_a2,
				text: country.printable_name,
			}));
		},
		cartLines(){
			if ( this.cartLines.length == 0 ){
				this.$router.push({"name": EMPTY_CART_SCREEN });
			};
		},
		shippingAddress() {
			if ( this.shippingAddress ) {
				if(this.cart.total_incl_tax > 0) {
					return this.$router.push({ name:"PlaceOrder"});
				}
				// When apply 100% Promo Code
				var data = {
					"basket": this.userProfile.basket.url,
					"guest_email": this.userProfile.email,
					"total": this.basket_total = Number(this.cart.total_excl_tax) + Number(this.shippingMethods[0].total_tax_of_products) + Number(this.shippingMethods[0].price.incl_tax),
					"shipping_method_code": this.shippingMethods[0].code,
					"shipping_charge": this.shippingMethods[0].price,
					"shipping_address": this.shippingAddress,
					"billing_address": this.billingAddress,
					"paymentIntentId": "",
					"paymentMethod": "",
				};
				let vueApp = this;
				CheckoutHelper.placeOrder(data).then(function(){
					BasketHelper.getCart()
					vueApp.loading = false
					vueApp.$router.push({"name": "Checkout Payment"})
				})
			}
		}
	},
	methods: {
		/// Update Validation Flag of Billing and Shipping Address Form.
		///
		/// This Function Triger by chilldren components.
		billingShippingFormValidationChange(value) {
			this.billingShippingAddressFormValid = value
		},

		/// Save Billing and Shipping Adress of User Profile
		saveUserProfileChanges() {
			if(!this.billingShippingAddressFormValid) return;
			return UsersHelper.saveUserProfile();
		},

		/// Apply Checkout to get shipping data and calcute VAT.
		///
		/// Need to replace country code with country url.
		checkout() {
			let billingCountry = this.countries.filter(
				c => c.iso_3166_1_a2 === this.userProfile.billing_country
			)[0]
			let billingAddress = {
            	"first_name": this.userProfile.billing_first_name,
            	"last_name": this.userProfile.billing_last_name,
            	"email": this.userProfile.billing_email,
            	"phone": this.userProfile.billing_phone_number,
            	"country": billingCountry ? billingCountry.url : '',
            	"city": this.userProfile.billing_city,
            	"line1": this.userProfile.billing_address,
            	"zip": this.userProfile.billing_zip,
        	};
			let shippingCountry = this.countries.filter(
				c => c.iso_3166_1_a2 === this.userProfile.shipping_country
			)[0]
			let shippingAddress = {
        		"first_name": this.userProfile.shipping_first_name,
        		"last_name": this.userProfile.shipping_last_name,
        		"email": this.userProfile.shipping_email,
        		"phone": this.userProfile.shipping_phone_number,
        		"country": shippingCountry ? shippingCountry.url : '',
        		"city": this.userProfile.shipping_city,
        		"line1": this.userProfile.shipping_address,
        		"zip": this.userProfile.shipping_zip,
      		};
			// 	When Shipping Address not set use Billing Address instade.
			if(!this.userProfile.differentShippingAddress) {
				shippingAddress = billingAddress;
			}
			CheckoutHelper.getShippingMethods({
				shipping: shippingAddress,
				billing: billingAddress,
			})
		},
	}
};
</script>

<style lang="scss">
.checkOut {
	&__right {
		flex: 0 0 350px;
		max-width: 350px;
		margin-left: rem(24px);
		@media screen and (max-width: 1600px) {
			flex: 0 0 300px;
			max-width: 300px;
		}
		@media screen and (max-width: 991px) {
			margin-left: 0;
			margin-bottom: 25px;
			flex: 0 0 100%;
			max-width: 100%;
		}
		::v-deep .card {
			@media screen and (max-width: 991px) {
				padding: 0;
				border: 0;
				border-radius: 0;
				padding-bottom: 20px;
				.card__head {
					background: transparent;
					padding: 0;
					border: 0;
					border-radius: 0;
					margin-bottom: 12px;
				}
				.card__body {
					padding: 0;
				}
			}
		}
	}
	h1 {
		margin-bottom: rem(34px);
	}
	h2 {
		font-size: rem(16px);
		font-weight: 400;
		color: var(--default);
		margin-bottom: rem(16px);
	}
	.contentBox {
		margin-bottom: rem(24px);
		@media screen and (max-width: 991px) {
			border: 0;
			padding: 0;
		}
		.card {
			margin-bottom: rem(32px);
			@media screen and (max-width: 991px) {
				border: 0;
				padding: 0;
				.card__body {
					border: 0;
					padding: 0;
				}
			}
		}
		.textWrapper {
			display: flex;
			align-items: center;
			justify-content: space-between;
			@media screen and (max-width: 991px) {
				flex-direction: column;
				align-items: center;
				text-align: center;
			}
			p {
				font-size: rem(12px);
				font-weight: 400;
				letter-spacing: 1px;
				a {
					font-weight: 500;
					color: var(--primary);
					padding-right: 10px;
					&:hover {
						color: var(--secondary);
					}
				}
				svg {
					width: 24px;
					height: 24px;
					margin-right: rem(8px);
				}
				&:not(:last-child) {
					@media screen and (max-width: 991px) {
						margin-bottom: 10px;
					}
				}
				&:last-child {
					text-align: right;
				}
			}
		}
	}
	.inline-btns-wrapper {
		a {
			padding-right: rem(75px);
			padding-left: rem(75px);
		}
		.back-btn {
			padding-left: rem(0px);
		}
		p {
			margin-bottom: 0;
			text-align: right;
			span {
				color: #000000;
				font-weight: 500;
			}
		}
	}
	.checkbox {
		padding-top: rem(5px) !important;
		span {
			padding-left: rem(32px) !important;
		}
	}
	&__proceed {
		display: flex;
		align-items: center;
		justify-content: space-between;
		.btn {
			padding-right: rem(75px);
			padding-left: rem(75px);
		}
		p {
			color: var(--default);
			span {
				font-weight: 500;
				color: #000;
			}
		}
	}
	@media screen and (max-width: 991px) {
		.d-flex {
			flex-direction: column-reverse;
		}
		::v-deep.card {
			&__body {
				padding-left: 0;
				padding-right: 0;
			}
		}
	}
}
</style>

