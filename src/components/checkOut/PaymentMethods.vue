<template>
	<div>
		<b-tabs content-class="mt-3" justified nav-class="tabHeader" >
			<b-tab title="Card Payment ( powered by Stripe)" active title-link-class="title" >
				<stripe-payment />
			</b-tab>
			<!-- <b-tab title="PayPal" title-link-class="title" >
				<pay-pal />
			</b-tab> -->
			<b-tab title="Direct Bank Transfer" title-link-class="title">
				<direct-transfer />
			</b-tab>
		</b-tabs>
	</div>
</template>

<script>

import PayPal from '@/components/checkOut/partials/PayPal.vue';
import DirectTransfer from '@/components/checkOut/partials/DirectTransfer.vue';
import StripePayment from '@/components/checkOut/StripePayment.vue';


export default {
	components: {
		PayPal,
		StripePayment,
		DirectTransfer
	},
	data() {
		return {
		};
	},
};
</script>

<style lang="scss" >
	.tabHeader {
		height: rem(70px) !important;
		li {
			height: 100% !important;
		}
	}
	.title{
		padding: 0px !important;
		min-height: 100% !important;
		text-transform: capitalize !important;
        font-size: rem(16px) !important;
        color: var(--default) !important;
        font-weight: 400 !important;
		a{
			height: min-content !important;
		}
	}
</style>
