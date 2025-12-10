<template>
	<div class="productItem card">
		<div v-if="skelton">
			<div class="card__body">
				<div class="productItem__image">
					<b-skeleton-img  style="border-radius: 12px;"></b-skeleton-img>
				</div>
				<div class="productItem__info">
					<div class="productItem__info">
						<b-skeleton height="32px"  animation="fade"></b-skeleton>
					</div>
					<div class="productItem__info">
						<b-skeleton height="22px" width="35%"  animation="throb"></b-skeleton>
					</div>
					<div v-if="this.product.soldby" class="productItem__info">
						<b-skeleton height="22px" width="50%"  animation="throb"></b-skeleton>
					</div>
					<div class="button-row">
						<b-skeleton type="button" height="42px" width="100%"></b-skeleton>
					</div>
				</div>
			</div>
		</div>
		<div v-else>
			<span class="productItem__bestSeller" v-if="this.product.bestseller">
				best seller
			</span>
			<div class="card__body">
				<div class="productItem__image">
					<router-link :to="{ name: 'product-details', params: {lang: $i18n.locale, productId: String(this.product.id)}, product: this.product, }">
						<!-- <div   v-if="this.product.images.length > 1" >
							<b-carousel  v-model="slide" :interval="2000"  indicators controls :no-hover-pause="false">
								<b-carousel-slide  v-for="(image, index) in this.product.images"  :img-src="image.original" :key="`Carousel'${index}`" class="carousel"></b-carousel-slide>
							</b-carousel>
						</div> -->
					<img v-if="this.product.images.length > 0" :src="this.product.images[0].original"  class="img-fluid" :alt="this.product.title"/>
					</router-link>
				</div>
				<div class="productItem__info">
					<div class="productItem__info--title">
						{{ this.product.title }}
					</div>
					<div class="productItem__info--price"
						v-if="this.product.product_class == 'online-ai-service' && this.product.cheapest_variant_price_availability">
						<money-format :value="Number(this.product.cheapest_variant_price_availability.discounted_price)" 
							:locale='`en`' 
							:currency-code='userProfile.default_currency' 
							:subunits-value='false'
							:hide-subunits='false'>
						</money-format>
						<span class="productItem__info--oldprice" v-if="this.product.cheapest_variant_price_availability && this.product.cheapest_variant_price_availability.is_discounted">
							<money-format :value="Number(this.product.cheapest_variant_price_availability.price.excl_tax)" 
								:locale='`en`' 
								:currency-code='userProfile.default_currency' 
								:subunits-value='false' 
								:hide-subunits='false'>
							</money-format>
						</span>
					</div>
					<div class="productItem__info--price" v-else>
						<money-format :value="Number(this.product.discounted_price)"
							:locale='`en`'
							:currency-code='userProfile.default_currency'
							:subunits-value=false
							:hide-subunits=false>
						</money-format>
						<span class="productItem__info--oldprice" v-if="this.product.is_discounted">
							<money-format :value="Number(this.product.price_availability.price.excl_tax)"
								:locale='`en`'
								:currency-code='userProfile.default_currency'
								:subunits-value='false'
								:hide-subunits='false'>
							</money-format>
						</span>
					</div>
					<!-- <p v-if="this.product.description">{{ this.product.description }}</p> -->
					<!-- <div v-if="this.product.soldby" class="productItem__info--soldby">
						<i>Sold by</i> {{ this.product.soldby }}
					</div> -->
					<router-link  class="productItem__info--seemore"
						:to="{
							name: 'product-details',
							params: {lang: $i18n.locale, productId: String(this.product.id)},
							product: this.product,
						}">
						see more details
					</router-link>
					<div class="inline-button" :class="[!this.added ? '' : 'd-none',]">
						<a href="#" class="btn btn-default" :class="this.product.case_definitions.length > 0 ? 'btn-small' : 'full'" v-if="product.children.length == 0" @click="addToCart(product.url, product.product_options)">
							<span class="icon big only-icon">
								<svg-icon
									icon-id="cart-icon"
									icon-viewbox="0 0 24 24"
								></svg-icon>
							</span>
							<div v-if="this.product.case_definitions.length == 0"> Add to Cart </div>
						</a>
						<a href="#" class="btn btn-default btn-small" v-if="product.children.length > 0" @click="addToCart(product.add_cart_url, product.product_options)">
							<span class="icon big only-icon">
								<svg-icon
									icon-id="cart-icon"
									icon-viewbox="0 0 24 24"
								></svg-icon>
							</span>
						</a>
						<a href="#" class="btn btn-secondary full" @click.prevent="startDigitalService" v-if="this.product.product_class == 'digital-service' && this.product.case_definitions.length > 0">
							Start This Service
						</a>
						<router-link  class="btn btn-secondary full"  v-if="this.product.product_class == 'online-ai-service'"
							:to="{
								name: 'Start New AI Service',
								params: {
									lang: $i18n.locale,
									productId: String(this.product.id),
									product: this.product
								},
							}">
							Start This Service
						</router-link>
					</div>
					<div class="button-row" :class="[ this.added == true ? '' : 'd-none', ]">
						<label class="productItem__addToCart">
							<span class="icon">
								<svg-icon
									icon-id="checked"
									icon-viewbox="0 0 14 10"
								></svg-icon> </span
							>Added to Cart Successfully
						</label>
					</div>
					<!--<div class="button-row"
						:class="[ this.is_adding ? '' : 'd-none', ]"
					>
						<label class="productItem__addToCart">
							<span class="icon">
								<div v-if="is_adding" style="text-align: center; margin: 20px;"> 
									<font-awesome-icon icon="spinner" size="3x" spin />
								</div>
							</span
							>Adding to Cart
						</label>
					</div> !-->
				</div>
			</div>
		</div>
		<b-modal ref="pricing-plan-modal" size="xl" id="pricingPlan" centered v-model="pricingPlanModal" v-if="this.product.product_class == 'online-ai-service'">
			<div class="modal-title">Choose Pricing Plan</div>
			<p>Here are the offers created for you.</p>
			<!-- choose pricing plan -->
			<pricing-plans :cartLineId="cartLineId" :next="hidePricingPlanModal"/>
		</b-modal>
	</div>
