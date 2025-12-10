<template>
  <div>
    <filters :applyFilter="applyFilter" />
    <div class="table">
      <div class="table__head">
        <div class="table__row">
          <div class="table__row--cell" data-width="11">Patient ID</div>
          <div class="table__row--cell" data-width="15">Name</div>
          <div class="table__row--cell" data-width="8">Gender</div>
          <div class="table__row--cell" data-width="8">Age</div>
          <div class="table__row--cell">Last added service</div>
          <div class="table__row--cell" data-width="10">Date</div>
          <div class="table__row--cell" data-width="12">Service Status</div>
          <div class="table__row--cell" data-width="16">Service Phase</div>
          <div class="table__row--cell" data-width="5">More</div>
        </div>
      </div>
      <div class="table__body" style="border: 0px">
        <div v-if="loading">
          <div
            class="table__row"
            v-for="(_, index) in 5"
            :key="'skelton_patient' + index"
          >
            <div
              class="table__row--cell"
              data-width="11"
              data-label="Patient ID"
            >
              <b-skeleton
                height="32px"
                width="100%"
                animation="fade"
              ></b-skeleton>
            </div>
            <div class="table__row--cell" data-width="15" data-label="Name">
              <b-skeleton
                height="32px"
                width="100%"
                animation="fade"
              ></b-skeleton>
            </div>
            <div class="table__row--cell" data-width="8" data-label="Gender">
              <b-skeleton
                height="32px"
                width="100%"
                animation="fade"
              ></b-skeleton>
            </div>
            <div class="table__row--cell p-0" data-width="8" data-label="Age">
              <b-skeleton
                height="32px"
                width="100%"
                animation="fade"
              ></b-skeleton>
            </div>
            <div class="table__row--cell blue" data-label="Last added service">
              <b-skeleton
                height="32px"
                width="100%"
                animation="fade"
              ></b-skeleton>
            </div>
            <div class="table__row--cell" data-width="10" data-label="Date">
              <b-skeleton
                height="32px"
                width="100%"
                animation="fade"
              ></b-skeleton>
            </div>
            <div
              class="table__row--cell"
              data-width="16"
              data-label="Service Phase"
            >
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
        <div v-if="!loading && filterdPatient.length == 0">
          <div class="table__row">
            <div
              class="table__row--cell"
              style="display: flex; justify-content: center"
            >
              {{ "No patients to show yet." }}
            </div>
          </div>
        </div>
        <div v-if="filterdPatient.length > 0">
          <div
            class="table__row"
            v-for="patient in filterdPatient"
            :key="'patient' + patient.id"
          >
            <div
              class="table__row--cell"
              data-width="11"
              data-label="Patient ID"
            >
                {{ "#" + format(patient.id) }}
            </div>
            <div class="table__row--cell" data-width="15" data-label="Name">
              {{ patient.first_name + " " + patient.last_name }}
            </div>
            <div class="table__row--cell" data-width="8" data-label="Gender">
              {{ patient.gender }}
            </div>
            <div class="table__row--cell p-0" data-width="8" data-label="Age">
              {{ patient.age + " Years" }}
            </div>
            <div
              class="table__row--cell blue"
              data-label="Last added service"
              v-if="patient.last_service"
            >
              <div class="text-turncate">
                {{ patient.last_service.planing }}
              </div>
            </div>
            <div
              class="table__row--cell"
              data-label="Last added service"
              v-if="!patient.last_service"
            >
              <div :class="!patient.last_service ? 'noService' : ''">
                No service has been created for this patient yet ...
              </div>
            </div>
            <div
              class="table__row--cell"
              data-width="10"
              data-label="Date"
              v-if="patient.last_service"
            >
              {{ patient.last_service.date.split("T")[0] }}
            </div>
            <div
              class="table__row--cell"
              data-width="12"
              data-label="Service Status"
              v-if="patient.last_service"
            >
              <span
                :class="
                  patient.last_service.status == 'NEW'
                    ? 'pending'
                    : patient.last_service.status == 'DONE'
                    ? 'completed'
                    : patient.last_service.status == true
                    ? 'failed'
                    : patient.last_service.status == true
                    ? 'cancelled'
                    : patient.last_service.status == true
                    ? 'refunded'
                    : ''
                "
              ></span>
              {{
                patient.last_service.status == "NEW"
                  ? "Pending"
                  : patient.last_service.status == "DONE"
                  ? "Completed"
                  : "..."
              }}
            </div>
            <div
              class="table__row--cell"
              data-width="16"
              data-label="Service Phase"
              v-if="patient.last_service"
            >
              <router-link
                class="viewMore"
                :class="
                  patient.last_service.status != 'DONE' ? 'phase' : 'result'
                "
                v-if="patient.last_service.type != 'online-ai-service'"
                :to="{
                  name: 'continue-service-flow',
                  params: {
                    lang: $i18n.locale,
                    type: 'service',
                    index: String(patient.last_service.id),
                  },
                }"
              >
                {{
                  patient.last_service.status != "DONE"
                    ? "Go to Next Phase"
                    : "See results"
                }}
                <font-awesome-icon :icon="['fa', 'angle-right']" />
              </router-link>
              <router-link
                v-else-if="
                  patient.last_service.type == 'online-ai-service' &&
                  patient.last_service.serviceName ==
                    'AI Cephalometric Analysis'
                "
                class="viewMore"
                :class="
                  patient.last_service.status != 'DONE' ? 'phase' : 'result'
                "
                :to="{
                  name: 'Start New Ceph Service analysis',
                  params: {
                    lang: $i18n.locale,
                    type: 'service',
                    id: String(patient.last_service.id),
                    patient: String(patient.id),
                  },
                }"
              >
                {{
                  patient.last_service.status != "DONE"
                    ? "Go to Next Phase"
                    : "See results"
                }}
                <font-awesome-icon :icon="['fa', 'angle-right']" />
              </router-link>
              <router-link
                v-else-if="
                  patient.last_service.type == 'online-ai-service' &&
                  patient.last_service.serviceName == 'Pan Ai'
                "
                class="viewMore"
                :class="
                  patient.last_service.status != 'DONE' ? 'phase' : 'result'
                "
                :to="{
                  name: 'Start New Panoramic Service analysis',
                  params: {
                    lang: $i18n.locale,
                    type: 'service',
                    id: String(patient.last_service.id),
                    patient: String(patient.id),
                  },
                }"
              >
                {{
                  patient.last_service.status != "DONE"
                    ? "Go to Next Phase"
                    : "See results"
                }}
                <font-awesome-icon :icon="['fa', 'angle-right']" />
              </router-link>
            </div>
            <div
              class="table__row--cell"
              data-width="5"
              data-label="More"
              v-if="patient.last_service"
            >
              <b-dropdown class="action-dropdown">
                <b-dropdown-item
                  href="#"
                  v-for="(item, i) in moreActions"
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
      path="/my-patients/page="
      :itemPerPage="10"
      :count="myPatientCount"
    />
  </div>
