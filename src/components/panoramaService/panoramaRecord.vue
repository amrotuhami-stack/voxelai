<template>
  <div class="panoramaServiceRecord">
    <b-container fluid>
      <b-row>
        <b-col lg="6" cols="12">
          <p class="panoramaServiceRecord__heading">Panoramic Analysis</p>
          <p class="panoramaServiceRecord__subHeading">
            Artificial Intelligence automatically analysis panoramic radiograph.
          </p>
        </b-col>
        <b-col v-if="isAnalysisButtonViewed" lg="6" cols="12">
          <div class="buttonContainer">
            <button
              type="button"
              class="btn btn-primary"
              @click="startAnalysis"
              :disabled="isAnalyzing"
            >
              Start Analysis
            </button>
          </div>
        </b-col>
      </b-row>
      <!-- 
        - component for uploading and analyzing if there is not analyzed image (status is (NEW or Start Analysis))
        - component fot the other work if the imaged uploaded and analyzed
      -->

      <upload-and-analyzing v-if="isUploadOrAnalyze" />
    </b-container>
  </div>
</template>

<script>
import { START_PANORAMA_ANALYSIS } from "@/store/modules/panoramaService/actions";
import { mapState } from "vuex";
import UploadAndAnalyzing from "@/components/panoramaService/uploadAndAnalyzing/index.vue";
import { SERVICE_STATUS } from "@/utils/constants";
import { ServiceHelper } from "@/common/crud-helpers/service";

export default {
  name: "panoramaRecord",
  props: {
    recordId: {
      type: String | Number,
      default: "",
    },
  },
  components: { UploadAndAnalyzing },
  data() {
    return {
      SERVICE_STATUS,
    };
  },
  computed: {
    ...mapState({
      service: (state) => state.service.serviceDetail,
      isAnalyzing: (state) => state.panoramaService.isAnalyzing,
    }),
    isUploadOrAnalyze() {
      return (
        this.service?.status === SERVICE_STATUS.NEW.title ||
        this.service?.status === SERVICE_STATUS.TEETH_NUMBERING_VALIDATION.title
      );
    },
    isAnalysisButtonViewed() {
      return (
        this.service?.status === SERVICE_STATUS.NEW.title &&
        this.service?.files?.length > 0
      );
    },
  },
  created() {
    this.getService();
  },
  methods: {
    getService() {
      ServiceHelper.getServiceDetail(this.recordId);
    },
    startAnalysis() {
      this.$store.dispatch(START_PANORAMA_ANALYSIS, {
        service: this.service,
        imageUrl: this.service.files[0].file,
        serviceId: this.recordId,
      });
    },
  },
};
</script>

<style scoped lang="scss">
.panoramaServiceRecord {
  padding: 16px;

  &__heading {
    font-family: "Rubik";
    font-style: normal;
    font-weight: 500;
    font-size: 20px;
    color: #171716;
    margin-top: 0;
    margin-bottom: 8px;
  }

  &__subHeading {
    font-family: "Rubik";
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    color: #6b6b6b;
    margin-top: 0;
    margin-bottom: 28px;
  }

  .buttonContainer {
    display: flex;
    justify-content: flex-end;
  }

  @media (max-width: 991.98px) {
    .buttonContainer {
      justify-content: flex-start;
      margin-bottom: 28px;
    }
  }
}
</style>

<style lang="scss">
.panoramaServiceRecord {
  .btn-primary {
    --bs-btn-bg: var(--primary-blue);
    --bs-btn-border-color: var(--primary-blue);
    --bs-btn-hover-bg: var(--primary-blue);
    --bs-btn-hover-border-color: var(--primary-blue);
    --bs-btn-active-bg: var(--primary-blue);
    --bs-btn-active-border-color: var(--primary-blue);
    --bs-btn-disabled-bg: var(--secondary-blue);
    --bs-btn-disabled-border-color: var(--secondary-blue);

    height: 52px;
    width: 100%;
    max-width: 384px;
  }
}
</style>
