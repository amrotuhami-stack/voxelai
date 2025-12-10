<template>
	<div class="row justify-content-center">
		<div
			class="col-md-4 col-sm-6"
			v-for="(content, index) in cardContent"
			:key="index"
		>
			<div
				class="card paymentPlan__item"
				:class="content.most_popular == true ? 'popular' : ''"
			>
				<div v-if="content.most_popular" class="popular__label">
					most popular
				</div>
				<div class="card__body">
					<div class="paymentPlan__item--image">
						<svg-icon
							fill="currentColor"
							:icon-viewbox="'0 0 42 54'"
							:icon-id="'documentIcon'"
						></svg-icon>
					</div>
					<div class="paymentPlan__item--title">
						{{ content.title }}
					</div>
					<div class="paymentPlan__item--price">
						<money-format :value="Number(content.price_availability.price.excl_tax)" 
							:locale='`en`' 
							:currency-code='userProfile.default_currency' 
							:subunits-value=false 
							:hide-subunits=false>
						</money-format>
					</div>
					<div class="paymentPlan__item--subtitle">
						{{ content.subscription_size }} Cases a Month
					</div>
					<div class="paymentPlan__item--duration">
						{{ content.subscription_duration_m }} Months Access
					</div>
					<a href="#" class="btn btn-secondary" @click.prevent="setSelectedAiPricePlan(content)"
						:class="selectedAiPricePlan && selectedAiPricePlan.id == content.id ? 'selected' : ''"
						>Go {{ content.title }}</a
					>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { CHECKOUT } from '@/store/modules/checkout/actions';
import { mapGetters } from 'vuex';
import MoneyFormat from 'vue-money-format';

export default {
	props: {
		cardContent: Array,
	},
	components: { MoneyFormat },
	mounted() {
		let items = document.querySelectorAll('.paymentPlan__item');
		items.forEach((item) => {
			item.addEventListener('click', () => {
				items.forEach((i) => i.classList.remove('active'));
				item.classList.add('active');
			});
		});
		
	},
	computed: {
		...mapGetters(['selectedAiPricePlan', 'userProfile']),
    },
	watch: {
		cardContent(){
		},
		selectedAiPricePlan(){

		},
	},
	methods: {
		setSelectedAiPricePlan(price_plab){
			this.$store.commit(CHECKOUT.SET_AI_SELECTED_PRICE_PLAN, price_plab);
		},
	}
};
</script>

<style lang="scss" scoped>
.paymentPlan__item {
	cursor: pointer;
	transition: 0.4s ease all;
	$self: &;
	@media screen and (max-width: 767px) {
		margin-bottom: rem(20px);
	}
	@media screen and (max-width: 575px) {
		max-width:350px;
		margin:auto auto rem(20px) auto;
	}
	&.popular {
		position: relative;
		border: 1px solid #f7c0b7;
		overflow: unset;
		.popular__label {
			display: block;
			color: #ea5a43;
			text-transform: uppercase;
			font-weight: 500;
			font-size: rem(12px);
			letter-spacing: 1px;
			position: absolute;
			padding: rem(10px) rem(12px);
			width: 135px;
			border: 2px solid #f7c0b7;
			border-radius: 6px;
			text-align: center;
			left: 50%;
			transform: translateX(-50%);
			top: -15px;
			background: #fdefed;
		}
	}
	.card__body {
		padding: rem(32px);
		display: flex;
		justify-content: center;
		align-items: center;
		flex-direction: column;
		@media screen and (max-width:1199px) and (min-width:992px){
			padding-left:rem(20px);
			padding-right:rem(20px);
		}
		.selected {
			background-color: #ea5a43;
			color: white;
		}
	}
	&--image {
		margin-top: rem(24px);
		position: relative;
		svg {
			position: static !important;
			fill: #fff;
			color: #e9e9e9;
			width: 38px !important;
			height: 100% !important;
			transition: 0.4s ease all;
		}
	}
	&--title {
		// margin-top: rem(25px);
		text-transform: uppercase;
		font-size: rem(20px);
		color: var(--default);
	}
	&--price {
		color: var(--textPrimary);
		margin-top: rem(16px);
		font-size: rem(24px);
		font-weight: 500;
	}
	&--subtitle {
		position: relative;
		color: #ea5a43;
		font-size: rem(16px);
		margin-top: rem(24px);
		padding-bottom: rem(16px);
		&::before {
			content: '';
			position: absolute;
			height: 1px;
			width: 180px;
			background: #eeeded;
			left: -40px;
			bottom: 0;
		}
	}
	&--duration {
		margin-top: rem(16px);
		margin-bottom: rem(24px);
		font-size: rem(14px);
		color: var(--textSecondary);
	}
	.btn {
		padding: rem(14px) rem(46px);
		@media screen and (max-width:575px){
			width:100%;
		}
	}
	&.active {
		border-color: var(--primary);
		#{ $self }--image {
			svg {
				color: var(--primary);
			}
		}
		.btn {
			background: var(--primary);
			color: #fff;
			&:hover {
				opacity: 0.7;
			}
		}
	}
}
</style>
