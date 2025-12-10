<template>
	<div>
		<div class="contentBox">
			
				<div class="form-group no-label">
					<b-form-select
						v-model="selected_patient"
						:options="patientsList"
						style="text-transform: capitalize;"
					></b-form-select>
				</div>
				<div class="form-group" v-if="!readOnly && !service">
					<div class="add-patient">
						Or
						<a href="#" v-b-modal="'my-modal'">Add New Patient</a>
					</div>
				</div>
				<div class="form-group" >
					<textarea class="form-control" v-model="patientNote" :readonly="readOnly"></textarea>
					<!-- <label class="control-label">Notes <span class="required">(Required At Least 8 Characters)</span></label> -->
					<label class="control-label">Notes</label>
				</div>
			
		</div>
		<!-- The modal -->
		<b-modal ref="my-modal" id="my-modal" centered>
			<div class="modal-title">Add New Patient</div>
			<p>
				Voxel is created for every dental practitioner.
			</p>
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
							<b-dropdown :text="patientGender" v-model="patientGender" >
								<b-dropdown-item href="#" v-for="(record, index) in gender" :key="index" @click="updatePatientGender(record.value)">
									{{ record.text  }}
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
      						<li v-for="(error,index) in addPatientErrors" :key="index">{{"[ X ] " + error }}</li>
    					</ul>
  					</div>
				</div>
				<div class="inline-buttons">
					<button type="submit" class="btn btn-primary" >Add</button>
					<a href="javascript:void(0)" @click="hideModal" class="link">Cancel</a>
				</div>
			</form>
		</b-modal>
	</div>
</template>

<script>
// [*] Vuex State Getter And Action Helper
import { ServiceHelper } from '@/common/crud-helpers/service';
import { mapGetters } from 'vuex';

// [*] Import form validator
import AppValidator from "@/common/validator"

export default {
	props: {
		updateService: Function,
		service: Object,
		readOnly: {
      		type: Boolean,
      		default: false,
    	},
	},
	data() {
		return {
			selected_patient: null,
			patientNote: null,
			patientsList: [],
			newPatientCraeted: false,

			gender: [
				{ value: 'male', text: 'Male' },
				{ value: 'female', text: 'Female' },
			],
			addPatientErrors: [],
			patientFirstName: "",
			patientLastName: "",
			patientAge: null,
			patientGender: "male",
		};
	},
	computed: {
        ...mapGetters(['patients']),
    },
	mounted(){
		ServiceHelper.getPatients({});
	},
	created() {
		if(this.service) {
			this.patientsList = [
				{
					value: this.service.patient_obj.id,
					text: this.service.patient_obj.first_name + " " + this.service.patient_obj.last_name,
					readonly: true,
				}
			]
			this.selected_patient = this.service.patient_obj.id
			if(this.service.service_data) {
				this.patientNote = this.service.service_data.patientNote
			}
		}
	},
	watch: {
		service() {
			if(this.service) {
				this.patientsList = [
					{
						value: this.service.patient_obj.id,
						text: this.service.patient_obj.first_name + " " + this.service.patient_obj.last_name,
						readonly: true,
					}
				]
				this.selected_patient = this.service.patient_obj.id
				if(this.service.service_data) {
					this.patientNote = this.service.service_data.patientNote
				}
			}
		},
        patients() {
			this.patientsList = [
				{ value: null, text: 'Select or Add new patient', disabled: true}
			];
			this.patients.forEach((item) => {
				this.patientsList.push({
					value: item.id, text: item.first_name + " " + item.last_name
				})
			})

			if(this.newPatientCraeted) {
				this.selected_patient = this.patients[this.patients.length - 1].id
				this.newPatientCraeted = false
			}
			// [Note] When create service defualt value of selected patient is empty.
			// this.selected_patient = this.patientsList[this.patientsList.length - 1].value
        },
		selected_patient() {
			this.updateService({
				patient: this.patients.filter((patient) => patient.id == this.selected_patient)[0],
			})
		},
		patientNote() {
			this.updateService({
				patientNote: this.patientNote,
			})
		}
    },
	methods: {
		hideModal() {
			this.$refs['my-modal'].hide();
		},
		updatePatientGender(value) {
			this.patientGender = value
			this.validateForm()
		},
		addPatient: function(e){
			e.preventDefault();
			if(!this.validateForm())
				return
			ServiceHelper.addPatients({
				"first_name": this.patientFirstName,
				"last_name": this.patientLastName,
				"age": this.patientAge,
				"gender": this.patientGender
			})
			this.hideModal();
			this.newPatientCraeted = true
		},
		validateForm() {
			let error = AppValidator.addNewPatient({
				patientFirstName: this.patientFirstName,
				patientLastName: this.patientLastName,
				patientAge: this.patientAge,
				patientGender: this.patientGender,
			})
			this.addPatientErrors = [...error]
			return this.addPatientErrors.length > 0 ? false : true
		},
	}
};
</script>

<style lang="scss" scoped>
.contentBox {
	border-radius: 12px;
	padding-bottom: 7px;
	@media screen and (max-width: 991px) {
		border: 0;
		padding: 0;
	}
	.add-patient {
		margin-left: 26px;
		color: #8e8e8e;
	}
	.required {
		font-size: rem(11px);
		font-weight: normal;
	}
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
</style>
