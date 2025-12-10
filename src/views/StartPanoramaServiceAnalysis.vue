<template>
  <div class="panoramaService">
    <!-- <base-offer-notifications /> -->
    <base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
    <h1 class="main-title">Start New Service</h1>
    <div class="contentBox serviceDetails" v-if="order && order.product_obj">
      <div class="serviceRow">
        <div class="serviceRow__image">
          <img
            v-if="order.product_obj.images.length > 0"
            :src="order.product_obj.images[0].original"
            alt=""
            class="img-fluid"
          />
        </div>
        <div class="serviceRow__title">
          {{ order.product_obj.parent_obj.title }} -
          {{ order.product_obj.title }}
          <div
            class="serviceRow__cases"
            v-if="order.product_obj.subscription_size - order.used_cases"
          ></div>
          <div class="serviceRow__details">
            <router-link
              class="viewMore"
              :to="{
                name: 'product-details',
                params: {
                  lang: $i18n.locale,
                  productId: String(order.product_obj.parent_obj.id),
                },
              }"
            >
              See More Details
              <font-awesome-icon :icon="['fa', 'angle-right']" />
            </router-link>
          </div>
        </div>
        <div class="serviceRow__progress">
          <b-progress
            :value="order.used_cases"
            :max="order.product_obj.subscription_size"
          ></b-progress>
          <div class="d-flex justify-content-between align-items-center">
            <div
              v-if="!isDateBeforeToday(order.expire_date)"
              class="serviceRow__cases--remaining"
            >
              <span
                v-html="order.product_obj.subscription_size - order.used_cases"
              ></span>
              cases remaining
              <svg-icon
                v-b-tooltip.hover
                title="cases remaining"
                icon-id="info-circle"
                icon-viewbox="0 0 24 24"
              ></svg-icon>
            </div>
            <div v-else class="serviceRow__cases--remaining">
              Product Expired
            </div>
            <div class="serviceRow__cases--duration">
              {{ order.expire_date | formatDate }}
            </div>
          </div>
        </div>
        <!-- <div class="serviceRow__link" v-if="item.links == true">
					<a href="#" class="btn btn-default">{{ item.link }}</a>
				</div> -->
      </div>
    </div>
    <!-- add patient filters -->
    <div class="pageHead">
      <div class="textWrapper">
        <h2>Select or Add new patient to get started</h2>
      </div>
    </div>
    <div class="d-flex patientRecord">
      <div class="patientRecord__left">
        <div class="form-group">
          <b-dropdown
            :text="selected_patient_display"
            v-model="selected_patient"
          >
            <b-dropdown-text>
              Or
              <router-link to="" v-b-modal="'addpatient'">
                Add New Patient
              </router-link>
            </b-dropdown-text>
            <b-dropdown-item
              href="#"
              v-for="(patient, index) in patients"
              :key="index"
            >
              <div @click="changeSelectedPatient(index)">
                <span>{{ patient.first_name }} {{ patient.last_name }}</span
                >{{ patient.age }} years
              </div>
            </b-dropdown-item>
          </b-dropdown>
          <label class="control-label dropdownTitle static-label">
            Patient Information
          </label>
        </div>
      </div>
    </div>
    <div class="pageHead" v-if="order">
      <div class="textWrapper">
        <h2>Select or Add new record</h2>
        <p>You can select or add new record to start a panoramic analysis</p>
      </div>
      <button
        v-if="!isDateBeforeToday(order.expire_date)"
        href="#"
        class="btn btn-primary"
        @click="createNewRecord"
        :disabled="
          !selected_patient ||
          order.product_obj.subscription_size - order.used_cases < 1
        "
      >
        <span class="icon">
          <svg-icon icon-id="plus-icon" icon-viewbox="0 0 17 18"></svg-icon>
        </span>
        New Record
      </button>
    </div>
    <div class="patientRecord__right">
      <div class="form-group">
        <b-dropdown :text="selected_record_display" v-model="selected_record">
          <b-dropdown-item
            href="#"
            v-for="(record, index) in patientAiServices"
            :key="index"
            @click.prevent="updateSelectedRecord(index)"
          >
            {{ record.created | formatDate }}
            <!-- <svg-icon icon-id="trash-icon" icon-viewbox="0 0 24 24"></svg-icon> -->
          </b-dropdown-item>
        </b-dropdown>
        <label class="control-label dropdownTitle static-label">
          Select Record
        </label>
      </div>
    </div>
    <Records
      v-if="selected_patient && !selected_record"
      :updateSelectedRecord="updateSelectedRecord"
    />
    <div
      v-if="(selected_patient && selected_record) || !selected_patient"
      class="contentBox analysis"
      style="padding: 0px"
    >
      <PanoramaService
        v-if="selected_patient && selected_record"
        :recordId="selected_record.id"
      />
      <div v-if="!selected_patient" class="noService">
        <img
          src="@/assets/images/svg/Logoo.svg"
          class="img-fluid d-none-sm"
          alt="vetro logo"
          width="300px"
        />
        <img
          src="@/assets/images/svg/Logo-mob.svg"
          class="img-fluid d-none show-on-sm"
          alt="vetro logo"
        />
        <p>Select or add a new patient's record to get started!!</p>
      </div>
    </div>
    <!-- Add Patient Record PopUp-->
    <b-modal ref="my-modal" id="addpatient" centered>
      <div class="modal-title">Add New Patient</div>
      <p>Voxel is created for every dental practitioner.</p>
      <form key="Add-new-patient" @submit="addPatient">
        <div class="row">
          <div class="col-sm-6">
            <div class="form-group">
              <input
                type="text"
                class="form-control"
                name="First name"
                placeholder="First name"
                v-model="patientFirstName"
                @change="validateForm"
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
                  name="Last name"
                  placeholder="Last name"
                  v-model="patientLastName"
                  @change="validateForm"
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
                name="Age"
                placeholder="Age"
                v-model="patientAge"
                @change="validateForm"
              />
              <label class="control-label">Age</label>
            </div>
          </div>
          <div class="col-sm-6">
            <div class="form-group">
              <b-dropdown :text="patientGender" v-model="patientGender">
                <b-dropdown-item
                  href="#"
                  v-for="(record, index) in gender"
                  :key="index"
                  @click="updatePatientGender(record.value)"
                >
                  {{ record.text }}
                </b-dropdown-item>
              </b-dropdown>
              <label class="control-label dropdownTitle static-label">
                Gender
              </label>
            </div>
          </div>
        </div>
        <div class="errors">
          <div v-if="addPatientErrors.length > 0">
            <p>Please correct the following error(s):</p>
            <ul>
              <li v-for="(error, index) in addPatientErrors" :key="index">
                {{ "[ X ] " + error }}
              </li>
            </ul>
          </div>
        </div>
        <div class="inline-buttons">
          <button type="submit" class="btn btn-primary">Add</button>
          <a href="javascript:void(0)" @click="hideModal" class="link"
            >Cancel</a
          >
        </div>
      </form>
    </b-modal>
  </div>
