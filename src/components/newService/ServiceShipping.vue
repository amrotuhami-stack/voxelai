<template>
	<div class="accordion" role="tablist">
		<b-card no-body v-if="requireShipping">
			<b-card-header header-tag="header" role="tab">
				<div class="row">
					<div class="col-lg-9">
						<b-button block v-b-toggle.shipping variant="info">
                            Shiping Details
                            <!--<b-badge variant="light">
                                Out for Delivery
                            </b-badge> !-->
                        </b-button>
					</div>
				</div>
			</b-card-header>
			<div  id="shipping"   accordion="my-accordion" role="tabpanel" v-if="allPhasesComplete() && requireShipping" >
				<b-card-body>
					<b-card-text>
						<div class="orderShipping">
							<div class="row w-100 col-gap-0">
								<div class="col-lg-9">
									<div class="row col-gap-25">
										<!-- <div class="col-lg-5 pt-3">
											<div class="card">
												<div class="card__head">
													Shipment Tracking
												</div>
												<div class="card__body">
													<shipment-tracking />
												</div>
											</div>
										</div> -->
										<div class="col-lg-12 pt-3">
											<shipment-detail :service="service"></shipment-detail>
										</div>
									</div>
								</div>
							</div>
						</div>
					</b-card-text>
				</b-card-body>
			</div>
		</b-card>
	</div>
</template>

<script>
// [*] Import UI Components
import ShipmentDetail from '@/components/newService/ShipmentDetail.vue';
import ShipmentTracking from '@/components/newService/ShipmentTracking.vue';

// [*] Vuex State Getter And Action Helper
import { clientDoctorFilesStatus } from '@/common/helpers/index';

import { ServiceHelper } from '@/common/crud-helpers/service';
import { mapGetters } from 'vuex';

export default {
	props: {
		data: Object,
	},
	components: {
		ShipmentDetail,
		ShipmentTracking,
	},
	data() {
		return {
			service: null,
            servicePhases: null,
			clientFileStatus: false,
			requireShipping:  false,
		};
	},
    created() {
		this.service = this.data
        this.servicePhases = this.service.phases
    },
	computed: {
		...mapGetters(['serviceDetail']),
	},
	watch: {
		serviceDetail() {
			this.service = this.serviceDetail
			this.servicePhases = this.service.phases
		},
		service() {
			let optionsRequireShipping = false
			this.service.order_line_obj.attributes.forEach((attr) => {
				if(attr.value == "1" && attr.option_obj.requires_shipping) {
					optionsRequireShipping = true
				}
			})
			if(this.service.order_line_obj.product_obj.requires_shipping || optionsRequireShipping) {
				this.requireShipping = true;
			}
		}
	},
	methods: {
        allPhasesComplete() {
            let completed  = true
            this.servicePhases.forEach((phase) => {
                if(this.phaseStatus(phase) != 'approved') {
                    completed = false
                }
            })
            return completed
        },
        updatePhaseStatus(phase, _status) {
			ServiceHelper.updatePhaseStatus({
				'serviceId': this.service.id,
				'id': phase.id,
				'status': _status
			})
		},
		convertToSlug(Text) {
			return 'file-' + Text
					.toLowerCase()
					.replace(/ /g, '-')
					.replace(/[^\w-]+/g, '');
		},
		phaseStatus(phase) {
            if(phase.status == "new") {
                return 'not_completed'
            }
			else if(phase.status == "approved" || phase.status == 'rejected') {
                return phase.status
            }
            else {
                let numberOfEmptyFiles = phase.deleiver_fields.filter((item) => item.value == '').length
                if(numberOfEmptyFiles == 0) {
                    return 'waiting'
                }
                else {
                    return 'not_completed'
                }
            }
        },
		canStartPhase(phaseIndex) {
			if(phaseIndex == 0)
				return true
			return this.phaseStatus(this.servicePhases[phaseIndex -1]) == 'approved' ? true : false
		},
		getCurrentPhase() {
			let currentPhase = -1
			if(this.service.phases.length > 0) {
				let index = 0
				while(currentPhase == -1 && index < this.service.phases.length) {
					if(this.service.phases[index].status == 'approved') {
						index = index + 1
					}
					else {
						currentPhase = index
					}
				}
			}
			return currentPhase == -1 ? this.service.phases.length -1 : currentPhase;
		}
	}
};
</script>

