<template>
	<div>
		<div class="topHead">
			<div>
				<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
				<h1 class="main-title">Checkout</h1>
			</div>
			<activity-card :data="activity.wallet" color="green" />
		</div>
		<div class="checkout">
			<div class="d-flex">
				<div class="checkout__left">
					<div class="contentBox">
						<h3>Order Information</h3>
						<div class="card mb-4">
							<div
								class="card__body grid"
								data-grid-item-width="1/5"
							>
								<div class="item">
									<p>Mohamed Ahmed</p>
									<span>Doctor Name</span>
								</div>
								<div class="item">
									<p>65432365</p>
									<span>Order ID</span>
								</div>
								<div class="item">
									<p>09/12/2020</p>
									<span>Ordered date</span>
								</div>
								<div class="item">
									<p>$1,295.00</p>
									<span>Order Amount</span>
								</div>
								<div class="item">
									<p>$50.00</p>
									<span>Commission</span>
								</div>
							</div>
						</div>
						<h3>Choose payment method</h3>

						<!-- accordian -->

						<div class="accordion" role="tablist">
							<b-card no-body>
								<b-card-header header-tag="header" role="tab">
									<b-button
										block
										v-b-toggle.my-wallet
										variant="info"
									>
										<span></span>
										My Wallet</b-button
									>
								</b-card-header>
								<b-collapse
									id="my-wallet"
									visible
									accordion="my-accordion "
									role="tabpanel"
									v-model="collapseStates[0]"
								>
									<b-card-body>
										<div class="contentBox">
											<div class="card">
												<div class="card__body items">
													<div class="item">
														<p class="sucess">
															$2,275.00
														</p>
														<span
															>Current
															Balance</span
														>
													</div>
													<div class="item">
														<p>$1,295.00</p>
														<span
															>Order Amount</span
														>
													</div>
													<div class="item">
														<p>$980.00</p>
														<span>Remaining</span>
													</div>
												</div>
											</div>
											<a
												href="javascript:void(0);"
												class="btn btn-primary"
												v-on:click.stop.prevent="
													openStep(1)
												"
												>Complete Payment</a
											>
										</div>
									</b-card-body>
								</b-collapse>
							</b-card>
							<b-card no-body>
								<b-card-header header-tag="header" role="tab">
									<b-button
										block
										v-b-toggle.payment-method
										variant="info"
									>
										<span></span>
										Credit / Debit Cards</b-button
									>
								</b-card-header>
								<b-collapse
									id="payment-method"
									invisible
									accordion="my-accordion "
									role="tabpanel"
									v-model="collapseStates[1]"
								>
									<b-card-body>
										<div class="contentBox">
											<div class="card">
												<credit-card />
											</div>
											<div class="textWrapper">
												<p>
													By completing your purchase
													you agree to these
													<a href="#"
														>Terms of Service</a
													>.
												</p>
												<p>
													<svg-icon
														icon-id="lock-icon"
														icon-viewbox="0 0 24 24"
													></svg-icon
													>Secure Connection
												</p>
											</div>
											<div class="inline-btns-wrapper">
												<a
													href="#"
													class="btn btn-primary"
													>Complete Payment</a
												>
												<p>
													Your card will be
													charged<span>
														$1,295.00</span
													>
												</p>
											</div>
										</div>
									</b-card-body>
								</b-collapse>
							</b-card>
							<b-card no-body>
								<b-card-header header-tag="header" role="tab">
									<b-button
										block
										v-b-toggle.paypal
										variant="info"
									>
										<span></span>
										PayPal</b-button
									>
								</b-card-header>
								<b-collapse
									id="paypal"
									invisible
									accordion="my-accordion "
									role="tabpanel"
								>
									<b-card-body>
										<div class="contentBox">
											<div class="card">
												<pay-pal />
											</div>
											<div class="textWrapper">
												<p>
													By completing your purchase
													you agree to these
													<a href="#"
														>Terms of Service</a
													>.
												</p>
												<p>
													<svg-icon
														icon-id="lock-icon"
														icon-viewbox="0 0 24 24"
													></svg-icon
													>Secure Connection
												</p>
											</div>
											<div class="inline-btns-wrapper">
												<a
													href="#"
													class="btn btn-primary"
													>Complete Payment</a
												>
												<p>
													Your card will be
													charged<span>
														$1,295.00</span
													>
												</p>
											</div>
										</div>
									</b-card-body>
								</b-collapse>
							</b-card>
							<b-card no-body>
								<b-card-header header-tag="header" role="tab">
									<b-button
										block
										v-b-toggle.direct-transfer
										variant="info"
									>
										<span></span>
										Direct Bank Transfer</b-button
									>
								</b-card-header>
								<b-collapse
									id="direct-transfer"
									invisible
									accordion="my-accordion "
									role="tabpanel"
								>
									<b-card-body>
										<div class="contentBox">
											<div class="card">
												<div class="card__body">
													<p>
														Make your payment
														directly into our bank
														account.
													</p>
													<form>
														<div class="row">
															<div
																class="col-md-6"
															>
																<div
																	class="
																		form-group
																		link
																	"
																>
																	<input
																		type="text"
																		class="
																			form-control
																		"
																		required=""
																		name="IBAN"
																		id="copy-link"
																		placeholder="IBAN"
																		value="KW81CBKU0000000000001234560101"
																	/>
																	<span
																		@click="
																			copyLink
																		"
																	>
																		<svg-icon
																			icon-id="copy-icon"
																			icon-viewbox="0 0 24 24"
																		></svg-icon>
																	</span>
																	<label
																		class="
																			control-label
																		"
																		>IBAN</label
																	>
																</div>
															</div>
															<div
																class="col-md-6"
															>
																<div
																	class="
																		form-group
																	"
																>
																	<div
																		class="
																			form-group
																		"
																	>
																		<input
																			type="text"
																			class="
																				form-control
																			"
																			required=""
																			name="Sorting Number"
																			placeholder="Sorting Number"
																			value="608371"
																		/>
																		<label
																			class="
																				control-label
																			"
																			>Sorting
																			Number
																		</label>
																	</div>
																</div>
															</div>
															<div
																class="col-md-6"
															>
																<div
																	class="
																		form-group
																	"
																>
																	<input
																		type="text"
																		class="
																			form-control
																		"
																		required=""
																		name="Account Number"
																		placeholder="Account Number"
																		value="100087367234"
																	/>
																	<label
																		class="
																			control-label
																		"
																		>Account
																		Number</label
																	>
																</div>
															</div>
															<div
																class="col-md-6"
															>
																<div
																	class="
																		form-group
																	"
																>
																	<div
																		class="
																			form-group
																		"
																	>
																		<input
																			type="text"
																			class="
																				form-control
																			"
																			required=""
																			name="Bank Name"
																			placeholder="Bank Name"
																			value="Banque Misr - DownTown"
																		/>
																		<label
																			class="
																				control-label
																			"
																			>Bank
																			Name
																		</label>
																	</div>
																</div>
															</div>
														</div>
														<b-alert
															show
															variant="warning"
															><svg-icon
																icon-id="alert-icon"
																icon-viewbox="0 0 24 24"
															></svg-icon>
															<p>
																Please use your
																Order ID as the
																payment
																reference and
																Email us your
																payment advice.
																Your order won't
																be in progress
																until funds have
																cleared in our
																account. Thank
																you!
															</p>
														</b-alert>
													</form>
												</div>
											</div>
											<div class="inline-btns-wrapper">
												<a
													href="#"
													class="btn btn-primary"
													>Complete Payment</a
												>
												<p>
													Your card will be
													charged<span>
														$1,295.00</span
													>
												</p>
											</div>
										</div>
									</b-card-body>
								</b-collapse>
							</b-card>
						</div>
					</div>
				</div>
				<div class="checkout__right">
					<checkout-summary />
					<checkout-details class="mt-4" />
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import ActivityCard from '../../components/distributors/ActivityCard.vue';
import CheckoutSummary from '@/components/checkOut/CheckoutSummary.vue';
import CheckoutDetails from '@/components/checkOut/CheckoutDetails.vue';
import CreditCard from '@/components/checkOut/partials/CreditCard.vue';
import PayPal from '@/components/checkOut/partials/PayPal.vue';

