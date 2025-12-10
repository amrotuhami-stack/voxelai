<template>
	<div class="uikit2">
		<div class="container">
			<div class="changePassword">
				<a href="#" class="btn btn-default" v-b-modal="'my-modal'"
					>Change Password</a
				>
				<!-- The modal -->
				<b-modal ref="my-modal" id="my-modal" centered>
					<div class="modal-title">Change Password</div>
					<p>Voxel is created for every dental practitioner.</p>
					<form>
						<div class="form-group">
							<input
								type="password"
								id="current"
								class="form-control"
								required=""
								name="Current password"
								placeholder="First Current password"
							/>
							<label class="control-label"
								>Current password</label
							>
							<span
								id="currentSpan"
								@click="showPassword('current', 'currentSpan')"
							>
								<svg-icon
									class="show"
									icon-id="eye-icon"
									icon-viewbox="0 0 24 24"
								>
								</svg-icon>
								<svg-icon
									class="hide d-none"
									icon-id="closeEye-icon"
									icon-viewbox="0 0 24 24"
								>
								</svg-icon>
							</span>
						</div>
						<div class="form-group">
							<input
								type="password"
								id="news"
								class="form-control"
								required=""
								name="New password"
								placeholder="First New password"
							/>
							<label class="control-label">New password</label>
							<span
								id="newSpan"
								@click="showPassword('news', 'newSpan')"
							>
								<svg-icon
									class="show"
									icon-id="eye-icon"
									icon-viewbox="0 0 24 24"
								>
								</svg-icon>
								<svg-icon
									class="hide d-none"
									icon-id="closeEye-icon"
									icon-viewbox="0 0 24 24"
								>
								</svg-icon>
							</span>
						</div>
						<div class="form-group">
							<input
								type="password"
								id="confirm"
								class="form-control"
								required=""
								name="confirm password"
								placeholder="confirm password"
							/>
							<label class="control-label"
								>confirm password</label
							>
							<span
								id="confirmSpan"
								@click="showPassword('confirm', 'confirmSpan')"
							>
								<svg-icon
									class="show"
									icon-id="eye-icon"
									icon-viewbox="0 0 24 24"
								>
								</svg-icon>
								<svg-icon
									class="hide d-none"
									icon-id="closeEye-icon"
									icon-viewbox="0 0 24 24"
								>
								</svg-icon>
							</span>
						</div>
						<div class="inline-buttons">
							<button type="button" class="btn btn-primary">
								Update
							</button>
							<a
								href="javascript:void(0)"
								@click="hideModal"
								class="link"
								>Cancel</a
							>
						</div>
					</form>
				</b-modal>
			</div>
			<br />
			<br />
			<label class="bestSeller">best seller</label>
			<div class="card">
				<div class="card__head">subtotal</div>
				<div class="card__body">card body</div>
			</div>
			<br />
			<br />
			<base-touch-spin />
			<br />
			<br />
			<div class="checkbox">
				<label>
					<input type="checkbox" name="radio" />
					<span>3D Printings</span>
				</label>
			</div>
			<br />
			<br />
			<!-- table -->
			<div class="table">
				<div class="table__head">
					<div class="table__row">
						<div class="table__row--cell" data-width="16">ID</div>
						<div class="table__row--cell" data-width="18">
							Order Date
						</div>
						<div class="table__row--cell" data-width="16">
							Amount
						</div>
						<div class="table__row--cell" data-width="23">
							Payment Status
						</div>
						<div class="table__row--cell">Payment Method</div>
						<div class="table__row--cell" data-width="5">More</div>
					</div>
				</div>
				<div class="table__body">
					<div class="table__row">
						<div class="table__row--cell" data-width="16">
							#123456
						</div>
						<div class="table__row--cell" data-width="18">
							19/04/2021
						</div>
						<div class="table__row--cell" data-width="16">
							$1,295.00
						</div>
						<div class="table__row--cell p-0" data-width="23">
							<span class="pending"></span>
							Pending
						</div>
						<div class="table__row--cell">Bank Transfer</div>
						<div class="table__row--cell" data-width="5">
							<b-dropdown>
								<b-dropdown-item href="#"
									>Change Payment Method</b-dropdown-item
								>
								<b-dropdown-item href="#"
									>Report a problem</b-dropdown-item
								>
							</b-dropdown>
						</div>
					</div>
					<div class="table__row">
						<div class="table__row--cell" data-width="16">
							#123456
						</div>
						<div class="table__row--cell" data-width="18">
							19/04/2021
						</div>
						<div class="table__row--cell" data-width="16">
							$1,295.00
						</div>
						<div class="table__row--cell p-0" data-width="23">
							<span class="completed"></span>
							Pending
						</div>
						<div class="table__row--cell">Bank Transfer</div>
						<div class="table__row--cell" data-width="5">
							<b-dropdown>
								<b-dropdown-item href="#"
									>Change Payment Method</b-dropdown-item
								>
								<b-dropdown-item href="#"
									>Report a problem</b-dropdown-item
								>
							</b-dropdown>
						</div>
					</div>
					<div class="table__row">
						<div class="table__row--cell" data-width="16">
							#123456
						</div>
						<div class="table__row--cell" data-width="18">
							19/04/2021
						</div>
						<div class="table__row--cell" data-width="16">
							$1,295.00
						</div>
						<div class="table__row--cell p-0" data-width="23">
							<span class="failed"></span>
							Pending
						</div>
						<div class="table__row--cell">Bank Transfer</div>
						<div class="table__row--cell" data-width="5">
							<b-dropdown>
								<b-dropdown-item href="#"
									>Change Payment Method</b-dropdown-item
								>
								<b-dropdown-item href="#"
									>Report a problem</b-dropdown-item
								>
							</b-dropdown>
						</div>
					</div>
				</div>
			</div>
			<base-pagination :info="info" />
			<br />
			<br />
			<payment-plan-item :cardContent="cardContent" />
			<br />
			<br />
			<br />
			<!-- <cart-item /> -->
			<br />
			<br />
			<br />
			<div class="servicesType">
				<div class="wrapper">
					<div class="image">
						<img
							src="@/assets/images/shoppingCart/mobile.png"
							alt=""
							class="img-fluid"
						/>
					</div>
					3D Implant Planing
				</div>
				<a href="#" class="btn btn-default">Continue</a>
			</div>
			<br />
			<br />
			<br />
			<!-- accordion -->
			<div class="accordion" role="tablist">
				<b-card no-body>
					<b-card-header header-tag="header" role="tab">
						<b-button block v-b-toggle.accordion-1 variant="info"
							>Service Details</b-button
						>
					</b-card-header>
					<b-collapse
						id="accordion-1"
						visible
						accordion="my-accordion"
						role="tabpanel"
					>
						<b-card-body>
							<b-card-text>
								<ul class="list-unstyle">
									<li class="steps active">
										Step 01
										<span>Select or Add Patient</span>
									</li>
									<li class="steps">
										Step 02
										<!-- <span>Define Case</span> -->
										<div class="patientType">
											<h3>Define Case</h3>
											<span>
												<p>
													Lorem Ipsum is simply dummy
													text of the printing
													industry.
												</p>
												<a href="#"
													><svg
														width="24"
														height="24"
														viewBox="0 0 24 24"
														fill="none"
													>
														<path
															fill-rule="evenodd"
															clip-rule="evenodd"
															d="M12 3C7.02999 3 3 7.02999 3 12C3 16.97 7.02998 21 12 21C16.9706 21 21 16.9703 21 12C21 7.0297 16.9706 3 12 3ZM12 5C15.866 5 19 8.13424 19 12C19 15.8658 15.866 19 12 19C8.13455 19 5 15.8654 5 12C5 8.13456 8.13456 5 12 5Z"
															fill="#1A90D2"
														/>
														<g opacity="0.5">
															<path
																fill-rule="evenodd"
																clip-rule="evenodd"
																d="M12 7C11.4477 7 11 7.44772 11 8V12C11 12.5523 11.4477 13 12 13C12.5523 13 13 12.5523 13 12V8C13 7.44772 12.5523 7 12 7ZM12 15C11.4477 15 11 15.4477 11 16C11 16.5523 11.4477 17 12 17C12.5523 17 13 16.5523 13 16C13 15.4477 12.5523 15 12 15Z"
																fill="#1A90D2"
															/>
														</g>
													</svg>
													See how to define your
													case</a
												>
											</span>
											<div class="contentBox">
												<p>
													I want my Guide to be
													supported on:
												</p>
												<div class="wrapper">
													<div class="card">
														<div class="card__body">
															<div
																class="
																	card__body--item
																"
															>
																<div
																	class="
																		image
																	"
																>
																	<img
																		src="@/assets/images/tooth.png"
																		alt=""
																		class="
																			img-fluid
																		"
																	/>
																</div>
																<p>
																	Bone<span
																		>Open
																		Large
																		Surgical
																		Flap</span
																	>
																</p>
															</div>
															<svg-icon
																icon-id="tick-icon"
																icon-viewbox="0 0 32 32"
															></svg-icon>
														</div>
													</div>
													<div class="card">
														<div class="card__body">
															<div
																class="
																	card__body--item
																"
															>
																<div
																	class="
																		image
																	"
																>
																	<img
																		src="@/assets/images/tooth.png"
																		alt=""
																		class="
																			img-fluid
																		"
																	/>
																</div>
																<p>
																	Bone<span
																		>Open
																		Large
																		Surgical
																		Flap</span
																	>
																</p>
															</div>
														</div>
													</div>
												</div>
												<p>
													Select your patient type<svg
														width="24"
														height="24"
														viewBox="0 0 24 24"
														fill="none"
													>
														<path
															fill-rule="evenodd"
															clip-rule="evenodd"
															d="M12 3C7.02999 3 3 7.02999 3 12C3 16.97 7.02998 21 12 21C16.9706 21 21 16.9703 21 12C21 7.0297 16.9706 3 12 3ZM12 5C15.866 5 19 8.13424 19 12C19 15.8658 15.866 19 12 19C8.13455 19 5 15.8654 5 12C5 8.13456 8.13456 5 12 5Z"
															fill="#1A90D2"
														/>
														<g opacity="0.5">
															<path
																fill-rule="evenodd"
																clip-rule="evenodd"
																d="M12 7C11.4477 7 11 7.44772 11 8V12C11 12.5523 11.4477 13 12 13C12.5523 13 13 12.5523 13 12V8C13 7.44772 12.5523 7 12 7ZM12 15C11.4477 15 11 15.4477 11 16C11 16.5523 11.4477 17 12 17C12.5523 17 13 16.5523 13 16C13 15.4477 12.5523 15 12 15Z"
																fill="#1A90D2"
															/>
														</g>
													</svg>
												</p>
												<div
													class="patientType__wrapper"
												>
													<div class="row">
														<div class="col-md-4">
															<div class="card">
																<div
																	class="
																		card__body
																	"
																>
																	<div
																		class="
																			image
																		"
																	>
																		<img
																			src="@/assets/images/jaw.png"
																			class="
																				img-fluid
																			"
																			alt=""
																		/>
																	</div>
																	<h4>
																		Type 1
																	</h4>
																	<ul>
																		<li>
																			Teeth
																			are
																			Sound
																		</li>
																		<li>
																			At
																			Least
																			4
																			Sound
																			teeth
																			without
																			large
																			restorations
																			available
																			2 at
																			the
																			anterior
																			& 2
																			at
																			the
																			posterior
																		</li>
																		<li>
																			No
																			teeth
																			mobility
																		</li>
																		<li>
																			No
																			Large
																			restoration
																			or
																			full
																			arch
																			crowns
																		</li>
																	</ul>
																</div>
															</div>
														</div>
														<div class="col-md-4">
															<div class="card">
																<div
																	class="
																		card__body
																	"
																>
																	<div
																		class="
																			image
																		"
																	>
																		<img
																			src="@/assets/images/jaw.png"
																			class="
																				img-fluid
																			"
																			alt=""
																		/>
																	</div>
																	<h4>
																		Type 1
																	</h4>
																	<ul>
																		<li>
																			Teeth
																			are
																			Sound
																		</li>
																		<li>
																			At
																			Least
																			4
																			Sound
																			teeth
																			without
																			large
																			restorations
																			available
																			2 at
																			the
																			anterior
																			& 2
																			at
																			the
																			posterior
																		</li>
																		<li>
																			No
																			teeth
																			mobility
																		</li>
																		<li>
																			No
																			Large
																			restoration
																			or
																			full
																			arch
																			crowns
																		</li>
																	</ul>
																</div>
															</div>
														</div>
														<div class="col-md-4">
															<div class="card">
																<div
																	class="
																		card__body
																	"
																>
																	<div
																		class="
																			image
																		"
																	>
																		<img
																			src="@/assets/images/jaw.png"
																			class="
																				img-fluid
																			"
																			alt=""
																		/>
																	</div>
																	<h4>
																		Type 1
																	</h4>
																	<ul>
																		<li>
																			Teeth
																			are
																			Sound
																		</li>
																		<li>
																			At
																			Least
																			4
																			Sound
																			teeth
																			without
																			large
																			restorations
																			available
																			2 at
																			the
																			anterior
																			& 2
																			at
																			the
																			posterior
																		</li>
																		<li>
																			No
																			teeth
																			mobility
																		</li>
																		<li>
																			No
																			Large
																			restoration
																			or
																			full
																			arch
																			crowns
																		</li>
																	</ul>
																</div>
															</div>
														</div>
													</div>
												</div>
											</div>
											<div class="button-row">
												<div class="inline-btn">
													<a
														href="#"
														class="btn btn-primary"
														>Next</a
													>
													<a href="#">Skip for now</a>
												</div>
												<a
													href="#"
													class="btn btn-secondary"
													>Back</a
												>
											</div>
										</div>
									</li>
									<li class="steps">
										Step 03
										<span>Upload Files</span>
									</li>
								</ul>
							</b-card-text>
						</b-card-body>
					</b-collapse>
				</b-card>
			</div>
			<br />
			<br />
			<br />
			<!-- modal -->
			<div>
				<b-button v-b-modal.modal-1>Open Modal</b-button>

				<b-modal id="modal-1" title="Choose Pricing Plan">
					<p>Here are the offers created for you.</p>
				</b-modal>
			</div>
			<br />
			<br />
			<br />
			<!-- Tabs -->
			<div class="card">
				<b-tabs>
					<b-tab title="Credit Card" active
						><div class="card__body">
							<p>I'm the first tab</p>
						</div></b-tab
					>
					<b-tab title="PayPal"><p>I'm the second tab</p></b-tab>
				</b-tabs>
			</div>
			<br />
			<br />
			<br />
			<!-- link-bar -->
			<a class="linkBox">
				<p>Choose a service from Shop</p>
				<i>></i>
			</a>
			<br />
			<br />
			<br />
			font awesome
			<font-awesome-icon icon="user-secret" />
			<div class="pageHead">
				<h1 class="main-title">My Patients<span>(24)</span></h1>
				<a href="#" class="btn btn-primary">
					<span class="icon">
						<svg-icon
							icon-id="plus-icon"
							icon-viewbox="0 0 17 18"
						></svg-icon>
					</span>
					New Service
				</a>
			</div>
			<br />
			<br />
			<br />
			<b-progress :value="value" :max="max2"></b-progress>
			<br />
			<br />
			<br />
		</div>
	</div>
