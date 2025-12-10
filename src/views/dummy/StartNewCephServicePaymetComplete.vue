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
				<div class="card__body grid" data-grid-item-width="1/4">
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
						<span>Total Amount</span>
					</div>
					<div class="item">
						<p>Credit or Debit Cards</p>
						<span>Payment Type</span>
					</div>
				</div>
			</div>
			<h2>You can start with one of your purchased services</h2>
			<services :service="service" />
			<div class="paymentCompleted__proceed">
				<button class="btn btn-secondary orange">
					Continue Shopping
				</button>
				<a href="#" class="viewMore"
					>See Order Details
					<font-awesome-icon :icon="['fa', 'angle-right']"
				/></a>
			</div>
		</div>
	</div>
</template>
<script>
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import { startNewCephServicePaymentCompleteBreadCrumbs } from "@/common/constant/breadCrumbs"
import Services from '@/components/service/Services.vue';
export default {
	components: {
		BaseBreadCrumb,
		Services,
	},

	data() {
		return {
			breadCrumbsItems: [...startNewCephServicePaymentCompleteBreadCrumbs],
			service: [
				{
					index: 1,
					image: 'mobile.png',
					title: '3D Implant Planing',
					showBtn: true,
					link: 'Continue',
					seeMore: false,
					detail: 'See More Details',
					remaining: true,
					case: 5,
					remainingCase: 'cases remaining',
					duration: 'exp. Jan 2022',
					value: 0,
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
			padding: rem(24px) rem(74px) rem(28px) rem(74px);
			@media screen and (max-width: 767px) {
				padding: 16px;
			}
			&.grid {
				grid-template-columns: 93px 91px 90px 1fr;
				grid-gap: 86px;
				@media screen and (max-width: 1200px) {
					grid-gap: 50px;
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
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-top: rem(40px);
		@media screen and (max-width: 991px) {
			
		}
		@media screen and (max-width: 575px) {
			flex-direction: column;
			justify-content: center;
		}
		.btn {
			padding-right: rem(75px);
			padding-left: rem(75px);
		}
		a {
			display: flex;
			align-items: center;
			justify-content: space-between;
			@media screen and (max-width: 767px) {
				margin-top: 15px;
			}
			svg {
				margin-left: rem(10px);
				height: 16px;
				width: 16px;
				
			}
			&.viewMore {
				&:hover {
					svg {
						transform: translate(7px, 0px);	
					}
				}
			}	
		}
	}
	@media screen and (max-width:414px){
		::v-deep{
			.serviceRow{
				&__image{
					max-width:80px;
					margin-right:0;
				}
			}
		}
	}
}
</style>
