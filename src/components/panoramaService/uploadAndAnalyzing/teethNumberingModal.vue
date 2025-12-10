<template>
  <b-modal
    v-model="teethNumberingModal"
    hide-footer
    hide-header
    size="xl"
    centered
    no-close-on-backdrop
    no-close-on-esc
    modal-class="teethNumberingModal"
  >
    <div class="teethNumberingModal__container">
      <div class="headingContainer">
        <div>
          <p class="heading">Teeth Numbering Validation</p>
          <p class="subHeading">
            You can add, edit , or remove teeth numbering
          </p>
        </div>
        <div>
          <button
            type="button"
            class="btn btn-success confirmButton"
            @click="updateService()"
            :disabled="isMissingTooth || isDuplicateTooth"
          >
            Confirm
          </button>
        </div>
      </div>

      <hr />

      <div class="numberingContainer">
        <div v-if="!isAddingNewTooth" class="numberingHeadingContainer">
          <div class="numberingTypes">
            <div
              :class="[
                'numberingType',
                { 'numberingType--active': isFDINumbering },
              ]"
              @click="isFDINumbering = true"
            >
              FDI Tooth Numbering
            </div>
            <div
              :class="[
                'numberingType',
                { 'numberingType--active': !isFDINumbering },
              ]"
              @click="isFDINumbering = false"
            >
              Universal Numbering
            </div>
          </div>
          <button
            type="button"
            class="btn btn-secondary newToothButton"
            @click="startAddNewTooth"
          >
            <font-awesome-icon :icon="['fa', 'plus']" />
            New Tooth
          </button>
        </div>
        <div v-else class="numberingHeadingContainer">
          <div class="addToothHeading">
            <p class="heading">Add New Tooth</p>
            <p class="subHeading">
              Draw a rectangle over the tooth area you want to add
            </p>
          </div>
          <div>
            <button
              type="button"
              class="btn cancelButton"
              @click="cancelAddingTooth"
            >
              Cancel
            </button>
            <button
              type="button"
              class="btn btn-secondary newToothButton"
              @click="openTeethNumberingModal"
            >
              Set Tooth Number
            </button>
          </div>
        </div>

        <img
          :src="service.files[0].file"
          class="img-fluid orthoImage"
          :style="{
            width: `${service.service_data.imageDimensions.width}px`,
            height: `${service.service_data.imageDimensions.height}px`,
          }"
        />

        <div
          v-for="(point, index) in service.service_data.points"
          :key="point.classes + index"
          class="teethNumberContainer"
          :class="{
            'teethNumberContainer--duplicate': isToothDuplicate(point.classes),
          }"
          :style="getToothPosition(point.classes, point)"
          @click="openTeethNumberingModal(point.classes, index)"
        >
          <div
            v-if="!isNaN(point.classes) || point.classes == 'Missing'"
            class="teethNumber"
          >
            {{ getToothNumber(point.classes) }}
          </div>
        </div>

        <VueDragResize
          v-if="isAddingNewTooth"
          :isActive="true"
          :isResizable="true"
          :isDraggable="true"
          :parentLimitation="true"
          :aspectRatio="false"
          :w="newAddedTooth.width"
          :h="newAddedTooth.height"
          :x="newAddedTooth.x"
          :y="newAddedTooth.y"
          class="newToothWrapper"
          @dragstop="changeToothPosition"
          @resizing="changeToothPosition"
          :z="1"
        >
        </VueDragResize>

        <div class="patientInfoContainer">
          <div class="patientInfo">
            <div>
              <p class="title">Record date:</p>
              <p class="subTitle">{{ serviceCreated }}</p>
            </div>
            <div>
              <p class="title">Patient name:</p>
              <p class="subTitle">
                {{
                  `${service.patient_obj.first_name} ${service.patient_obj.last_name}`
                }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <select-tooth-number
      :selectedTooth="selectedTooth"
      :selectedToothIndex="selectedToothIndex"
      :changeTeethNumberModal="changeTeethNumberModal"
      :isFDINumbering="isFDINumbering"
      :closeTeethNumberingModal="closeTeethNumberingModal"
      :isAddingNewTooth="isAddingNewTooth"
      :setNewToothNumber="setNewToothNumber"
    />
  </b-modal>
</template>

<script>
import { mapState } from "vuex";
import moment from "moment";
import VueDragResize from "vue-drag-resize";

import { UPDATE_PANORAMA_SERVICE } from "@/store/modules/panoramaService/actions";
import { SERVICE_MUTATIONS } from "@/store/modules/service/actions";
import { SERVICE_STATUS } from "@/utils/constants";
import {
  leftTopTeethNumbers,
  leftBottomTeethNumbers,
  leftTopTeethNumbers2,
  leftBottomTeethNumbers2,
  rightTopTeethNumbers,
  rightBottomTeethNumbers,
  rightTopTeethNumbers2,
  rightBottomTeethNumbers2,
  universalNumbering,
} from "@/utils/constants";

import selectToothNumber from "./selectToothNumber";

export default {
  name: "TeethNumberingModal",
  components: { selectToothNumber, VueDragResize },
  data() {
    return {
      teethNumberingModal: true,
      selectedTooth: null,
      selectedToothIndex: null,
      changeTeethNumberModal: false,
      isFDINumbering: true,

      leftTopTeethNumbers,
      leftBottomTeethNumbers,
      leftTopTeethNumbers2,
      leftBottomTeethNumbers2,
      rightTopTeethNumbers,
      rightBottomTeethNumbers,
      rightTopTeethNumbers2,
      rightBottomTeethNumbers2,
      universalNumbering,

      isAddingNewTooth: false,
      newAddedTooth: {
        classes: null,
        x: 600,
        y: 250,
        width: 50,
        height: 100,
      },
    };
  },
  computed: {
    ...mapState({
      service: (state) => state.service.serviceDetail,
    }),
    serviceCreated() {
      return moment(this.service.created).format("YYYY-MM-DD");
    },
    isDuplicateTooth() {
      let isDuplicate = false;

      this.service?.service_data?.points?.forEach((point) => {
        if (!isNaN(point.classes) && this.isToothDuplicate(point.classes)) {
          isDuplicate = true;
          return;
        }
      });

      return isDuplicate;
    },
    isMissingTooth() {
      const missingItems = this.service?.service_data?.points?.filter(
        (point) => point.classes == "Missing"
      );

      return missingItems?.length > 0;
    },
  },
  methods: {
    getToothNumber(toothNumber) {
      return toothNumber == "Missing"
        ? "X"
        : this.isFDINumbering
        ? toothNumber
        : this.universalNumbering[toothNumber];
    },
    isToothDuplicate(toothNumber) {
      if (!isNaN(toothNumber)) {
        const points = this.service.service_data.points;
        const allMachingPoints = points.filter(
          (point) => point.classes == toothNumber
        );
        return allMachingPoints?.length > 1;
      }

      return false;
    },
    selectTooth(toothNumber, toothIndex) {
      this.selectedTooth = toothNumber;
      this.selectedToothIndex = toothIndex;
    },
    openTeethNumberingModal(toothNumber, toothIndex) {
      this.selectTooth(toothNumber, toothIndex);
      this.changeTeethNumberModal = true;
    },
    closeTeethNumberingModal() {
      this.changeTeethNumberModal = false;
      this.selectTooth(null, null);
    },
    getToothPosition(toothNumber, tooth) {
      if (!isNaN(toothNumber)) {
        const originalImageHeight =
          this.service.service_data.imageDimensions.height;
        const originalImageWidth =
          this.service.service_data.imageDimensions.width;
        const pred_boxes = tooth.pred_boxes;
        const left = `${
          ((pred_boxes[0] + (pred_boxes[2] - pred_boxes[0] - 35) / 2) * 100) /
          originalImageWidth
        }%`;

        if (
          this.isLeftTopTooth(toothNumber) ||
          this.isRightTopTooth(toothNumber)
        ) {
          const top = `${((pred_boxes[3] - 50) * 100) / originalImageHeight}%`;

          return { top, left };
        } else if (
          this.isLeftBottomTooth(toothNumber) ||
          this.isRightBottomTooth(toothNumber)
        ) {
          const top = `${((pred_boxes[1] + 30) * 100) / originalImageHeight}%`;

          return { top, left };
        }
      }

      return { top: 0, left: 0 };
    },
    isLeftTopTooth(toothNumber) {
      return (
        this.leftTopTeethNumbers.includes(toothNumber) ||
        this.leftTopTeethNumbers2.includes(toothNumber)
      );
    },
    isLeftBottomTooth(toothNumber) {
      return (
        this.leftBottomTeethNumbers.includes(toothNumber) ||
        this.leftBottomTeethNumbers2.includes(toothNumber)
      );
    },
    isRightTopTooth(toothNumber) {
      return (
        this.rightTopTeethNumbers.includes(toothNumber) ||
        this.rightTopTeethNumbers2.includes(toothNumber)
      );
    },
    isRightBottomTooth(toothNumber) {
      return (
        this.rightBottomTeethNumbers.includes(toothNumber) ||
        this.rightBottomTeethNumbers2.includes(toothNumber)
      );
    },
    updateService() {
      this.$store.dispatch(UPDATE_PANORAMA_SERVICE, {
        serviceId: this.service.id,
        ...this.service,
        status: SERVICE_STATUS.ANALYZED.title,
      });
    },
    startAddNewTooth() {
      this.isAddingNewTooth = true;
    },
    endAddingNewTooth() {
      this.isAddingNewTooth = false;
      this.newAddedTooth = {
        classes: null,
        x: 600,
        y: 250,
        width: 50,
        height: 100,
      };
    },
    cancelAddingTooth() {
      this.endAddingNewTooth();
    },
    changeToothPosition(newRect) {
      this.newAddedTooth = {
        ...this.newAddedTooth,
        x: newRect.left,
        y: newRect.top,
        width: newRect.width,
        height: newRect.height,
      };
    },
    setNewToothNumber(toothNumber) {
      this.newAddedTooth = {
        ...this.newAddedTooth,
        classes: toothNumber,
      };

      const service = { ...this.service };
      service.service_data.points.push({
        classes: toothNumber,
        scores: 1,
        pred_boxes: [
          this.newAddedTooth.x,
          this.newAddedTooth.y,
          this.newAddedTooth.x + this.newAddedTooth.width,
          this.newAddedTooth.y + this.newAddedTooth.height,
        ],
      });

      this.$store.commit(SERVICE_MUTATIONS.SET_SERVICE_DETAIL, {
        ...service,
      });

      this.endAddingNewTooth();
    },
  },
};
</script>

<style lang="scss" scoped></style>

<style lang="scss">
.teethNumberingModal {
  .modal-content {
    padding: 48px !important;
  }

  .modal-dialog {
    max-width: unset !important;
    width: auto !important;
    display: inline-flex !important;
  }

  svg {
    position: initial !important;
    margin-right: 12px;
    margin-top: 24px;
  }

  &__container {
    position: relative;

    .headingContainer {
      display: flex;
      justify-content: space-between;

      .heading {
        font-family: "Rubik";
        font-weight: 500;
        font-size: 32px !important;
        color: #171716 !important;
        margin-bottom: 0;
      }
      .subHeading {
        font-family: "Rubik";
        font-style: normal;
        font-weight: 400;
        font-size: 16px !important;
        color: #6b6b6b !important;
        margin-bottom: 32px;
      }
    }

    hr {
      margin: 0;
    }

    .numberingContainer {
      position: relative;
      display: inline-block;
      margin-top: 32px;

      .numberingHeadingContainer {
        position: absolute;
        top: 0;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        padding: 24px;
        background: rgba(23, 23, 22, 0.87);
        border-radius: 12px 12px 0px 0px;
        height: 100px;
        width: 100%;

        .numberingTypes {
          background: #444441;
          border-radius: 55px;

          .numberingType {
            font-family: "Rubik";
            font-weight: 500;
            color: #8e8e8e;
            font-size: 16px;
            cursor: pointer;
            padding: 12px 32px;
            display: inline-block;
            border-radius: 55px;

            &--active {
              color: #fcfcfc;
              background: #5c5c5c;
              border: 1px solid #8e8e8e;
            }
          }
        }

        .newToothButton {
          color: white;
          background: var(--primary);
        }

        .addToothHeading {
          .heading {
            font-family: "Rubik";
            font-weight: 500;
            font-size: 24px;
            color: #fcfcfc;
            margin-bottom: 0;
          }
          .subHeading {
            font-family: "Rubik";
            font-weight: 400;
            font-size: 16px;
            color: #c9c9c9;
            margin-bottom: 0;
          }
        }

        .cancelButton {
          color: #c9c9c9;
          &:hover {
            color: #c9c9c9;
          }
        }
      }

      .newToothWrapper {
        border: 2px solid #6cf760;
        cursor: pointer;
      }

      .patientInfoContainer {
        position: absolute;
        bottom: 0;
        width: 100%;
        padding: 12px 48px;
        background: rgba(23, 23, 22, 0.87);
        border-radius: 0px 0px 12px 12px;

        .patientInfo {
          display: flex;
          flex-wrap: wrap;
          justify-content: space-between;

          div {
            display: inline-block;

            .title {
              font-family: "Rubik";
              font-weight: 400;
              font-size: 16px;
              color: #8e8e8e;
              margin-bottom: 5px;
            }
            .subTitle {
              font-family: "Rubik";
              font-weight: 400;
              font-size: 14px;
              color: #f5f5f5;
              margin: 0;
            }
          }
        }
      }
    }
    .orthoImage {
      border-radius: 16px;
    }
    .teethNumberContainer {
      position: absolute;
      width: 32px;
      height: 32px;

      &--duplicate {
        .teethNumber {
          border: 2px solid #ea5a43 !important;
        }
      }

      .teethNumber {
        cursor: pointer;
        width: 32px;
        height: 32px;
        background: #ffffff;
        opacity: 0.7;
        border: 1px solid #6b6b6b;
        border-radius: 8px;
        display: flex;
        justify-content: center;
        align-items: center;
      }
    }

    .confirmButton {
      background: #ea5a43;
      border-color: #ea5a43;
      margin-bottom: 0 !important;

      &:hover,
      &:active {
        background: #ea5a43;
        border-color: #ea5a43;
      }

      &:disabled {
        background: #f7bdb4;
        border-color: #f7bdb4;

        &:hover {
          background: #f7bdb4;
          border-color: #f7bdb4;
        }
      }

      height: 52px;
      width: 149px;
      margin-top: 24px;
    }
  }
}
</style>
