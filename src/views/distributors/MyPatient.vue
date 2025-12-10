<template>
	<div class="myPatients">
		<div class="pageHead">
			<h1 class="main-title">Doctors<span>(24)</span></h1>
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
		<div class="filters">
			<div class="form-group no-label">
				<input
					type="text"
					class="form-control"
					placeholder="Search by Doctor ID, Name"
				/>
			</div>
		</div>
		<!-- table -->
		<div class="table">
			<div class="table__head">
				<div class="table__row">
					<div class="table__row--cell" data-width="10">ID</div>
					<div class="table__row--cell">Name</div>
					<div class="table__row--cell" data-width="16">
						Last Order Date
					</div>
					<div class="table__row--cell" data-width="16">
						Number of Orders
					</div>
					<div class="table__row--cell" data-width="16">
						Total Amount
					</div>
					<div class="table__row--cell" data-width="16">
						Total Commission
					</div>
					<div class="table__row--cell" data-width="11">More</div>
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
						data-label="ID"
						data-width="10"
					>
						{{ data.id }}
					</div>
					<div class="table__row--cell" data-label="Name">
						<p>
							{{ data.name }}
						</p>
					</div>
					<div
						class="table__row--cell"
						data-width="16"
						data-label="Last Order Date"
					>
						{{ data.date }}
					</div>
					<div
						class="table__row--cell p-0"
						data-width="16"
						data-label="Number of Orders"
					>
						{{ data.order }}
					</div>
					<div
						class="table__row--cell"
						data-width="16"
						data-label="Total Amount"
					>
						{{ data.amount }}
					</div>
					<div
						class="table__row--cell"
						data-width="16"
						data-label="Total Commission"
					>
						{{ data.commission }}
					</div>
					<div
						class="table__row--cell"
						data-width="11"
						data-label="More"
					>
						<a href="#" class="result">{{ data.more }}</a>
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
					name: 'Mohamed Mohsen',
					date: '19/04/2021',
					order: '0',
					amount: '$0',
					commission: '$0',
					more: 'View Orders',
				},
				{
					index: 1,
					id: '#654321',
					name: 'Mohamed Mohsen',
					date: '19/04/2021',
					order: '10',
					amount: '$4,295.00',
					commission: '$100.00',
					more: 'View Orders',
				},
				{
					index: 2,
					id: '#654321',
					name: 'Mohamed Mohsen',
					date: '19/04/2021',
					order: '2',
					amount: '$1,295.00',
					commission: '$50.00',
					more: 'View Orders',
				},
				{
					index: 3,
					id: '#654321',
					name: 'Mohamed Mohsen',
					date: '19/04/2021',
					order: '0',
					amount: '$0',
					commission: '$0',
					more: 'View Orders',
				},
			],
		};
	},
};
</script>

<style lang="scss" scoped>
.myPatients {
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
	.filters {
		margin-bottom: rem(24px);
		.form-group {
			margin-bottom: 0;
			@media screen and (min-width:575px){
				width: 408px;
			}
			input {
				background: #f5f5f5;
				padding: 12px 24px;
				padding-left: 46px;
				border-radius: 12px;
				border: 0;
				background-image: url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M11 3C6.58172 3 3 6.58172 3 11C3 15.4183 6.58172 19 11 19C15.4183 19 19 15.4183 19 11C19 6.58172 15.4183 3 11 3ZM11 5C14.3137 5 17 7.68629 17 11C17 14.3137 14.3137 17 11 17C7.68629 17 5 14.3137 5 11C5 7.68629 7.68629 5 11 5Z' fill='%238E8E8E'/%3E%3Cg opacity='0.5'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M15.2926 15.2971C15.6529 14.9365 16.2201 14.9085 16.6125 15.2133L16.7068 15.2965L20.7068 19.2928C21.0975 19.6832 21.0978 20.3164 20.7074 20.7071C20.3471 21.0677 19.7799 21.0957 19.3875 20.7908L19.2932 20.7077L15.2932 16.7113C14.9025 16.321 14.9022 15.6878 15.2926 15.2971Z' fill='%238E8E8E'/%3E%3C/g%3E%3C/svg%3E%0A");
				background-repeat: no-repeat;
				background-position: 15px center;
				max-height: 64px;
				@media screen and (max-width:575px){
					max-height: 55px;
				}
				&::placeholder {
					font-weight: 400;
				}
			}
		}
	}
}
</style>