</template>

<script>
// [*] Import UI Components .
import Filters from "@/components/Patients/Filters.vue";
import BasePagination from "@/common/components/base/BasePagination.vue";

// [*] Import Helpers ...
import { formatIds } from "@/common/helpers/index";

// [*] Import vue Components
import { mapGetters } from "vuex";
import { ServiceHelper } from "@/common/crud-helpers/service";

export default {
  props: {
    page: String,
  },
  components: {
    Filters,
    BasePagination,
  },
  data() {
    return {
      allPatients: [],
      filterdPatient: [],
      filter: [],
      loading: true,

      moreActions: ["Change Payment Method", "Report a problem"],
    };
  },
  computed: {
    ...mapGetters(["patients", "myPatientCount", "serviceList"]),
  },
  mounted() {
    ServiceHelper.getPatients({ page: this.page });
  },
  watch: {
    page() {
      ServiceHelper.getPatients({ page: this.page });
    },
    patients() {
      this.allPatients = [];
      this.filterdPatient = [];
      ServiceHelper.getServices({});
    },
    serviceList() {
      this.allPatients = this.patients.map((patient) => {
        let services = this.serviceList.filter(
          (service) => service.patient_obj.id === patient.id
        );
        if (services.length > 0) {
          return {
            ...patient,
            last_service: {
              id: services[0].id,
              status: services[0].status,
              date: services[0].created,
              planing: services[0].order_line_obj.product_obj.title,
              type: services[0].order_line_obj.product_obj.product_class,
              orderLineId: services[0].order_line_obj.id,
              //serviceName:services[0].order_line_obj.product_obj.parent_obj.title,
              
              serviceName:services[0].order_line_obj.product_obj.parent_obj == null ? services[0].order_line_obj.product_obj.title : services[0].order_line_obj.product_obj.parent_obj.title,
            },
          };
        } else {
          return {
            ...patient,
            last_service: null,
          };
        }
      });
      this.filterdPatient = [...this.allPatients];
      this.loading = false;
    },
    filter() {
      let filterList = [];
      if (this.filter.length > 0) {
        this.allPatients.forEach((patient, index) => {
          let patientPassFilter = true;
          this.filter.forEach((filter) => {
            if (filter.name == "search" && filter.value != "") {
              if (
                !patient.id.toString().trim().includes(filter.value) &&
                !patient.first_name
                  .toString()
                  .trim()
                  .toLowerCase()
                  .includes(filter.value) &&
                !patient.last_name
                  .toString()
                  .trim()
                  .toLowerCase()
                  .includes(filter.value)
              ) {
                patientPassFilter = false;
              }
            }
            if (filter.name == "date" && filter.value != "") {
              if (
                !patient.last_service ||
                patient.last_service.date.split("T")[0].toString().trim() !=
                  filter.value
              ) {
                patientPassFilter = false;
              }
            }
            if (filter.name == "service-type" && filter.value != "all") {
              if (
                !patient.last_service ||
                patient.last_service.type != filter.value
              ) {
                patientPassFilter = false;
              }
            }
            if (filter.name == "service-status" && filter.value != "all") {
              if (
                !patient.last_service ||
                patient.last_service.status != filter.value
              ) {
                patientPassFilter = false;
              }
            }
          });
          if (patientPassFilter == true) {
            filterList.push(patient);
          }
        });
        this.filterdPatient = [...filterList];
      } else {
        this.filterdPatient = [...this.allPatients];
      }
    },
  },
  methods: {
    format(id) {
      return formatIds(id);
    },
    applyFilter(filter) {
      let index = this.filter.findIndex((item) => item.name == filter.name);
      if (index > -1) {
        let newFilterList = this.filter;
        newFilterList[index] = filter;
        this.filter = [...newFilterList];
      } else {
        this.filter.push(filter);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.table {
  &__row {
    text-transform: capitalize;
    &--cell {
      &:first-child {
        a {
          color: var(--primary);
          font-weight: 400;
        }
      }
      .noService {
        color: var(--textSecondary);
        text-align: center;
        text-transform: none;
      }
    }
  }
}
</style>