export default {
	components: {
		BaseBreadCrumb,
		ActivityCard,
		CheckoutSummary,
		CheckoutDetails,
		CreditCard,
		PayPal,
	},

	data() {
		return {
			collapseStates: [true, false, false, false, false],
			breadCrumbsItems: [
				{
					text: 'Orders',
					href: '#',
				},
				{
					text: 'Checkout',
					active: true,
				},
			],
			activity: {
				wallet: {
					icon: 'wallet-icon',
					iewBox: '0 0 24 24',
					value: '$275.00',
					label: 'Your Wallet',
					isDropdown: true,
				},
				order: {
					icon: 'documents-icon',
					iewBox: '0 0 24 24',
					value: '15',
					label: 'Number of Orders',
					isDropdown: false,
				},
				amount: {
					icon: 'documents-icon',
					iewBox: '0 0 24 24',
					value: '$4,295.00',
					label: 'Total Amount',
					isDropdown: false,
				},
				Commission: {
					icon: 'discount',
					iewBox: '0 0 24 24',
					value: '$275.00',
					label: 'Commission',
					isDropdown: false,
				},
			},
		};
	},
	methods: {
		copyLink() {
			let copyText = document.getElementById('copy-link');

			copyText.select();
			copyText.setSelectionRange(0, 99999);

			navigator.clipboard.writeText(copyText.value);
		},
		openStep(index) {
			this.collapseStates.splice(index, 1, true);
		},
	},
};
</script>

