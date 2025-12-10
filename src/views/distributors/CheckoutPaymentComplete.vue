<template>
	<div class="paymentCompleted">
		<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
		<div class="paymentCompleted__wrapper">
			<svg-icon
				icon-id="correct-icon"
				icon-viewbox="0 0 72 72"
			></svg-icon>
			<div class="paymentCompleted__wrapper--text">
				<h1 class="main-title">Payment Completed</h1>
				<p>
					Thank you! Your payment has been processed, Details of your
					order are included below...
				</p>
			</div>
			<div class="card">
				<div class="card__body grid" data-grid-item-width="1/6">
					<div class="item">
						<p>Mohamed Ahmed</p>
						<span>Doctor Name</span>
					</div>
					<div class="item">
						<p>#123456</p>
						<span>Order Number</span>
					</div>
					<div class="item">
						<p>09/12/2020</p>
						<span>Ordered date</span>
					</div>
					<div class="item">
						<p>$1,295.00</p>
						<span>Order Amount</span>
					</div>
					<div class="item">
						<p>My Wallet</p>
						<span>Payment Type</span>
					</div>
					<div class="item">
						<p>$50.00</p>
						<span>Commission</span>
					</div>
				</div>
			</div>
			<h2>Order purchased services</h2>
			<services :service="service" />
			<div class="paymentCompleted__proceed">
				<button class="btn btn-secondary orange">View Orders</button>
			</div>
		</div>
	</div>
</template>
<script>
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import Services from '@/components/service/Services.vue';
export default {
	components: {
		BaseBreadCrumb,
		Services,
	},

	data() {
		return {
			breadCrumbsItems: [
				{
					text: 'Orders',
					href: '#',
				},
				{
					text: 'checkout',
					active: true,
				},
			],
			service: [
				{
					index: 0,
					image: 'mobile.png',
					title: '3D Implant Planing',
					link: 'Start This Service',
					showBtn: false,
					seeMore: false,
					detail: 'See More Details',
					remaining: false,
					case: 15,
					remainingCase: 'cases remaining',
					duration: 'exp. Jan 2022',
					value: 40,
					max: 100,
				},
				{
					index: 1,
					image: 'mobile.png',
					title: 'Cephalometric Analysis ',
					showBtn: false,
					link: 'Start This Service',
					seeMore: false,
					detail: 'See More Details',
					remaining: false,
					case: 15,
					remainingCase: 'cases remaining',
					duration: 'exp. Jan 2022',
					value: 0,
					max: 100,
				},
				{
					index: 2,
					image: 'mobile.png',
					title: 'Surgical guide for implant (2 or 3 Implant)',
					link: 'See Details',
					showBtn: false,
					seeMore: false,
					detail: 'See More Details',
					remaining: false,
					case: 15,
					remainingCase: 'cases remaining',
					duration: 'exp. Jan 2022',
					value: 40,
					max: 100,
				},
			],
		};
	},
};
</script>

<style lang="scss" scoped>
.paymentCompleted {
	&__wrapper {
		margin-top: rem(48px);
		max-width: 840px;
		margin-left: auto;
		margin-right: auto;
		text-align: center;
		@media screen and (max-width: 991px) {
			margin-top: rem(32px);
			.contentBox {
				border: 0;
				padding: 0;
			}
		}
		svg {
			height: 72px;
			width: 72px;
			display: block;
			margin-left: auto;
			margin-right: auto;
		}
		&--text {
			max-width: 392px;
			margin-left: auto;
			margin-right: auto;
			h1 {
				margin-top: rem(24px);
			}
			p {
				color: var(--default);
			}
		}
		.card__body {
			padding-bottom: rem(28px);
			@media screen and (max-width: 767px) {
				padding: 16px;
			}
			&.grid {
				grid-template-columns: 1fr 95px 95px 100px 100px 90px;
				grid-gap: 35px;
				@media screen and (max-width: 1205px) {
					grid-template-columns: repeat(4, 1fr);
					grid-gap: 40px;
				}
				@media screen and (max-width: 767px) {
					grid-template-columns: unset;
					grid-gap: unset;
				}
			}
			.item {
				text-align: left;
				@media screen and (max-width: 767px) {
					text-align: center;
					display: flex;
					flex-direction: row-reverse;
					width: 100%;
					justify-content: space-between;
					&:not(:last-child) {
						margin-bottom: 12px;
					}
				}
				p {
					margin-bottom: rem(5px);
					color: #171716;
					font-size: rem(16px);
					@media screen and (max-width: 767px) {
						margin-bottom: rem(0px);
					}
				}
				span {
					font-size: rem(14px);
					color: var(--textSecondary);
				}
			}
		}
		h2 {
			margin-top: rem(32px);
			margin-bottom: rem(24px);
			font-size: rem(20px);
		}
	}
	&__proceed {
		margin-top: rem(40px);
		text-align: left;
		.btn {
			padding-right: rem(75px);
			padding-left: rem(75px);
		}
		@media screen and (max-width: 767px) {
			text-align: center;
		}
		@media screen and (max-width: 575px) {
			.btn {
				width: 100%;
			}
		}
	}
}
</style>
