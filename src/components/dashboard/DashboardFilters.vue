<template>
	<div class="filters">
		<div class="row">
			<div class="col-xl-4 col-sm-8">
				<div class="form-group no-label">
					
						<input
							type="text"
							class="form-control"
							placeholder="Search by Service ID"
							v-model="search"
						/>
				</div>
			</div>
			<div class="col-xl-2 col-sm-4">
				<div class="date">
					<label @click="removeDateFilter" for="">{{date == "" ? 'Filter by' : 'Remove'}}</label>
					<div class="form-group">
						<b-form-datepicker
							class="datePicker"
							placeholder="filter"
							v-model="date"
							id="datepicker-dateformat2"
							:date-format-options="{
								year: 'numeric',
								month: 'numeric',
								day: 'numeric',
							}"
							locale="en"
						></b-form-datepicker>
					</div>
				</div>
			</div>
			<div class="col-xl-3 col-sm-6">
				<div class="form-group">
					<b-form-select
						v-model="selectedPatientId"
						:options="patientsList"
					></b-form-select>
					<label class="control-label static-label"
						>Patients</label
					>
				</div>
			</div>
			<div class="col-xl-3 col-sm-6">
				<div class="form-group">
					<b-form-select
						v-model="selectedServiceStatus"
						:options="serviceStatus"
					></b-form-select>
					<label class="control-label static-label"
						>Service Status</label
					>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { mapGetters } from "vuex";
import { ServiceHelper } from "@/common/crud-helpers/service";

export default {
	props: {
		applyFilter: Function,
	},
	data() {
		return {
			search: '',
			typingTimer: null,

			date: "",
			selectedPatientId: '',
			patientsList: [
				{value: '', text: "All"}
			],
			selectedServiceStatus: '',
			serviceStatus: [
				{ value: '', text: 'All' },
				{ value: 'new', text: 'New' },
				{ value: 'fulfilled', text: 'Fulfilled' },
				{ value: 'rejected', text: 'Rejected' },
			],
		};
	},
	mounted() {
		ServiceHelper.getPatients({});
	},
	computed: {
		...mapGetters(['patients']),
	},
	methods: {
		removeDateFilter() {
			this.date = ""
		},
		submitSearch() {
			this.applyFilter({
				name: "search",
				value: this.search.trim().toLowerCase(),
			})
		}
	},
	watch: {
		patients() {
			let list = [{value: '', text: 'All'}]
			this.patients.forEach((patient) => {
				list.push({value: patient.id, text: patient.first_name + ' ' + patient.last_name})
			})
			this.patientsList = list
		},
		search() {
			clearTimeout(this.typingTimer);
  			this.typingTimer = setTimeout(this.submitSearch, 2000);
		},
		date() {
			this.applyFilter({
				name: "service_date",
				value: this.date.trim(),
			})
		},
		selectedServiceStatus() {
			this.applyFilter({
				name: "fulfillment_status",
				value: this.selectedServiceStatus,
			})
		},
		selectedPatientId() {
			this.applyFilter({
				name: "patient",
				value: this.selectedPatientId,
			})
		},

	}
};
</script>

