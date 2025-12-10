<template>
	<div>
		<div class="patientRecord">
			<base-offer-notifications />
			<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
			<h1 class="main-title">Start New Service</h1>
			<div class="contentBox">
				<div
					class="serviceRow"
					v-for="item in service"
					:key="item.index"
				>
					<div class="serviceRow__image">
						<img
							:src="`${require(`@/assets/images/shoppingCart/${item.image}`)}`"
							alt=""
							class="img-fluid"
						/>
					</div>
					<div class="serviceRow__title">
						{{ item.title }}
						<div
							class="serviceRow__cases"
							v-if="item.remaining == true"
						></div>
						<div
							class="serviceRow__details"
							v-if="item.details == true"
						>
							<a href="#" class="viewMore"
								>{{ item.detail }}
								<font-awesome-icon
									:icon="['fa', 'angle-right']"
							/></a>
						</div>
					</div>
					<div class="serviceRow__progress">
						<b-progress :value="value" :max="max"></b-progress>
						<div
							class="
								d-flex
								justify-content-between
								align-items-center
							"
						>
							<div class="serviceRow__cases--remaining">
								<span>{{ item.case }} </span
								>{{ item.remainingCase }}
								<svg-icon
									v-b-tooltip.hover
									title="cases remaining"
									icon-id="info-circle"
									icon-viewbox="0 0 24 24"
								></svg-icon>
							</div>
							<div class="serviceRow__cases--duration">
								{{ item.duration }}
							</div>
						</div>
					</div>
					<div class="serviceRow__link" v-if="item.links == true">
						<a href="#" class="btn btn-default">{{ item.link }}</a>
					</div>
				</div>
			</div>
			<div class="pageHead">
				<div class="textWrapper">
					<h2>Add Patient Record</h2>
					<p>
						Lorem Ipsum is simply dummy text of the printing
						industry.
					</p>
				</div>
				<a href="#" class="btn btn-primary" v-b-modal="'addrecord'">
					<span class="icon">
						<svg-icon
							icon-id="plus-icon"
							icon-viewbox="0 0 17 18"
						></svg-icon>
					</span>
					New Record
				</a>
			</div>
			<!-- add patient filters -->
			<add-patient-filters />
			<div class="contentBox allCases">
				<button
					:class="toggleDropDown ? 'active' : ''"
					@click="toggleDropDown = !toggleDropDown"
					type="button"
					class="toggleTab d-none btn btn-secondary grey"
					aria-label="mobile category tabs"
				>
					All
				</button>
				<div
					class="responsiveFilters"
					:class="toggleDropDown ? 'active' : ''"
				>
					<b-tabs pills>
						<b-tab title="Case Photos" active>
							<case-photos-upload />
						</b-tab>
						<b-tab title="Digitization">2</b-tab>
						<b-tab title="Analysis">3</b-tab>
						<b-tab title="Assessment">4</b-tab>
						<b-tab title="Treatment">5</b-tab>
					</b-tabs>
				</div>
				<div class="case">
					<svg-icon
						icon-id="case-icon"
						icon-viewbox="0 0 24 24"
					></svg-icon>
					Case Summary
				</div>
			</div>
		</div>
		<!-- Add Patient Record PopUp-->
		<b-modal ref="my-modal" id="addpatient" centered>
			<div class="modal-title">Add New Patient</div>
			<p>Voxel is created for every dental practitioner.</p>
			<form>
				<div class="row">
					<div class="col-sm-6">
						<div class="form-group">
							<input
								type="text"
								class="form-control"
								required=""
								name="First name"
								placeholder="First name"
							/>
							<label class="control-label">First name</label>
						</div>
					</div>
					<div class="col-sm-6">
						<div class="form-group">
							<div class="form-group">
								<input
									type="text"
									class="form-control"
									required=""
									name="Last name"
									placeholder="Last name"
								/>
								<label class="control-label">Last name</label>
							</div>
						</div>
					</div>
					<div class="col-sm-6">
						<div class="form-group">
							<input
								type="text"
								class="form-control"
								required=""
								name="Age"
								placeholder="Age"
							/>
							<label class="control-label">Age</label>
						</div>
					</div>
					<div class="col-sm-6">
						<div class="form-group no-label">
							<b-form-select
								v-model="selected"
								:options="gender"
							></b-form-select>
						</div>
					</div>
				</div>
				<div class="inline-buttons">
					<button type="button" class="btn btn-primary">Add</button>
					<a href="javascript:void(0)" @click="hideModal" class="link"
						>Cancel</a
					>
				</div>
			</form>
		</b-modal>
		<!-- New Record PopUp-->
		<b-modal ref="my-modal" id="addrecord" centered>
			<div class="modal-title">Add New Record</div>
			<p>(yyyy-mm-dd)</p>
			<form>
				<div class="form-group">
					<div class="form-group">
						<input
							type="text"
							class="form-control"
							required=""
							name="Last name"
							placeholder="Last name"
						/>
						<label class="control-label">Date</label>
					</div>
				</div>
				<div class="inline-buttons">
					<button type="button" class="btn btn-primary">
						Add Record
					</button>
					<a href="javascript:void(0)" @click="hideModal" class="link"
						>Cancel</a
					>
				</div>
			</form>
		</b-modal>
	</div>
