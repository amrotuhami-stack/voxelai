<template>
  <b-container fluid class="panoramaService__recordsView">
    <!-- patientAiServices -->
    <!-- updateSelectedRecord(index) -->
    <b-row>
      <b-col
        xl="3"
        lg="4"
        md="6"
        sm="12"
        class="panoramaService__recordsView__col"
        v-for="(record, index) in patientAiServices"
        :key="record.id"
      >
        <div
          class="panoramaService__recordsView__record"
          @click="updateSelectedRecord(index)"
        >
          <img :src="getImageURL(record)" class="img-fluid recordImage" />
          <b-badge pill :class="['pill-badge', getRecordData(record).class]">
            {{ getRecordData(record).status }}
          </b-badge>
          <div class="record-date">
            {{ record.created | formatDate }}
          </div>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import Vue from "vue";

// [*] Vuex State Getter And Action Helper
import { mapGetters } from "vuex";

export default {
  props: {
    updateSelectedRecord: Function,
  },
  data() {
    return {
      recordStatus: {
        NEW: {
          status: "Upload File",
          class: "orange-color",
        },
        "Start Analysis": {
          status: "Start Analysis",
          class: "blue-color",
        },
        "Needs Approval": {
          status: "Needs Approval",
          class: "orange-color",
        },
        Signed: {
          status: "Signed",
          class: "success-color",
        },
      },
    };
  },
  computed: {
    ...mapGetters(["patientAiServices"]),
  },
  methods: {
    getImageURL(record) {
      return record.files?.length > 0
        ? record.files[0].file
        : require("@/assets/images/dummyOrtho.png");
    },
    getRecordData(record) {
      const status = record.status;

      if (status === "NEW") {
        if (record?.files?.length > 0) {
          return this.recordStatus["Start Analysis"];
        } else {
          return this.recordStatus["NEW"];
        }
      } else if (
        status === "TEETH_NUMBERING_VALIDATION" ||
        status === "ANALYZED"
      ) {
        return this.recordStatus["Needs Approval"];
      } else if (status === "SIGNED") {
        return this.recordStatus["SIGNED"];
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.panoramaService {
  &__recordsView {
    &__col {
      padding-left: 0;
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
        height: 100%;
        width: 100%;
        border-radius: 12px;
      }

      .pill-badge {
        padding: 5px 16px;
        position: absolute;
        left: 16px;
        top: 16px;
        background: rgba(23, 23, 22, 0.4);
        border-radius: 16px;
        font-size: 12px;
        font-weight: 500;

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
