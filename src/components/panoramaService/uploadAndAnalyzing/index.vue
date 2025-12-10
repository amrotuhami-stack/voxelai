<template>
  <div v-if="service && service.id">
    <!-- 
      - component for uploading and analyzing if there is not analyzed image
    -->
    <image-uploading v-if="isUploadingPhase" />
    <service-analyzing v-else-if="isAnalyzingPhase" />
  </div>
</template>

<script>
import { mapState } from "vuex";
import { SERVICE_STATUS } from "@/utils/constants";
import ImageUploading from "./imageUploading.vue";
import ServiceAnalyzing from "./serviceAnalyzing.vue";

export default {
  name: "uploadAndAnalyzing",
  components: {
    ImageUploading,
    ServiceAnalyzing,
  },
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
    imageURL() {
      return this.service?.files?.length > 0
        ? this.service?.files[0]?.file
        : require("@/assets/images/dummyOrthoBG.png");
    },
    isUploadingPhase() {
      return (
        !this.isAnalyzing && this.service?.status === SERVICE_STATUS.NEW.title
      );
    },
    isAnalyzingPhase() {
      return (
        this.isAnalyzing ||
        this.service?.status === SERVICE_STATUS.TEETH_NUMBERING_VALIDATION.title
      );
    },
  },
  methods: {},
};
</script>
