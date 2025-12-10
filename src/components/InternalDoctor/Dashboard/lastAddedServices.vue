<template>
	<div>
		<Filters :applyFilter="applyFilter" />
		<div class="table">
			<div class="table__head">
				<div class="table__row">
					<div class="table__row--cell" data-width="10">ID</div>
					<div class="table__row--cell" data-width="17">Service Name</div>
					<div class="table__row--cell" data-width="17">Checked In</div>
					<div class="table__row--cell" data-width="17">Patient Name</div>
					<div class="table__row--cell" data-width="15">Modality Type</div>
					<div class="table__row--cell" data-width="17">Doctor</div>
					<div class="table__row--cell" data-width="30">Status</div>
					<div class="table__row--cell" data-width="10">Action</div>
				</div>
			</div>
			<div class="table__body" style="border: 0px" >
				<div v-if="loading">
					<div class="table__row" v-for="(_, index) in 5" :key="'internal skelton' + index">
						<div class="table__row--cell patient" data-width="10" data-label="Service Id">
							<b-skeleton height="32px"  width="100%" animation="fade"></b-skeleton>
						</div>
						<div class="table__row--cell patient" data-width="17" data-label="Service Name">
							<b-skeleton height="32px"  width="100%" animation="fade"></b-skeleton>
						</div>
						<div class="table__row--cell" data-label="Check In" data-width="17">
							<b-skeleton height="32px" width="100%"  animation="fade"></b-skeleton>
						</div>
						<div class="table__row--cell" data-width="17" data-label="Patient Name">
							<b-skeleton height="32px" width="100%" animation="fade"></b-skeleton>
						</div>
						<div class="table__row--cell p-0" data-width="15" data-label="Modality Type">
							<b-skeleton height="32px"  width="100%" animation="fade"></b-skeleton>
						</div>
						<div class="table__row--cell p-0" data-width="17" data-label="Doctor">
							<b-skeleton height="32px"  width="100%" animation="fade"></b-skeleton>
						</div>
						<div class="table__row--cell"  data-width="30" data-label="Status" >
							<b-skeleton height="32px"  width="100%" animation="fade"></b-skeleton>
						</div>
						<div class="table__row--cell" data-width="10" data-label="Action">
							<b-skeleton height="32px"  width="100%" animation="fade"></b-skeleton>
						</div>
					</div>
				</div>
				<div v-if="!loading && services.length == 0">
					<div class="table__row" >
						<div class="table__row--cell" style="display: flex; justify-content: center;">
							{{'No cases to show yet.'}}
						</div>
					</div>
				</div>
				<div v-if="services.length > 0">
					<div class="table__row" v-for="(data, index) in services" :key="data.created + index" >
						<div class="table__row--cell" data-width="10" data-label="Service Id">
							{{formatId(data.id)}}
						</div>
						<div class="table__row--cell" data-width="17" data-label="Service Name">
							{{ data.order_line_obj.product_obj.title }}
						</div>
						<div class="table__row--cell date" data-label="Check In" data-width="17">
							{{ data.created | formatDate }}
						</div>
						<div class="table__row--cell" data-width="17" data-label="Patient Name">
							{{data.patient_obj.first_name + " " + data.patient_obj.last_name}}
						</div>
						<div class="table__row--cell p-0" data-width="15" data-label="Modality Type">
							{{ data.modality_type }}
						</div>
						<div class="table__row--cell p-0" data-width="17" data-label="Wait Time">
							{{ data.owner_obj.name || data.owner_obj.first_name + " " + data.owner_obj.last_name }}
						</div>
						<div class="table__row--cell p-0 status" data-width="30" data-label="Status">
							<div :class="serviceStatus(data).class">
								{{ serviceStatus(data).messege }}
							</div>
						</div>
						<div class="table__row--cell" data-width="10" data-label="Action" >
							<a href="#" class="viewMore" v-if="checkIfServiceCompleted(data)">
								<router-link
									class="view"
									:to="{
										name: 'Internal Doctor Service Summery',
										params: {
											lang: $i18n.locale,
											serviceId: data.id.toString(),
										},
									}"
								>
									view
								</router-link>
							</a>
						</div>
					</div>
				</div>
			</div>
		</div>
		<base-pagination path="/internal-doctor/dashboard/page=" :itemPerPage="10" :count="serviceCount"/>
	</div>
