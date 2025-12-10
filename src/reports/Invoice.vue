<template>
	<div id="report-viewer" v-if="order">
		<div class="page" v-for="(page, index) in pages" :key="'report-page' + index">
			<!-- Page Header -->
			<div class="page__header">
				<div class="section__left">
					<img
						src="@/assets/images/Logo.png"
						class="img-fluid d-none-sm"
						alt="Voxel 3DI Logo"
					/>
				</div>
				<div class="section__right">
					<div class="text__headline3">Invoice</div>
					<div>
						<div class="text__headline5 mb-2">Invoice Number:</div>
						<div class="text__body1">{{ order.number }}</div>
					</div>
					<div>
						<div class="text__headline5 mb-2">Date:</div>
						<div class="text__body1">{{ order.date_placed.split('T')[0] }}</div>
					</div>
				</div>
			</div>
			<!-- Page Body !-->
			<div class="page__body">
				<!-- Company Data -->
				<div class="address-content">
					<div class="section">
						<div class="text__headline5 mb-2">Bill To</div>
						<div class="text__body1">
							<p>{{ order.shipping_address.first_name + ' ' + order.shipping_address.last_name }}</p>
							<p>{{ order.email }}</p>
							<p>{{ order.shipping_address.line1 }}</p>
							<p>{{ order.country_obj.text }}</p>
						</div>
					</div>
					<div class="section">
						<div class="text__headline5 mb-2">Bill From</div>
						<div class="text__body1">
							<p>VOXEL3Di LLC</p>
							<p>831 Manor Dr.</p>
							<p>London, 22 Wenlock Road</p>
							<p>United Kingdom</p>
						</div>
					</div>
				</div>
				<!-- Invoice Items -->
				<div>
					<!-- Table Hader !-->
					<div class="table__header">
						<div class="table__cell--item text__headline5">ITEM</div>
						<div class="table__cell--cost text__headline5">COST</div>
						<div class="table__cell--qty  text__headline5">QTY</div>
						<div class="table__cell--price text__headline5">PRICE</div>
					</div>
					<!-- Table Body !-->
					<div class="table__body" v-for="(item, index) in page.items" :key="'invoice-item' + index">
						<!-- Table Row !-->
						<div class="row">
							<div class="table__cell--item text__headline6" v-if="item.product_obj.product_class !== 'online-ai-service'"> 
								{{ item.product_obj.title }}
							</div>
							<div class="table__cell--item text__headline6" v-else> 
								{{ item.product_obj.parent_obj.title }} - {{ item.product_obj.title }}
							</div>
							<div class="table__cell--cost text__headline6">
								<money-format :value="Number(item.price_excl_tax)"
									:locale='`en`'
									:currency-code='item.price_currency'
									:subunits-value='false'
									:hide-subunits='false'>
								</money-format>
							</div>
							<div class="table__cell--qty  text__headline6">{{ item.quantity }}</div>
							<div class="table__cell--price text__headline6">
								<money-format :value="Number(item.quantity) * Number(item.price_excl_tax)"
									:locale='`en`'
									:currency-code='item.price_currency'
									:subunits-value='false'
									:hide-subunits='false'>
								</money-format>
							</div>
						</div>
					</div>
					<div class="table__footer">
						<div class="section"></div>
						<div class="section">
							<div class="divider" />
							<div class="summery">
								<div class="text__headline6">Subtotal</div>
								<div class="text__headline6">
									<money-format :value="Number(order.total_excl_tax)"
										:locale='`en`'
										:currency-code='order.currency'
										:subunits-value='false'
										:hide-subunits='false'>
									</money-format>
								</div>
							</div>
							<div class="summery" v-for="(discount, index) in order.voucher_discounts" :key="'disccount' + index">
								<div class="text__headline6">{{ 'Discount (' + discount.name  + ')'}}</div>
								<div class="text__headline6">
									<money-format :value="Number(discount.amount)"
										:locale='`en`'
										:currency-code='order.currency'
										:subunits-value='false'
										:hide-subunits='false'>
									</money-format>
								</div>
							</div>
							<div class="summery">
								<div class="text__headline6">VAT</div>
								<div class="text__headline6">
									<money-format :value="Number(order.total_incl_tax) - Number(order.total_excl_tax)"
										:locale='`en`'
										:currency-code='order.currency'
										:subunits-value='false'
										:hide-subunits='false'>
									</money-format>
								</div>
							</div>
							<div class="summery">
								<div class="text__headline6">Delivery Charge</div>
								<div class="text__headline6">
									<money-format :value="Number(order.shipping_incl_tax)"
										:locale='`en`'
										:currency-code='order.currency'
										:subunits-value='false'
										:hide-subunits='false'>
									</money-format>
								</div>
							</div>
							<div class="divider" />
							<div class="summery mt-2">
								<div class="text__headline4">Invoice Total</div>
								<div class="text__headline4">
									<money-format :value="Number(order.total_incl_tax)"
										:locale='`en`'
										:currency-code='order.currency'
										:subunits-value='false'
										:hide-subunits='false'>
									</money-format>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div class="payments-details">
					<div class="text__headline5 mb-2">Payments</div>
					<div class="text__body1 mb-3">Credit or Debit Cards</div>
					<div class="text__headline5 mb-2">Notes</div>
					<div class="text__body1">{{ order.shipping_method}}</div>
				</div>
			</div>
			<!-- Page Footer -->
			<div class="page__footer">
				<div class="text__headline5">Thanks for being a VOXEL3Di customer :)</div>
				<div class="contact">
					<div class="text__headline5">Need help?</div>
					<div class="text__body1"><a> help@voxel3di.co.uk </a></div>
				</div>
			</div>
		</div>
		<div class="html2pdf__page-break"></div>
	</div>
