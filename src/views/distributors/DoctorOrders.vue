<template>
	<div>
		<div class="topHead">
			<div>
				<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
				<h1 class="main-title">Doctor’s Orders</h1>
			</div>
			<activity-card :data="activity.wallet" color="green" />
		</div>
		<div class="doctorOrder">
			<div class="contentBox">
				<div class="row">
					<div class="col-xxl-5 col-xl-4">
						<div class="user">
							<div class="user__icon">
								<img
									src="@/assets/images/icons/Avatar.png"
									alt=""
									class="img-fluid"
								/>
							</div>
							<div class="user__info">
								<h2>Mohamed Mohsen Mohamed</h2>
								<span
									><svg-icon
										icon-id="message-icon"
										icon-viewbox="0 0 20 20"
									></svg-icon
									>mohsenmohamed782@gmail.com</span
								>
								<span
									><svg-icon
										icon-id="phone-icon"
										icon-viewbox="0 0 20 20"
									></svg-icon
									>+20 010 967 36 396</span
								>
							</div>
						</div>
					</div>
					<div class="col-xxl-7 col-xl-8">
						<div class="row">
							<div class="col-md-4">
								<activity-card :data="activity.order" />
							</div>
							<div class="col-md-4">
								<activity-card :data="activity.amount" />
							</div>
							<div class="col-md-4">
								<activity-card :data="activity.Commission" />
							</div>
						</div>
					</div>
				</div>
			</div>
			<filters />
			<div class="d-flex columnWrapper">
				<div class="doctorOrder__left">
					<div class="table">
						<div class="table__head">
							<div class="table__row">
								<div class="table__row--cell" data-width="14">
									ID
								</div>
								<div class="table__row--cell" data-width="16">
									Order Date
								</div>
								<div class="table__row--cell" data-width="14">
									Amount
								</div>
								<div class="table__row--cell" data-width="14">
									Commission
								</div>
								<div class="table__row--cell" data-width="18">
									Payment Status
								</div>
								<div class="table__row--cell">
									Payment Method
								</div>
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
									data-width="14"
								>
									{{ data.id }}
								</div>
								<div
									class="table__row--cell"
									data-label="Order Date"
									data-width="16"
								>
									{{ data.date }}
								</div>
								<div
									class="table__row--cell"
									data-label="Amount"
									data-width="14"
								>
									{{ data.amount }}
								</div>
								<div
									class="table__row--cell"
									data-label="Commission"
									data-width="14"
								>
									{{ data.Commission }}
								</div>
								<div
									class="table__row--cell"
									data-width="18"
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
									class="table__row--cell"
									data-label="Payment Method"
								>
									<a
										v-if="data.isMethod"
										href="#"
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
							</div>
						</div>
					</div>
				</div>
				<div class="doctorOrder__right">
					<div class="card">
						<div class="card__head">
							Order<span> #123456 </span>Details
						</div>
						<div class="card__body">
							<div class="card__body--item">
								<base-inner-scrollbar height="195px">
									<cart-items :cartItem="cartItem" />
								</base-inner-scrollbar>
							</div>
							<div class="card__body--summary">
								<h4>Summary</h4>
								<div class="item">
									<p>Item(s) Subtotal:</p>
									<p>$3,276.00</p>
								</div>
								<div class="item">
									<p>Shipping Fees:</p>
									<p>-$1,981.00</p>
								</div>
								<div class="item">
									<p>Coupon discounts:</p>
									<p>-$1,981.00</p>
								</div>
								<div class="item total">
									<p>Grand Total:</p>
									<p>-$1,981.00</p>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<base-pagination :info="info" />
		</div>
	</div>
</template>

<script>
import BasePagination from '@/common/components/base/BasePagination.vue';
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import ActivityCard from '../../components/distributors/ActivityCard.vue';
import Filters from '../../components/Patients/Filters.vue';
import CartItems from '@/components/checkOut/partials/CartItems.vue';

