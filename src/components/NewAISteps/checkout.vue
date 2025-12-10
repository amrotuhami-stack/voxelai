<template>
	<div class="checkOut">
		<div class="d-flex">
			<div class="checkOut__left">
					<billing-address :countries="listOfcountries" :validation="changeFormValidation"></billing-address>
					<shipping-address :countries="listOfcountries" :validation="changeFormValidation"></shipping-address>
					<div class="inline-btns-wrapper" v-if="userProfile">
						<button @click="performCheckout" v-if="!userProfileChanged" :class="`${isFormValid ?  'btn btn-primary' : 'btn btn-primary disabled'}`">Checkout</button>
						<button @click="saveAddress" v-if="userProfileChanged" 	class="btn btn-primary">Save Address</button>
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
import BillingAddress from '@/components/accountSettings/BillingAddress.vue';
import ShippingAddress from '@/components/accountSettings/ShippingAddress.vue';
import CheckoutSummary from '@/components/checkOut/CheckoutSummary.vue';
import CheckoutDetails from '@/components/checkOut/CheckoutDetails.vue';


// [*] Vuex State Getter And Action Helper
import { CheckoutHelper } from '@/common/crud-helpers/checkout';
import { UsersHelper } from '@/common/crud-helpers/users';
import { mapGetters } from 'vuex';

export default {
	components: {
		BillingAddress,
		ShippingAddress,
		CheckoutSummary,
		CheckoutDetails,
	},

	data() {
		return {
			listOfcountries: [],
			isFormValid: true,
		};
	},
	computed: {
		...mapGetters(['userProfile', 'userProfileChanged', 'countries', 'cartLines', 'shippingAddress']),
    },
	mounted() {
		UsersHelper.getUserProfile()
		CheckoutHelper.getCountries({});
	},
	watch: {
		countries(){
			this.listOfcountries = this.countries.map(country => ({
				value: country.iso_3166_1_a2,
				text: country.printable_name,
			}));
		},
	},
	methods: {
		saveAddress(){
			return UsersHelper.saveUserProfile()
		},
		performCheckout() {
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
			shippingAddress = billingAddress;
			CheckoutHelper.getShippingMethods({
				shipping: shippingAddress,
				billing: billingAddress,
			})
		},
		changeFormValidation: function(value) {
			this.isFormValid = value
		}
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

