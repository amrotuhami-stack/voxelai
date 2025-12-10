<template>
  <b-modal
    v-model="changeTeethNumberModal"
    hide-footer
    hide-header
    size="xl"
    centered
    no-close-on-backdrop
    no-close-on-esc
    modal-class="selectTeethNumberModal"
  >
    <div class="selectTeethNumberModal__container">
      <div v-if="!isAddingNewTooth" class="heading">
        <p class="text">Change Tooth Number - {{ selectedTooth }}</p>
        <button
          type="button"
          class="btn removeToothButton"
          @click="removeTooth()"
        >
          <img
            src="@/assets/images/icons/redTrashIcon.svg"
            class="img-fluid mr-2"
          />
          Remove Tooth
        </button>
      </div>

      <div v-else class="heading">
        <p class="text">Set Tooth Number</p>
        <button
          type="button"
          class="btn removeToothButton"
          @click="closeTeethNumberingModal()"
        >
          Cancel
        </button>
      </div>

      <div class="container" fluid>
        <div class="row">
          <div class="col-6">
            <div class="teethNumberContainerRow justify-content-end">
              <div
                v-for="toothNumber in leftTeethNumbersRow1"
                :key="toothNumber"
                class="teethNumberContainer"
              >
                <div
                  class="teethNumber"
                  :class="{
                    'teethNumber--selected': toothNumber == selectedTooth,
                  }"
                  @click="changeToothNumber(toothNumber)"
                >
                  {{ getToothNumber(toothNumber) }}
                </div>
              </div>
            </div>
            <div class="teethNumberContainerRow justify-content-end">
              <div
                v-for="toothNumber in leftTopTeethNumbers2"
                :key="toothNumber"
                class="teethNumberContainer"
              >
                <div
                  class="teethNumber"
                  :class="{
                    'teethNumber--selected': toothNumber == selectedTooth,
                  }"
                  @click="changeToothNumber(toothNumber)"
                >
                  {{ getToothNumber(toothNumber) }}
                </div>
              </div>
            </div>
            <div class="teethNumberContainerRow justify-content-end">
              <div
                v-for="toothNumber in leftBottomTeethNumbers2"
                :key="toothNumber"
                class="teethNumberContainer"
              >
                <div
                  class="teethNumber mb-0"
                  :class="{
                    'teethNumber--selected': toothNumber == selectedTooth,
                  }"
                  @click="changeToothNumber(toothNumber)"
                >
                  {{ getToothNumber(toothNumber) }}
                </div>
              </div>
            </div>
          </div>

          <div class="col-6">
            <div class="teethNumberContainerRow">
              <div
                v-for="toothNumber in rightTeethNumbersRow1"
                :key="toothNumber"
                class="teethNumberContainer"
              >
                <div
                  class="teethNumber"
                  :class="{
                    'teethNumber--selected': toothNumber == selectedTooth,
                  }"
                  @click="changeToothNumber(toothNumber)"
                >
                  {{ getToothNumber(toothNumber) }}
                </div>
              </div>
            </div>
            <div class="teethNumberContainerRow">
              <div
                v-for="toothNumber in rightTopTeethNumbers2"
                :key="toothNumber"
                class="teethNumberContainer"
              >
                <div
                  class="teethNumber"
                  :class="{
                    'teethNumber--selected': toothNumber == selectedTooth,
                  }"
                  @click="changeToothNumber(toothNumber)"
                >
                  {{ getToothNumber(toothNumber) }}
                </div>
              </div>
            </div>
            <div class="teethNumberContainerRow">
              <div
                v-for="toothNumber in rightBottomTeethNumbers2"
                :key="toothNumber"
                class="teethNumberContainer"
              >
                <div
                  class="teethNumber mb-0"
                  :class="{
                    'teethNumber--selected': toothNumber == selectedTooth,
                  }"
                  @click="changeToothNumber(toothNumber)"
                >
                  {{ getToothNumber(toothNumber) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </b-modal>
</template>

<script>
import { mapState } from "vuex";
import { SERVICE_MUTATIONS } from "@/store/modules/service/actions";
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

export default {
  name: "TeethNumberingModal",
  components: {},
  props: {
    selectedTooth: {
      type: Number | String | null,
      default: null,
    },
    selectedToothIndex: {
      type: Number | String | null,
      default: null,
    },
    changeTeethNumberModal: {
      type: Boolean,
      default: false,
    },
    isFDINumbering: {
      type: Boolean,
      default: false,
    },
    closeTeethNumberingModal: {
      type: Function,
      default: () => {},
    },
    isAddingNewTooth: {
      type: Boolean,
      default: false,
    },
    setNewToothNumber: {
      type: Function,
      default: () => {},
    },
  },
  data() {
    return {
      leftTopTeethNumbers,
      leftBottomTeethNumbers,
      leftTopTeethNumbers2,
      leftBottomTeethNumbers2,
      rightTopTeethNumbers,
      rightBottomTeethNumbers,
      rightTopTeethNumbers2,
      rightBottomTeethNumbers2,
      universalNumbering,
    };
  },
  computed: {
    ...mapState({
      service: (state) => state.service.serviceDetail,
    }),
    leftTeethNumbersRow1() {
      return this.leftTopTeethNumbers.concat(this.leftBottomTeethNumbers);
    },
    rightTeethNumbersRow1() {
      return this.rightTopTeethNumbers.concat(this.rightBottomTeethNumbers);
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
    selectTooth(toothNumber, toothIndex) {
      this.selectedTooth = toothNumber;
      this.selectedToothIndex = toothIndex;
    },
    changeToothNumber(toothNumber) {
      if (this.isAddingNewTooth) {
        this.setNewToothNumber(toothNumber);
      } else {
        this.updatePointNumber(toothNumber);
      }
      this.closeTeethNumberingModal();
    },
    updatePointNumber(toothNumber) {
      const oldNumber = this.selectedTooth;
      if (toothNumber != oldNumber) {
        const toothIndex = this.selectedToothIndex;
        const service = { ...this.service };
        service.service_data.points[toothIndex] = {
          ...service.service_data.points[toothIndex],
          classes: toothNumber,
        };

        this.$store.commit(SERVICE_MUTATIONS.SET_SERVICE_DETAIL, {
          ...service,
        });
      }
    },
    removeTooth() {
      const toothIndex = this.selectedToothIndex;
      let service = { ...this.service };

      const newPoints = service.service_data.points.filter(
        (_, index) => index != toothIndex
      );

      service = {
        ...service,
        service_data: {
          ...service.service_data,
          points: newPoints,
        },
      };

      this.$store.commit(SERVICE_MUTATIONS.SET_SERVICE_DETAIL, {
        ...service,
      });
      this.closeTeethNumberingModal();
    },
  },
};
</script>

<style lang="scss">
.selectTeethNumberModal {
  .modal-dialog {
    max-width: 752px !important;
    width: 752px !important;
  }

  &__container {
    .heading {
      display: flex;
      justify-content: space-between;
      margin-bottom: 32px;

      .text {
        font-family: "Rubik";
        font-weight: 500;
        font-size: 24px !important;
        color: #171716 !important;
        margin-bottom: 0;
      }

      .removeToothButton {
        font-family: "Rubik";
        font-weight: 500;
        font-size: 16px !important;
        color: #c3000c !important;
        padding: 0;
      }
    }

    .teethNumberContainerRow {
      display: flex;
      flex-wrap: wrap;

      .teethNumberContainer {
        padding-right: 8px;

        .teethNumber {
          cursor: pointer;
          width: 32px;
          height: 32px;
          background: #f5f5f5;
          opacity: 0.7;
          border: 1px solid #f5f5f5;
          border-radius: 8px;
          display: flex;
          justify-content: center;
          align-items: center;
          margin-bottom: 16px;

          font-family: "Rubik";
          font-weight: 500;
          font-size: 14px;

          &--selected {
            background: #fff;
            color: #171716;
            border: 1px solid #c9c9c9;
          }
        }
      }
    }
  }
}
</style>