</template>

<script>
// [*] Import UI Components
import BaseBreadCrumb from "@/common/components/base/BaseBreadCrumb.vue";
import moment from "moment";

// [*] Import Breadcrumbs
import { startPanoramaServiceAnalysisBreadCrumbs } from "@/common/constant/breadCrumbs";

// [*] Vuex State Getter And Action Helper
import { ServiceHelper } from "@/common/crud-helpers/service";
import { CommonHelper } from "@/common/crud-helpers/common";
import { mapGetters } from "vuex";

// [*] Import form validator
import AppValidator from "@/common/validator";
import Records from "../components/panoramaService/records.vue";
import PanoramaService from "@/components/panoramaService/panoramaRecord.vue";

import { SERVICE_MUTATIONS } from "@/store/modules/service/actions";

export default {
  components: {
    BaseBreadCrumb,
    Records,
    PanoramaService,
  },
  props: {
    type: String,
    id: String,
    patient: String,
  },
  data() {
    return {
      breadCrumbsItems: [...startPanoramaServiceAnalysisBreadCrumbs],
      myIframe: null,

      order: null,

      selected_patient: null,
      selected_patient_display: "Select or Add Paient",
      isPatient_initiated: false,

      selected_record: null,
      selected_record_display: "Select or Add Record",

      gender: [
        { value: "male", text: "Male" },
        { value: "female", text: "Female" },
      ],
      addPatientErrors: [],
      patientFirstName: "",
      patientLastName: "",
      patientAge: null,
      patientGender: "male",
    };
  },
  computed: {
    ...mapGetters([
      "orderLine",
      "patients",
      "patientAiServices",
      "serviceDetail",
    ]),
  },
  mounted() {
    this.type == "order"
      ? ServiceHelper.getActiveOrderLine(this.id)
      : ServiceHelper.getServiceDetail(Number.parseInt(this.id));
  },
  watch: {
    order() {
      ServiceHelper.getPatients({});
    },
    orderLine() {
      this.order = this.orderLine;
    },
    serviceDetail() {
      this.order = this.serviceDetail.order_line_obj;
    },
    patients() {
      if (this.patients.length > 0) {
        let index = this.patients.findIndex(
          (item) => item.id == Number.parseInt(this.patient)
        );
        if (index != -1) this.initiateSelectedPatient(index, this.id);
      }
    },
    patientAiServices() {
      if (this.order && this.patientAiServices.length > 0) {
        let index = this.patientAiServices.findIndex(
          (item) => item.id == Number.parseInt(this.id)
        );
        if (index != -1) this.updateSelectedRecord(index);
      }
    },
    selected_record(newValue, oldValue) {
      if (newValue && newValue?.id != oldValue?.id) {
        this.$router.push({
          name: "Start New Panoramic Service analysis",
          params: {
            lang: this.$i18n.locale,
            type: "service",
            id: String(this.selected_record.id),
            patient: String(this.selected_patient.id),
          },
        });
      }
    },
  },
  methods: {
    isDateBeforeToday(date) {
      return new Date(date).valueOf() < new Date().valueOf();
    },
    hideModal() {
      this.addPatientErrors = [];
      this.patientFirstName = "";
      (this.patientLastName = ""), (this.patientAge = "");
      this.patientGender = "male";
      this.$refs["my-modal"].hide();
    },
    changeSelectedPatient(index) {
      let id = this.id;

      if (this.selected_record) {
        id = String(this.selected_record.order_line);
        if (this.patients[index].id != this.selected_patient.id) {
          this.selected_record = null;
          this.selected_record_display = "Select or Add Record";
        }
      }

      this.updateSelectedPatient(index, id);
    },
    setSelectedPatient(index) {
      this.selected_patient = this.patients[index];
      this.selected_patient_display =
        this.selected_patient.first_name +
        " " +
        this.selected_patient.last_name;
    },
    openOrderPanoramaService(id) {
      if (this.selected_patient.id != this.patient && !this.selected_record) {
        this.$router.push({
          name: "Start New Panoramic Service analysis",
          params: {
            lang: this.$i18n.locale,
            type: "order",
            id: id,
            patient: String(this.selected_patient.id),
          },
        });
      }
    },
    initiateSelectedPatient(index, id) {
      this.setSelectedPatient(index);
      if (!this.isPatient_initiated) {
        this.getPatientAiServices();
        this.isPatient_initiated = true;
      }
      this.openOrderPanoramaService(id);
    },
    updateSelectedPatient(index, id) {
      this.setSelectedPatient(index);
      if (this.patient != this.selected_patient.id) {
        this.getPatientAiServices();
      }
      this.openOrderPanoramaService(id);
    },

    updateSelectedRecord(index) {
      this.selected_record = this.patientAiServices[index];
      this.selected_record_display = moment(
        String(this.selected_record.created)
      ).format("MM/DD/YYYY hh:mm");

      this.$store.commit(
        SERVICE_MUTATIONS.SET_SERVICE_DETAIL,
        this.selected_record
      );

      CommonHelper.closeOverLay();
    },
    updatePatientGender(value) {
      this.patientGender = value;
      this.validateForm();
    },
    addPatient: async function (e) {
      e.preventDefault();
      if (!this.validateForm()) return;
      await ServiceHelper.addPatients({
        first_name: this.patientFirstName,
        last_name: this.patientLastName,
        age: this.patientAge,
        gender: this.patientGender,
      }).then(() => {
        this.changeSelectedPatient(this.patients.length - 1);
      });

      this.hideModal();
    },
    validateForm() {
      let error = AppValidator.addNewPatient({
        patientFirstName: this.patientFirstName,
        patientLastName: this.patientLastName,
        patientAge: this.patientAge,
        patientGender: this.patientGender,
      });
      this.addPatientErrors = [...error];
      return this.addPatientErrors.length > 0 ? false : true;
    },
    getPatientAiServices() {
      if (this.order.product_obj != undefined) {
        return ServiceHelper.getPatientAiServices({
          patient_id: this.selected_patient.id,
          product_id: this.order.product_obj.id,
        });
      }
    },
    createNewRecord() {
      ServiceHelper.addService({
        product: this.order.product_obj.id,
        patient: this.selected_patient.id,
        order_line: this.order.id,
      }).then((serviceId) => {
        ServiceHelper.getServiceDetail(serviceId).then((responce) => {
          this.selected_record = responce;
        });
        this.getPatientAiServices().then(() => {
          this.updateSelectedRecord(0);
        });
      });
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
  .errors {
    p {
      margin-bottom: rem(10px);
    }
    ul {
      list-style-type: none;
      margin-bottom: rem(15px);
      li {
        padding-left: rem(10px);
        margin-bottom: rem(10px);
        color: var(--orange);
      }
    }
  }
}
.panoramaService {
  @media screen and (max-width: 991px) {
    .contentBox {
      border: 0;
      padding: 0;
      border-radius: 0;
      padding-bottom: rem(20px);
    }
    .row.p-4 {
      padding-left: 0 !important;
      padding-right: 0 !important;
    }
    .mt-30-lg {
      margin-top: rem(30px);
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
    margin-top: rem(12px);
    margin-bottom: rem(0px);
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

  &__left {
    flex: 1;
  }
  &__right {
    flex: 0 0 300px;
    margin-left: rem(24px);
  }
  .contentBox.analysis {
    padding: 0;
    position: relative;

    .table {
      border-width: 2px;
      margin: 0;
      &__body {
        .table__row {
          border-width: 2px;
        }
      }
    }
    .height-100 {
      height: calc(100% - 18px);
    }

    .frame {
      min-height: 1200px;
      @media screen and (max-width: 767px) {
        min-height: 1600px;
      }
    }

    .noService {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 350px;
      flex-direction: column;
      p {
        margin-top: rem(24px);
        font-size: rem(20px);
        color: var(--textPrimary) !important;
      }
    }

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
                content: "";
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
      .tab-content {
        .pageHead {
          padding: rem(24px);
          padding-bottom: 0;
          margin: 0;
          p {
            margin-bottom: 0;
          }
          @media screen and (max-width: 767px) {
            flex-direction: column;
            align-items: flex-start;
            padding-left: 0;
            padding-right: 0;
          }
        }
        .inline-button {
          .btn.btn-primary {
            padding-left: rem(40px);
            padding-right: rem(40px);
          }
          .btn.grey {
            padding-left: rem(60px);
            padding-right: rem(60px);
            margin-left: rem(16px);
          }
          @media screen and (max-width: 767px) {
            margin: rem(25px) 0;
            width: 100%;
            @include flex(center, space-between);
          }
          @media screen and (max-width: 450px) {
            flex-direction: column;
            .btn {
              width: 100%;
            }
            .btn.grey {
              margin: rem(16px) 0 0 0;
            }
          }
        }
        .nav.nav-pills {
          padding: 0 rem(56px);
          @media screen and (max-width: 767px) {
            padding-left: rem(20px);
            justify-content: start;
            li {
              &:not(:last-child) {
                margin-right: rem(20px);
              }
            }
          }
          @media screen and (max-width: 575px) {
            display: flex !important;
            flex-direction: row !important;
            box-shadow: none !important;
            li {
              width: auto !important;
            }
          }
        }
        .columnWrapper {
          &.p-4 {
            @media screen and (max-width: 1500px) {
              padding-right: rem(15px) !important;
              padding-left: rem(15px) !important;
            }
            @media screen and (max-width: 991px) {
              padding-left: 0 !important;
              padding-right: 0 !important;
            }
          }
        }
        &__left {
          flex: 0 0 385px;
          max-width: 385px;
          margin-right: rem(24px);
          @media screen and (max-width: 1500px) {
            flex: 0 0 340px;
            max-width: 340px;
            margin-right: rem(15px);
          }
          @media screen and (max-width: 1300px) {
            flex: 0 0 300px;
            max-width: 300px;
          }
          @media screen and (max-width: 1250px) {
            flex: none;
            max-width: 50%;
            margin: auto auto rem(25px) auto;
          }
          @media screen and (max-width: 991px) {
            max-width: 100%;
            width: 100%;
          }
        }
        &__right {
          flex: 1;
          .card {
            border: none;
            &__head {
              padding: rem(10px) rem(24px);
              border: 0;
              background: var(--imageBg);
              font-size: rem(14px);
              p {
                margin: 0;
                margin-top: rem(5px);
                font-weight: 500;
                color: var(--textPrimary);
              }
            }
          }
          .custom-col {
            display: flex;
            align-items: center;
            flex-direction: column;
            justify-content: center;
          }
          .btn {
            &.add {
              position: relative;
              padding-left: rem(44px);
              padding-right: rem(20px);
              height: 42px;
              &:before {
                background-image: url("data:image/svg+xml,%3Csvg width='16' height='9' viewBox='0 0 16 9' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M5.20711 0.792893C4.81658 0.402369 4.18342 0.402369 3.79289 0.792893L0.792893 3.79289L0.709705 3.8871C0.40468 4.27939 0.432409 4.84662 0.792893 5.20711L3.79289 8.20711L3.8871 8.2903C4.27939 8.59532 4.84662 8.56759 5.20711 8.20711L5.2903 8.1129C5.59532 7.72061 5.56759 7.15338 5.20711 6.79289L3.91466 5.5H14.5L14.6166 5.49327C15.114 5.43551 15.5 5.01284 15.5 4.5C15.5 3.94772 15.0523 3.5 14.5 3.5H3.91466L5.20711 2.20711L5.2903 2.1129C5.59532 1.72061 5.56759 1.15338 5.20711 0.792893Z' fill='white'/%3E%3C/svg%3E%0A");
                content: "";
                position: absolute;
                left: 15px;
                width: 18px;
                height: 10px;
                background-repeat: no-repeat;
                top: 50%;
                transform: translateY(-50%);
                @media screen and (max-width: 991px) {
                  transform: translateY(-50%) rotate(90deg);
                }
              }
              &:hover {
                &:before {
                  background-image: url("data:image/svg+xml,%3Csvg width='16' height='9' viewBox='0 0 16 9' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M5.20711 0.792893C4.81658 0.402369 4.18342 0.402369 3.79289 0.792893L0.792893 3.79289L0.709705 3.8871C0.40468 4.27939 0.432409 4.84662 0.792893 5.20711L3.79289 8.20711L3.8871 8.2903C4.27939 8.59532 4.84662 8.56759 5.20711 8.20711L5.2903 8.1129C5.59532 7.72061 5.56759 7.15338 5.20711 6.79289L3.91466 5.5H14.5L14.6166 5.49327C15.114 5.43551 15.5 5.01284 15.5 4.5C15.5 3.94772 15.0523 3.5 14.5 3.5H3.91466L5.20711 2.20711L5.2903 2.1129C5.59532 1.72061 5.56759 1.15338 5.20711 0.792893Z' fill='%231a90d2'/%3E%3C/svg%3E%0A");
                }
              }
            }
          }
        }
        @media screen and (max-width: 1250px) {
          .columnWrapper {
            flex-direction: column;
          }
        }
        .table {
          &__row {
            @media screen and (min-width: 992px) {
              padding-top: rem(8px);
              padding-bottom: rem(8px);
            }
            &--cell {
              &:first-child {
                padding-left: 1.5625rem !important;
                @media screen and (max-width: 1200px) {
                  padding-left: 1rem !important;
                }
                @media screen and (max-width: 991px) {
                  padding-left: 0 !important;
                }
              }
              &:last-child {
                @media screen and (max-width: 1200px) {
                  padding-right: 1rem !important;
                }
                @media screen and (max-width: 991px) {
                  padding-right: 0 !important;
                }
              }
            }
          }
          &__head {
            padding: rem(12px) rem(0px);
            border-width: 2px;
            .table__row {
              padding: 0;
              &--cell {
                padding: 0;
                font-size: rem(12px);
                font-weight: 400;
                color: var(--textSecondary);
                svg {
                  width: 24px;
                  height: 24px;
                }
              }
            }
          }
          &__body {
            border-radius: 0;
            border-width: 2px;
            border-bottom: none;
            .table__row {
              &:not(:last-child) {
                border-width: 2px;
              }
              &--cell {
                font-size: rem(16px);
                color: var(--default);
                padding-top: rem(4px);
                padding-bottom: rem(4px);
                // @media screen and (max-width: 1500px) {
                // 	font-size: rem(13px);
                // }
                @media screen and (max-width: 1500px) {
                  font-size: rem(15px);
                }
                @media screen and (max-width: 1300px) {
                  font-size: rem(14px);
                }
                svg {
                  width: 24px;
                  height: 24px;
                }
              }
              &:hover {
                @media screen and (min-width: 992px) {
                  background: #f5f5f5;
                }
                .table__row--cell {
                  text-decoration: none !important;
                  color: var(--textPrimary);
                }
              }
            }
          }
          a {
            &:hover {
              svg {
                opacity: 0.6;
              }
            }
          }
          .inline-buttons {
            display: flex;
            align-items: center;
          }
          &__footer {
            padding: rem(16px);
            border-top: 2px solid var(--borderColor);
            @media screen and (max-width: 991px) {
              padding: 0;
              padding-top: rem(16px);
              border: 0;
              border-radius: 0;
              margin-top: rem(16px);
            }
            @media screen and (min-width: 576px) and (max-width: 991px) {
              text-align: center;
              .btn {
                &.full {
                  width: 50%;
                }
              }
            }
          }
        }
        @media screen and (max-width: 1200px) {
          .table {
            &__row {
              &--cell {
                font-size: rem(13px);
              }
            }
          }
          // &__left {
          // 	max-width: 300px;
          // 	flex: 0 0 300px;
          // 	margin-right: rem(20px);
          // }
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
  .contentBox.serviceDetails {
    margin-bottom: 48px !important;
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
.patientRecord {
  &__left {
    margin-top: rem(15px);
    flex: 1;
  }
  &__right {
    flex: 0 0 300px;
  }
  @media screen and (max-width: 991px) {
    &__right {
      flex: 0 0 270px;
    }
  }
  @media screen and (max-width: 767px) {
    flex-direction: column;
    &__right {
      flex: none;
      width: 100%;
      margin: 0;
    }
  }
}
</style>
