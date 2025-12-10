<template>
	<div class="orders">
		<div class="pageHead">
			<h1 class="main-title">Orders<span>(24)</span></h1>
			<a href="#" v-b-modal="'invite-doctor'" class="btn btn-primary">
				<span class="icon">
					<svg-icon
						icon-id="doctor-icon"
						icon-viewbox="0 0 25 24"
					></svg-icon>
				</span>
				Invite Doctors
			</a>
		</div>
		<filters />

		<!-- table -->
		<div class="table">
			<div class="table__head">
				<div class="table__row">
					<div class="table__row--cell" data-width="10">Order ID</div>
					<div class="table__row--cell">Doctor Name</div>
					<div class="table__row--cell" data-width="14">
						Ordered date
					</div>
					<div class="table__row--cell" data-width="11">Amount</div>
					<div class="table__row--cell" data-width="12">
						Commission
					</div>
					<div class="table__row--cell" data-width="16">
						Payment Status
					</div>
					<div class="table__row--cell" data-width="16">
						Payment Method
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
						data-label="Order ID"
						data-width="10"
					>
						{{ data.id }}
					</div>
					<div class="table__row--cell" data-label="Doctor Name">
						<p>
							{{ data.doctorName }}
						</p>
					</div>
					<div
						class="table__row--cell"
						data-width="14"
						data-label="Ordered date"
					>
						{{ data.date }}
					</div>
					<div
						class="table__row--cell p-0"
						data-width="11"
						data-label="Amount"
					>
						{{ data.amount }}
					</div>
					<div
						class="table__row--cell"
						data-width="12"
						data-label="Commission"
					>
						{{ data.commission }}
					</div>
					<div
						class="table__row--cell"
						data-width="16"
						data-label="Payment Status"
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
						class="table__row--cell p-0"
						data-width="16"
						data-label="Payment Method"
					>
						<a
								href="#"
								v-if="data.isMethod"
								class="viewMore"
								:class="data.servicePhase"
							>
								{{ data.method }}

								<font-awesome-icon
									:icon="['fa', 'angle-right']"
								/>
							</a>
							<p v-if="data.isPay">{{ data.pay }}</p>
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
								:key="i"
								>{{ item }}</b-dropdown-item
							>
						</b-dropdown>
					</div>
				</div>
			</div>
		</div>
		<!-- table end -->
		<base-pagination :info="info" />

		<!-- invite doctor Modal -->
		<invite-doctor-modal />
	</div>
</template>

<script>
import Filters from '@/components/Patients/Filters.vue';
import BasePagination from '@/common/components/base/BasePagination.vue';
import InviteDoctorModal from '../../components/distributors/InviteDoctorModal.vue';

export default {
	components: {
		Filters,
		BasePagination,
		InviteDoctorModal,
	},

	data() {
		return {
			info: '24 doctors',
			tableContent: [
				{
					index: 0,
					id: '#654321',
					doctorName: 'Mohamed Ahmed',
					date: '19/04/2021',
					amount: '$1,295.00',
					commission: '$50.00',
					status: 'Pending',
					method: 'Pay through You',
					pay: 'Pay through You',
					isPay: false,
					isMethod: true,
					more: [
						'View order details',
						'Pay this order',
						'Report a problem',
					],
					pending: true,
				},
				{
					index: 1,
					id: '#654321',
					doctorName: 'Abdel-Rahman Amr',
					date: '19/04/2021',
					amount: '$1,295.00',
					commission: '$50.00',
					status: 'Completed',
					method: 'Credit Card',
					pay: 'Credit Card',
					isPay: true,
					isMethod: false,
					more: [
						'View order details',
						'Pay this order',
						'Report a problem',
					],
					complete: true,
				},
				{
					index: 2,
					id: '#654321',
					doctorName: 'Mohamed Ahmed',
					date: '19/04/2021',
					amount: '$1,295.00',
					commission: '$50.00',
					status: 'Pending',
					method: 'Pay through You',
					pay: 'Credit Card',
					isPay: false,
					isMethod: true,
					
					more: [
						'View order details',
						'Pay this order',
						'Report a problem',
					],
					pending: true,
				},
				{
					index: 3,
					id: '#654321',
					doctorName: 'Abdel-Rahman Amr',
					date: '19/04/2021',
					amount: '$1,295.00',
					commission: '$50.00',
					status: 'Completed',
					method: 'Credit Card',
					pay: 'Credit Card',
					isPay: true,
					isMethod: false,
					more: [
						'View order details',
						'Pay this order',
						'Report a problem',
					],
					complete: true,
				},
			],
		};
	},
};
</script>

<style lang="scss" scoped>
.orders {
	.result {
		&:hover {
			color: var(--secondary);
		}
	}
	.pageHead {
		p {
			margin-bottom: rem(24px);
		}
		.btn {
			padding-right: rem(25px);
			padding-left: rem(25px);
			.icon svg {
				width: 24px;
				height: 25px;
			}
		}
		@media screen and (max-width: 575px) and (min-width: 400px) {
			flex-direction: row;
			align-items: center;
		}
	}
}
</style>