</template>

<script>
import BaseIcons from '@/common/components/base/BaseSvgIcons.vue';
import BaseTouchSpin from '../common/components/base/BaseTouchSpin.vue';
import BasePagination from '../common/components/base/BasePagination.vue';
import PaymentPlanItem from '@/components/PaymentPlanItem.vue';
import CartItem from '@/components/cart/CartItem.vue';

export default {
	components: {
		BaseIcons,
		BaseTouchSpin,
		BasePagination,
		PaymentPlanItem,
		CartItem,
	},
	data() {
		return {
			info: '7 orders',
			value: 33.333333333,
			max: 50,
			cardContent: [
				{
					index: 0,
					image: 'docs.png',
					title: 'Basic',
					price: '$236.00',
					subtitle: '15 Cases a Month',
					duration: '6 Months Access',
				},
				{
					index: 1,
					popular: true,
					image: 'docs.png',
					title: 'Pro',
					price: '$236.00',
					subtitle: '15 Cases a Month',
					duration: '6 Months Access',
				},
				{
					index: 2,
					image: 'docs.png',
					title: 'Elite',
					price: '$236.00',
					subtitle: '15 Cases a Month',
					duration: '6 Months Access',
				},
			],
		};
	},
	methods: {
		hideModal() {
			this.$refs['my-modal'].hide();
		},
		showPassword: function (id, spanId) {
			let input = document.querySelector(`#${id}`);
			let eye = document.querySelector(`#${spanId}`);
			let showicon = eye.querySelector('.show');
			let hideicon = eye.querySelector('.hide');
			if (input.type === 'password') {
				showicon.classList.add('d-none');
				hideicon.classList.remove('d-none');
				return (input.type = 'text');
			} else {
				showicon.classList.remove('d-none');
				hideicon.classList.add('d-none');
				return (input.type = 'password');
			}
		},
	},
};
</script>

<style lang="scss" scoped>
.progress {
	.progress-bar {
		height: 16px !important;
	}
}
</style>
