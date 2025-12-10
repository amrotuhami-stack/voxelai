<template>
	<div>
		<div class="tableDesktop">
			<div class="table__row cartItem">
				<div class="table__row--cell">
					<product :product="cart.product_obj" :showAmount="false" :showOptions="true" :cartLine="cart" :basketId="cart.basket_id" />  
				</div>
				<div class="table__row--cell cartItem__price" data-width="10" v-if="!loading.value">
					<money-format :value="Number(cart.unit_price_excl_tax)"
						:locale='`en`' 
						:currency-code='userProfile.default_currency' 
						:subunits-value='false' 
						:hide-subunits='false'>
					</money-format>
					<span class="cartItem__price--actualPrice" v-if="cart.unit_price_excl_tax != cart.unti_price_excl_tax_excl_discounts">
						<money-format :value="Number(cart.unti_price_excl_tax_excl_discounts)" 
							:locale='`en`' 
							:currency-code='userProfile.default_currency' 
							:subunits-value='false'
						:hide-subunits='false'>
						</money-format>
					</span>
				</div>
				<div class="table__row--cell cartItem__price" data-width="10" v-if="loading.value">
					<font-awesome-icon id="spinner" class="spinner" icon="spinner" size="1x" spin />
				</div>
				<div class="table__row--cell" data-width="20">
					<div class="quantityToggle">
						<button
							:disabled="quantity == 1 ? true : false"
							@click="decrement"
							class="decrement"
						>
							<svg-icon icon-id="minus-icon" icon-viewbox="0 0 15 2"></svg-icon>
						</button>
						<input type="text" v-model="quantity" @change="handleSubmitQuantity"/>
						<button
							:disabled="quantity == 150 ? true : false"
							@click="increment"
							class="increament"
						>
							<svg-icon icon-id="plus-Icon" icon-viewbox="0 0 15 14"></svg-icon>
						</button>
					</div>
				</div>
				<div class="table__row--cell cartItem__price" data-width="10" v-if="!loading.value">
					<money-format :value="Number(cart.price_excl_tax)"
						:locale='`en`'
						:currency-code='userProfile.default_currency'
						:subunits-value='false'
						:hide-subunits='false'>
					</money-format>
					<span class="cartItem__price--actualPrice" v-if="cart.price_excl_tax != cart.price_excl_tax_excl_discounts"> 
						<money-format :value="Number(cart.price_excl_tax_excl_discounts)"
							:locale='`en`'
							:currency-code='userProfile.default_currency'
							:subunits-value='false'
							:hide-subunits='false'>
						</money-format>
					</span>
				</div>
				<div class="table__row--cell cartItem__price" data-width="10" v-if="loading.value">
					<font-awesome-icon id="spinner" class="spinner" icon="spinner" size="1x" spin />
				</div>
				<div class="table__row--cell" data-width="10" @click.prevent="removeFromCart(cart.id)">
					<div class="actions">
						<svg-icon icon-id="cross-icon" icon-viewBox="0 0 12 12"></svg-icon>
					</div>
				</div>
			</div>
		</div>

		<div class="tableResponsive">
			<div class="table__row cartItem">
				<div class="table__row--cell">
					<product :product="cart.product_obj" :total='cart.price_excl_tax' :showAmount="false" :showOptions="true" :cartLine="cart" :basketId="cart.basket_id" />  
					<div class="cartItem__price" v-if="!loading.value">
						<money-format :value="Number(cart.price_excl_tax)"
							:locale='`en`'
							:currency-code='userProfile.default_currency'
							:subunits-value='false'
							:hide-subunits='false'>
						</money-format>
						<span class="cartItem__price--actualPrice" v-if="cart.price_excl_tax != cart.price_excl_tax_excl_discounts"> 
							<money-format :value="Number(cart.price_excl_tax_excl_discounts)"
								:locale='`en`'
								:currency-code='userProfile.default_currency'
								:subunits-value='false'
								:hide-subunits='false'>
							</money-format>
						</span>
					</div>
					<div class="cartItem__price" v-if="loading.value">
						<font-awesome-icon id="spinner" class="spinner" icon="spinner" size="1x" spin />
					</div>
				</div>
				<div class="table__row--cell justify-content-between">
					<div class="quantityToggle">
						<button
							:disabled="quantity == 1 ? true : false"
							@click="decrement"
							class="decrement"
						>
							<svg-icon icon-id="minus-icon" icon-viewbox="0 0 15 2"></svg-icon>
						</button>
						<input type="text" v-model="quantity" @change="handleSubmitQuantity"/>
						<button
							:disabled="quantity == 150 ? true : false"
							@click="increment"
							class="increament"
						>
							<svg-icon icon-id="plus-Icon" icon-viewbox="0 0 15 14"></svg-icon>
						</button>
					</div>
					<a href="#" @click.prevent="removeFromCart(cart.id)" class="remove-cart">Remove from cart</a>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { BasketHelper } from '@/common/crud-helpers/basket';