</template>

<script>
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import { startNewCephServicePatienBreadCrumbs } from "@/common/constant/breadCrumbs"
import CasePhotosUpload from '@/components/newService/CasePhotosUpload.vue';
import AddPatientFilters from '@/components/service/partials/AddPatientFilters.vue';

export default {
	components: {
		BaseBreadCrumb,
		CasePhotosUpload,
		AddPatientFilters,
	},

	data() {
		return {
			toggleDropDown: false,
			value: 10,
			max: 100,
			breadCrumbsItems: [...startNewCephServicePatienBreadCrumbs],
			service: [
				{
					index: 0,
					image: 'mobile.png',
					title: 'Cephalometric Analysis ',
					link: true,
					link: 'Continue',
					details: true,
					detail: 'See More Details',
					remaining: true,
					case: 15,
					remainingCase: 'cases remaining',
					duration: 'exp. Jan 2022',
					value: 30,
					max: 100,
				},
			],

			selected: null,
			information: [
				{ value: null, text: 'Mohamed Mohsen   25 years, Male' },
				{ value: 'a', text: 'This is First option' },
				{ value: 'b', text: 'Selected Option' },
			],
			selected2: null,
			record: [
				{ value: null, text: '2021-02-20' },
				{ value: 'a', text: 'This is First option' },
				{ value: 'b', text: 'Selected Option' },
			],
			selected: null,
			gender: [
				{ value: null, text: 'Male' },
				{ value: 'a', text: 'Male' },
				{ value: 'b', text: 'Female' },
			],
		};
	},

	methods: {
		hideModal() {
			this.$refs['my-modal'].hide();
		},
	},
	watch: {
		tabIndex: function (e) {
			var activeText = document
				.querySelector(
					`.patientRecord .nav-pills li:nth-child(${
						e + 1
					}) a.nav-link`
				)
				.innerText.toLowerCase();
			document.querySelector(
				'.patientRecord .allCases .toggleTab'
			).innerText = activeText;
			this.toggleDropDown = !this.toggleDropDown;
		},
	},
};
</script>

