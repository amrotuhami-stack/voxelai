<template>
  <div>
    <dashboard-filters :applyFilter="applyFilter" />
    <div class="table">
      <div class="table__head">
        <div class="table__row">
          <div class="table__row--cell" data-width="10">Service ID</div>
          <div class="table__row--cell" data-width="25">Service Name</div>
          <div class="table__row--cell" data-width="15">Patient Name</div>
          <div class="table__row--cell" data-width="15">Added date</div>
          <div class="table__row--cell">Service Status</div>
          <div class="table__row--cell" data-width="5">More</div>
        </div>
      </div>
      <div class="table__body" style="border: 0px">
        <div v-if="loading">
          <div
            class="table__row"
            v-for="(_, index) in 5"
            :key="'skelton' + index"
          >
            <div class="table__row--cell" data-label="ID" data-width="10">
              <b-skeleton
                height="32px"
                width="100%"
                animation="fade"
              ></b-skeleton>
            </div>
            <div
              class="table__row--cell"
              data-width="25"
              data-label="Service Name"
            >
              <b-skeleton
                height="32px"
                width="100%"
                animation="fade"
              ></b-skeleton>
            </div>
            <div
              class="table__row--cell patient"
              data-width="15"
              data-label="Patient Name"
            >
              <b-skeleton
                height="32px"
                width="100%"
                animation="fade"
              ></b-skeleton>
            </div>
            <div
              class="table__row--cell p-0"
              data-width="15"
              data-label="Added date"
            >
              <b-skeleton
                height="32px"
                width="100%"
                animation="fade"
              ></b-skeleton>
            </div>
            <div class="table__row--cell" data-label="Service Status">
              <b-skeleton
                height="32px"
                width="100%"
                animation="fade"
              ></b-skeleton>
            </div>
            <div class="table__row--cell" data-width="5" data-label="More">
              <b-skeleton
                height="32px"
                width="100%"
                animation="fade"
              ></b-skeleton>
            </div>
          </div>
        </div>
        <div v-if="!loading && services.length == 0">
          <div class="table__row">
            <div
              class="table__row--cell"
              style="display: flex; justify-content: center"
            >
              No cases to show yet.
            </div>
          </div>
        </div>
        <div v-if="services.length > 0">
          <div
            class="table__row"
            v-for="data in services"
            :key="data.id"
            @click.prevent="pushService(data)"
          >
            <div class="table__row--cell" data-label="ID" data-width="10">
              {{ formatId(data.id) }}
            </div>
            <div
              class="table__row--cell"
              data-width="25"
              data-label="Service Name"
            >
              <p
                v-if="
                  data.order_line_obj.product_obj.product_class ==
                  'online-ai-service'
                "
              >
                {{ data.order_line_obj.product_obj.parent_obj.title }} -
                {{ data.order_line_obj.product_obj.title }} !
              </p>
              <p v-else>{{ data.order_line_obj.product_obj.title }} !</p>
            </div>
            <div
              class="table__row--cell patient"
              data-width="15"
              data-label="Patient Name"
            >
              {{ data.patient_obj.first_name }} {{ data.patient_obj.last_name }}
            </div>
            <div
              class="table__row--cell p-0"
              data-width="15"
              data-label="Added date"
            >
              {{ data.created | formatDate }}
            </div>
            <div class="table__row--cell status" data-label="Service Status">
              <span :class="serviceStatus(data).clientClass"></span>
              {{ serviceStatus(data).clientMessege }}
            </div>
            <!-- <div class="table__row--cell" data-width="15" data-label="Service Phase" >
							<a href="#" class="viewMore" :class="data.status != 'DONE' ? 'phase' : 'result'">
								<router-link v-if="data.order_line_obj.product_obj.product_class == 'online-ai-service'"
									:to="{
										name: 'Start New Ceph Service analysis',
										params: {
											action: 'new',
											lang: $i18n.locale,
											serviceId: String(activeOrderLine.findIndex((line) => line.id == data.order_line_obj.id)),
										},
									}"
								>
									{{ data.status != 'DONE' ? 'Go to Next Phase' : 'See results'}}
								</router-link>
								<router-link v-else
									:to="{
										name: 'continue-service-flow',
										params: {lang: $i18n.locale, type: 'service', index: String(data.id),},
									}"
								>
									{{ data.status != 'DONE' ? 'Go to Next Phase' : 'See results'}}
								</router-link>
								<font-awesome-icon :icon="['fa', 'angle-right']" />
							</a>
						</div> !-->
            <div class="table__row--cell" data-width="5" data-label="More">
              <b-dropdown class="action-dropdown">
                <b-dropdown-item
                  href="#"
                  v-for="(item, i) in data.more"
                  :key="i"
                  >{{ item }}</b-dropdown-item
                >
              </b-dropdown>
            </div>
          </div>
        </div>
      </div>
    </div>
    <base-pagination
      path="/dashboard/page="
      :itemPerPage="10"
      :count="serviceCount"
    />
  </div>
</template>

<script>
// [*] Import vue Components
import BasePagination from "@/common/components/base/BasePagination.vue";

import { ServiceHelper } from "@/common/crud-helpers/service";
import { mapGetters } from "vuex";

import { formatIds } from "@/common/helpers/index";
import { serviceStatusMessege } from "@/common/helpers/index";
import DashboardFilters from "./DashboardFilters.vue";

export default {
	props: {
		page: String,
	},
	components: {
		BasePagination,
    DashboardFilters
	},
	data() {
		return {
			services: [],
      filters: [],
			loading: true,
		};
	},
	computed: {
		...mapGetters(['serviceList', 'activeOrderLine', 'serviceCount']),
	},
	watch: {
		serviceList() {
			this.services =  this.serviceList.filter((item) => item.order_line_obj)
			this.loading = false
		},
		page() {
			ServiceHelper.getServices({page: this.page})
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
	mounted() {
		ServiceHelper.getServices({page: this.page})
	},
	methods: {
		formatId(id) {
			return '#' + formatIds(id)
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
		
		pushService(service) {
			if(service.order_line_obj.product_obj.product_class == 'online-ai-service') {
				this.$router.push({
					name: 'Start New Ceph Service analysis',
					params: {
						lang: this.$i18n.locale,
						type: 'service',
						id: String(service.id),
					},
				})
			}
			else {
				this.$router.push({
					name: 'continue-service-flow',
					params: {lang: this.$i18n.locale, type: 'service', index: String(service.id),},
				})
			}
		}
	}
};
</script>

<style lang="scss" scoped>
.table__body {
  .table__row {
    padding: 1.6rem 0;
    text-transform: capitalize;
  }
  .patient {
    color: var(--primary);
  }
  .status {
    text-align: left;
    text-transform: none;
    padding: 0px;
  }
}
</style>
