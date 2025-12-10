<template>
  <div class="analyzingContainer">
    <img :src="this.service.files[0].file" class="img-fluid orthoImage" />

    <div v-if="isAnalyzing" class="analyzingContainer__upladBar">
      <p class="text">Analyzing...</p>
      <b-progress
        :value="fileAnalyzedPercentage"
        max="100"
        height="12px"
      ></b-progress>
    </div>

    <div
      v-else-if="isTeethNumbringValidationPhase"
      class="analyzingContainer__teethNumbering"
    >
      <teeth-numbering-modal />
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { SERVICE_STATUS } from "@/utils/constants";
import TeethNumberingModal from "@/components/panoramaService/uploadAndAnalyzing/teethNumberingModal.vue";

export default {
  name: "AnalyzingService",
  components: { TeethNumberingModal },
  data() {
    return {};
  },
  computed: {
    ...mapState({
      service: (state) => state.service.serviceDetail,
      fileAnalyzedPercentage: (state) =>
        state.panoramaService.fileAnalyzedPercentage,
      isAnalyzing: (state) => state.panoramaService.isAnalyzing,
    }),
    isTeethNumbringValidationPhase() {
      return (
        this.service?.status === SERVICE_STATUS.TEETH_NUMBERING_VALIDATION.title
      );
    },
  },
  methods: {},
};
</script>

<style lang="scss" scoped>
.analyzingContainer {
  position: relative;

  .orthoImage {
    height: 627px;
    width: 100%;
  }

  &__upladBar {
    position: absolute;
    top: calc(50% - 26px);
    left: calc(50% - 150px);
    width: 300px;

    .text {
      font-family: "Rubik";
      font-weight: 500;
      font-size: 16px;
      line-height: 40px;
      text-align: center;
      color: #c9c9c9;
      margin-bottom: 0;
    }
  }
}
</style>

<style lang="scss">
.analyzingContainer {
  .progress {
    --bs-progress-bar-bg: #ea5a43;

    .progress-bar {
      background-color: #ea5a43 !important;
      background-image: linear-gradient(
        45deg,
        hsla(0, 0%, 100%, 0.15) 25%,
        transparent 0,
        transparent 50%,
        hsla(0, 0%, 100%, 0.15) 0,
        hsla(0, 0%, 100%, 0.15) 75%,
        transparent 0,
        transparent
      );
      background-size: 1rem 1rem;
      height: 12px;
    }
  }
}
</style>
