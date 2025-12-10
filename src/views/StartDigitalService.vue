<template>
	<div>
		<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
		<h1 class="main-title">Start New Digital Service</h1>
		<div class="row">
			<div class="col-lg-8">
				<div class="row">
					<div class="col-lg-12">
						<div class="contentBox">
							<div class="serviceRow" v-if="productDetail && item">
								<div class="serviceRow__image" v-if="productDetail.images">
									<img :src="productDetail.images[0].original" alt="" class="img-fluid" />
								</div>
								<div class="serviceRow__title" v-if="userProfile">
									<span>{{ productDetail.title }}</span>
									<div class="checkbox serviceRow__title" v-if="item && productDetail.product_options"
										style="padding-top: 10px;">
										<label v-for="(attribute, index) in sortAttributes" :key="index"
											class="options">
											<input type="checkbox" :name="attribute.option_obj.code"
												@click.prevent="updateOption(attribute, $event)"
												:checked="attribute.value == '1' ? true : false" />
											<span>
												<div class="item">
													{{ attribute.option_obj.name + " - " }}
													<money-format :value="Number(attribute.option_obj.price)"
														:locale='`en`' :currency-code='userProfile.default_currency'
														:subunits-value=false :hide-subunits=true>
													</money-format>
												</div>
											</span>
										</label>
									</div>
								</div>
							</div>
							<div class="serviceRow" v-else>
								<div class="serviceRow__image p-0">
									<b-skeleton animation="fade" width="100%" height="100px"
										class="skelton"></b-skeleton>
								</div>
								<div class="serviceRow__title">
									<b-skeleton animation="fade" width="50%" height="25px" class="skelton"></b-skeleton>
									<div class="serviceRow__details serviceData">
										<b-skeleton animation="fade" width="20%" height="25px"
											class="skelton"></b-skeleton>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
				<!-- accordion -->
				<div class="row" v-if="!item">
					<div style="margin-top: 35px;" v-for="(_, index) in 5" :key="index">
						<b-skeleton animation="fade" width="5%" height="30px" class="skelton"></b-skeleton>
						<b-skeleton animation="fade" width="50%" height="35px" class="skelton mt-2"></b-skeleton>
						<b-skeleton animation="fade" width="20%" height="30px" class="skelton mt-2"></b-skeleton>
					</div>
				</div>
				<div class="caseSteps accordion" role="tablist" v-if="item">
					<!-- 1 -->
					<div class="caseSteps__item completed">
						<div class="caseSteps__item--head" role="tab">
							<a href="javascript:void(0)" v-b-toggle.patients>
								<span class="counter">STEP 01</span> Select or Add Patient
							</a>
						</div>
						<b-collapse id="patients" visible accordion="services" role="tabpanel"
							v-model="collapseStates[0]">
							<div class="caseSteps__item--body">
								<div class="row">
									<div class="col-lg-12">
										<div class="caseSteps__item--subtitle">
											<p>Please select a patient or add a new patient</p>
										</div>
									</div>
									<div class="col-lg-12">
										<add-patient :updateService="updateService" />
										<div class="button-row">
											<a href="javascript:void(0);" class="btn btn-primary"
												:class="!canGoToNextStep(2) ? 'disabled' : ''"
												v-on:click.stop.prevent="openStep(1, 'next')">
												Next
											</a>
										</div>
									</div>
								</div>
							</div>
						</b-collapse>
					</div>
					<!-- 1 -->

					<!-- 2 -->
					<div class="caseSteps__item">
						<div class="caseSteps__item--head" role="tab">
							<a href="javascript:void(0)" v-b-toggle="canGoToNextStep(2) ? 'defineCase' : ''">
								<span class="counter">STEP 02</span> Define Case
							</a>
						</div>
						<b-collapse id="defineCase" invisible accordion="services" role="tabpanel"
							v-model="collapseStates[1]">
							<div class="caseSteps__item--body">
								<div class="row">
									<div class="col-lg-12">
										<div class="caseSteps__item--subtitle">
											<p>Select the option that represents your case</p>
											<a href="#">
												<svg-icon v-b-tooltip.hover title="See how to define your case"
													icon-id="info-circle" icon-viewbox="0 0 24 24"></svg-icon>
												See how to define your case
											</a>
										</div>
									</div>
									<div class="col-lg-12">
										<div class="DefineCase">
											<div class="contentBox">
												<caseType :product="productDetail" :updateService="updateService" />
											</div>
											<div class="inline-btns-wrapper">
												<div class="inline-btns">
													<a href="#" @click.stop.prevent="openStep(2, 'next')"
														class="btn btn-primary"
														:class="!canGoToNextStep(3) ? 'disabled' : ''">
														Next
													</a>
													<a href="#" @click.stop.prevent="openStep(2, 'skip')">
														Skip for now
													</a>
												</div>
												<a href="#" @click.stop.prevent="openStep(0, 'back')"
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
					<div class="caseSteps__item">
						<div class="caseSteps__item--head" role="tab">
							<a href="javascript:void(0)"
								v-b-toggle="canGoToNextStep(3) && !serviceData.skipStep2 ? 'uploadFiles' : ''">
								<span class="counter">STEP 03</span> Upload Files
							</a>
						</div>
						<b-collapse id="uploadFiles" visible accordion="services" role="tabpanel"
							v-model="collapseStates[2]">
							<div class="caseSteps__item--body">
								<div class="row">
									<div class="col-lg-12">
										<div class="caseSteps__item--subtitle">
											<p>Upload the patient's required files and write your clinical notes</p>
										</div>
									</div>
									<div class="col-lg-12">
										<div class="uploadFiles">
											<div class="contentBox">
												<div class="inner-title">
													Upload the patient’s files
													<svg-icon v-b-tooltip.hover title="Upload the patient’s files"
														icon-id="info-circle" icon-viewbox="0 0 24 24"></svg-icon>
												</div>
												<base-upload-files v-for="(file, index) in files"
													:fileDefinition="{ ...file, 'slug': convertToSlug(file.name), 'type': 'file' }"
													:key="index" :uploadFile="uploadFile" :removeFile="removeFile" />
												<required-field v-if="fields.length" :fields="fields"
													:updateService="updateService" />
												<div class="inner-title">
													Files Notes
													<svg-icon v-b-tooltip.hover title="Files Note" icon-id="info-circle"
														icon-viewbox="0 0 24 24"></svg-icon>
												</div>
												<div class="form-group">
													<textarea class="form-control" v-model="filesNote"
														:readonly="false"></textarea>
													<label class="control-label">Notes </label>
												</div>
												<div v-if="teethChart">
													<div class="inner-title">
														Choose teeth numbers
														<svg-icon v-b-tooltip.hover title="Implant Sites"
															icon-id="info-circle" icon-viewbox="0 0 24 24"></svg-icon>
													</div>
													<div class="main-image text-center">
														<implant :updateService="updateService" />
													</div>
												</div>
											</div>
											<div class="inline-btns-wrapper">
												<div class="inline-btns">
													<a href="#" class="btn btn-primary"
														:class="!canGoToNextStep(4) ? 'disabled' : ''"
														@click.stop.prevent="openStep(3, 'next')">
														Next
													</a>
													<a href="#" @click.stop.prevent="openStep(3, 'skip')">
														Skip for now
													</a>
												</div>
												<a href="#" @click.stop.prevent="openStep(1, 'back')"
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

					<!-- 4 -->
					<div class="caseSteps__item">
						<div class="caseSteps__item--head" role="tab">
							<a href="javascript:void(0)"
								v-b-toggle="canGoToNextStep(4) || serviceData.skipStep3 ? 'billing' : ''">
								<span class="counter">STEP 04</span> Create Billing Account
							</a>
						</div>
						<b-collapse id="billing" invisible accordion="services" role="tabpanel"
							v-model="collapseStates[3]">
							<div class="caseSteps__item--body">
								<div class="row">
									<div class="col-lg-12">
										<div class="caseSteps__item--subtitle">
											<p>Add your billing and shipping address</p>
										</div>
									</div>
								</div>
								<div class="col-lg-12">
									<checkout />
								</div>
							</div>
						</b-collapse>
					</div>
					<!-- 4 -->

					<!-- 5 -->
					<div class="caseSteps__item">
						<div class="caseSteps__item--head" role="tab">
							<a href="javascript:void(0)" v-b-toggle="canGoToNextStep(5) ? 'confirmation' : ''">
								<span class="counter">STEP 05</span> Confirm Payment
							</a>
						</div>
						<b-collapse id="confirmation" invisible accordion="services" role="tabpanel"
							v-model="collapseStates[4]">
							<div class="caseSteps__item--body">
								<div class="row">
									<div class="col-lg-12">
										<div class="caseSteps__item--subtitle">
											<p>Choose your payment method and pay</p>
										</div>
									</div>
								</div>
								<div class="row" v-if="shippingMethods">
									<div class="col-lg-12">
										<confirm-payment />
									</div>
								</div>
							</div>
						</b-collapse>
					</div>
					<!-- 5 -->
				</div>
				<!-- accordion -->
			</div>
			<div class="col-lg-4" style="position: relative;">
				<div class="contentBox p-0" style="position: sticky; top: 24px;"  v-if="serviceData.product">
					<chat :id="`SD-${productId}-${userProfile.id}`" :user="String(userProfile.id)" :contact="'admin'" :items="{source: 'START-DIGTAL', id: String(serviceData.product.id)}"/>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
