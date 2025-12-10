<template>
	<div class="serviceFlow">
		<div class="accordion" role="tablist">
			<b-card no-body>
				<b-card-header header-tag="header" role="tab">
					<div class="row">
						<div class="col-lg-12">
							<b-button block v-b-toggle.serviceDetail variant="info">
								<span class="counter">Service Details</span>
							</b-button>
						</div>
					</div>
				</b-card-header>
				<b-collapse id="serviceDetail" :visible="!approved" accordion="my-accordion " role="tabpanel">
					<b-card-body>
						<div class="caseSteps accordion">
							<!-- 1 -->
							<div class="caseSteps__item completed">
								<div class="caseSteps__item--head" role="tab">
									<a href="javascript:void(0)" v-b-toggle.generalInfo>
										General Info and Instructions
									</a>
								</div>
								<b-collapse id="generalInfo" visible accordion="my-accordion" role="tabpanel" v-model="collapseStates[0]">
									<div class="caseSteps__item--body">
										<div class="row">
											<div class="col-lg-12">
												<general-info  :service="service"/>
											</div>
										</div>
									</div>
								</b-collapse>
							</div>
							<!-- 2 -->
							<div class="caseSteps__item completed">
								<div class="caseSteps__item--head" role="tab">
									<a href="javascript:void(0)" v-b-toggle.serviceDefinition>
										Service Definition
									</a>
								</div>
								<b-collapse id="serviceDefinition" visible accordion="my-accordion" role="tabpanel" v-model="collapseStates[1]">
									<div class="caseSteps__item--body">
										<div class="row">
											<div class="col-lg-12">
												<div class="DefineCase">
													<div class="contentBox">
														<service-definition :service="service" />
													</div>
												</div>
											</div>
										</div>
									</div>
								</b-collapse>
							</div>
							<!-- 3 -->
							<div class="caseSteps__item completed">
								<div class="caseSteps__item--head" role="tab">
									<a href="javascript:void(0)" v-b-toggle.uploadedFiles>
										Uploaded Files
									</a>
								</div>
								<b-collapse id="uploadedFiles" visible accordion="my-accordion" role="tabpanel" v-model="collapseStates[2]">
									<div class="caseSteps__item--body">
										<div class="row">
											<div class="col-lg-12">
												<div class="uploadFiles">
													<!-- Photon Files -->
													<div class="contentBox" v-if="isPhotonService">
														<div class="inner-title">
															Download and review the service files
														</div>
														<div v-if="service.files.length">
															<base-download-file  v-for="file in service.files" :key="file.name" :fileName="file.name" :files="service.files"/>
														</div>
														<div v-else>
															<base-download-file :key="'Patient_Files.zip'" :fileName="'Patient_Files.zip'" :files="[]" :photonFile="{...photonDummyFile, service: service.id, created: service.created, modmodified: service.created}"/>
														</div>
													</div>
													<div class="contentBox" v-if="!isPhotonService">
														<div class="inner-title">
															Download and review the service files
														</div>
														<div v-if="service.service_data.files.length">
															<base-download-file  v-for="file in service.service_data.files" :key="file.name" :fileName="file.name" :files="service.files"/>
														</div>
														<required-field  v-if="'fields' in service.service_data"  :fields="service.service_data.fields" :service="service" :readOnly="true" />
														<div class="inner-title">
															Files Note
														</div>
														<div class="form-group" >
															<textarea class="form-control" v-model="service.service_data.filesNote" :readonly="true"></textarea>
															<label class="control-label">Notes</label>
														</div>
														<div v-if="service.service_data.implant">
															<div class="inner-title">
																Implant Sites
															</div>
															<div class="main-image text-center">
																<implant  :service="service" :readOnly="true"/>
															</div>
														</div>
													</div>
													
												</div>
											</div>
										</div>
									</div>
								</b-collapse>
							</div>
							<div class="caseSteps__item completed" v-if="ServiceDataStatus(this.service) == 'waiting'">
								<div class="row">
									<div class="col-lg-9">
										<div class="inline-btns-wrapper" >
											<a href="#" class="btn btn-primary" @click.prevent="updateServiceDataStatus('approved')">
												Approve Service Files
											</a>
											<a href="#"  class="btn btn-secondary grey" @click.prevent="updateServiceDataStatus('rejected')">
												Reject
											</a>
										</div>
									</div>
								</div>
							</div>
							<!-- 3 -->
						</div>
					</b-card-body>
				</b-collapse>
			</b-card>
		</div>
	</div>
</template>

<script>
// [*] Import UI Components
import GeneralInfo from '@/components/InternalDoctor/ServiceSummery/GeneralInfo.vue';
import ServiceDefinition from '@/components/InternalDoctor/ServiceSummery/ServiceDefinition.vue';
import BaseDownloadFile from '@/common/components/base/BaseDownloadFile.vue';
import Implant from '@/components/service/partials/Implant.vue';
import RequiredField from '@/components/newService/RequiredField.vue';

import { serviceIsCompleted, clientDoctorFilesStatus } from '@/common/helpers/index';
import { ServiceHelper } from '@/common/crud-helpers/service';

export default {
	props: {
		service: Object,
	},
	components: {
		GeneralInfo,
		ServiceDefinition,
		BaseDownloadFile,
		Implant,
		RequiredField,
		
	},
	data() {
		return {
			collapseStates: [false, false, true],
			approved: false,
			isPhotonService: false,

			// Photon Service Dummy File
			photonDummyFile:  {
			    id: 1,
			    value: "https://voxel3di.co.uk/en/documents/9/CF05fK07VIA90VVrpM9ALUA_patient_files.zip",
			    name: "Patient_Files.zip",
			}
		};
	},
	created() {
		if(	serviceIsCompleted(this.service)  &&
			this.ServiceDataStatus(this.service) != 'waiting' &&
			this.ServiceDataStatus(this.service) != 'rejected'
		) {
			this.approved = true
			this.collapseStates= [false, false, false]

			/// Service Come From Photon Lab
			if(this.ServiceDataStatus(this.service) == 'approved-photon') {
				this.isPhotonService = true;
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
		ServiceDataStatus(service) {
			return clientDoctorFilesStatus(service);
		},
		updateServiceDataStatus(status) {
			ServiceHelper.updateServiceData({
				service_data: {
					...this.service.service_data,
					'files_status': status
				},
				serviceId: this.service.id
			})
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