<style lang="scss" scoped>
.filters {
	margin-bottom: rem(24px);
	@media screen and (min-width: 992px) and (max-width: 1350px) {
		.row {
			margin-left: calc((10px / 2) * -1) !important;
			margin-right: calc((10px / 2) * -1) !important;
			> div {
				padding-left: calc(10px / 2) !important;
				padding-right: calc(10px / 2) !important;
			}
		}
	}
	@media screen and (max-width: 1199px) {
		.row {
			> div {
				margin-bottom: 15px;
			}
		}
	}
	.form-group {
		margin-bottom: 0;
		input {
			background: #f5f5f5;
			padding: 12px 24px;
			padding-left: 46px;
			border-radius: 12px;
			border: 0;
			background-image: url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M11 3C6.58172 3 3 6.58172 3 11C3 15.4183 6.58172 19 11 19C15.4183 19 19 15.4183 19 11C19 6.58172 15.4183 3 11 3ZM11 5C14.3137 5 17 7.68629 17 11C17 14.3137 14.3137 17 11 17C7.68629 17 5 14.3137 5 11C5 7.68629 7.68629 5 11 5Z' fill='%238E8E8E'/%3E%3Cg opacity='0.5'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M15.2926 15.2971C15.6529 14.9365 16.2201 14.9085 16.6125 15.2133L16.7068 15.2965L20.7068 19.2928C21.0975 19.6832 21.0978 20.3164 20.7074 20.7071C20.3471 21.0677 19.7799 21.0957 19.3875 20.7908L19.2932 20.7077L15.2932 16.7113C14.9025 16.321 14.9022 15.6878 15.2926 15.2971Z' fill='%238E8E8E'/%3E%3C/g%3E%3C/svg%3E%0A");
			background-repeat: no-repeat;
			background-position: 15px center;
			max-height: 64px;
			&::placeholder {
				font-weight: 400;
			}
		}
	}
	.date {
		display: flex;
		align-items: center;
		label {
			flex: 0 0 80px;
			max-width: 80px;
			font-weight: 500;
			color: var(--textSecondary);
			// font-size: rem(20px);
		}

		.form-group {
			flex: 1;
			margin: 0;
			.datePicker {
				position: relative;
				background: #f5f5f5;
				padding: 0 5px !important;
				::v-deep .form-control {
					padding: 0;
					font-size: rem(15px);
					@media screen and (min-width: 1200px) and (max-width: 1300px) {
						font-size: rem(13px);
					}
				}
				::v-deep.form-control.text-muted {
					font-size: 0;
					position: relative;
					&::before {
						content: '';
						position: absolute;
						background-image: url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M7 2C7 1.44772 7.44772 1 8 1C8.55228 1 9 1.44772 9 2V3H15V2C15 1.44772 15.4477 1 16 1C16.5523 1 17 1.44772 17 2V3.03373C20.0939 3.31474 22.01 5.33654 22 8.53697V17.4538C22 20.9131 19.7632 23 16.229 23H7.77096C4.24009 23 2 20.8785 2 17.3799V8.53697C2 5.34053 3.91802 3.31951 7 3.03473V2ZM7 5.04437C5.04021 5.28257 4 6.47611 4 8.53697V17.3799C4 19.7489 5.32107 21 7.77096 21H16.229C18.6885 21 20 19.7763 20 17.4538L20 8.53385C20.0065 6.46856 18.9694 5.27744 17 5.04296V6C17 6.55228 16.5523 7 16 7C15.4477 7 15 6.55228 15 6V5H9V6C9 6.55228 8.55228 7 8 7C7.44772 7 7 6.55228 7 6V5.04437Z' fill='%238E8E8E'/%3E%3Cg opacity='0.5'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M4 9C3.44772 9 3 9.44772 3 10C3 10.5523 3.44772 11 4 11H20C20.5523 11 21 10.5523 21 10C21 9.44772 20.5523 9 20 9H4ZM7.99386 13C7.44497 13 7 13.4477 7 14C7 14.5523 7.44497 15 7.99386 15H8.00614C8.55503 15 9 14.5523 9 14C9 13.4477 8.55503 13 8.00614 13H7.99386ZM11 14C11 13.4477 11.445 13 11.9938 13H12.0062C12.555 13 13 13.4477 13 14C13 14.5523 12.555 15 12.0062 15H11.9938C11.445 15 11 14.5523 11 14ZM15 14C15 13.4477 15.445 13 15.9939 13H16.0061C16.555 13 17 13.4477 17 14C17 14.5523 16.555 15 16.0061 15H15.9939C15.445 15 15 14.5523 15 14ZM15 18C15 17.4477 15.445 17 15.9939 17H16.0061C16.555 17 17 17.4477 17 18C17 18.5523 16.555 19 16.0061 19H15.9939C15.445 19 15 18.5523 15 18ZM11.9938 17C11.445 17 11 17.4477 11 18C11 18.5523 11.445 19 11.9938 19H12.0062C12.555 19 13 18.5523 13 18C13 17.4477 12.555 17 12.0062 17H11.9938ZM7 18C7 17.4477 7.44497 17 7.99386 17H8.00614C8.55503 17 9 17.4477 9 18C9 18.5523 8.55503 19 8.00614 19H7.99386C7.44497 19 7 18.5523 7 18Z' fill='%238E8E8E'/%3E%3C/g%3E%3C/svg%3E%0A");
						background-repeat: no-repeat;
						top: 50%;
						left: 50%;
						transform: translate(-50%, -50%);
						width: 24px;
						height: 24px;
						z-index: 1;
					}
				}
			}
		}
	}
}
</style>