// [*] Import UI Components .
import MoneyFormat from 'vue-money-format'
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import Services from '@/components/service/Services.vue';
import AddPatient from '@/components/newService/AddPatient.vue';
import caseType from '@/components/newService/caseType.vue';
import RequiredField from '@/components/newService/RequiredField.vue';

import BaseUploadFiles from '@/common/components/base/BaseUploadFiles.vue';
import Implant from '@/components/service/partials/Implant.vue';
import Checkout from "@/components/NewAISteps/checkout.vue"
import ConfirmPayment from '../components/NewAISteps/confirmPayment.vue';
import Chat from '@/components/Chat/chat.vue';

// [*] Import Breadcrumbs
import { startDigitalServiceBreadCrumbs } from "@/common/constant/breadCrumbs"

// [*] Vuex State Getter And Action Helper
import { mapGetters } from 'vuex';
import { CatalogueHelper } from '@/common/crud-helpers/catalogue';
import { BasketHelper } from '@/common/crud-helpers/basket';
import { CheckoutHelper } from '@/common/crud-helpers/checkout';
import { v1 as uuidv1 } from 'uuid';

export default {
	props: {
		productId: String,
	},
	components: {
		BaseBreadCrumb,
		AddPatient,
		Services,
		caseType,
		RequiredField,
		Chat,

		BaseUploadFiles,
		MoneyFormat,
		Implant,
		Checkout,
		ConfirmPayment,
	},
	data() {
		return {
			breadCrumbsItems: [...startDigitalServiceBreadCrumbs],
			collapseStates: [true, false, false, false, false],

			firstRender: false,

			item: null,
			sortAttributes: [],

			teethChart: false,
			files: [],
			fields: [],
			filesNote: null,

			serviceData: {
				product: null,
				patient: null,
				patientNote: null,
				caseType: null,
				patientType: null,
				files: [],
				filesNote: null,
				implant: null,
				skipStep2: false,
				skipStep3: false,
				fields: []
			},
		};
	},
	mounted() {
		this.getProductDetail()
	},
	created() {
		this.firstRender = true
	},
	computed: {
		...mapGetters(['productDetail', 'cartLines', 'userProfile', 'shippingMethods']),
	},
	watch: {
		productDetail() {
			if (this.productDetail) BasketHelper.getCart();
			this.serviceData.product = this.productDetail
		},
		cartLines() {
			if (!this.productDetail) return
			if (this.firstRender && this.cartLines.length == 0) {
				this.addToCart(this.productDetail.url, this.productDetail.product_options)
			}
			else {
				let index = this.cartLines.findIndex((item) => item.product_obj.id == this.productId)
				if (index === -1 && this.firstRender) {
					this.addToCart(this.productDetail.url, this.productDetail.product_options)
				}
				else {
					this.item = this.cartLines[index]
					if (this.item.attributes)
						this.sortAttributes = [...this.item.attributes].sort((a, b) => a.id - b.id)
				}
			}
		},
		shippingMethods() {
			if (this.shippingMethods.length > 0) {
				this.collapseStates = [false, false, false, false, true];
			}
		},
		serviceData() {
			if (this.serviceData.caseType) {
				if (this.serviceData.caseType.children.length == 0) {
					this.files = this.serviceData.caseType.required_files
					this.fields = this.serviceData.caseType.children
					this.teethChart = this.serviceData.caseType.teeth_chart
				}
				else {
					if (this.serviceData.patientType) {
						this.files = this.serviceData.patientType.required_files
						this.teethChart = this.serviceData.patientType.teeth_chart
						this.fields = this.serviceData.patientType.children
					}
				}
			}
		},
		filesNote() {
			this.updateService({ filesNote: this.filesNote })
		}
	},
	methods: {
		getProductDetail() {
			CatalogueHelper.getProductDetail({ id: Number(this.productId) })
		},
		addToCart: function (url, options) {
			let params = { "quantity": 1, "url": url }
			if (options.length > 0) params["options"] = options.map(item => ({ "option": item.url, "value": 0 }))
			BasketHelper.addCart(params)
		},
		openStep(index, action) {
			if (index === 2) {
				this.updateService({ skipStep2: action == 'skip' ? true : false })
			}
			if (index === 3) {
				this.updateService({ skipStep3: action == 'skip' ? true : false })
			}
			if (index === 2 && action == 'skip') {
				this.collapseStates = [false, false, false, true, false];
			}
			else {
				this.collapseStates.splice(index, 1, true);
			}
		},
		canGoToNextStep(stepNumber) {
			if (stepNumber == 2) {
				if (this.serviceData.patient && this.productDetail.case_definitions.length > 0
				) {
					return true;
				}
				return false
			}
			else if (stepNumber == 3) {
				if ((this.serviceData.caseType && this.serviceData.caseType.children.length == 0) ||
					(this.serviceData.caseType && this.serviceData.caseType.children.length > 0 && this.serviceData.patientType)
				) {
					return true
				}
				return false
			}
			else if (stepNumber == 4) {
				let allrequiredFileExist = true
				this.files.forEach((reqFile) => {
					if (reqFile.is_required) {
						let index = this.serviceData.files.findIndex((file) => file.name == reqFile.name)
						allrequiredFileExist = index == -1 ? false : true
					}
				})

				let allRequiredFieldsSeted = true
				this.serviceData.fields.forEach((collection) => {
					collection.required_fields.forEach((field) => {
						if (field.is_required && (!('value' in field) || field.value == null || field.value == "")) {
							allRequiredFieldsSeted = false
						}
					})
				})


				let teetChartRequired = this.teethChart
				if (allRequiredFieldsSeted && !teetChartRequired && allrequiredFileExist && this.serviceData.caseType) {
					return true
				}
				else if (allRequiredFieldsSeted && teetChartRequired && allrequiredFileExist && this.serviceData.caseType && this.serviceData.implant) {
					return true
				}
				return false
			}
			else if (stepNumber == 5) {
				if (this.shippingMethods && this.shippingMethods.length > 0) {
					return true
				}
				return false
			}
		},
		updateOption(attribute, event) {
			let params = {
				"basket_id": this.item.basket_id,
				"lineId": this.item.id,
				"attrId": attribute.id,
				"option": attribute.option,
				"value": event.target.checked ? 1 : 0
			}
			BasketHelper.updateCartLineAttr(params)
		},
		convertToSlug(Text) {
			return 'file-' + Text
				.toLowerCase()
				.replace(/ /g, '-')
				.replace(/[^\w-]+/g, '');
		},
		updateService(data) {
			this.serviceData = { ...this.serviceData, ...data }
			if (this.serviceData.skipStep2)
				CheckoutHelper.loadDigitalProductData({
					...this.serviceData,
					caseType: null,
					patientType: null,
					implant: null,
					files: [],
					filesNote: null,
				})
			else if (this.serviceData.skipStep3) {
				CheckoutHelper.loadDigitalProductData({
					...this.serviceData,
					implant: null,
					files: [],
					filesNote: null,
				})
			}
			else {
				CheckoutHelper.loadDigitalProductData(this.serviceData)
			}
		},
		uploadFile(data) {
			this.removeFile(data)
			this.updateService({ files: [...this.serviceData.files, data] })
		},
		removeFile(data) {
			this.updateService({ files: this.serviceData.files.filter((file) => file.name != data.name) })
		}
	},
};
</script>

