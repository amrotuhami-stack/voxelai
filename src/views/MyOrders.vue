<template>
	<div class="myOrder">
		<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
		<h1 class="main-title">My Orders <span v-if="filterdOrders">{{"(" + myOrders.length + ")"}}</span></h1>
		<div class="row" v-if="loading">
			<div class="col-md-3 col-6" v-for="(_, index) in 4" :key="'myOrder_card' + index">
				<div class="activityCard__item--value">
					<b-skeleton height="52px" width="75px" animation="fade"></b-skeleton>
				</div>
				<div class="activityCard__item--label">
					<b-skeleton height="32px"  animation="fade"></b-skeleton>
				</div>
			</div>
		</div>
		<div class="row" v-else>
			<div class="col-md-3 col-6">
				<base-activity-card :data="totalOrders" />
			</div>
			<div class="col-md-3 col-6">
				<base-activity-card :data="pendingOrders" color="blue" />
			</div>
			<div class="col-md-3 col-6">
				<base-activity-card :data="progressOrders" color="pink" />
			</div>
			<div class="col-md-3 col-6">
				<base-activity-card :data="completedOrders" color="green" />
			</div>
		</div>
		<filters class="mt-4" :applyFilter="applyFilter"/>
		<div class="d-flex columnWrapper">
			<div class="myOrder__left">
				<div class="table">
					<div class="table__head">
						<div class="table__row">
							<div class="table__row--cell" data-width="17">
								ID
							</div>
							<div class="table__row--cell" data-width="17">
								Order Date
							</div>
							<div class="table__row--cell" data-width="15">
								Amount
							</div>
							<div class="table__row--cell" data-width="20">
								Payment Status
							</div>
							<div class="table__row--cell">Payment Method</div>
							<div class="table__row--cell" data-width="9">
								More
							</div>
						</div>
					</div>
					<div class="table__body" style="border: 0px">
						<div v-if="loading">
							<div class="table__row" v-for="(_, index) in 5" :key="'order_row' + index">
								<div class="table__row--cell" data-label="ID" data-width="17">
									<b-skeleton height="32px" width="100%"  animation="fade"></b-skeleton>
								</div>
								<div class="table__row--cell" data-label="Order Date" data-width="17">
									<b-skeleton height="32px" width="100%" animation="fade"></b-skeleton>
								</div>
								<div class="table__row--cell" data-label="Amount" data-width="15">
									<b-skeleton height="32px" width="100%" animation="fade"></b-skeleton>
								</div>
								<div class="table__row--cell p-0" data-label="Payment Status" data-width="20">
									<b-skeleton height="32px" width="100%" animation="fade"></b-skeleton>
								</div>
								<div class="table__row--cell" data-label="Payment Method">
									<b-skeleton height="32px" width="100%" animation="fade"></b-skeleton>
								</div>
								<div class="table__row--cell" data-width="9" data-label="More">
									<b-skeleton height="32px" width="100%" animation="fade"></b-skeleton>
								</div>
							</div>
						</div>
						<div v-if="!loading && filterdOrders.length == 0">
							<div class="table__row">
								<div class="table__row--cell" style="display: flex; justify-content: center;">
									{{ 'No orders to show yet.'}}
								</div>
							</div>
						</div>
						<div v-if="filterdOrders.length > 0 ">
							<div
								class="table__row"
								:class="selectedOrder && selectedOrder.number == data.number ? 'selected' : ''"
								v-for="(data, index) in filterdOrders"
								:key="data.index"
								@click.prevent="selectOrder(index)"
								@mouseenter="selectOrder(index)"
							>
								<div
									class="table__row--cell"
									data-label="ID"
									data-width="17"
								>
									{{ '#' + data.number }}
								</div>
								<div
									class="table__row--cell"
									data-label="Order Date"
									data-width="17"
								>
									{{ data.date_placed.split('T')[0] }}
								</div>
								<div
									class="table__row--cell"
									data-label="Amount"
									data-width="15"
								>
									{{ data.total_excl_tax_currency }}
								</div>
								<div
									class="table__row--cell p-0"
									data-label="Payment Status"
									data-width="20"
								>
									<span
										:class="
											data.status == 'New'
												? 'pending'
												: data.status == 'Done'
												? 'completed'
												: data.status == 'In Progress'
												? 'failed'
												: data.cancel == true
												? 'cancelled'
												: data.refund == true
												? 'refunded'
												: ''
										"
									></span>
										{{ data.status == 'New'
											? 'Pending'
											: data.status == 'Done'
											? 'Completed'
											: data.status == 'In Progress'
											? 'In Progress' : '' 
										}}
								</div>
								<div
									class="table__row--cell"
									data-label="Payment Method"
								>
									{{ 'Credit or Debit Cards' }}
								</div>
								<div
									class="table__row--cell"
									data-width="9"
									data-label="More"
								>
									<b-dropdown class="action-dropdown" >
										<b-dropdown-item-button
											@click.prevent="() => handleMoreActions(item)"
											v-for="(item, index) in actions"
											:key="item + index"
											>{{ item }}</b-dropdown-item-button
										>
									</b-dropdown>
								</div>
							</div>
						</div>
					</div>
				</div>
				<base-pagination path="/my-order/page=" :itemPerPage="10" :count='myOrdersCount'/>
			</div>
			<div class="myOrder__right">
				<div class="card" v-if="selectedOrder">
					<div class="card__head">
						Order<span> {{'#'+ selectedOrder.number}}</span>Details
					</div>
					<div class="card__body">
						<div class="card__body--item">
							<cart-items :lines="lines" />
						</div>
						<div class="card__body--summary">
							<h4>Summary</h4>
							<div class="item">
								<p>Item(s) Subtotal:</p>
								<p>{{ selectedOrder.total_excl_tax_currency[0] + selectedOrder.total_excl_tax }}</p>
							</div>
							<div class="item">
								<p>Shipping Fees:</p>
								<p>{{ selectedOrder.total_excl_tax_currency[0] + selectedOrder.shipping_excl_tax}}</p>
							</div>
							<!-- <div class="item">
								<p>Coupon discounts:</p>
								<p>-$1,981.00</p>
							</div> !-->
							<div class="item total">
								<p>Grand Total:</p>
								<p>{{selectedOrder.total_excl_tax_currency}}</p>
							</div>
							<!-- <a href="#">Change Payment Method</a> !-->
						</div>
					</div>
				</div>
			</div>
		</div>
		<div v-if="invoiceData"  style="position: absolute; top: -10000px;">
			<invoice-report :order="invoiceData" />
		</div>
	</div>
