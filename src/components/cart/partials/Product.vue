<template>
	<div class="cartItem__product">
		<div class="cartItem__product--image">
			<img
				v-if="product.images.length > 0"
				:src="product.images[0].original"
				alt=""
				class="img-fluid"
			/>
		</div>
		<div>
			<p class="cartItem__product--title" v-if="product.parent_obj && product.product_class === 'online-ai-service'">
				{{ product.parent_obj.title }} - {{ product.title }}
			</p>
			<p class="cartItem__product--title" v-if="product && product.product_class !== 'online-ai-service'">
				{{ product.title }}
			</p>

			<!-- Display selected option definitions -->
			<div class="cartItem__product--selectedOptions" v-if="selectedOptionDefinitions.length > 0">
				<p class="selectedOptions__label">Selected Options:</p>
				<div class="selectedOptions__list">
					<span v-for="attr in selectedOptionDefinitions" :key="attr.id" class="selectedOption__item">
						{{ attr.option_obj.name }}<span v-if="attr.quantity && attr.quantity > 1" class="selectedOption__quantity"> (x{{ attr.quantity }})</span>
					</span>
				</div>
			</div>

			<div class="cartItem__price hideDesktop" v-if="showAmount">
				<money-format :value="Number(cartLine.price_excl_tax)"
					:locale='`en`'
					:currency-code='userProfile.default_currency'
					:subunits-value='false'
					:hide-subunits='false'>
				</money-format>
				<span class="cartItem__price--actualPrice" v-if="product.is_discounted">
					<money-format :value="Number(cartLine.price_excl_tax_excl_discounts)" 
						:locale='`en`' 
						:currency-code='userProfile.default_currency' 
						:subunits-value='false' 
						:hide-subunits='false'>
					</money-format>
				</span>
			</div>
			<p class="cartItem__product--price" v-if="showAmount">
				<money-format :value="Number(cartLine.price_excl_tax)" 
					:locale='`en`' 
					:currency-code='userProfile.default_currency' 
					:subunits-value='false'
					:hide-subunits='false'>
				</money-format>
				<span v-if="product.is_discounted">
					<money-format :value="Number(cartLine.price_excl_tax_excl_discounts)" 
						:locale='`en`' 
						:currency-code='userProfile.default_currency' 
						:subunits-value='false' 
						:hide-subunits='false'>
					</money-format>
				</span>
			</p>
			<router-link class="cartItem__product--seemore" v-if="!showAmount" 
				:to="{name: 'product-details', params: { lang: $i18n.locale, productId: String(product.product_class === 'online-ai-service' ? product.parent_obj.id :  product.id)},}"
			>
				See More Details
				<font-awesome-icon :icon="['fa', 'angle-right']"/>
			</router-link>
			<div class="cartItem__product--checkbox showDesktop" v-if="showOptions && product.product_options.length > 0" >
				<label v-for="(attribute, index) in sortAttributes" :key="index">
					<input type="checkbox" :name="attribute.option_obj.code" @click.prevent="updateOption(attribute, $event)" :checked="attribute.value=='1' ? true : false" />
					<p>{{ attribute.option_obj.name }}</p>
				</label>
			</div>
		</div>
		<div class="cartItem__product--checkbox hideDesktop" v-if="showOptions && product.product_options.length > 0">
			<label v-for="(attribute, index) in sortAttributes" :key="index" class="option">
				<input type="checkbox" :name="attribute.option_obj.code" @click.prevent="updateOption(attribute, $event)" :checked="attribute.value=='1' ? true : false" />
				<p>{{ attribute.option_obj.name }}</p>
			</label>
		</div>
	</div>
</template>

<script>
// [*] Import UI Components .
import MoneyFormat from 'vue-money-format';

// [*] Vuex State Getter And Action Helper
import { mapGetters } from 'vuex';
import { BasketHelper } from '@/common/crud-helpers/basket';
import { CATALOGUE } from '@/store/modules/catalogue/actions';

export default {
	props: {
		product: Object,
		total: String,
		cartLine: Object,
		basketId: Number,
		showAmount: Boolean,
		showOptions: Boolean,
	},
	
	components: {
		MoneyFormat,
	},
	data() {
		return {
			sortAttributes: []
		}
	},
	created() {
		this.sortAttributes = [...this.cartLine.attributes].sort((a,b) => a.id - b.id)
	},
	computed: {
		...mapGetters(['userProfile']),
		selectedOptionDefinitions() {
			// Get option codes from product_options to exclude them
			const productOptionCodes = this.product.product_options.map(opt => opt.code);

			// Filter attributes to get only selected option_definitions (value == 1 or true)
			// Exclude product_options which are shown as checkboxes separately
			return this.sortAttributes.filter(attr => {
				const isSelected = attr.value == 1 || attr.value === true || attr.value === '1';
				const isNotProductOption = !productOptionCodes.includes(attr.option_obj?.code);
				return isSelected && isNotProductOption;
			});
		}
    },
	watch: {
		cartLine() {
			this.sortAttributes = [...this.cartLine.attributes].sort((a,b) => a.id - b.id)
		}
	},
	methods: {
		updateOption(attribute, event){
			let params = {
				"basket_id": this.cartLine.basket_id,
				"lineId": this.cartLine.id,
				"attrId": attribute.id,
				"option": attribute.option,
				"value": event.target.checked ? 1 : 0
			}
			BasketHelper.updateCartLineAttr(params)
		},
	}

};
</script>