</template>


<script>
import MoneyFormat from 'vue-money-format';

export default {
	props: {
		order: Object,
	},
	components: {
		MoneyFormat,
	},
	data() {
		return {
			pages: [],
		}
	},
	created() {
		this.divideReportPages()
	},
	watch: {
		order() {
			this.divideReportPages()
		}
	},
	methods: {
		divideReportPages() {
			let pageNumber = 1;
			let pages = [{number: pageNumber, items: []}];
			for(let i = 0; i < this.order.lines.length; i++) {
				if((i + 1) % 6 == 0) { // 6 Items per page.
					pageNumber++;
					pages.push({ number: pageNumber, items: [] })
				}
				else {
					pages[pageNumber - 1] = {
						number: pageNumber, 
						items: [...pages[pageNumber - 1].items, this.order.lines[i] ],
					}
				}
			}
			this.pages = [...pages]
		}
	}
};
</script>

<style lang="scss" scoped>
	.page {
		width: 210mm;
    	min-height: 296mm;
		padding: 0px;
		margin: 0px;
		box-sizing: border-box;
		-moz-box-sizing: border-box;
		-webkit-box-sizing: border-box;
		-ms-box-sizing: border-box;
		-o-box-sizing: border-box;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		.text {
			&__headline6 {
				font-size: 14px;
				font-weight: 400;
				color: #171716;
			}
			&__headline5 {
				font-size: 14px;
				font-weight: 500;
				color: #171716;
			}
			&__headline4 {
				font-size: 16px;
				font-weight: 500;
				color: #171716;
			}
			&__headline3 {
				font-size: 24px;
				font-weight: 500;
				color: #171716;
			}
			&__body1 {
				font-size: 14px;
				font-weight: 400;
				color: #6B6B6B;
			}
		}
		&__header {
			width: 100%;
			height: 50mm;
			background-color: #F5F5F5;
			display: flex;
			.section {
				&__left {
					width: 50%;
					padding: 32px 56px;
					img {
						width: 150px;
						height: 40px;
					}
				}
				&__right {
					width: 50%;
					display: flex;
					flex-direction: column;
					align-items: left;
					justify-content: center;
					gap: 24px;
				}
			}
		}
		&__body {
			width: 100%;
			height: 226mm;
			.address-content {
				display: flex;
				flex-direction: row;
				padding: 32px 56px;
				.section {
					width: 50%;
					display: flex;
					flex-direction: column;
					align-items: left;
					justify-content: start;
					p {
						margin-bottom: 4px;
					}
				}
			}
			.table {
				&__header {
					background-color: #F5F5F5;
					display: flex;
					flex-direction: row;
					padding: 12px 32px 12px 56px;
				}
				&__body {
					padding: 12px 0px;
					.row {
						margin: 0px;
						padding: 12px 32px 12px 56px;
						display: flex;
						flex-direction: row;
						div {
							padding: 0px;
						}
					}
				}
				&__footer {
					display: flex;
					flex-direction: row;
					.section {
						width: 50%;
						display: flex;
						flex-direction: column;
						padding: 0px 32px;
						.divider {
							background-color: #171716;
							height: 1.5px;
							width: 100%;
						}
						.summery {
							display: flex;
							flex-direction: row;
							justify-content: space-between;
							padding: 12px 0px;
						}
					}
				}
				&__cell {
					&--item {
						width: 50%;
						text-align: left;
					}
					&--cost {
						width: 15%;
						text-align: center;
					}
					&--qty {
						width: 15%;
						text-align: center;
					}
					&--price {
						width: 20%;
						text-align: right;
					}
				}
			}
			.payments-details {
				display: flex;
				flex-direction: column;
				padding: 32px 56px;
			}
		}
		&__footer {
			background-color: #F5F5F5;
			width: 100%;
			height: 20mm;
			display: flex;
			flex-direction: row;
			justify-content: center;
			align-items: center;
			gap: 32px;
			.contact {
				display: flex;
				flex-direction: row;
				gap: 8px;
			}
		}
	}
</style>