</template>
<script>
// [*] Import UI Components.
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import BaseActivityCard from '@/common/components/base/BaseActivityCard.vue';
import Filters from '@/components/myOrders/Filters.vue';
import BasePagination from '@/common/components/base/BasePagination.vue';
import CartItems from '@/components/checkOut/partials/CartItems.vue';
import InvoiceReport from '@/reports/Invoice.vue';

// [*] Import Page BreadCrumbs.
import { myOrdersBreadCrumbs } from "@/common/constant/breadCrumbs"

// [*] Import vue Components
import { mapGetters } from 'vuex';
import { UsersHelper } from '@/common/crud-helpers/users';
import { CheckoutHelper } from '@/common/crud-helpers/checkout';

import html2pdf from "html2pdf.js";

export default {
	props: {
		page: String,
	},
	components: {
		BaseBreadCrumb,
		BaseActivityCard,
		Filters,
		BasePagination,
		CartItems,
		InvoiceReport
	},

	data() {
		return {
			breadCrumbsItems: [...myOrdersBreadCrumbs],
			actions: ['Download invoice', 'Report a problem'],
			listOfcountries: [],
			selectedOrder: null,
			lines: [],

			allOrders: [],
			filterdOrders: [],
			filter: [],
			loading: true,

			invoiceData: null,

		};
	},
	mounted() {
		UsersHelper.getMyOrders({page: this.page})
		CheckoutHelper.getCountries({});
	},
	computed: {
		...mapGetters(['myOrders', 'myOrdersCount', 'countries']),
		totalOrders() {
			return [{label: 'Total Orders', value: this.myOrders.length}]
		},
		pendingOrders() {
			return [{label: 'Pending Orders', value: this.myOrders.filter((order) => order.status == 'New').length}]
		},
		progressOrders() {
			return [{label: 'In Progress Orders', value: this.myOrders.filter((order) => order.status == 'In Progress').length}]
		},
		completedOrders() {
			return [{label: 'Completed Orders', value: this.myOrders.filter((order) => order.status == 'Done').length}]
		},
    },
	watch: {
		countries(){
			this.listOfcountries = this.countries.map(country => ({
				url: country.url,
				value: country.iso_3166_1_a2,
				text: country.printable_name,
			}));
		},
		page() {
			UsersHelper.getMyOrders({page: this.page})
		},
		myOrders() {
			this.allOrders = [...this.myOrders]
			this.filterdOrders = [...this.myOrders]
			this.loading = false
		},
		filterdOrders() {
			this.selectedOrder = this.filterdOrders[0]
			this.loading = false
		},
		selectedOrder() {
			if(!this.selectOrder.lines) return;
			UsersHelper.getOrderLines({url: this.selectedOrder.lines}).then((data) => {
				this.lines = data.results
				let country = this.listOfcountries.find((c) => c.url == this.selectedOrder.shipping_address.country)
				this.invoiceData = {...this.selectedOrder, lines: [...this.lines], country_obj: country}
			})
			
		},
		filter() {
			let filterList =  []
			if(this.filter.length > 0) {
				this.allOrders.forEach((order, index) => {
					let orderPassFilter = true
					this.filter.forEach((filter) => {
						if(filter.name == "search" && filter.value != '') {
							if(	!order.number.toString().trim().includes(filter.value)) {
								orderPassFilter = false
							}
						}
						if(filter.name == "date" && filter.value != '') {
							if(	order.date_placed.split('T')[0].toString().trim() != filter.value) {
								orderPassFilter = false
							}
						}
						if(filter.name == "payment-status" && filter.value != 'all') {
							if(	order.status != filter.value) {
								orderPassFilter = false
							}
						}
					})
					if(orderPassFilter == true) {
						filterList.push(order)
					}
				})
				this.filterdOrders = [...filterList]
			}
			else {
				this.filterdOrders = [...this.allOrders]
			}
		}
	},
	
	methods: {
		selectOrder(index) {
			this.selectedOrder = this.filterdOrders[index]
		},
		applyFilter(filter) {
			let index = this.filter.findIndex((item) => item.name == filter.name)
			if(index > -1) {
				let newFilterList = this.filter
				newFilterList[index] = filter
				this.filter = [...newFilterList]
			} else {
				this.filter.push(filter)
			}
		},
		handleMoreActions(value) {
			if(value == 'Download invoice') {
				this.exportToPDF()
			}
		},
		exportToPDF() {
			var element = document.getElementById('report-viewer');
			var options = {
			  margin: 0,
			  filename: `Voxel3DI-Invoice-Order-${this.invoiceData.number}.pdf`,
			  image: { type: 'jpeg', quality: 0.98 },
			  html2canvas: { scale: 2 },
			  jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
			};
			html2pdf().from(element).set(options).save()
    	},
	}
};
</script>

<style lang="scss" scoped>
.myOrder {
	h1 {
		margin: rem(32px) 0;
	}
	&__left {
		flex: 1;
		.table__body {
			.table__row {
				padding: 1.7rem 0;
				// @media screen and (max-width:991px){
				// 	border:0 !important;
				// }
			}
			.selected {
				background-color: #eef7fb;
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
						p {
							font-size: rem(14px);
							margin-bottom: 0;
							color: var(--textSecondary);
							margin-bottom: rem(12px);
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
	}
	::v-deep .card__body {
		.activityCard__item {
			padding-bottom: 0;
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
	@media screen and (max-width:991px){
		&__right{
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
