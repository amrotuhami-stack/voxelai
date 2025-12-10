<template>
	<div class="dashBoard">
		<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
		<h1 class="main-title">Internal Doctor Dashboard</h1>
		<p>See all updates about your assigned services</p>
		<div class="row" v-if="userProfile">
			<div class="col-md-3 col-6">
				<div class="activityCard card" :class="`grey`">
					<div class="card__body">
						<div class="activityCard__item">
							<div class="activityCard__item--value">{{ userProfile.dashboard.not_started }}</div>
							<div class="activityCard__item--label">Not Started Services</div>
						</div>
					</div>
				</div>
			</div>
			<div class="col-md-3 col-6">
				<div class="activityCard card" :class="`blue`">
					<div class="card__body">
						<div class="activityCard__item">
							<div class="activityCard__item--value">{{ userProfile.dashboard.in_progress }}</div>
							<div class="activityCard__item--label">In Progress Services</div>
						</div>
					</div>
				</div>
			</div>
			<div class="col-md-3 col-6">
				<div class="activityCard card" :class="`orange`">
					<div class="card__body">
						<div class="activityCard__item">
							<div class="activityCard__item--value">{{ userProfile.dashboard.delayed }}</div>
							<div class="activityCard__item--label">Delayed Services</div>
						</div>
					</div>
				</div>
			</div>
			<div class="col-md-3 col-6">
				<div class="activityCard card" :class="`pink`">
					<div class="card__body">
						<div class="activityCard__item">
							<div class="activityCard__item--value">{{ userProfile.dashboard.rejected }}</div>
							<div class="activityCard__item--label">Rejected Services</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div class="dashBoard__wrapper" >
			<div class="pageHead">
				<h2>Last Added Services</h2>
			</div>
			<last-added-services :page="page"/>
		</div>
	</div>
</template>

<script>
// [*] Import UI Compenents.
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import BaseActivityCard from '@/common/components/base/BaseActivityCard.vue';
import LastAddedServices from '@/components/InternalDoctor/Dashboard/lastAddedServices.vue';

// [*] Import Breadcrumbs ...
import {internalDoctorDashboardBreadCumbs} from "@/common/constant/breadCrumbs"

// [*] Import vue Components
import { mapGetters } from 'vuex';
import { ServiceHelper } from '@/common/crud-helpers/service';

export default {
	props: {
		page: String,
	},
	components: {
		BaseBreadCrumb,
		BaseActivityCard,
		LastAddedServices,
	},
	computed: {
		...mapGetters(['userProfile',]),
    },
	data() {
		return {
			breadCrumbsItems: [...internalDoctorDashboardBreadCumbs],
		};
	},
	mounted() {
		ServiceHelper.getServices({'page': this.page})
	},
	watch: {
		page() {
			ServiceHelper.getServices({'page': this.page})
		}
	}

};
</script>

<style lang="scss" scoped>
.dashBoard {
	.main-title {
		margin-bottom: rem(10px);
	}
	h2 {
		font-size: rem(28px);
	}
	&__wrapper {
		margin-top: rem(40px);
		.pageHead{
			@media screen and (max-width:575px) and (min-width:401px){
				flex-direction: row;
				align-items: center;
			}
			margin-bottom: rem(12px);
		}
	}
}

.activityCard {
	@media screen and (max-width: 767px) {
		margin-bottom: 15px !important;
		text-align: center;
		.card__body {
			padding-left: rem(15px);
			padding-right: rem(15px);
		}
	}
	&__item {
		&:first-child {
			padding-bottom: rem(20px);
		}
		&:not(:last-child) {
			border-bottom: 1px solid var(--borderColor);
			margin-bottom: rem(18px);
		}
		&--value {
			font-size: rem(48px);
			font-weight: 500;
			color: var(--textPrimary);
			margin: rem(8px) 0 rem(14px) 0;
			@media screen and (max-width:767px){
				font-size:rem(35px);
			}
		}
		&--label {
			font-size: rem(16px);
			font-weight: 400;
			color: var(--default);
		}
	}
	&.grey {
		background: #F5F5F5;
		--borderColor: #C9C9C9;
	}
	&.blue {
		background: #eef7fb;
		--borderColor: #a8d5ee;
	}
	&.pink {
		background: #fdefed;
		--borderColor: #f7c0b7;
	}
	&.green {
		background: #edfdf3;
		--borderColor: #a8eec4;
	}
	&.orange {
		background: rgba(236, 171, 8, 0.12);;
		--borderColor: rgba(236, 171, 8, 0.5);
	}
}
</style>
