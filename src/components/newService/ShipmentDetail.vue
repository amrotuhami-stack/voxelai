<template>
	<div class="card">
		<div class="card__head">
			Order
			<span>{{'#' + service.order_line_obj.id}}</span>Shipping Details
			<router-link
				:to="{
					name: 'Account Settings',
					params: {
						lang: $i18n.locale,
					},
				}"
			>
				<button>Edit</button>
			</router-link>
		</div>
		<div class="card__body">
			<div class="row">
				<div class="col-md-7 col-sm-6">
					<h4>Shipping Address</h4>
					<p v-if="!differentShippingAddress">
						{{userProfile.name}}<br />
						<span style="font-weight: 500;">Same as Billing Address.</span>
					</p>
					<p v-else>
						{{userProfile.name}}<br />
						{{shipping.billing_country + ', ' +  shipping.billing_city + ', '}}<br />
						{{shipping.billing_zip + ', '}}<br />
						{{shipping.billing_address}}
					</p>
				</div>
				<div class="col-md-5 col-sm-6">
					<h4>Billing Address</h4>
					<p>
						{{userProfile.name}}<br />
						{{billing.billing_country + ', ' +  billing.billing_city + ', '}}<br />
						{{billing.billing_zip + ', '}}<br />
						{{billing.billing_address}}
					</p>
				</div>
			</div>
			<div class="row">
				<div class="col-md-7 col-sm-6">
					<h4>Track Your Shipment</h4>
					<p>
						<a :href="'https://'+ service.order_line_obj.shipping_event_quantities[0].event.notes" target="_blank" class="contact">
							{{ service.order_line_obj.shipping_event_quantities[0].event.notes }}
						</a>
					</p>
				</div>
			</div>
			<h4>Contact Information</h4>
			<div class="row">
				<div class="col-md-7 col-sm-6">
					<p>
						E-mail:<br />
						<a :href="'mailto:' + userProfile.email" class="contact">
							{{userProfile.email}}
						</a>
					</p>
				</div>
				<div class="col-md-5 col-sm-6">
					<p>
						Phone number:
						<br />
						<a :href="'tel:' + userProfile.phone_number" class="contact">
							{{userProfile.phone_number}}
						</a>
					</p>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
// [*] Import vue Components
import { mapGetters } from 'vuex';
import { UsersHelper } from '@/common/crud-helpers/users'
import service from '../../store/modules/service';

export default {
	props: {
		service: Object
	},
	components: {
	},
	data() {
		return {
			billing: {},
			shipping: {},
			differentShippingAddress: true,
		}
	},
    created() {
		UsersHelper.getUserProfile()
    },
	computed: {
		...mapGetters(['userProfile']),
	},
	watch: {
		userProfile() {
			this.billing = {
				billing_first_name: this.userProfile.billing_first_name,
    			billing_last_name: this.userProfile.billing_last_name,
    			billing_email: this.userProfile.billing_email,
    			billing_phone_number: this.userProfile.billing_phone_number,
    			billing_country: this.userProfile.billing_country,
    			billing_city: this.userProfile.billing_city,
    			billing_address: this.userProfile.billing_address,
    			billing_zip: this.userProfile.billing_zip,
			}
			if(this.userProfile.shipping_country == null || this.userProfile.shipping_city == null || this.userProfile.shipping_address == null) {
				this.shipping = {...this.billing}
				this.differentShippingAddress = false
			}
			else {
				this.shipping = {
					shipping_first_name: this.userProfile.shipping_first_name,
    				shipping_last_name: this.userProfile.shipping_last_name,
    				shipping_email: this.userProfile.shipping_email,
    				shipping_phone_number: this.userProfile.shipping_phone_number,
    				shipping_country: this.userProfile.shipping_country,
    				shipping_city: this.userProfile.shipping_city,
    				shipping_address: this.userProfile.shipping_address,
    				shipping_zip: this.userProfile.shipping_zip,
				}
			}
		}
	},
	methods: {
	},
};
</script>

<style lang="scss" scoped>
.card {
	&__head {
		button {
			float: right;
			background: transparent;
			color: var(--secondary);
			font-size: rem(14px);
			border: 0;
			outline: 0;
			font-weight: 500;
			&:hover {
				opacity: 0.8;
			}
		}
	}
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