import Product from './partials/Product.vue';
import { mapGetters } from 'vuex';
import MoneyFormat from 'vue-money-format';

export default {
	components: { Product, MoneyFormat },
	props: {
		cart: Object,
	},
	data(){
		return {
			quantity: 1,
		}
	},
	created() {
		this.quantity = this.cart.quantity;
	},
	computed: {
		...mapGetters(['loading', 'userProfile']),
    },
	methods: {
		decrement: function () {
			this.quantity -= 1;
			this.updateCart();
		},
		increment: function () {
			this.quantity += 1;
			this.updateCart();
		},
		handleSubmitQuantity: function () {
			if(this.quantity > 0) this.updateCart()
		},
		updateCart: function(){
			BasketHelper.updateCartQty({
				basket_id: this.cart.basket_id,
				lineId: this.cart.id,
				quantity: this.quantity
			})
		},
		removeFromCart: function(line_id){
			let params = {basket_id: this.cart.basket_id, id:line_id};
			BasketHelper.removeCart(params);
		},
	},
};
</script>

<style lang="scss" scoped>
.cartItem {
	&.table__row {
		padding: 0px;
		padding-top: rem(15px);
		&:hover {
			background-color: transparent !important;
			.table__row--cell {
				&:first-child {
					text-decoration: none !important;
				}
			}
		}
		&--cell {
			padding-top: rem(10px);
			padding-bottom: rem(10px);
		}
		svg {
			height: 12px;
			width: 12px;
			&:hover {
				opacity: 0.7;
				cursor: pointer;
			}
		}
		&:hover {
			background: unset;
			cursor: unset;
			.table__row--cell {
				text-decoration: unset !important;
			}
		}
		.cartItem__price {
		svg {
			height: 40px;
			width: 40px;
		}
	}
	}
	&__price {
		font-weight: 500;
		font-size: rem(20px);
		color: var(--textPrimary);

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
		}
	}
	.checkbox {
		@media screen and (max-width: 991px) {
			padding-top: 0;
			    margin-bottom: 12px;
		}
	}
	.actions {
		display: flex;
		justify-content: center;
		align-items: center;
	}
}
@media screen and (max-width:1300px){
	.quantityToggle{
		width:140px;
	}
	.cartItem{
		&__product{
			&--title{
				font-size:rem(17px);
			}
			&--image{
				img{
					width: 100px;
				}
			}
		}
		&__price{
			font-size: rem(17px);
		}
	}
}
.quantityToggle {
	display: flex;
	justify-content: space-around;
	align-items: center;
	border-radius: 12px;
	padding: rem(12px);
	margin-right: rem(10px);
	border: 2px solid var(--borderColor);
	input {
		width: 50px;
		text-align: center;
		font-size: rem(16px);
		font-weight: 500;
		border: none;
		outline: none;
		background: transparent;
	}
	button {
		width: 24px;
		height: 24px;
		fill: #000;
		background: transparent;
		border: none;
		transition: all 0.5s ease;
		&.decrement{
			svg{
				height:2px;
			}
		}
		&:hover {
			opacity: 0.7;
		}
	}
}
</style>
