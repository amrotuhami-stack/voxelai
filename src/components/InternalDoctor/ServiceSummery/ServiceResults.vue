<template>
	<div class="accordion" role="tablist">
		<b-card no-body>
			<b-card-header header-tag="header" role="tab">
				<div class="row">
					<div class="col-lg-12">
						<b-button block v-b-toggle.serviceResult variant="info">
							Service Results
							<!-- <b-badge variant="light">PHASE_02</b-badge> !-->
						</b-button>
					</div>
				</div>
			</b-card-header>
			<b-collapse id="serviceResult" :visible="true" accordion="my-accordion" role="tabpanel">
				<b-card-body>
					<div class="caseSteps accordion">
						<!-- 1 -->
						<div class="caseSteps__item completed" v-for="(phase, index) in servicePhases" :key="phase.title+phase.id" v-if="!hidePhaseIfEmpty(phase)">
							<div class="caseSteps__item--head" role="tab">
								<a href="javascript:void(0)" v-b-toggle="'phase' + phase.id">
									<span class="counter">{{ 'PHASE 0' + (index + 1) }}</span>
									{{ phase.title }}
								</a>
							</div>
							<b-collapse :id="'phase' + phase.id" :visible="getCurrentPhase() == index"  accordion="inner-accordion" role="tabpanel">
								<div class="caseSteps__item--body">
									<div class="row">
										<div class="col-lg-12">
											<div class="uploadFiles">
												<!-- Upload Required Files !-->
												<div>
													<div class="contentBox">
														<div class="inner-title">
															{{ 'Upload the service’s files of ' + phase.title + ' phase'}}
															<svg-icon
																v-b-tooltip.hover
																:title="'Upload the files of stage ' + phase.title"
																icon-id="info-circle"
																icon-viewbox="0 0 24 24"
															></svg-icon>
														</div>
														<!-- Service From Photon File -->
														<div v-if="isPhotonService && phaseStatus(phase) == 'approved'" >
															<div v-for="file in phase.deleiver_fields" :key="'deleiveryFile' + file.field_name">
																<base-download-file   :fileName="file.field_name"  :files="service.files" v-if="file.value" :photonFile="file"/>
															</div>
                                                        </div>
                                                        <div v-if="!isPhotonService && phaseStatus(phase) == 'waiting' || phaseStatus(phase) == 'approved' || phaseStatus(phase) == 'rejected'">
                                                            <base-download-file v-for="file in phase.deleiver_fields" :key="'deleiveryFile' + file.field_name" :fileName="file.field_name" :files="service.files"/>
                                                        </div>
														<div v-else>
                                                            <base-upload-files v-for="(file, findex) in phase.deleiver_fields"
															    :fileDefinition="{'name': file.field_name, 'slug': convertToSlug(phase.title + '/' + file.field_name), 'required': true, 'type': file.field_type}"
															    :key="'uploadFile' + file.field_name" :uploadFile="(data) => uploadPhaseFile(data, index, findex)"
														    />
                                                        </div>
													</div>
													<div class="inline-btns-wrapper" v-if="phaseStatus(phase) == 'new'">
														<div class="inline-btns">
                                                            <button type="button" @click.prevent="updatePhaseStatus(phase, 'under_processing')" class="btn btn-primary">
																{{`   Start ${phase.title} Phase   `}}
															</button>
														</div>
													</div>
                                                    <div class="inline-btns-wrapper" v-if="phaseStatus(phase) == 'not_completed'">
														<div class="inline-btns">
                                                            <button type="button" @click.prevent="submitPhase(phase)" class="btn btn-primary" :disabled="phase.deleiver_fields.filter((item) => !('url' in item)).length > 0 ? true : false">
																{{`   Submit ${phase.title} Files   `}}
															</button>
														</div>
													</div>
												</div>
                                                <!-- Phase Are Waiting !-->
												<div class="inline-btns-wrapper" v-if="phaseStatus(phase) == 'waiting'">
													<p>
														<i>Finished</i> on {{ phase.change_status_date  | formatDate }} and
														<span class="waiting">Waiting</span> for the doctor approval
													</p>
												</div>
												<!-- Phase Are Approved !-->
												<div class="inline-btns-wrapper" v-if="phase.status == 'approved'">
													<p v-if="phase.change_status_date">
														<i>Finished</i> and
														<span>Approved</span>, at {{ phase.change_status_date | formatDate }} by the doctor.
													</p>
													<p v-else>
														<i>Finished</i> and
														<span>Approved</span>
													</p>
												</div>
                                                <!-- Phase Are Rejected !-->
												<div class="inline-btns-wrapper" v-if="phase.status == 'rejected'">
													<p>
														<i>Finished</i> and
														<span class="rejected">Rejected</span>, at {{ phase.change_status_date | formatDate }} by the doctor.
													</p>
                                                    <div class="inline-btns">
                                                        <button type="button" @click.prevent="restartPhase(phase)" class="btn btn-secondary grey" >
															Restart
														</button>
													</div>
												</div>
												 
											</div>
										</div>
									</div>
								</div>
							</b-collapse>
						</div>
						<!-- 1 -->
						 <!-- Close Service !-->
						 <div class="inline-btns-wrapper">
                                                    <div class="inline-btns">
                                                        <button type="button" @click.prevent="closeCurrentService()" class="btn btn-secondary grey" >
															Close Service
														</button>
													</div>
												</div>
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
import { ServiceHelper } from '@/common/crud-helpers/service';
import { CommonHelper } from '@/common/crud-helpers/common';
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
			isPhotonService: false,
		};
	},
    created() {
		this.service = this.data
        this.servicePhases = this.service.phases
		if(!this.service.service_data) {
			this.isPhotonService = true
			this.servicePhases = this.servicePhases.map((phase) => {
				return {
					...phase,
					status: "approved"
				}
			})
		}
    },
	computed: {
		...mapGetters(['serviceDetail']),
	},
	watch: {
		serviceDetail() {
			this.service = this.serviceDetail
			this.servicePhases = this.service.phases
			if(!this.service.service_data) {
				this.isPhotonService = true
				this.servicePhases = this.servicePhases.map((phase) => {
					return {
						...phase,
						status: "approved"
					}
				})
			}
		}
	},
	methods: {
		convertToSlug(Text) {
			return 'file-' + Text
					.toLowerCase()
					.replace(/ /g, '-')
					.replace(/[^\w-]+/g, '');
		},
		async uploadPhaseFile(file, phaseIndex, fieldIndex)  {
			let data = await ServiceHelper.pushServiceFile({
				...file,
				'name': file.name,
				'service': this.service.id,
				'value': file.value,
				'files': this.service.files
			})
			CommonHelper.closeOverLay()
			let phases = [...this.servicePhases]
			phases[phaseIndex].deleiver_fields[fieldIndex] = {
				...phases[phaseIndex].deleiver_fields[fieldIndex],
				url: data.file,
			}
			this.servicePhases = phases
		},
		submitPhase(phase) {
            let _deleiver_fields = []
			phase.deleiver_fields.forEach((item) => {
				_deleiver_fields.push({...item, value: item.url})
			})
			ServiceHelper.submitPhaseFields({
				'serviceId': this.service.id,
				'deleiver_fields': _deleiver_fields,
				'id': phase.id,
			})
			this.updatePhaseStatus(phase, 'ready');
		},
		updatePhaseStatus(phase, _status) {
			ServiceHelper.updatePhaseStatus({
				'serviceId': this.service.id,
				'id': phase.id,
				'status': _status
			})
		},
        phaseStatus(phase) {
			
            if(phase.status != "under_processing" && phase.status != "ready") {
                return phase.status
            }
            else {
                let numberOfEmptyFiles = phase.deleiver_fields.filter((item) => item.value == '' || item.value == '.').length
                if(numberOfEmptyFiles == 0) {
                    return 'waiting'
                }
                else {
                    return 'not_completed'
                }
            }
        },
        restartPhase(phase) {
            let _deleiver_fields = []
			phase.deleiver_fields.forEach((item) => {
				_deleiver_fields.push({...item, value: "."})
			})
			ServiceHelper.submitPhaseFields({
				'serviceId': this.service.id,
				'deleiver_fields': _deleiver_fields,
				'id': phase.id,
			})
			this.updatePhaseStatus(phase, 'under_processing')
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
		hidePhaseIfEmpty(phase) {
			if(this.service.fulfillment_status == 'fulfilled') {
				let hide = true
				phase.deleiver_fields.forEach((field) => {
					if(field.value != "") hide = false
				})
				return hide;
			}
			return false
		},
		closeCurrentService(id) {
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
							color: orange;
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