export default {
	components: {
		BasePagination,
		BaseBreadCrumb,
		ActivityCard,
		Filters,
		CartItems,
	},

	data() {
		return {
			info: '24 doctors',
			breadCrumbsItems: [
				{
					text: 'dashboard',
					href: '#',
				},
				{
					text: 'doctors',
					href: '#',
				},
				{
					text: 'Doctor’s Orders',
					active: true,
				},
			],
			activity: {
				wallet: {
					icon: 'wallet-icon',
					iewBox: '0 0 24 24',
					value: '$275.00',
					label: 'Your Wallet',
					isDropdown: true,
				},
				order: {
					icon: 'documents-icon',
					iewBox: '0 0 24 24',
					value: '15',
					label: 'Number of Orders',
					isDropdown: false,
				},
				amount: {
					icon: 'documents-icon',
					iewBox: '0 0 24 24',
					value: '$4,295.00',
					label: 'Total Amount',
					isDropdown: false,
				},
				Commission: {
					icon: 'discount',
					iewBox: '0 0 24 24',
					value: '$275.00',
					label: 'Commission',
					isDropdown: false,
				},
			},
			tableContent: [
				{
					index: 1,
					id: '#123456',
					date: '19/04/2021',
					amount: '$1,295.00',
					Commission: '$50.00',
					status: 'In Progress',
					method: 'Pay through You',
					pay: 'Pay through You',
					isPay: false,
					isMethod: true,
					pending: true,
				},
				{
					index: 2,
					id: '#123456',
					date: '19/04/2021',
					amount: '$1,295.00',
					Commission: '$50.00',
					status: 'Completed',
					pay: 'Credit or Debit Cards',
					isPay: true,
					isMethod: false,
					method: 'Bank Transfer',
					complete: true,
				},
				{
					index: 3,
					id: '#123456',
					date: '19/04/2021',
					amount: '$1,295.00',
					Commission: '$50.00',
					status: 'Completed',
					pay: 'Pay through You',
					isPay: false,
					isMethod: true,
					method: 'Credit or Debit Cards',
					complete: true,
				},
				{
					index: 4,
					id: '#123456',
					date: '19/04/2021',
					Commission: '$50.00',
					amount: '$1,295.00',
					pay: 'Pay with Paypal',
					isPay: true,
					isMethod: false,
					status: 'Completed',
					method: 'Pay with Paypal',
					complete: true,
				},
				{
					index: 5,
					id: '#123456',
					date: '19/04/2021',
					amount: '$1,295.00',
					Commission: '$50.00',
					pay: 'Credit / Debit Cards',
					isPay: true,
					isMethod: false,
					status: 'In Progress',
					method: 'Credit or Debit Cards',
					fail: true,
				},
				{
					index: 6,
					id: '#123456',
					date: '19/04/2021',
					Commission: '$50.00',
					amount: '$1,295.00',
					pay: 'Bank Transfer',
					isPay: true,
					isMethod: false,
					status: 'In Progress',
					method: 'Credit or Debit Cards',
					cancel: true,
				},
				{
					index: 7,
					id: '#123456',
					date: '19/04/2021',
					amount: '$1,295.00',
					Commission: '$50.00',
					pay: 'Pay with Paypal',
					isPay: true,
					isMethod: false,
					status: 'In Progress',
					method: 'Bank Transfer',
					refund: true,
				},
			],
			cartItem: [
				{
					index: 0,
					image: 'mobile.png',
					title: '3D Implant Planning',
					amount: true,
					price: '$400.00',
					oldprice: '$655.00',
					seeMore: false,
					detail: 'See Details',
					showBtn: 'false',
				},
				{
					index: 1,
					image: 'mobile.png',
					title: 'Surgical guide for single implant',
					amount: true,
					price: '$400.00',
					oldprice: '$655.00',
					seeMore: false,
					detail: 'See Details',
					showBtn: 'false',
				},
				{
					index: 2,
					image: 'mobile.png',
					title: 'Surgical guide for single implant',
					amount: true,
					price: '$400.00',
					oldprice: '$655.00',
					seeMore: false,
					detail: 'See Details',
					showBtn: 'false',
				},
				{
					index: 3,
					image: 'mobile.png',
					title: 'Surgical guide for single implant',
					amount: true,
					price: '$400.00',
					oldprice: '$655.00',
					seeMore: false,
					detail: 'See Details',
					showBtn: 'false',
				},
			],
		};
	},
};
</script>