<style lang="scss" scoped>
.serviceFlow {
	.notification {
		margin-top: rem(24px);
		padding-top: rem(45px);
		padding-bottom: rem(45px);
		@media screen and (max-width: 767px) {
			padding-top: rem(25px);
			padding-bottom: rem(25px);
		}
		&__icon {
			text-align: center;
			margin-bottom: rem(20px);
			svg {
				width: 70px;
				height: auto;
			}
		}
		&__detail {
			max-width: 585px;
			margin: auto;
			text-align: center;
			p {
				font-size: rem(20px);
				font-weight: 400;
				color: var(--textPrimary);
				line-height: 1.5;
				margin-bottom: rem(15px);
				&.date {
					font-size: rem(12px);
					font-weight: 500;
					color: #8e8e8e;
					line-height: 1;
					letter-spacing: 1px;
					margin: 0;
				}
			}
		}
	}
	.caseSteps {
		margin-left: 2%;
		&__item {
			&--head {
				text-transform: capitalize;
			}
			&:last-child {
				padding-bottom: 0;
			}
			&--body {
				.inline-btns-wrapper {
					p {
						font-size: rem(16px);
						color: var(--textSecondary);
						font-weight: 400;
						span {
							color: #00966d;
							font-style: italic;
						}
						.waiting {
							color: yellow;
						}
						.rejected {
							color: crimson;
						}
						@media screen and (max-width: 767px) {
							margin-bottom: 12px;
							text-align: center;
						}
					}
					.btn.btn-primary {
						padding-left: rem(40px);
						padding-right: rem(40px);
						text-transform: capitalize;
					}
					.btn.grey {
						padding-left: rem(45px);
						padding-right: rem(45px);
					}
					@media screen and (max-width: 450px) {
						.inline-btns {
							display: flex;
							align-items: center;
							flex-direction: column;
							width: 100%;
							.btn {
								width: 100%;
								&.btn-primary {
									margin-right: 0;
								}
							}
						}
					}
				}
				.notification {
					padding-top: rem(45px);
					padding-bottom: rem(45px);
					@media screen and (max-width: 767px) {
						padding-top: rem(25px);
						padding-bottom: rem(25px);
					}
					&__icon {
						text-align: center;
						margin-bottom: rem(20px);
						svg {
							width: 70px;
							height: auto;
						}
					}
					&__detail {
						max-width: 585px;
						margin: auto;
						text-align: center;
						p {
							font-size: rem(20px);
							font-weight: 400;
							color: var(--textPrimary);
							line-height: 1.5;
							margin-bottom: rem(15px);
							&.date {
								font-size: rem(12px);
								font-weight: 500;
								color: #8e8e8e;
								line-height: 1;
								letter-spacing: 1px;
								margin: 0;
							}
						}
					}
				}
			}
		}
		.notifications {
			@media screen and (max-width: 767px) and (min-width: 451px) {
				.inline-btns-wrapper {
					.inline-btns {
						.btn {
							&:not(:last-child) {
								margin-bottom: 0;
							}
						}
					}
				}
			}
			@media screen and (max-width: 450px) {
				.inline-btns-wrapper {
					.inline-btns {
						display: flex;
						align-items: center;
						flex-direction: column;
						width: 100%;
						.btn {
							width: 100%;
							&.btn-primary {
								margin-right: 0;
							}
						}
					}
				}
			}
		}
	}
	.accordion .card .card-body {
		padding-top: 0;
	}
}
</style>
