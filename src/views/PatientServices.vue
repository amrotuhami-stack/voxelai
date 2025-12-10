<template>
	<div class="patientService">
		<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
		<a class="linkBox">
			<div class="id">
				#ID 654321
				<div class="title">
					<p>Mohamed Mohsen Mohamed</p>
					<p>25 years, Male</p>
				</div>
			</div>
			<div>
				<b-dropdown class="action-dropdown">
					<b-dropdown-item href="#"
						>Change Payment Method</b-dropdown-item
					>
					<b-dropdown-item href="#">Report a problem</b-dropdown-item>
				</b-dropdown>
			</div>
		</a>
		<h1 class="main-title">Patient Services</h1>
		<div class="row">
			<div class="col-md-3 col-6">
				<base-activity-card :data="activity.total" />
			</div>
			<div class="col-md-3 col-6">
				<base-activity-card :data="activity.pending" color="blue" />
			</div>
			<div class="col-md-3 col-6">
				<base-activity-card :data="activity.inProgress" color="pink" />
			</div>
			<div class="col-md-3 col-6">
				<base-activity-card :data="activity.completed" color="green" />
			</div>
		</div>
		<filters class="mt-4" />
		<div class="table">
			<div class="table__head">
				<div class="table__row">
					<div class="table__row--cell" data-width="10">
						Service ID
					</div>
					<div class="table__row--cell">Service Name</div>
					<div class="table__row--cell" data-width="11">
						Added date
					</div>
					<div class="table__row--cell" data-width="12">
						Service Status
					</div>
					<div class="table__row--cell" data-width="18">
						Service Phase
					</div>
					<div class="table__row--cell" data-width="13">
						Shipping Status
					</div>
					<div class="table__row--cell" data-width="5">More</div>
				</div>
			</div>
			<div class="table__body">
				<div
					class="table__row"
					v-for="data in tableContent"
					:key="data.index"
				>
					<div
						class="table__row--cell"
						data-width="10"
						data-label="Service ID"
					>
						{{ data.id }}
					</div>
					<div class="table__row--cell" data-label="Service Name">
						<p>{{ data.ServiceName }}</p>
					</div>
					<div
						class="table__row--cell p-0"
						data-width="11"
						data-label="Added date"
					>
						{{ data.date }}
					</div>
					<div
						class="table__row--cell"
						data-width="12"
						data-label="Service Status"
					>
						<span
							:class="
								data.pending == true
									? 'pending'
									: data.complete == true
									? 'completed'
									: data.fail == true
									? 'failed'
									: data.cancel == true
									? 'cancelled'
									: data.refund == true
									? 'refunded'
									: ''
							"
						></span>
						{{ data.status }}
					</div>
					<div
						class="table__row--cell"
						data-width="18"
						data-label="Service Phase"
					>
						<a href="#" class="viewMore" :class="data.servicePhase">
							{{ data.phase }}
							<font-awesome-icon :icon="['fa', 'angle-right']" />
						</a>
					</div>
					<div
						class="table__row--cell"
						data-width="13"
						data-label="Shipping Status"
					>
						<span
							:class="
								data.statusPending == true
									? 'pending'
									: data.statusComplete == true
									? 'completed'
									: data.statusFail == true
									? 'failed'
									: data.statusCancel == true
									? 'cancelled'
									: data.statusRefund == true
									? 'refunded'
									: ''
							"
						></span>
						{{ data.shipingStatus }}
					</div>
					<div
						class="table__row--cell"
						data-width="5"
						data-label="More"
					>
						<b-dropdown class="action-dropdown">
							<b-dropdown-item
								href="#"
								v-for="(item, i) in data.more"
								:key="i + 1"
								>{{ item }}</b-dropdown-item
							>
						</b-dropdown>
					</div>
				</div>
			</div>
		</div>
		<base-pagination :info="info" />
	</div>
</template>
<script>
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import { patienServicesBreadCrumbs } from "@/common/constant/breadCrumbs"

import BaseActivityCard from '@/common/components/base/BaseActivityCard.vue';
import Filters from '@/components/Patients/Filters.vue';
import BasePagination from '@/common/components/base/BasePagination.vue';

