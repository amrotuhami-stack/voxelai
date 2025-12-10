<template>
  <b-container fluid class="cephService__recordsView">
    <b-row>
      <!-- Cephalo.AI Patient Records -->
      <b-col lg="3" md="6" sm="12" class="cephService__recordsView__col" :key="record.id" v-for="(record) in patientAiServices">
        <a :href="`https://voxel3di.web.app/services/${record.id}/?token=${token}`" target="_blank" rel="noopener">
        <!-- <a :href="`https://voxel3di.web.app/services/${record.id}/`" target="_blank" rel="noopener"> -->
          <div class="cephService__recordsView__record" >
            <img :src="getImageURL(record)" class="img-fluid recordImage" alt="Cephalo.AI Image"/>
            <b-badge pill :class="['pill-badge', getRecordData(record).class]"> {{ getRecordData(record).status }} </b-badge>
            <div class="record-date"> {{ record.created | formatDate }} </div>
          </div>
        </a>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>

// [*] Vuex State Getter And Action Helper
import Vue from "vue";
import { mapGetters } from "vuex";

export default {
  props: {},
  data() {
    return {
      token: null,
      recordStatus: {
        "NEW": {
          status: "Upload File",
          class: "orange-color",
        },
        "START": {
          status: "Start AI Analysis",
          class: "blue-color",
        },
      },
    };
  },
  computed: {
    ...mapGetters(["patientAiServices"]),
  },
  created() {
    this.$auth.isUserAuth((auth_obj) => {
      this.token = auth_obj.access_token
    })
  },
  methods: {
    getImageURL(record) {
      return record.files?.length > 0
        ? record.files[0].file
        : require("@/assets/images/cephRecord.png");
    },
    getRecordData(record) {
      const status = record.status;
      if (status === "NEW") {
        if (record?.files?.length > 0) return this.recordStatus["START"];
        return this.recordStatus["NEW"];
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.cephService {
  &__recordsView {
    &__col {
      padding-left: 0px;
      padding-right: 24px;
    }
    &__record {
      width: 100%;
      height: 169px;
      margin-bottom: 24px;
      position: relative;
      border-radius: 12px;
      cursor: pointer;

      .recordImage {
        object-fit: cover;
        border-radius: 12px;
        height: 100%;
        width: 100%;
      }

      .pill-badge {
        padding: 8px 16px;
        position: absolute;
        left: 16px;
        top: 16px;
        background: rgba(23, 23, 22, 0.4);
        border-radius: 12px;
        font-size: 14px;
        font-weight: 300;

        &.orange-color {
          border: 1px solid #f7c0b7;
          color: #f7c0b7;
        }
        &.blue-color {
          border: 1px solid #a8d5ee;
          color: #a8d5ee;
        }
        &.success-color {
          border: 1px solid #a8eec4;
          color: #a8eec4;
        }
      }

      .record-date {
        position: absolute;
        left: 16px;
        bottom: 16px;
        font-family: "Rubik";
        font-weight: 400;
        font-size: 16px;
        line-height: 24px;
        color: #e9e9e9;
      }
    }
  }
}
</style>
