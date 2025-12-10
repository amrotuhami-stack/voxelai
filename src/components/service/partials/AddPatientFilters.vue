<template>
	<div class="d-flex patientRecord">
		<div class="patientRecord__left">
			<div class="form-group">
				<b-dropdown text="Mohamed Mohsen 25 years, Male">
					<b-dropdown-text
						>Or
						<router-link to="" v-b-modal="'addpatient'"
							>Add New Patient</router-link
						></b-dropdown-text
					>
					<b-dropdown-item href="#" v-for="(index, patient) in patients" :key="index"
						><span>Amr Tuhami</span>35 years,
						Male</b-dropdown-item
					>
					<b-dropdown-item href="#"
						><span>Mostafa Ahmed</span>35 years,
						Male</b-dropdown-item
					>
				</b-dropdown>
				<label class="control-label dropdownTitle static-label"
					>Patient Information</label
				>
			</div>
		</div>
		<div class="patientRecord__right">
			<div class="form-group">
				<b-dropdown text="2021-02-20">
					<b-dropdown-item href="#">2021-02-21<svg-icon icon-id="trash-icon" icon-viewbox="0 0 24 24"></svg-icon></b-dropdown-item>
					<b-dropdown-item href="#">2021-02-22<svg-icon icon-id="trash-icon" icon-viewbox="0 0 24 24"></svg-icon></b-dropdown-item>
					<b-dropdown-item href="#">2021-02-23<svg-icon icon-id="trash-icon" icon-viewbox="0 0 24 24"></svg-icon></b-dropdown-item>
				</b-dropdown>
				<label class="control-label dropdownTitle static-label"
					>Select Record</label
				>
			</div>
		</div>
	</div>
</template>	

<script>
import { ServiceHelper } from '@/common/crud-helpers/service';
import { mapGetters } from 'vuex';
export default {
	data() {
		return {
			
		};
	},
	mounted(){
		ServiceHelper.getPatients({});
	},
	watch: {
		patients(){
		},
	},
	computed: {
		...mapGetters(['patients']),
	},
	
};
</script>

<style lang="scss" scoped>
	.patientRecord{
		&__left {
			flex: 1;
		}
		&__right {
			flex: 0 0 300px;
			margin-left: rem(24px);
		}
		@media screen and (max-width:991px){
			&__right{
				flex: 0 0 270px;
			}
		}
		@media screen and (max-width:767px){
			flex-direction: column;
			&__right{
				flex: none;
				width:100%;
				margin:0;
			}
		}
	}
	
</style>
