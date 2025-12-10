<template>
	<div class="dashBoard"> 
		<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
		<h1 class="main-title">Dashboard</h1>
		<p>See all updates about your orders and services</p>
		<div class="row" v-if="userProfile">
			<div class="col-md-3 col-6">
				<div class="activityCard card">
					<div class="card__body">
						<div class="activityCard__item">
							<div class="activityCard__item--value">{{ userProfile.dashboard.total_orders }}</div>
							<div class="activityCard__item--label">Total Orders</div>
						</div>
						<div class="activityCard__item">
							<div class="activityCard__item--value">{{ userProfile.dashboard.total_services }}</div>
							<div class="activityCard__item--label">Total Services</div>
						</div>
					</div>
				</div>
			</div>
			<div class="col-md-3 col-6">
				<div class="activityCard card" :class="`blue`">
					<div class="card__body">
						<div class="activityCard__item">
							<div class="activityCard__item--value">{{ userProfile.dashboard.pending_orders }}</div>
							<div class="activityCard__item--label">Pending Orders</div>
						</div>
						<div class="activityCard__item">
							<div class="activityCard__item--value">{{ userProfile.dashboard.pending_services }}</div>
							<div class="activityCard__item--label">Pending Services</div>
						</div>
					</div>
				</div>
			</div>
			<div class="col-md-3 col-6">
				<div class="activityCard card" :class="`pink`">
					<div class="card__body">
						<div class="activityCard__item">
							<div class="activityCard__item--value">{{ userProfile.dashboard.inprogress_orders }}</div>
							<div class="activityCard__item--label">In Progress Orders</div>
						</div>
						<div class="activityCard__item">
							<div class="activityCard__item--value">{{ userProfile.dashboard.inprogress_inprogress }}</div>
							<div class="activityCard__item--label">In Progress Services</div>
						</div>
					</div>
				</div>
			</div>
			<div class="col-md-3 col-6">
				<div class="activityCard card" :class="`green`">
					<div class="card__body">
						<div class="activityCard__item">
							<div class="activityCard__item--value">{{ userProfile.dashboard.completed_orders }}</div>
							<div class="activityCard__item--label">Completed Orders</div>
						</div>
						<div class="activityCard__item">
							<div class="activityCard__item--value">{{ userProfile.dashboard.completed_services }}</div>
							<div class="activityCard__item--label">Completed Services</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div class="row" v-if="!userProfile">
			<div class="col-md-3 col-6" v-for="(_, index) in 4" :key="'skelton' + index + 'dashboard'">
				<div class="activityCard card">
					<div class="card__body">
						<div class="activityCard__item">
							<div class="activityCard__item--value">
								<b-skeleton height="52px" width="75px"  animation="fade"></b-skeleton>
							</div>
							<div class="activityCard__item--label">
								<b-skeleton height="32px" animation="fade"></b-skeleton>
							</div>
						</div>
						<div class="activityCard__item">
							<div class="activityCard__item--value">
								<b-skeleton height="52px" width="75px"  animation="fade"></b-skeleton>
							</div>
							<div class="activityCard__item--label">
								<b-skeleton height="32px" animation="fade"></b-skeleton>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div class="dashBoard__wrapper" >
			<div class="pageHead">
				<h2>Last Added Services</h2>
				<router-link class="btn btn-primary"
					:to="{name: 'Start Existing Services', params: { lang: $i18n.locale, page: '1' }}"
				>
				<span class="icon">
					<svg-icon
						icon-id="plus-icon"
						icon-viewbox="0 0 17 18"
					></svg-icon>
				</span>
					New Service
				</router-link>
			</div>
			<latest-services :page="page"/>
			
		</div>
	</div>
</template>

<script>
// [*] Import UI Compenents.
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import BaseActivityCard from '@/common/components/base/BaseActivityCard.vue';
import LatestServices from '@/components/dashboard/LatestServices.vue';


// [*] Import Breadcrumbs ...
import {dashboardBreadCumbs} from "@/common/constant/breadCrumbs"

// [*] Import vue Components
import { mapGetters } from 'vuex';
import Vue from 'vue';

export default {
	props: {
		page: String,
	},
	components: {
		BaseBreadCrumb,
		BaseActivityCard,
		LatestServices,
	},
	computed: {
		...mapGetters(['userProfile']),
    },
	data() {
		return {
			breadCrumbsItems: [...dashboardBreadCumbs],
		};
	},
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
}
</style>
