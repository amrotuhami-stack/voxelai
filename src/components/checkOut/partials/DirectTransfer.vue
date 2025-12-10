<template>
	<div class="card__body">
		<div class="row">
			<div class="col-6">
				<h4>Recipient</h4>
				<p>
					VOXEL3DI LTD<br />
				</p>
			</div>
			<div class="col-6">
				<h4>Recipient address</h4>
				<p>
					20-22 Wenlock Road, N1 7GU, London, United Kingdom
				</p>
			</div>
		</div>
		<div class="row">
			<div class="col-12">
				<h4>Transfer from a UK bank</h4>
			</div>
			<hr />
		</div>
		<div class="row">
			<div class="col-6">
				<h4>Account number</h4>
				<p>
					76511049<br />
				</p>
			</div>
			<div class="col-6">
				<h4>Sort code</h4>
				<p>
					Sort code
				</p>
			</div>
		</div>
		<div class="row">
			<div class="col-12">
				<h4>Transfer from outside the UK</h4>
			</div>
			<hr />
		</div>
		<div class="row">
			<div class="col-6">
				<h4>IBAN</h4>
				<p>
					GB49 REVO 0099 6907 2266 48<br />
				</p>
			</div>
			<div class="col-6">
				<h4>BIC</h4>
				<p>
					REVOGB21
				</p>
			</div>
			<div class="col-6">
				<h4>Intermediary BIC</h4>
				<p>
					CHASGB2L
				</p>
			</div>
		</div>
		<div class="row">
			<hr />
			<div class="col-6">
				<h4>Bank Name</h4>
				<p>
					Revolut Ltd  <br />
				</p>
			</div>
			<div class="col-6">
				<h4>Bank Address</h4>
				<p>
					7 Westferry Circus, E14 4HD, London, United Kingdom<br />
				</p>
			</div>
			<div class="col-12 mt-3">
				<button @click.prevent="() => placeOrder()" class="btn btn-primary payment_button w-100">
					<span id="button-text">Confirm Payment</span>
				</button>
			</div>
		</div>
	</div>
</template>

<script>
// [*] Vuex State Getter And Action Helper
import { CheckoutHelper } from '@/common/crud-helpers/checkout';
import { mapGetters } from 'vuex';

export default {
    data() {
        return {
            shippingMethod: null,
			basket_total: null,
        }
    },
	computed: {
		...mapGetters(['userProfile', 'cart', 'shippingAddress', 'billingAddress', 'shippingMethods', 'serviceDetail', 'digitalOrderData']),
    },
    mounted() {
		if (!this.shippingAddress ||  !this.billingAddress || this.shippingMethods.length < 1)
			this.$router.push({"name": "CheckOut"})
		else {
			if ( this.userProfile && this.cart ) {
				this.basket_total = this.cart.total_excl_tax;
				if(this.shippingMethods && this.shippingMethods.length > 0) {
					this.shippingMethod = this.shippingMethods[0];
					this.basket_total = Number(this.cart.total_excl_tax) + Number(this.shippingMethods[0].total_tax_of_products) + Number(this.shippingMethods[0].price.incl_tax);
				};
			}
		}
	},
	watch: {
		cart() {
			if ( this.userProfile && this.cart ) {
				this.basket_total = this.cart.total_excl_tax;
				if(this.shippingMethods && this.shippingMethods.length > 0) {
					this.shippingMethod = this.shippingMethods[0];
					this.basket_total = Number(this.cart.total_excl_tax) + Number(this.shippingMethods[0].total_tax_of_products) + Number(this.shippingMethods[0].price.incl_tax);
				};
			}
		},
	},
	methods: {
		async placeOrder(){
			let vueApp = this
			var data = {
				"basket": this.userProfile.basket.url,
				"guest_email": this.userProfile.email,
				"total": this.basket_total,
				"shipping_method_code": this.shippingMethod.code,
				"shipping_charge": this.shippingMethod.price,
				"shipping_address": this.shippingAddress,
				"billing_address": this.billingAddress,
				"paymentIntentId": "",
				"paymentMethod": "bank_transfer",
			};
			await CheckoutHelper.placeOrder(data).then(() => {
				vueApp.$router.push({"name": "Checkout Payment"})
			})
		}
	}
};
</script>

<style lang="scss" scoped>
	.card {
		&__body {
			h4 {
				font-size: rem(14px);
				color: var(--default) !important;
				font-weight: 500;
				margin-bottom: rem(8px);
			}
			p {
				color: var(--textSecondary) !important;
				font-size: rem(14px) !important;
				.contact {
					color: var(--primary);
					font-weight: 400;
				}
			}
		}
	}

</style>