<style lang="scss" scoped>
.checkout {
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
		@media screen and (max-width: 991px) {
			::v-deep .cartItem__product {
				flex-wrap: nowrap;
			}
		}
	}
	&__left {
		flex: 1;
		h3 {
			font-size: rem(16px);
			font-weight: 400;
			color: var(--default);
			margin-bottom: rem(16px);
		}
		.card {
			&__body {
				@media screen and (max-width: 767px) {
					padding: 16px;
				}
				&.grid {
					grid-template-columns: 1fr 88px 90px 95px 90px;
					grid-gap: 50px;
					@media screen and (max-width: 1300px) {
						grid-gap: 30px;
					}
					@media screen and (max-width: 1205px) {
						grid-template-columns: repeat(3, 1fr);
						grid-gap: 40px;
					}
					@media screen and (max-width: 991px) {
						grid-template-columns: repeat(5, 1fr);
						grid-gap: 40px;
					}
					@media screen and (max-width: 767px) {
						grid-template-columns: unset;
						grid-gap: unset;
					}
					.item {
						text-align: left;
						@media screen and (max-width: 767px) {
							text-align: center;
							display: flex;
							flex-direction: row-reverse;
							width: 100%;
							justify-content: space-between;
							&:not(:last-child) {
								margin-bottom: 12px;
							}
						}
						p {
							margin-bottom: rem(5px);
							color: #171716;
							font-size: rem(16px);
							@media screen and (max-width: 767px) {
								margin-bottom: rem(0px);
							}
						}
						span {
							font-size: rem(14px);
							color: var(--textSecondary);
						}
					}
				}
			}
		}
		.accordion .card {
			> .card-header .btn {
				height: 72px;
				@media screen and (max-width: 767px) {
					height: 60px;
				}
				span {
					height: 20px;
					width: 20px;
					background: #fcfcfc;
					border: 2px solid #c9c9c9;
					border-radius: 50%;
					margin-right: rem(18px);
				}
				&::after {
					display: none;
				}
				&.not-collapsed {
					color: var(--textPrimary);
					span {
						border: 2px solid var(--primary);
						background-position: center;
						background-image: url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22ZM12 15.3333C13.8409 15.3333 15.3333 13.8409 15.3333 12C15.3333 10.1591 13.8409 8.66667 12 8.66667C10.1591 8.66667 8.66667 10.1591 8.66667 12C8.66667 13.8409 10.1591 15.3333 12 15.3333Z' fill='%231A90D2'/%3E%3C/svg%3E%0A");
					}
				}
			}
			.card-body {
				padding-top: rem(24px);
				.contentBox {
					background: #fcfcfc;
					.card__body {
						&.items {
							display: flex;
							align-items: center;
							justify-content: space-between;
							padding: rem(24px) rem(36px);
							@media screen and (max-width: 425px) {
								padding: rem(20px);
								.item {
									&:not(:last-child) {
										margin-bottom: rem(16px);
									}
									&:last-child {
										width: 100%;
									}
									p {
										margin-bottom: 8px;
									}
								}
								flex-wrap: wrap;
							}
							p {
								font-size: rem(16px);
								margin-bottom: rem(5px);

								font-weight: 500;
								&.sucess {
									color: #00966d;
								}
								@media screen and (max-width: 767px) {
									margin-bottom: rem(0px);
								}
							}
							span {
								font-size: rem(14px);
								font-weight: 400;
								color: var(--textSecondary);
							}
						}
					}
					.btn.btn-primary {
						padding-left: rem(70px);
						padding-right: rem(70px);
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
					.inline-btns-wrapper {
						a {
							padding-right: rem(75px);
							padding-left: rem(75px);
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
				}
				.link {
					.form-control {
						padding-right: rem(56px);
						@media screen and (max-width: 450px) {
							padding-right: rem(70px);
						}
					}
					svg {
						position: absolute;
						width: 24px;
						height: 24px;
						top: 50%;
						transform: translateY(-50%);
						right: 24px;
						cursor: pointer;
						&:hover {
							opacity: 0.7;
						}
					}
				}
			}
		}
	}
}
@media screen and (max-width: 991px) {
	.d-flex {
		flex-direction: column-reverse;
	}
}
</style>
