<template>
	<div class="accordion" role="tablist">
		<b-card no-body>
				<b-card-header header-tag="header" role="tab">
					<div class="row">
						<div class="col-lg-9">
							<b-button block v-b-toggle.serviceResult variant="info">
								Service Results
							</b-button>
						</div>
					</div>
				</b-card-header>
				<div class="row" v-if="clientFileStatus == 'waiting'">
					<div class="col-lg-9">
						<div class="contentBox notification" >
							<div class="notification__icon">
								<svg-icon
									icon-id="clock-icon"
									icon-viewbox="0 0 72 72"
								></svg-icon>
							</div>
							<div class="notification__detail">
								<p>Great! We're currently checking on the files . We'll notify you once the files are accepted.</p>
							</div>
						</div>
					</div>
				</div>
				
				<b-collapse v-if="clientFileStatus == 'approved'" id="serviceResult" visible accordion="my-accordion" role="tabpanel">
					<b-card-body>
						<div class="caseSteps accordion">
							<!-- 1 -->
							<div class="caseSteps__item completed" v-for="(phase, index) in servicePhases" :key="phase.title+phase.id">
								<div class="caseSteps__item--head" role="tab">
									<a href="javascript:void(0)" v-b-toggle="'phase' + phase.id">
										<span class="counter">{{ 'PHASE 0' + (index + 1) }}</span>
										{{ phase.title }}
									</a>
								</div>
								<b-collapse :id="'phase' + phase.id" v-if="canStartPhase(index)" :visible="getCurrentPhase() == index" accordion="inner-accordion" role="tabpanel">
									<div class="caseSteps__item--body">
										<div class="row">
											<div class="col-lg-9">
												<div class="uploadFiles">
													<!-- Deleivery Files exist !-->
													<div v-if="phaseStatus(phase) != 'not_completed'">
														<div class="contentBox">
															<div class="inner-title">
																{{ 'Download and review the files of stage ' + phase.title}}
																<svg-icon
																	v-b-tooltip.hover
																	:title="'Download and review the files of stage ' + phase.title"
																	icon-id="info-circle"
																	icon-viewbox="0 0 24 24"
																></svg-icon>
															</div>
															<base-download-file v-for="file in phase.deleiver_fields" :key="'deleiveryFile' + file.field_name" :fileName="file.field_name" :files="service.files" />
														</div>
														<div class="inline-btns-wrapper" v-if="phaseStatus(phase) == 'waiting'">
															<div class="inline-btns">
																<button type="button" class="btn btn-primary" @click.prevent="updatePhaseStatus(phase, 'approved')">
																	{{ index != servicePhases.length - 1 ? 'Approve and Go to Next Stage' : 'Approve and Finish' }}
																</button>
																<button type="button" class="btn btn-secondary grey" @click.prevent="updatePhaseStatus(phase, 'rejected')">
																	Reject Files
																</button>
															</div>
														</div>
													</div>
													<!-- Waiting Deleivery Files !-->
													<div class="contentBox notification" v-if="phaseStatus(phase) == 'not_completed'">
														<div class="notification__icon">
															<svg-icon
																icon-id="clock-icon"
																icon-viewbox="0 0 72 72"
															></svg-icon>
														</div>
														<div class="notification__detail">
															<p>Great! We're currently working on the files of this stage. Please, Wait for us and we'll notify you when the files are ready.</p>
														</div>
													</div>
													<!-- Phase Are completed !-->
													<div class="inline-btns-wrapper" v-if="phaseStatus(phase) == 'approved'">
														<p>
															<i>Reviewed</i> and
															<span>Approved</span> {{ phase.change_status_date | formatDate}}
														</p>
													</div>
													<!-- Phase Are Rejected !-->
													<div class="inline-btns-wrapper" v-if="phaseStatus(phase) == 'rejected'">
														<p>
															<i>Reviewed</i> and
															<span class="rejected">Rejected</span> {{ phase.change_status_date | formatDate}}
														</p>
													</div>
												</div>
											</div>
										</div>
									</div>
								</b-collapse>
							</div>
							<!-- 1 -->
						</div>
					</b-card-body>
				</b-collapse>
			</b-card>
	</div>
</template>

<script>
// [*] Import UI Components
import BaseUploadFiles from '@/common/components/base/BaseUploadFiles.vue';
import BaseDownloadFile from '@/common/components/base/BaseDownloadFile.vue';

// [*] Vuex State Getter And Action Helper
import { clientDoctorFilesStatus } from '@/common/helpers/index';

import { ServiceHelper } from '@/common/crud-helpers/service';
import { mapGetters } from 'vuex';

export default {
	props: {
		data: Object,
	},
	components: {
		BaseUploadFiles,
		BaseDownloadFile,
	},
	data() {
		return {
			service: null,
            servicePhases: null,
			clientFileStatus: false,
		};
	},
    created() {
		this.service = this.data
        this.servicePhases = this.service.phases
		this.clientFileStatus = clientDoctorFilesStatus(this.service)

    },
	computed: {
		...mapGetters(['serviceDetail']),
	},
	watch: {
		serviceDetail() {
			this.service = this.serviceDetail
			this.servicePhases = this.service.phases
		}
	},
	methods: {
        updatePhaseStatus(phase, _status) {
			ServiceHelper.updatePhaseStatus({
				'serviceId': this.service.id,
				'id': phase.id,
				'status': _status
			});
			if(this.allphasesApproved()) {
				this.closeCurrentService()
			}
		},
		convertToSlug(Text) {
			return 'file-' + Text
					.toLowerCase()
					.replace(/ /g, '-')
					.replace(/[^\w-]+/g, '');
		},
		phaseStatus(phase) {
            if(phase.status == "new") { 
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
		},
		closeCurrentService() {
			ServiceHelper.closeService({id: this.service.id})
		},
		allphasesApproved() {
			let allPhasesApproved = true;
			this.servicePhases.forEach(phase => {
				if(phase.status != 'approved') {
					allPhasesApproved = false;
				}
			})
			return allPhasesApproved
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