<style lang="scss" scoped>
#addpatient {
	.custom-select {
		color: var(--textSecondary);
		background-image: url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M15.5858 9C16.4767 9 16.9229 10.0771 16.2929 10.7071L12.7071 14.2929C12.3166 14.6834 11.6834 14.6834 11.2929 14.2929L7.70711 10.7071C7.07714 10.0771 7.52331 9 8.41421 9H15.5858Z' fill='%238E8E8E'/%3E%3C/svg%3E%0A");
	}
}
.patientRecord {
	@media screen and (max-width: 991px) {
		.contentBox {
			border: 0;
			padding: 0;
			border-radius: 0;
			padding-bottom: rem(20px);
		}
	}
	h1 {
		margin-bottom: rem(24px);
	}
	h2 {
		font-size: rem(24px);
	}
	h4 {
		margin-top: rem(16px);
		font-size: rem(16px);
		color: var(--default);
	}

	.contentTitle {
		color: var(--textPrimary);
		font-weight: 500;
		margin-bottom: rem(12px);
	}
	.pageHead {
		margin-top: rem(42px);
		margin-bottom: rem(10px);
		a {
			padding-left: rem(88px);
			padding-right: rem(88px);
			@media screen and (max-width: 991px) {
				padding-left: rem(50px);
				padding-right: rem(50px);
			}
		}
		@media screen and (max-width: 450px) {
			flex-direction: column;
			margin: rem(25px) 0;
			.textWrapper {
				text-align: center;
				width: 100%;
				p {
					text-align: center;
				}
			}
			a {
				width: 100%;
			}
		}
	}
	.contentBox.allCases {
		padding: 0;
		position: relative;
		.case {
			position: absolute;
			top: 27px;
			right: 35px;
			font-weight: 500;
			color: var(--default);
			svg {
				width: 24px;
				height: 24px;
				margin-right: rem(10px);
			}
			&:hover {
				cursor: pointer;
				opacity: 0.8;
			}
			@media screen and (max-width: 767px) {
				top: 23px;
				right: 20px;
			}
		}
		::v-deep {
			.nav.nav-pills {
				border-bottom: 1px solid var(--borderColor);
				padding: 0 rem(64px);
				li {
					border-radius: 0;
					height: auto;
					&:not(:last-child) {
						margin-right: rem(50px);
					}
					a {
						height: 74px;
						display: flex;
						align-items: center;
						background: transparent;
						color: var(--textSecondary);
						font-size: rem(16px);
						font-weight: 500;
						&.active {
							background: transparent;
							color: var(--primary);
							position: relative;
							border-top-right-radius: 100px;

							&::after {
								position: absolute;
								content: '';
								width: 100%;
								height: 3px;
								background-color: var(--primary);
								bottom: 0;
								left: 0;
								border-radius: 12px 12px 0px 0px;
							}
						}
					}
				}
				@media screen and (max-width: 1300px) {
					padding-left: rem(35px);
					li {
						&:not(:last-child) {
							margin-right: rem(30px);
						}
					}
				}
				@media screen and (max-width: 767px) {
					padding-left: rem(20px);
					li {
						&:not(:last-child) {
							margin-right: rem(16px);
						}
						a {
							height: 65px;
						}
					}
				}
			}
		}
		@media screen and (max-width: 767px) {
			padding-top: rem(55px);
			.case {
				top: 10px;
			}
			::v-deep {
				.nav.nav-pills {
					padding: 0 rem(20px);
					justify-content: space-between;
					li {
						&:not(:last-child) {
							margin-right: 0;
						}
					}
				}
			}
		}
		@media screen and (max-width: 575px) {
			.toggleTab {
				display: block !important;
				width: 95%;
				margin: auto;
				margin-bottom: rem(20px);
			}
			.responsiveFilters {
				::v-deep {
					.nav.nav-pills {
						flex-direction: column;
						box-shadow: 0px 4px 25px rgba(107, 107, 107, 0.24);
						// position: absolute;
						width: 100%;
						z-index: 9;
						background: #fff;
						display: none;
						li {
							width: 100%;
							a {
								height: auto;
								padding: rem(15px) 0;
							}
						}
					}
				}
				&.active {
					::v-deep {
						.nav.nav-pills {
							display: block;
						}
					}
				}
			}
		}
	}
	.serviceRow {
		&__progress {
			width: 380px;
			::v-deep.progress {
				.progress-bar {
					background: #6b6b6b;
				}
			}
		}
		@media screen and (max-width: 991px) {
			&__progress {
				width: 320px;
			}
		}
		@media screen and (max-width: 767px) {
			&__progress {
				width: 260px;
			}
		}
		@media screen and (max-width: 700px) {
			&__progress {
				width: 100%;
				margin-top: rem(25px);
			}
		}
	}
}
</style>