<style lang="scss">
.hideDesktop {
	display: none;
}
.cartItem {
	&__product {
		position: relative;
		display: flex;
		align-items: flex-start;
		@media screen and (max-width: 991px) {
			width: 100%;
			flex-wrap: wrap;
		}
		> div:not(.cartItem__product--image) {
			flex: 1;
			min-width: 0;
		}
		&--image {
			flex: 0 0 118px;
			max-width: 118px;
			margin-right: rem(5px);
			background: var(--imageBg);
			text-align: center;
			border-radius: 6px;
			@media screen and (max-width: 1200px) {
				flex: 0 0 93px;
				max-width: 93px;
			}

			@media screen and (max-width: 991px) {
				margin-right: rem(20px);
			}
		}
		&--title {
			margin-bottom: 0px;
			margin-left: rem(8px);
			font-weight: 400;
			font-size: rem(20px);
			color: var(--textPrimary);
			@include truncate(2);
			word-break: break-all;
		}
		&--price {
			margin-top: rem(8px);
			margin-bottom: 0;
			margin-left: rem(8px);
			font-size: rem(16px);
			font-weight: 500;
			color: var(--textPrimary) !important;
			display: flex;
			span {
				font-size: rem(14px);
				font-weight: 400;
				color: var(--textSecondary) !important;
				text-decoration-line: line-through;
				margin-left: rem(8px);
			}
		}
		&--seemore {
			padding-top: rem(24px);
			margin-top: rem(12px);
			a {
				font-size: rem(16px);
				svg {
					margin-left: rem(17px);
					transform: translateY(2px);
				}
			}
		}
		&--close {
			position: absolute;
			right: 20px;
			top: 25px;
			svg {
				width: 12px;
				height: 12px;
				opacity: 0.5;
			}
			&:hover {
				svg {
					opacity: 0.9;
				}
			}
		}
		&--checkbox {
			width: 100%;
			padding-top: rem(8px);
			margin-left: rem(8px);
			label {
				margin-bottom: rem(8px);
				width: 100%;
				display: flex;
				p {
					margin: 0px rem(6px);
					text-overflow: ellipsis;
					text-transform: capitalize;
					font-size: rem(16px);
					font-weight: 400;
					color: var(--textSecondary) !important;
				}
				.checkBoxInput {
					width: rem(20px);
                	height: rem(20px);
                	background: #fcfcfc;
                	border: 2px solid red;
                	border-radius: 4px;
				}
			}
		}
		&--selectedOptions {
			width: 100%;
			max-width: 100%;
			margin-left: rem(8px);
			margin-right: rem(8px);
			margin-top: rem(16px);
			margin-bottom: rem(12px);
			padding-top: rem(12px);
			border-top: 1px solid #e9ecef;
			box-sizing: border-box;

			@media screen and (max-width: 991px) {
				margin-top: rem(12px);
				padding-top: rem(8px);
			}

			.selectedOptions__label {
				font-size: rem(13px);
				font-weight: 600;
				color: var(--textPrimary);
				margin-bottom: rem(8px);
				text-transform: uppercase;
				letter-spacing: 0.5px;
			}

			.selectedOptions__list {
				display: flex;
				flex-direction: column;
				gap: rem(8px);
				align-items: flex-start;
				max-width: 100%;
			}

			.selectedOption__item {
				font-size: rem(13px);
				font-weight: 500;
				color: #2c5f7a;
				background: linear-gradient(135deg, #e8f4f8 0%, #d4e9f2 100%);
				padding: rem(8px) rem(14px);
				border-radius: 6px;
				display: flex;
				align-items: center;
				border: 1px solid #b8dce8;
				transition: all 0.2s ease;
				box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
				width: fit-content;
				max-width: 100%;
				position: relative;
				padding-left: rem(28px);

				&::before {
					content: "•";
					position: absolute;
					left: rem(12px);
					color: #2c5f7a;
					font-weight: bold;
					font-size: rem(16px);
				}

				&:hover {
					background: linear-gradient(135deg, #d4e9f2 0%, #c0dfe9 100%);
					transform: translateX(4px);
					box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
				}
			}
		}
	}
	&__price {
		font-weight: 500;
		font-size: rem(20px);
		color: var(--textPrimary);
		margin-top: 8px;

		&--actualPrice {
			display: block !important;
			height: unset !important;
			width: unset !important;
			margin: 0;
			color: var(--textSecondary);
			font-size: rem(16px);
			font-weight: 400;
			text-decoration: line-through;
			margin-top: rem(5px);
			margin-left: 12px;
		}
	}
}
</style>