<style lang="scss" scoped>
.skelton {
	border-radius: 6px;
}

.skelton-card {
	border-radius: 12px;
	margin-top: rem(35px);
}

.options {
	width: 100%;
	text-transform: capitalize;

	.item {
		display: flex;
		justify-items: start;
	}
}

.required {
	font-size: rem(11px);
	font-weight: normal;
}

.inline-btns-wrapper {
	.btn.btn-primary {
		padding-left: rem(45px);
		padding-right: rem(45px);
	}

	.btn.grey {
		padding-left: rem(50px);
		padding-right: rem(50px);
	}
}

.DefineCase,
.uploadFiles {
	.inline-btns-wrapper {
		@media screen and (max-width: 767px) {
			flex-direction: row;

			.inline-btns {
				.btn {
					&.btn-primary {
						margin-bottom: 0;
					}
				}
			}
		}

		@media screen and (max-width: 575px) {
			justify-content: space-between;
			flex-wrap: wrap;

			.inline-btns {
				@include flex(center, space-between);
				width: 100%;
			}

			.btn-secondary {
				&.grey {
					width: 100%;
				}
			}
		}
	}
}

.totalSummary {
	.card__head {
		padding: rem(27px) rem(24px);
	}

	.totalSummary__item {
		display: flex;
		justify-content: space-between;
		align-items: center;

		&:not(:first-child) {
			border-bottom: 1px solid var(--borderColor);
		}

		p:nth-child(2) {
			color: #000 !important;
			font-size: rem(20px) !important;

			@media screen and (max-width:1199px) and (min-width:992px) {
				font-size: rem(18px) !important;
			}
		}

		p {
			font-size: rem(14px);
			color: var(--textSecondary);
			margin-bottom: rem(16px);
			padding-right: 5px;
		}

		&--total {
			display: flex;
			align-items: center;
			justify-content: space-between;
			margin-top: rem(27px);

			p {
				font-weight: 500;
				font-size: rem(20px);
				color: #171716;
				margin-bottom: 0;

				@media screen and (max-width:1025px) and (min-width:992px) {
					font-size: rem(18px);
				}
			}

			.total__price {
				font-size: rem(24px);
				color: #171716;
				font-weight: 500;

				@media screen and (max-width:1025px) and (min-width:992px) {
					font-size: rem(20px);
				}
			}
		}
	}

}
</style>


/*
'countryShippingCost','selectedPatient', 'serviceData', 'uploadedFiles', 'implantDate'
updateAddress(){
this.openStep(4);
if ( !this.differentShippingAddress ){
this.shippingAddress = this.billingAddress;
};
this.shipping_price = Number(this.countryShippingCost[this.shippingAddress.country]["cost"]);
this.total_price = Number(this.productDetail.price_availability.price.excl_tax) + this.shipping_price;
this.purchaseData = {
target: "pay_digital_service", productId: this.productDetail.id, options: this.selectedOptions,
billingAddress: this.billingAddress, shippingAddress: this.shippingAddress, selectedPatient: this.selectedPatient,
serviceData: this.serviceData, PatientTypeSlug: this.PatientTypeSlug, uploadedFiles: this.uploadedFiles,
implantDate:this.implantDate
};
} */