</template>

<script>
// [*] Import vue Components
import { ServiceHelper } from '@/common/crud-helpers/service';
import { mapGetters } from 'vuex';
import Filters from "@/components/InternalDoctor/Dashboard/Filters.vue";
import { formatIds } from '@/common/helpers/index';
import { serviceIsCompleted } from '@/common/helpers/index';
import { serviceStatusMessege } from '@/common/helpers/index';
import BasePagination from '@/common/components/base/BasePagination.vue';

export default {
	props: {
		page: String,
	},
	components: {
		BasePagination,
		Filters,
	},
	data() {
		return {
			services: [],
			loading: true,
      		filters: [],
		};
	},
	computed: {
		...mapGetters(['serviceList', 'serviceCount']),
	},
	watch: {
		serviceList() {
			this.services =  this.serviceList.filter((item) => item.order_line_obj)
			this.loading = false
			// let list = []
			// this.serviceList.forEach((service) => {
			// 	if(this.checkIfServiceCompleted(service)) {
			// 		list.push(service)
			// 	}
			// })
			//this.services =  [...this.serviceList]

			// let results = []
			// this.serviceList.forEach((service) => {
			// 	let remove = false
			// 	if(service.ser)
			// 	if(service.fulfillment_status == 'fulfilled') {
			// 		remove = true
			// 		service.phases.forEach((phase) => {
			// 			phase.deleiver_fields.forEach((field) => {
			// 				if(field.value != "") remove = false
			// 			})
			// 		})
			// 	}
			// 	if(!remove) results.push(service)
			// })
			// this.services = results
		},
		filters() {
			let query = {}
      		this.filters.forEach((filter) => {
      		  if(filter.value != '') {
      		    query[filter.name] = filter.value
      		  }
      		})
		
      		this.loading = true
      		this.services = []
      		ServiceHelper.filterServices(query)
		}
	},
	methods: {
		formatId(id) {
			return '#' + formatIds(id)
		},
		checkIfServiceCompleted(service) {
			return serviceIsCompleted(service)
		},
		serviceStatus(service) {
			return serviceStatusMessege(service)
		},
		applyFilter(filter) {
      		let index = this.filters.findIndex((item) => item.name == filter.name);
      		if (index > -1) {
      		  let newFilterList = this.filters;
      		  newFilterList[index] = filter;
      		  this.filters = [...newFilterList];
      		} else {
      		  this.filters.push(filter);
      		}
    	},
	}
};
</script>

<style lang="scss" scoped>
.view {
	color: var(--primary);
	text-transform: capitalize;
}
.status {
	text-align: center;
	text-transform: none;
	padding: 0px;
	.notStarted {
		padding: rem(10px);
		background: #F5F5F5;
		--borderColor: #C9C9C9;
		border-radius: 6px;
	}
	.rejected {
		padding: rem(10px);
		background: #fdefed;
		--borderColor: #f7c0b7;
		border-radius: 6px;
	}
	.inProgress {
		padding: rem(10px);
		background: #eef7fb;
		--borderColor: #a8d5ee;
		border-radius: 6px;
	}
	.delayed {
		padding: rem(10px);
		background: rgba(236, 171, 8, 0.12);;
		--borderColor: rgba(236, 171, 8, 0.5);
		border-radius: 6px;
	}
	.completed {
		padding: rem(10px);
		background: #edfdf3;
		--borderColor: #a8eec4;
		border-radius: 6px;
	}
}
.table__body {
	.table__row {
		padding: 1.6rem 0;
		text-transform: capitalize;
		.date {
			color: var(--primary);
		}
	}
}
</style>
