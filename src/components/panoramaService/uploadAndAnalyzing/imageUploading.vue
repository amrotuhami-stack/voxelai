<template>
  <div
    class="uploadingContainer"
    @dragover.prevent="isDraging = true"
    @dragleave.prevent="isDraging = false"
    @drop.prevent="onDropFile"
  >
    <img :src="imageURL" class="img-fluid orthoImage" />
    <div
      v-if="isDraging && !isServiceContainsFiles && !isUploading"
      class="uploadingContainer__upladText"
    >
      <p class="text">Drop Image here...</p>
    </div>
    <div
      v-else-if="!isDraging && !isServiceContainsFiles && !isUploading"
      class="uploadingContainer__upladText"
    >
      <img
        src="@/assets/images/icons/upload.svg"
        class="img-fluid"
        @drop.prevent="onDropFile"
      />
      <p class="text">Drag and Drop file here</p>
      <p class="text">-- or --</p>
      <p class="text browsButton" @click="openFileInput">Browse</p>
    </div>
    <div v-else-if="isUploading" class="uploadingContainer__upladBar">
      <p class="text">Uploading...</p>
      <b-progress
        :value="fileUploadedPercentage"
        max="100"
        height="12px"
        animated
      ></b-progress>
    </div>

    <div
      v-if="isServiceContainsFiles"
      class="uploadingContainer__uploadedImageInfo"
    >
      <div>
        <p class="fileNameText">File name:</p>
        <p class="fileName">{{ service.files[0].name }}</p>
      </div>
      <div>
        <button
          type="button"
          class="btn btn-outline-secondary"
          @click="deleteServiceImage"
        >
          <img src="@/assets/images/icons/trashIcon.svg" class="img-fluid" />
          Remove
        </button>
      </div>
    </div>

    <input
      id="questionInputFile"
      ref="questionInputFile"
      type="file"
      accept="image/*"
      @input="selectFile($event)"
    />
  </div>
</template>

<script>
import {
  ADD_PANORAMA_SERVICE_FILE,
  UPDATE_PANORAMA_SERVICE_FILE,
  DELETE_PANORAMA_SERVICE_FILE,
} from "@/store/modules/panoramaService/actions";
import { mapGetters, mapState } from "vuex";
import { ServiceHelper } from "@/common/crud-helpers/service";

export default {
  name: "ImageUploading",
  components: {},
  data() {
    return {
      isDraging: false,
      image: null,
      imageName: "",
    };
  },
  computed: {
    ...mapState({
      service: (state) => state.service.serviceDetail,
      fileUploadedPercentage: (state) =>
        state.panoramaService.fileUploadedPercentage,
      isUploading: (state) => state.panoramaService.isUploading,
    }),
    ...mapGetters(["orderLine"]),
    imageURL() {
      return this.service?.files?.length > 0
        ? this.service?.files[0]?.file
        : require("@/assets/images/dummyOrtho.png");
    },
    isServiceContainsFiles() {
      return this.service?.files?.length > 0;
    },
  },
  methods: {
    openFileInput() {
      document.getElementById("questionInputFile").click();
    },
    selectFile(event) {
      const file = event.target?.files[0];
      this.handleSelectedFile(file);
    },
    onDropFile(e) {
      this.isDraging = false;
      const file = e.dataTransfer.files[0];
      this.handleSelectedFile(file);
    },
    handleSelectedFile(file) {
      if (file) {
        this.isUploaded = false;
        this.image = file;
        this.imageName = file?.name || "";

        this.readImage();
      }
    },
    readImage() {
      const fr = new FileReader();
      fr.onload = () => {
        const img = new Image();
        img.onload = () => {
          this.handleUploadImage(img.width, img.height);
        };
        img.src = fr.result;
      };
      fr.readAsDataURL(this.image);
    },
    handleUploadImage(width, height) {
      let body = {
        file: this.image,
        fileName: this.imageName,
        serviceId: this.$route.params.id,
        width,
        height,
      };
      let uploadAPI = ADD_PANORAMA_SERVICE_FILE;

      if (this.service?.files?.length > 0) {
        body.fileId = this.service.files[0].id;
        uploadAPI = UPDATE_PANORAMA_SERVICE_FILE;
      }
      this.uploadImage(uploadAPI, body);
    },
    uploadImage(url, body) {
      this.$store
        .dispatch(url, body)
        .then(() => {
          this.getService();
          this.getPatientAiServices();
        })
        .catch(() => {});
    },
    getService() {
      ServiceHelper.getServiceDetail(this.$route.params.id);
    },
    getPatientAiServices() {
      ServiceHelper.getPatientAiServices({
        patient_id: this.$route.params.patient,
        product_id: this.orderLine.product_obj.id,
      });
    },
    deleteServiceImage() {
      this.$store
        .dispatch(DELETE_PANORAMA_SERVICE_FILE, {
          serviceId: this.$route.params.id,
          fileId: this.service.files[0].id,
        })
        .then(() => {
          this.getService();
        })
        .catch(() => {});
    },
  },
};
</script>

<style lang="scss" scoped>
.uploadingContainer {
  position: relative;

  .orthoImage {
    height: 627px;
    width: 100%;
  }

  &__upladText {
    position: absolute;
    top: calc(50% - 92px);
    left: calc(50% - 88px);
    display: flex;
    flex-direction: column;

    img {
      height: 64px;
      margin: auto;
      margin-bottom: 8px;
    }
    .text {
      font-family: "Rubik";
      font-weight: 500;
      font-size: 16px;
      line-height: 40px;
      text-align: center;
      color: #c9c9c9;
      margin-bottom: 0;
    }
    .browsButton {
      color: #ea5a43;
      cursor: pointer;
    }
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

  #questionInputFile {
    display: none;
  }

  &__uploadedImageInfo {
    padding-inline: 48px;
    position: absolute;
    bottom: 50px;
    display: flex;
    justify-content: space-between;
    width: 100%;

    .fileNameText {
      font-family: "Rubik";
      font-weight: 400;
      font-size: 16px;
      line-height: 24px;
      color: #8e8e8e;
      margin-bottom: 0;
    }
    .fileName {
      font-family: "Rubik";
      font-weight: 400;
      font-size: 14px;
      line-height: 20px;
      color: #f5f5f5;
      margin-bottom: 0;
    }
  }
}
</style>

<style lang="scss">
.uploadingContainer {
  &__uploadedImageInfo {
    .btn {
      border: 2px solid var(--bs-gray-600);

      &:hover {
        background: transparent;
      }
    }
    .btn-outline-secondary {
      --bs-btn-color: #fff;
      --bs-btn-hover-bg: transparent;
      --bs-btn-active-bg: transparent;
      height: 45px;
    }
  }

  .progress {
    .progress-bar {
      background-color: #1a90d2;
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
