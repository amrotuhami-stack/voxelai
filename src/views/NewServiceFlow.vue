<template>
	<div class="serviceFlow">
		<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
		<h1 class="main-title">Continue A Digital Service</h1>
		<div class="row">
			<div class="col-lg-8">
				<div class="row">
					<div class="col-lg-12">
						<div class="contentBox" v-if="activeOrderLine">
							<div class="serviceRow">
								<div class="serviceRow__image">
									<img v-if="activeOrderLine.product_obj.images.length > 0"
										:src="activeOrderLine.product_obj.images[0].original" alt=""
										class="img-fluid" />
								</div>
								<div class="serviceRow__title">
									{{ activeOrderLine.product_obj.title }}
									<div class="serviceRow__details">
										<router-link class="viewMore"
											:to="{ name: 'product-details', params: { lang: $i18n.locale, productId: String(activeOrderLine.product_obj.id) }, }">
											See More Details
											<font-awesome-icon :icon="['fa', 'angle-right']" />
										</router-link>
										<div class="row">
											<div class="col-lg-3" v-if="service">
												<div class="item">
													<p>{{ formatId(service.id) }}</p>
													<span>Service ID</span>
												</div>
											</div>
											<div class="col-lg-4" v-if="service">
												<div class="item">
													<p>{{ service.created | formatDate }}</p>
													<span>Created At</span>
												</div>
											</div>
											<div class="col-lg-3">
												<div class="item">
													<p>{{ formatId(activeOrderLine.id) }}</p>
													<span>Order ID</span>
												</div>
											</div>
											<div class="col-lg-4" v-if="!service">
												<div class="item">
													<p>{{ activeOrderLine.date_placed | formatDate }}</p>
													<span>Order Date</span>
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
						<div class="contentBox p-3 mt-3" v-if="activeOrderLine">
							<div class="row">
								<div class="col-lg-2"
									style="display: flex; align-items: center; justify-content: center;">
									<label class="options">
										<span> Order Options</span>
									</label>
								</div>
								<div class="col-lg-10">
									<div class="checkbox pt-2" v-if="activeOrderLine.attributes">
										<div class="row">
											<div class="col-lg-12 mb-2"
												v-for="(attribute, index) in activeOrderLine.attributes" :key="index">
												<label class="options" v-if="getProductOption(attribute.option)">
													<input type="checkbox" disabled
														:name="getProductOption(attribute.option).code"
														:checked="attribute.value == '1'" />
													<span class="pb-0">
														{{ getProductOption(attribute.option).name }}
													</span>
												</label>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
						<div class="contentBox" v-if="!activeOrderLine">
							<div class="serviceRow">
								<div class="serviceRow__image p-0">
									<b-skeleton animation="fade" width="100%" height="100px"
										class="skelton"></b-skeleton>
								</div>
								<div class="serviceRow__title">
									<b-skeleton animation="fade" width="50%" height="25px" class="skelton"></b-skeleton>
									<div class="serviceRow__details serviceData">
										<b-skeleton animation="fade" width="20%" height="25px"
											class="skelton"></b-skeleton>
										<div class="row">
											<div class="col-lg-3" v-for="(_, index) in 4" :key="index">
												<b-skeleton animation="fade" width="100%" height="25px"
													class="skelton"></b-skeleton>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div class="row" v-if="loading">
					<div class="col-lg-9">
						<b-skeleton animation="fade" width="100%" height="80px" class="skelton-card"></b-skeleton>
					</div>
					<div class="col-lg-9">
						<b-skeleton animation="fade" width="100%" height="80px" class="skelton-card"></b-skeleton>
					</div>
				</div>
				<div class="accordion" role="tablist" v-else>
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
						<div class="row" v-if="service && clientFileStatus(service) == 'rejected'">
							<div class="col-lg-12">
								<div class="contentBox notification">
									<div class="notification__icon">
										<svg-icon icon-id="clock-icon" icon-viewbox="0 0 72 72"></svg-icon>
									</div>
									<div class="notification__detail">
										<p>Sorry! The uploaded case files are rejected either for quality issue or some
											data are missing. Please upload new case files again.</p>
									</div>
								</div>
							</div>
						</div>
						<b-collapse id="serviceDetail" :visible="serviceCompleted ? false : true"
							accordion="my-accordion " role="tabpanel" v-if="activeOrderLine">
							<b-card-body>
								<div class="caseSteps accordion">
									<!-- 1 -->
									<div class="caseSteps__item completed">
										<div class="caseSteps__item--head" role="tab">
											<a href="javascript:void(0)" v-b-toggle.patient>
												<span class="counter">STEP 01</span>
												Select or Add Patient
											</a>
										</div>
										<b-collapse id="patient" visible accordion="my-accordion" role="tabpanel"
											v-model="collapseStates[0]">
											<div class="caseSteps__item--body">
												<div class="row">
													<div class="col-lg-12">
														<div class="caseSteps__item--subtitle">
															<p>
																Please select a patient or add a new patient.
															</p>
														</div>
													</div>
													<div class="col-lg-12">
														<add-patient :updateService="updateService" :service="service"
															:readOnly="serviceCompleted" />
														<div class="button-row" v-if="!serviceCompleted">
															<a href="#" class="btn btn-primary"
																:class="!currentService.patient ? 'disabled' : ''"
																v-on:click.stop.prevent="openStep(1)">
																{{ 'Next' }}
															</a>
														</div>
													</div>
												</div>
											</div>
										</b-collapse>
									</div>
									<!-- 1 -->
									<!-- 2 -->
									<div class="caseSteps__item completed">
										<div class="caseSteps__item--head" role="tab">
											<a href="javascript:void(0)"
												v-b-toggle="canGoToNextStep(2) ? 'defineCase' : ''">
												<span class="counter">STEP 02</span>
												Define Case
											</a>
										</div>
										<b-collapse id="defineCase" invisible accordion="my-accordion" role="tabpanel"
											v-model="collapseStates[1]">
											<div class="caseSteps__item--body">
												<div class="row">
													<div class="col-lg-9">
														<div class="caseSteps__item--subtitle">
															<p>
																Select the option that represents your case.
															</p>
															<a href="#">
																<svg-icon v-b-tooltip.hover
																	title="See how to define your case"
																	icon-id="info-circle"
																	icon-viewbox="0 0 24 24"></svg-icon>
																See how to define your case
															</a>
														</div>
													</div>
													<div class="col-lg-12">
														<div class="DefineCase">
															<div class="contentBox">
																<caseType :product="currentService.product"
																	:updateService="updateService" :service="service"
																	:readOnly="serviceCompleted" />
															</div>
															<div class="inline-btns-wrapper" v-if="!serviceCompleted">
																<a href="#" class="btn btn-primary"
																	:class="!currentService.caseType || (currentService.caseType.children.length > 0 && !currentService.patientType) ? 'disabled' : ''"
																	v-on:click.stop.prevent="openStep(2)">
																	{{ 'Next' }}
																</a>
																<a href="#" @click.stop.prevent="openStep(0)"
																	class="btn btn-secondary grey">
																	Back
																</a>
															</div>
														</div>
													</div>
												</div>
											</div>
										</b-collapse>
									</div>
									<!-- 2 -->

									<!-- 3 -->
									<div class="caseSteps__item completed">
										<div class="caseSteps__item--head" role="tab">
											<a href="javascript:void(0)"
												v-b-toggle="canGoToNextStep(3) ? 'uploadFile' : ''">
												<span class="counter">STEP 03</span>
												Upload Files
											</a>
										</div>
										<b-collapse id="uploadFile" invisible accordion="my-accordion" role="tabpanel"
											v-model="collapseStates[2]">
											<div class="caseSteps__item--body">
												<div class="row">
													<div class="col-lg-12">
														<div class="caseSteps__item--subtitle">
															<p>
																Upload the patient's required files and write your
																clinical notes
															</p>
														</div>
													</div>
													<div class="col-lg-12">
														<div class="uploadFiles">
															<div class="contentBox">
																<div class="inner-title" v-if="requiredFiles.length">
																	Upload the patient’s files
																	<svg-icon v-b-tooltip.hover
																		title="Upload the patient’s files"
																		icon-id="info-circle"
																		icon-viewbox="0 0 24 24"></svg-icon>
																</div>
																<div v-if="serviceCompleted">
																	<base-download-file
																		v-for="(file, index) in currentService.files"
																		:key="file.name + index"
																		:files="currentService.files"
																		:fileName="file.name" />
																</div>
																<base-upload-files v-else
																	v-for="(file, index) in requiredFiles"
																	:fileDefinition="{ ...file, 'slug': convertToSlug(file.name), 'type': 'file' }"
																	:key="index" :uploadFile="uploadFile"
																	:removeFile="removeFile" />
																<required-field v-if="fields.length" :fields="fields"
																	:updateService="updateService" :service="service"
																	:readOnly="serviceCompleted" />
																<div class="inner-title">
																	Files Notes
																	<svg-icon v-b-tooltip.hover title="Files Note"
																		icon-id="info-circle"
																		icon-viewbox="0 0 24 24"></svg-icon>
																</div>
																<div class="form-group">
																	<textarea class="form-control" v-model="filesNote"
																		:readonly="serviceCompleted"></textarea>
																	<label class="control-label">Notes <span
																			class="required"> (Required At Least 8
																			Characters) </span></label>
																</div>
																<div v-if="teethChart">
																	<div class="inner-title">
																		Choose teeth numbers
																		<svg-icon v-b-tooltip.hover
																			title="Implant Sites" icon-id="info-circle"
																			icon-viewbox="0 0 24 24"></svg-icon>
																	</div>
																	<div class="main-image text-center">
																		<implant :updateService="updateService"
																			:service="service"
																			:readOnly="serviceCompleted" />
																	</div>
																</div>
															</div>
															<div class="inline-btns-wrapper" v-if="!serviceCompleted">
																<a href="#" class="btn btn-primary"
																	:class="!canGoToNextStep('save') || loading || overlay ? 'disabled' : ''"
																	@click.prevent="saveService">
																	{{ 'Submit Service' }}
																</a>
																<a href="#" @click.stop.prevent="openStep(1)"
																	class="btn btn-secondary grey">
																	Back
																</a>
															</div>
														</div>
													</div>
												</div>
											</div>
										</b-collapse>
									</div>
									<!-- 3 -->
								</div>
							</b-card-body>
						</b-collapse>
					</b-card>
					<service-deliveries v-if="service && serviceCompleted" :data="service" />
					<service-shipping v-if="service && serviceCompleted" :data="service" />
				</div>
			</div>
			<div class="col-lg-4" style="position: relative;">
				<div class="contentBox p-0" style="position: sticky; top: 24px;" v-if="activeOrderLine">
					<chat  :id="String(activeOrderLine.id)" :user="userProfile.basket.owner.split('/')[8]" :contact="'admin'" :items="{source: service ? 'SERVICE' : 'ORDER', id: service ? service.id : activeOrderLine.id}"  />
				</div>
			</div>
		</div>
	</div>
