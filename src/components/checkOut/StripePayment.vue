<template>
    <form id="payment-form" >
		<div id="card-element"><!--Stripe.js injects the Card Element--></div>
		<button id="submit" class="btn btn-primary payment_button" :disabled="disable_payment_btn || loading || success">
			<font-awesome-icon id="spinner" class="spinner hidden" icon="spinner" size="2x" spin />
			<span id="button-text">Pay now</span>
		</button>
		<p id="card-error" role="alert" v-if="error.value">{{error.messege}}</p>
		<p class="result-message" v-if="success">
			Payment succeeded, see the result in your <a href="" target="_blank">dashboard.</a>
		</p>
	</form>
</template>

<script>
// [*] Import Stripe Constant
import stripeDataConstant from "@/common/constant/stripe"

// [*] Import Stripe API Key
import {stripeApiKey} from '@/conf.js'

// [*] Vuex State Getter And Action Helper
import { ApiService } from '@/common/api_services'
import { CheckoutHelper } from '@/common/crud-helpers/checkout';
import { BasketHelper } from '@/common/crud-helpers/basket'
import { mapGetters } from 'vuex';

export default {
    data() {
        return {
            shippingMethod: null,
			basket_total: null,
			// Falgs
			disable_payment_btn: false,
			loading: false,
			success: false,
			error: {value: false, messege: ""},
        }
    },
	computed: {
		...mapGetters(['userProfile', 'countries', 'cart', 'shippingAddress', 'billingAddress', 'shippingMethods', 'cartLines', 'workingOnService']),
    },
    mounted() {
		if (!this.shippingAddress ||  !this.billingAddress || this.shippingMethods.length < 1)
			this.$router.push({"name": "CheckOut"})
		else {
			let vueApp = this;

			if ( this.userProfile && this.cart ) {
				this.basket_total = this.cart.total_excl_tax;
				if(this.shippingMethods && this.shippingMethods.length > 0) {
					this.shippingMethod = this.shippingMethods[0];
					this.basket_total = Number(this.cart.total_excl_tax) + Number(this.shippingMethods[0].total_tax_of_products) + Number(this.shippingMethods[0].price.incl_tax);
				};
			}

			// The items the customer wants to buy
			// [Note] When Send shipping address replace country url with country code.
			let updatedShippingAddress = this.shippingAddress

			// if(!this.userProfile.differentShippingAddress) {
			// 	updatedShippingAddress = this.billingAddress;
			// }
			// let shippingCountry = this.countries.filter(
			// 	c => c.iso_3166_1_a2 === vueApp.userProfile.shipping_country
			// )[0]
			// updatedShippingAddress.country = shippingCountry.url
			var purchase = { target: "pay_basket",  shippingAddress: updatedShippingAddress};
			ApiService.post('/create-payment-intent/', purchase)
			.then(function(result) {
				return result.data;
			})
			.then(function(data) {
				let API_KEY = stripeApiKey()
				var stripe = Stripe(API_KEY);
				var elements = stripe.elements();

				var card = elements.create("card", { style: stripeDataConstant.style, hidePostalCode: true });

				// Stripe injects an iframe into the DOM
				card.mount("#card-element");
				card.on("change", function (event) {
					// Disable the Pay button if there are no card details in the Element
					vueApp.disable_payment_btn = false;
					event.error ? vueApp.error = {value: true, messege: event.error.message} : "";
				});
				var form = document.getElementById("payment-form");
				form.addEventListener("submit", function(event) {
					event.preventDefault();
					// Complete payment when the submit button is clicked
					vueApp.payWithCard(stripe, card, data.clientSecret, vueApp);
				});
			});
		}
	},
	watch: {
		cartLines(){
			if ( this.cartLines.length == 0 ){
				this.$router.push({"name": "empty-shopping-cart"});
			};
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
	methods: {
		// Calls stripe.confirmCardPayment
		// If the card requires authentication Stripe shows a pop-up modal to
		// prompt the user to enter authentication details without leaving your page.
		payWithCard(stripe, card, clientSecret, vueApp) {
			vueApp.loading = true;
			stripe.confirmCardPayment(clientSecret, { payment_method: { card: card}, })
			.then(function(result) {
				if (result.error) {
					vueApp.loading = false
					vueApp.error = {value: true, messege: result.error.message}
				} else {
					vueApp.disable_payment_btn = true
					vueApp.success = true
					vueApp.placeOrder(result.paymentIntent.id, vueApp);
				}
			});
		},
		placeOrder(paymentIntentId, vueApp){
			var data = {
				"basket": this.userProfile.basket.url,
				"guest_email": this.userProfile.email,
				"total": this.basket_total,
				"shipping_method_code": this.shippingMethod.code,
				"shipping_charge": this.shippingMethod.price,
				"shipping_address": this.shippingAddress,
				"billing_address": this.billingAddress,
				"paymentIntentId": paymentIntentId,
				"paymentMethod": "stripe",
			};
			CheckoutHelper.placeOrder(data).then(function(){
				BasketHelper.getCart()
				vueApp.loading = false
				vueApp.$router.push({"name": "Checkout Payment"})
			})
		}
	}
};
</script>
<style lang="scss" scoped>
#payment-form {
	padding: rem(40px);
}
.payment_button{
	margin-top: rem(50px) !important;
}

.hidden {
	display: none;
}
</style>