<style lang="scss" scoped>
.doctorOrder {
	.contentBox {
		margin: rem(22px) 0 rem(32px) 0;
		@media screen and (max-width: 1300px) {
			padding-left: rem(14px);
			padding-right: rem(14px);
		}
		.user {
			display: flex;
			align-items: center;
			&__icon {
				height: rem(80px);
				width: rem(80px);
				margin-right: rem(16px);
				@media screen and (max-width: 1300px) {
					width: rem(60px);
					height: rem(60px);
				}
			}
			&__info {
				display: flex;
				flex-direction: column;
				h2 {
					font-size: rem(20px);
				}
				span {
					font-size: rem(14px);
					color: var(--textSecondary);
					&:not(:last-child) {
						margin-bottom: 5px;
					}
					svg {
						width: 20px;
						height: 20px;
						margin-right: 5px;
					}
				}
			}
			@media screen and (max-width: 1199px) {
				margin-bottom: rem(25px);
			}
		}
		::v-deep .activityCard {
			padding: rem(16px) !important;
			align-items: flex-start;
			background: #fcfcfc;
			border-radius: 16px;
			&__icon {
				margin-right: rem(21px);
				width: auto;
				min-width: auto;
				height: auto;
				background-color: transparent;
				svg {
					margin-top: -3px;
				}
			}
			&__detail {
				span {
					font-size: rem(20px);
					margin: rem(4px) 0 rem(14px) 0;
					@media screen and (max-width: 767px) {
						font-size: rem(18px);
					}
				}
				p {
					font-size: rem(14px);
					font-weight: 400;
					color: var(--default);
					margin: 0;
					margin-top: 5px;
				}
			}
		}
	}
	::v-deep .filters {
		.custom-select {
			background-image: url("data:image/svg+xml,%3Csvg width='10' height='6' viewBox='0 0 10 6' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M8.58579 0C9.47669 0 9.92286 1.07714 9.29289 1.70711L5.70711 5.29289C5.31658 5.68342 4.68342 5.68342 4.29289 5.29289L0.707108 1.70711C0.0771428 1.07714 0.523309 0 1.41421 0H8.58579Z' fill='%238E8E8E'/%3E%3C/svg%3E%0A");
		}
	}
	&__left {
		flex: 1;
		.table {
			margin-bottom: 0;
		}
		@media screen and (min-width: 992px) {
			.table__row--cell:last-child {
				padding-right: 1.5625rem !important;
				text-align: left;
			}
		}
		.table__body {
			.table__row {
				padding: 1.7rem 0;
				@media screen and (max-width: 991px) {
					border: 0 !important;
				}
				.viewMore {
					svg {
						margin-left: 8px;
					}
				}
			}
		}
	}
	&__right {
		flex: 0 0 400px;
		max-width: 400px;
		margin-left: rem(24px);
		.card {
			border: 1px solid #a8d5ee;
			&__head {
				background: #eef7fb;
				border-bottom: 1px solid #a8d5ee;
				span {
					color: var(--textPrimary);
					font-weight: 500;
					margin: 0 rem(8px);
				}
			}
			&__body {
				padding: 0;
				&--item {
					padding: 0 0 0 rem(24px);
				}

				&--summary {
					border-top: 1px solid #a8d5ee;
					padding: rem(24px);
					background: #eef7fb;
					h4 {
						font-size: rem(16px);
						font-weight: 400;
						margin-bottom: rem(16px);
					}
					.item {
						display: flex;
						align-items: center;
						justify-content: space-between;
						&:not(:last-child) {
							margin-bottom: rem(12px);
						}
						p {
							font-size: rem(14px);
							margin-bottom: 0;
							color: var(--textSecondary);
							&:last-child {
								color: var(--default);
							}
						}
						&.total {
							p {
								color: #171716;
								font-size: rem(14px);
								font-weight: 500;
							}
						}
					}
					a {
						color: var(--primary);
						&:hover {
							color: var(--secondary);
						}
					}
				}
			}
		}
		::v-deep {
			.cartItem__product {
				margin-top: rem(16px);
				margin-bottom: rem(16px);
				padding-right: rem(24px);
				&--image {
					flex: 0 0 96px;
					max-width: 96px;
				}
				&--title {
					flex: 1;
					font-size: rem(14px);
					line-height: 1.2;
					@include truncate(1);
				}
			}
		}
		@media screen and (max-width: 1300px) {
			flex: 0 0 300px;
			max-width: 300px;
		}
	}
	::v-deep .card__body {
		.activityCard__item {
			padding-bottom: 0;
		}
	}
	@media screen and (max-width: 1100px) and (min-width: 1025px) {
		.columnWrapper {
			flex-direction: column-reverse;
		}
		&__right {
			flex: 0 0 400px;
			max-width: 400px;
			width: 400px;
			margin: auto auto rem(30px) auto;
		}
	}
	@media screen and (max-width: 1025px) {
		.columnWrapper {
			flex-direction: column-reverse;
		}
		&__right {
			flex: none;
			max-width: 100%;
			margin: 0 0 rem(25px) 0;
		}
	}
	@media screen and (max-width: 991px) {
		&__right {
			.card {
				border: 0;
				padding: 0;
				border-radius: 0;
				&__head {
					background: transparent;
					padding-left: 0;
					padding-right: 0;
				}
				&__body {
					&--summary {
						margin-top: rem(15px);
						background: transparent;
						padding-left: 0;
						padding-right: 0;
					}
					&--item {
						padding-left: 0;
					}
				}
			}
		}
	}
}
</style>
