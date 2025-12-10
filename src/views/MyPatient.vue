<template>
	<div>
		<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
		<div class="myPatients">
			<div class="pageHead">
				<h1 class="main-title">My Patients<span >{{"(" + myPatientCount + ")"}}</span></h1>
				<router-link class="btn btn-primary" :to="{name: 'Start Existing Services', params: { lang: $i18n.locale, page: '1' }}">
					<span class="icon">
						<svg-icon
							icon-id="plus-icon"
							icon-viewbox="0 0 17 18"
						></svg-icon>
					</span>
					New Service
				</router-link>
			</div>
			<patient-table :page="page"/>
		</div>
	</div>
</template>

<script>
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import { myPatienBreadCrumbs } from "@/common/constant/breadCrumbs"


import PatientTable from '@/components/Patients/PatientTable.vue';

// [*] Import vue Components
import { mapGetters } from 'vuex';


export default {
	props: {
		page: String,
	},
	components: {
		BaseBreadCrumb,
		PatientTable,
	},

	data() {
		return {
			count: 0,
			breadCrumbsItems: [...myPatienBreadCrumbs],
		};
	},
	computed: {
		...mapGetters(['myPatientCount']),
    },
	
};
</script>

<style lang="scss" scoped>
	.myPatients{
		.pageHead{
			@media screen and (max-width:575px) and (min-width:400px){
				flex-direction: row;
				align-items: center;
			}
		}
	}
</style>