</template>

<script>
// [*] Import UI Components
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import AddPatient from '@/components/newService/AddPatient.vue';
import caseType from '@/components/newService/caseType.vue';
import RequiredField from '@/components/newService/RequiredField.vue';
import Chat from '@/components/Chat/chat.vue';

import ServiceShipping from '@/components/newService/ServiceShipping.vue';
import ServiceDeliveries from '@/components/newService/ServiceDeliveries.vue';

import BaseUploadFiles from '@/common/components/base/BaseUploadFiles.vue';
import BaseDownloadFile from '@/common/components/base/BaseDownloadFile.vue';
import Implant from '@/components/service/partials/Implant.vue';

// [*] Import Breadcrumbs
import { continueServiceFlowBreadCrumbs } from "@/common/constant/breadCrumbs"

// [*] Vuex State Getter And Action Helper
import { serviceIsCompleted, clientDoctorFilesStatus, formatIds } from '@/common/helpers/index';

import { ServiceHelper } from '@/common/crud-helpers/service';
import { CommonHelper } from '@/common/crud-helpers/common';
import { mapGetters } from 'vuex';

export default {
	props: {
		type: String,
		index: String,
	},
	components: {
		BaseBreadCrumb,
		AddPatient,
		caseType,
		RequiredField,
		BaseUploadFiles,
		BaseDownloadFile,
		Implant,
		ServiceDeliveries,
		ServiceShipping,
		Chat,
	},
	data() {
		return {
			breadCrumbsItems: [...continueServiceFlowBreadCrumbs],
			collapseStates: [true, false, false],
			loading: true,

			activeOrderLine: null,
			service: null,

			requiredFiles: [],
			fields: [],
			teethChart: false,
			filesNote: null,

			currentService: {
				product: null,
				patient: null,
				patientNote: null,
				caseType: null,
				patientType: null,
				files: [],
				filesNote: null,
				implant: null,
				fields: []
			},

			serviceCompleted: false,

		};
	},
	mounted() {
		ServiceHelper.getPatients({});
		this.type == 'order'
			? ServiceHelper.getActiveOrderLine(Number.parseInt(this.index))
			: ServiceHelper.getServiceDetail(Number.parseInt(this.index))
	},
	computed: {
		...mapGetters(['userProfile', 'orderLine', 'patients', 'serviceList', 'serviceDetail', 'overlay']),
	},
	watch: {
		serviceDetail() {
			this.activeOrderLine = this.serviceDetail.order_line_obj
			this.service = this.serviceDetail
			if ('service_data' in this.service && this.service.service_data != null) {
				this.currentService = { ...this.currentService, ...this.service.service_data, }
				this.filesNote = this.serviceDetail.service_data.filesNote
			}
		},
		orderLine() {
			this.activeOrderLine = this.orderLine
			this.currentService.product = this.orderLine.product_obj
			ServiceHelper.getServices({});
		},
		serviceList() {
			if (this.activeOrderLine) {
				let results = this.serviceList.filter((service) => service.order_line == this.activeOrderLine.id)
				if (results.length > 0) {
					this.service = results[0]
					if ('service_data' in this.service && this.service.service_data != null) {
						this.currentService = { ...this.currentService, ...results[0].service_data, }
						this.filesNote = results[0].service_data.filesNote
					}
				}
				else {
					this.loading = false
				}
			}
		},
		currentService() {
			if (this.currentService.caseType) {
				if (this.currentService.caseType.children.length == 0) {
					this.requiredFiles = this.currentService.caseType.required_files
					this.fields = this.currentService.caseType.children
					this.teethChart = this.currentService.caseType.teeth_chart
				}
				else {
					if (this.currentService.patientType) {
						this.requiredFiles = this.currentService.patientType.required_files
						this.fields = this.currentService.patientType.children
						this.teethChart = this.currentService.patientType.teeth_chart
					}
				}
			}
			if (this.service && serviceIsCompleted(this.service)) {
				if (clientDoctorFilesStatus(this.service) != 'rejected') {
					this.serviceCompleted = true
					this.collapseStates = [false, false, false]
				}
				else {
					this.collapseStates = [false, false, true]
				}
			}
			this.loading = false
		},
		filesNote() {
			this.updateService({ filesNote: this.filesNote })
		},
	},
	methods: {
		formatId(id) {
			return '#' + formatIds(id)
		},
		openStep(index) {
			this.collapseStates.splice(index, 1, true);
		},
		canGoToNextStep(stepNumber) {
			if (stepNumber == 2) {
				if (this.currentService.patient) {
					return true;
				}
				return false
			}
			else if (stepNumber == 3) {
				if ((this.currentService.caseType && this.currentService.caseType.children.length == 0) ||
					(this.currentService.caseType && this.currentService.caseType.children.length > 0 && this.currentService.patientType)
				) {
					return true
				}
				return false
			}
			else if (stepNumber == 'save') {
				let allrequiredFileExist = true
				this.requiredFiles.forEach((reqFile) => {
					if (reqFile.is_required) {
						let index = this.currentService.files.findIndex((file) => file.name == reqFile.name)
						allrequiredFileExist = index == -1 ? false : true
					}
				})

				let allRequiredFieldsSeted = true
				this.currentService.fields.forEach((collection) => {
					collection.required_fields.forEach((field) => {
						if (field.is_required && (!('value' in field) || field.value == null || field.value == "")) {
							allRequiredFieldsSeted = false
						}
					})
				})

				let teetChartRequired = this.teethChart
				if (allRequiredFieldsSeted && !teetChartRequired && allrequiredFileExist && this.currentService.caseType) {
					return true
				}
				else if (allRequiredFieldsSeted && teetChartRequired && allrequiredFileExist && this.currentService.caseType && this.currentService.implant) {
					return true
				}
				return false
			}
		},
		convertToSlug(Text) {
			return 'file-' + Text
				.toLowerCase()
				.replace(/ /g, '-')
				.replace(/[^\w-]+/g, '');
		},
		updateService(data) {
			this.currentService = { ...this.currentService, ...data }
		},
		async uploadFile(data) {
			this.removeFile(data)
			if (this.service) {
				let file = await ServiceHelper.pushServiceFile({
					...data,
					'name': data.name,
					'service': this.service.id,
					'files': this.service.files
				})
				this.updateService({
					files: [...this.currentService.files, { ...data, ...file, value: file.file }],
				})
			}
			this.updateService({
				files: [...this.currentService.files, { ...data }],
			})
		},
		removeFile(data) {
			this.updateService({ files: this.currentService.files.filter((file) => file.name != data.name) })
		},
		async saveService() {
			if (!this.service) {
				let serviceId = await ServiceHelper.addService({
					"product": this.currentService.product.id,
					"patient": this.currentService.patient.id,
					"order_line": this.activeOrderLine.id,
					"service_data": {
						...this.currentService,
						'created': Date.now().toString(),
						'files_status': 'waiting'
					}
				})
				if (serviceId) {
					this.$router.push({
						name: 'continue-service-flow',
						params: { lang: this.$i18n.locale, type: 'service', index: String(serviceId), },
					})
				}

			}
			else {
				await ServiceHelper.updateServiceData({
					serviceId: this.service.id,
					service_data: {
						...this.currentService,
						'modified': Date.now().toString(),
						'files_status': 'waiting'
					},
				})
			}
		},
		clientFileStatus(service) {
			return clientDoctorFilesStatus(service)
		},
		getProductOption(url) {
			let options = this.activeOrderLine.product_obj.product_options.filter((option) => option.url == url)
			if(options.length < 1) return null;
			return options[0]
		}
	}
};
</script>

<style lang="scss" scoped>
.serviceFlow {
	.required {
		font-size: rem(11px);
		font-weight: normal;
	}

	.skelton {
		border-radius: 6px;
	}

	.skelton-card {
		border-radius: 12px;
		margin-top: rem(35px);
	}

	.options {
		text-transform: capitalize;
		span {
			color: var(--textPrimary);
		}
		.title {
			display: flex;
			align-content: center;
			padding-bottom: rem(12px);
		}
	}

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

