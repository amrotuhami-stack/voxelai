<template>
	<div class="checkOut">
		<div class="d-flex">
			<div class="checkOut__left">
				<div class="contentBox">
					<h3>Pay with</h3>
					<div class="card">
						<payment-methods />
					</div>
					<div class="textWrapper">
						<p> By completing your purchase you agree to these <a href="#">Terms of Service</a>.</p>
						<p>
							<svg-icon icon-id="lock-icon" icon-viewbox="0 0 24 24"></svg-icon>
							Secure Connection
						</p>
					</div>
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
// [*] Import UI Components .
import CheckoutSummary from '@/components/checkOut/CheckoutSummary.vue';
import CheckoutDetails from '@/components/checkOut/CheckoutDetails.vue';
import PaymentMethods from '@/components/checkOut/PaymentMethods.vue';


export default {
	components: {
		CheckoutSummary,
		CheckoutDetails,
		PaymentMethods
	},

	data() {
		return {
		};
	},
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
	h3 {
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