</template>
<script>
// [*] Import UI Components .
import MoneyFormat from 'vue-money-format';
import PricingPlans from '@/components/NewAISteps/pricingPlans.vue';

// [*] Vuex State Getter And Action Helper
import { BasketHelper } from '@/common/crud-helpers/basket';
import { mapGetters } from 'vuex';


export default {
	props: {
		product: Object,
		productListIndex: Number,
		skelton: {
      		type: Boolean,
      		default: false,
    	},
	},
	components: {
		MoneyFormat,
		PricingPlans,
	},
	data (){
		return {
			slide: 0,
			pricingPlanModal: false,
			pricingPlanSelected: false,
			cartLineId: "",
		}
	},
	computed: {
		...mapGetters(['userProfile', 'cartLines']),
		added: function() {
			if(this.cartLines.length === 0)
				return false
			if(this.product.product_class !== 'online-ai-service') {
				let index = this.cartLines.findIndex((item) => item.product_obj.id === this.product.id)
				return index === -1 ? false : true
			}
			else {
				let index = this.cartLines.findIndex((item) => item.product_obj.parent_id === this.product.id)
				return index === -1 ? false : true
			}
		},
	},
	watch: {
		cartLines() {
			if(this.product.product_class == 'online-ai-service') {
				let index = this.cartLines.findIndex((item) => item.product_obj.parent_id === this.product.id)
				if(index != -1 && !this.pricingPlanSelected) {
					this.cartLineId = this.cartLines[index].id.toString()
					this.pricingPlanModal = true
					this.pricingPlanSelected = true;
				}
				if(index == -1) {
					this.pricingPlanSelected = false;
				}
			}
		}
	},
	methods: {
		addToCart: function(url, options){
			let params = { "quantity": 1, "url": url }
			if (options.length > 0 ) params["options"] = options.map(item => ({"option": item.url, "value": 0}))
			BasketHelper.addCart(params)
		},
		startDigitalService() {
			this.$router.push({
				name: 'start_digital_service',
				params: {lang: this.$i18n.locale, productId: String(this.product.id),},
			})
		},
		hidePricingPlanModal() {
			this.pricingPlanModal = false;
			
			this.$bvModal.hide(`pricingPlan`);
		}
	},
};
</script>
<style lang="scss" scoped>
.productItem {
	&.card {
		border-radius: 16px;
		border: 2px solid var(--borderColor);
		margin-bottom: rem(24px);
		overflow: unset;
		position: relative;
	}
	&__bestSeller {
		position: absolute;
		top: -2px;
		left: -2px;
		font-size: rem(12px);
		font-weight: 500;
		letter-spacing: 1px;
		color: #ffffff;
		background: #ec9915;
		padding: rem(10px) rem(26px);
		text-transform: uppercase;
		border-top-left-radius: 14px;
		border-bottom-right-radius: 20px;
	}
	&__addToCart {
		color: #00966d;
		background: #edfdf3;
		border: 1px solid #a8eec4;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		padding: rem(19px) 0;
		padding-left: rem(17px);
		padding-right: rem(26px);
		height: 52px;
		font-size: rem(12px);
		font-weight: 500;
		border-radius: 8px;
		width: 100%;
		white-space: nowrap;
		.icon {
			margin-right: rem(13px);
			margin-top: rem(-6px);
		}
		svg {
			width: 14px;
			height: 10px;
		}
	}
	.card__body {
		padding: rem(24px);
		p {
			font-size: rem(14px);
			color: #6b6b6b;
			@include truncate(2);
		}
	}
	&__image {
		//background: #f5f5f5;
		text-align: center;
		border-radius: 16px;
		margin-bottom: rem(22px);
		margin-top: rem(12px);
		img {
			height: rem(225px);
			border-radius: 16px;
		}
		.carousel {
			height: rem(225px);
			border-radius: 16px;
		}
	}
	&__info {
		&--title {
			font-size: rem(20px);
			font-weight: 400;
			color: var(--textPrimary);
			margin-bottom: rem(16px);
			@include truncate(2);
		}
		&--price {
			display: flex;
			align-items: center;
			font-size: rem(24px);
			font-weight: 500;
			color: var(--textPrimary);
			margin-bottom: rem(14px);
		}
		&--oldprice {
			font-size: rem(16px);
			font-weight: 400;
			color: var(--textSecondary);
			text-decoration-line: line-through;
			padding-left: rem(10px);
		}

		&--soldby {
			font-size: rem(14px);
			font-weight: 400;
			font-style: italic;
			color: var(--textSecondary);
			margin-bottom: rem(19px);
			opacity: 1;
			i {
				opacity: 0.8;
			}
		}
		&--seemore {
			color: var(--secondary);
			text-decoration: none;
			text-transform: capitalize;
			font-size: rem(16px);
			font-weight: 500;
			position: relative;
			transition: 0.5s ease all;
			&:after {
				content: '';
				position: absolute;
				background-repeat: no-repeat;
				background-image: url("data:image/svg+xml,%3Csvg width='6' height='10' viewBox='0 0 6 10' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M0.292893 9.70711C-0.0675908 9.34662 -0.0953203 8.77939 0.209705 8.3871L0.292893 8.29289L3.585 5L0.292893 1.70711C-0.0675911 1.34662 -0.0953207 0.779391 0.209704 0.3871L0.292893 0.292893C0.653377 -0.0675907 1.22061 -0.0953208 1.6129 0.209704L1.70711 0.292893L5.70711 4.29289C6.06759 4.65338 6.09532 5.22061 5.7903 5.6129L5.70711 5.70711L1.70711 9.70711C1.31658 10.0976 0.683418 10.0976 0.292893 9.70711Z' fill='%23EA5A43'/%3E%3C/svg%3E ");
				height: 10px;
				width: 10px;
				right: -30px;
				top: 50%;
				transform: translateY(-50%);
				transition: 0.5s ease all;
			}
			&:hover {
				color: var(--secondary);
				&:after {
					right: -35px;
				}
			}
		}
	}
	.button-row {
		margin-top: rem(22px);
	}
	.inline-button {
		display: flex;
		margin-top: rem(22px);
		.btn {
			@media screen and (max-width: 1600px) {
				padding: rem(15px) rem(12px);
			}
			&:not(:last-child) {
				margin-right: rem(14px);
				@media screen and (max-width: 1350px) {
					margin-right: 6px;
				}
			}
		}
	}
	
}
</style>
