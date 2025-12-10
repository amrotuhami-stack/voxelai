<template>
	<div class="newService">
		<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
		<div>
			<h1 class="main-title">Continue A Service</h1>
			<div class="row">
				<div class="col-lg-9">
					<services :service="service" />
				</div>
			</div>
			<div class="accordion" role="tablist">
				<b-card no-body>
					<b-card-header header-tag="header" role="tab">
						<div class="row">
							<div class="col-lg-9">
								<b-button
									block
									v-b-toggle.serviceDetail
									variant="info"
									>Service Details</b-button
								>
							</div>
						</div>
					</b-card-header>
					<b-collapse
						id="serviceDetail"
						visible
						accordion="my-accordion"
						role="tabpanel"
					>
						<b-card-body>
							<div class="row">
								<div class="col-lg-9">
									<b-card-text> 1 </b-card-text>
								</div>
							</div>
						</b-card-body>
					</b-collapse>
				</b-card>
			</div>
			<div class="accordion" role="tablist">
				<b-card no-body>
					<b-card-header header-tag="header" role="tab">
						<div class="row">
							<div class="col-lg-9">
								<b-button
									block
									v-b-toggle.serviceResult
									variant="info"
									>Service Results
									<b-badge variant="light"
										>PHASE_02</b-badge
									></b-button
								>
							</div>
						</div>
					</b-card-header>
					<b-collapse
						id="serviceResult"
						visible
						accordion="my-accordion"
						role="tabpanel"
					>
						<b-card-body>
							<div class="row">
								<div class="col-lg-9">
									<b-card-text> 2 </b-card-text>
								</div>
							</div>
						</b-card-body>
					</b-collapse>
				</b-card>
			</div>
			<div class="accordion" role="tablist">
				<b-card no-body>
					<b-card-header header-tag="header" role="tab">
						<div class="row">
							<div class="col-lg-9">
								<b-button
									block
									v-b-toggle.shipingdetails
									variant="info"
									>Shiping Details<b-badge variant="light"
										>Out for Delivery</b-badge
									></b-button
								>
							</div>
						</div>
					</b-card-header>
					<b-collapse
						id="shipingdetails"
						visible
						accordion="my-accordion"
						role="tabpanel"
					>
						<b-card-body>
							<b-card-text>
								<div class="orderShipping">
									<div class="row w-100 col-gap-0">
										<div class="col-lg-9">
											<div class="row col-gap-25">
												<div class="col-lg-5">
													<div class="card">
														<div class="card__head">
															Shipment Tracking
														</div>
														<div class="card__body">
															<shipment-tracking />
														</div>
													</div>
												</div>
												<div class="col-lg-7">
													<shipment-detail />
												</div>
											</div>
										</div>
									</div>
								</div>
							</b-card-text>
						</b-card-body>
					</b-collapse>
				</b-card>
			</div>
		</div>
	</div>
</template>

<script>
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import { newServiceFlowShipmentBreadCrumbs } from "@/common/constant/breadCrumbs"

import Services from '@/components/service/Services.vue';
import ShipmentTracking from '@/components/newService/ShipmentTracking.vue';
import ShipmentDetail from '@/components/newService/ShipmentDetail.vue';

export default {
	components: {
		BaseBreadCrumb,
		Services,
		ShipmentTracking,
		ShipmentDetail,
	},

	data() {
		return {
			breadCrumbsItems: [...newServiceFlowShipmentBreadCrumbs],
			service: [
				{
					index: 0,
					image: 'mobile.png',
					title: '3D Implant Planing',
					seeMore: true,
					link: 'Continue',
					showBtn: false,
					detail: 'See More Details',
				},
			],
		};
	},
};
</script>

<style lang="scss" scoped>
.newService {
	h1 {
		margin-bottom: rem(24px);
	}
	.orderShipping {
		display: flex;
		.card {
			height: 100%;
			@media screen and (max-width: 991px) {
				border: 0;
				border-radius: 0;
				border-bottom: 1px solid #e9e9e9;
				::v-deep .card__head,
				.card__head {
					padding: 0;
					padding-top: rem(12px);
					border: 0;
					background: transparent;
				}

				::v-deep .card__body,
				.card__body {
					padding-left: 0;
					padding-right: 0;
				}
			}
		}
		&__left {
			flex: 0 0 405px;
			max-width: 405px;
			margin-right: rem(24px);
			.card {
				border: 1px solid var(--borderColor);
			}
		}
		&__right {
			flex: 1;
		}
		@media screen and (max-width: 991px) {
			> .row {
				> div {
					margin-bottom: 25px;
				}
			}
		}
	}
}
</style>