export default {
	components: {
		BaseBreadCrumb,
		BaseActivityCard,
		Filters,
		BasePagination,
	},

	data() {
		return {
			info: '4 patients',
			breadCrumbsItems: [...patienServicesBreadCrumbs],
			activity: {
				total: [
					{
						label: 'Total Orders',
						value: 6,
					},
				],
				pending: [
					{
						label: 'Pending Orders',
						value: 2,
					},
				],
				inProgress: [
					{
						label: 'In Progress Orders',
						value: 1,
					},
				],
				completed: [
					{
						label: 'Completed Orders',
						value: 3,
					},
				],
			},
			tableContent: [
				{
					index: 0,
					id: '#654321',
					ServiceName: 'Surgical guide for implant (2 or 3 implants)',
					date: '19/04/2021',
					status: 'In Progress',
					phase: 'Go to Next Phase',
					servicePhase: 'phase',
					shipingStatus: 'In Progress',
					more: ['Delete service', 'Report a problem'],
					pending: true,
					statusPending: true,
				},
				{
					index: 1,
					id: '#654321',
					ServiceName:
						'Surgical guide for implant (2 or 3 implants)Surgical guide for implant (2 or 3 implants)',
					date: '19/04/2021',
					status: 'Completed',
					phase: 'See Results',
					servicePhase: 'result',
					shipingStatus: 'Completed',
					more: ['Delete service', 'Report a problem'],
					complete: true,
					statusComplete: true,
				},
				{
					index: 2,
					id: '#654321',
					ServiceName: 'Surgical guide for implant (2 or 3 implants)',
					date: '19/04/2021',
					status: 'In Progress',
					phase: 'Go to Next Phase',
					servicePhase: 'phase',
					shipingStatus: 'In Progress',
					more: ['Delete service', 'Report a problem'],
					pending: true,
					statusPending: true,
				},
				{
					index: 3,
					id: '#654321',
					ServiceName: 'Surgical guide for implant (2 or 3 implants)',
					date: '19/04/2021',
					status: 'Completed',
					phase: 'See Results',
					servicePhase: 'result',
					shipingStatus: 'Completed',
					more: ['Delete service', 'Report a problem'],
					complete: true,
					statusComplete: true,
				},
				{
					index: 4,
					id: '#654321',
					ServiceName: 'Surgical guide for implant (2 or 3 implants)',
					date: '19/04/2021',
					status: 'Completed',
					phase: 'See Results',
					servicePhase: 'result',
					shipingStatus: 'Completed',
					more: ['Delete service', 'Report a problem'],
					complete: true,
					statusComplete: true,
				},
				{
					index: 5,
					id: '#654321',
					ServiceName: 'Surgical guide for implant (2 or 3 implants)',
					date: '19/04/2021',
					status: 'In Progress',
					phase: 'Go to Next Phase',
					servicePhase: 'phase',
					shipingStatus: 'In Progress',
					more: ['Delete service', 'Report a problem'],
					pending: true,
					statusPending: true,
				},
			],
		};
	},
};
</script>

<style lang="scss" scoped>
.patientService {
	.linkBox {
		border-color: var(--borderColor);
		background: unset;
		padding: rem(24px);
		.id {
			font-weight: 500;
			font-size: rem(16px);
			color: var(--default);
			.title {
				display: flex;
				align-items: center;
				margin-top: rem(8px);
				p {
					font-weight: 500;
					color: var(--textPrimary);
					font-size: rem(20px);
					&:last-child {
						font-size: rem(16px);
						font-weight: 400;
						color: var(--textSecondary);
						padding-left: rem(16px);
					}
				}
			}
		}
		::v-deep .dropdown.action-dropdown .dropdown-toggle::after {
			right: 0;
			left: auto;
			@media screen and (max-width: 767px) {
				right: -10px;
				transform: unset;
				top: -29px;
			}
		}
		@media screen and (max-width:991px){
			::v-deep{
				.dropdown.action-dropdown{
					.dropdown-menu{
						right: 0 !important;
					}
				}
			}
		}
	}
	h1 {
		margin: rem(32px) 0;
	}
	::v-deep .card__body {
		.activityCard__item {
			padding-bottom: 0;
		}
	}
}
</style>
