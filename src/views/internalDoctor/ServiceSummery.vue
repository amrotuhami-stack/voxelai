<template>
	<div class="serviceFlow">
		<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
		<h1 class="main-title">Service Summary</h1>
		<div class="row">
			<div class="col-lg-8">
				<div class="contentBox" v-if="service">
					<div class="serviceRow">
						<div class="serviceRow__image">
							<img v-if="service.order_line_obj.product_obj.images.length > 0"
								:src="service.order_line_obj.product_obj.images[0].original" alt="" class="img-fluid" />
						</div>
						<div class="serviceRow__title">
							{{ service.order_line_obj.product_obj.title }}
							<div class="serviceRow__details serviceData">
								<router-link class="viewMore"
									:to="{ name: 'product-details', params: { lang: $i18n.locale, productId: String(service.order_line_obj.product_obj.id) }, }">
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
									<div class="col-lg-3" v-if="service">
										<div class="item">
											<p>{{ service.created | formatDate }}</p>
											<span>Created At</span>
										</div>
									</div>
									<div class="col-lg-3">
										<div class="item">
											<p>{{ formatId(service.order_line_obj.id) }}</p>
											<span>Order ID</span>
										</div>
									</div>
									<div class="col-lg-3">
										<div class="item">
											<p>{{ service.patient_obj.first_name + " " +
												service.patient_obj.last_name }}</p>
											<span>Patient Name</span>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>

				<div class="contentBox" v-if="!service">
					<div class="serviceRow">
						<div class="serviceRow__image p-0">
							<b-skeleton animation="fade" width="100%" height="100px" class="skelton"></b-skeleton>
						</div>
						<div class="serviceRow__title">
							<b-skeleton animation="fade" width="50%" height="25px" class="skelton"></b-skeleton>
							<div class="serviceRow__details serviceData">
								<b-skeleton animation="fade" width="20%" height="25px" class="skelton"></b-skeleton>
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
			<div class="col-lg-4">
				<div class="activityCard card" :class="`orange`">
					<div class="card__body">
						<div class="activityCard__item">
							<div class="activityCard__item--value">{{ userProfile.dashboard.not_started }}</div>
							<div class="activityCard__item--label">Not Started Services</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div class="row mt-3">
			<div class="col-lg-8">
				<div class="contentBox p-3" v-if="service">
					<div class="row">
						<div class="col-lg-2" style="display: flex; align-items: center; justify-content: center;">
							<label class="options">
								<span> Order Options</span>
							</label>
						</div>
						<div class="col-lg-10">
							<div class="checkbox pt-2" v-if="service.order_line_obj.attributes">
								<div class="row">
									<div class="col-lg-12 mb-2"
										v-for="(attribute, index) in service.order_line_obj.attributes" :key="index">
										<label class="options" v-if="getProductOption(attribute.option)">
											<input type="checkbox" disabled
												:name="getProductOption(attribute.option).code"
												:checked="attribute.value == '1'" />
											<span class="pb-1">
												{{ getProductOption(attribute.option).name }}
											</span>
										</label>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div class="row" v-if="loading">
					<div class="col-lg-12">
						<b-skeleton animation="fade" width="100%" height="80px" class="skelton-card"></b-skeleton>
					</div>
					<div class="col-lg-12">
						<b-skeleton animation="fade" width="100%" height="80px" class="skelton-card"></b-skeleton>
					</div>
				</div>
				<div class="accordion" role="tablist">
					<service-details v-if="service" :service="service" />
					<service-results v-if="service && serviceDataApproved" :data="service" />
					<!--<service-shipping v-if="service && serviceDataApproved" :data="service"/> !-->
				</div>
			</div>
			<div class="col-lg-4" style="position: relative;">
				<div class="contentBox p-0" style="position: sticky; top: 24px;" v-if="service && service.order_line_obj">
					<chat :id="String(service.order_line_obj.id)" :user="'admin'" :contact="String(service.owner)" :items="{source: 'SERVICE', id: service.id}"/>
				</div>
			</div>
		</div>
	</div>

</template>

<script>
// [*] Import UI Components
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import ServiceDetails from '@/components/InternalDoctor/ServiceSummery/ServiceDetails.vue';
import ServiceResults from '@/components/InternalDoctor/ServiceSummery/ServiceResults.vue';
import ServiceShipping from '@/components/newService/ServiceShipping.vue';
import Chat from '@/components/Chat/chat.vue';

// [*] Import Breadcrumbs
import { internalDoctorServiceSummeryBreadCumbs } from "@/common/constant/breadCrumbs"

// [*] Vuex State Getter And Action Helper
import { ServiceHelper } from '@/common/crud-helpers/service';
import { mapGetters } from 'vuex';

// [*] Vuex State Getter And Action Helper
import { serviceIsCompleted, clientDoctorFilesStatus, formatIds } from '@/common/helpers/index';

export default {
	props: {
		serviceId: String,
	},
	components: {
		BaseBreadCrumb,
		ServiceDetails,
		ServiceResults,
		ServiceShipping,
		Chat,
	},
	data() {
		return {
			loading: true,
			breadCrumbsItems: [...internalDoctorServiceSummeryBreadCumbs],
			service: null,
			serviceDataApproved: false,
		};
	},
	mounted() {
		ServiceHelper.getServiceDetail(this.serviceId)
	},
	computed: {
		...mapGetters(['serviceDetail', 'userProfile']),
	},
	watch: {
		serviceDetail() {
			this.service = this.serviceDetail
			this.loading = false
			if (serviceIsCompleted(this.service) &&
				clientDoctorFilesStatus(this.service) != 'waiting' &&
				clientDoctorFilesStatus(this.service) != 'rejected'
			) {
				this.serviceDataApproved = true
			}
		}
	},
	methods: {
		formatId(id) {
			return '#' + formatIds(id)
		},
		getProductOption(url) {
			let options = this.service.order_line_obj.product_obj.product_options.filter((option) => option.url == url)
			if(options.length < 1) return null;
			return options[0]
		}
	}
};
</script>

<style lang="scss" scoped>
.activityCard {
	height: 100%;

	@media screen and (max-width: 767px) {
		margin-bottom: 15px !important;
		text-align: center;

		.card__body {
			padding-left: rem(15px);
			padding-right: rem(15px);
		}
	}

	&__item {
		&--value {
			font-size: rem(46px);
			font-weight: 500;
			color: var(--textPrimary);
			margin: rem(8px) 0 rem(14px) 0;

			@media screen and (max-width:767px) {
				font-size: rem(35px);
			}
		}

		&--label {
			font-size: rem(16px);
			font-weight: 400;
			color: var(--default);
		}
	}

	&.orange {
		background: rgba(236, 171, 8, 0.12);
		;
		--borderColor: rgba(236, 171, 8, 0.5);
	}
}

.serviceFlow {
	.skelton {
		border-radius: 6px;
	}

	.skelton-card {
		border-radius: 12px;
		margin-top: rem(35px);
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