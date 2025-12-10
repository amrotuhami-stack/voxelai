<template>
	<div class="productDetail">
		<!-- <base-offer-notifications /> !-->
		<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
		<div class="productDetailWrapper" v-if="productDetail && userProfile">
			<div class="productDetail__left">
				<img v-if="productDetail.images && productDetail.images.length > 1"
					:src="productDetail.images[0].original" width="50%" :alt="productDetail.title" />
				<div v-html="productDetail.description"></div>
			</div>
			<div class="productDetail__right">
				<div class="productDetail__right--selectItems">
					<label class="bestSeller" v-if="productDetail.bestseller">best seller</label>
					<div class="productDetail__right--selectItems--subTitle">
						{{ 'PART NUMBER: ' + productDetail.upc }}
					</div>
					<div class="productDetail__right--selectItems--Title">
						{{ productDetail.title }}
					</div>
					<div class="productDetail__right--selectItems--price"
						v-if="productDetail.product_class == 'online-ai-service' && productDetail.cheapest_variant_price_availability">
						<money-format
							:value="Number(productDetail.cheapest_variant_price_availability.discounted_price)"
							:locale='`en`' :currency-code='userProfile.default_currency' :subunits-value=false
							:hide-subunits=false>
						</money-format>
						<span class="productItem__info--oldprice"
							v-if="productDetail.cheapest_variant_price_availability && productDetail.cheapest_variant_price_availability.is_discounted">
							<money-format
								:value="Number(productDetail.cheapest_variant_price_availability.price.excl_tax)"
								:locale='`en`' :currency-code='userProfile.default_currency' :subunits-value=false
								:hide-subunits=false>
							</money-format>
						</span>
					</div>
					<div class="productDetail__right--selectItems--price" v-else>
						<money-format :value="Number(productDetail.discounted_price)" :locale='`en`'
							:currency-code='userProfile.default_currency' :subunits-value=false :hide-subunits=false>
						</money-format>
						<span class="productItem__info--oldprice" v-if="productDetail.is_discounted">
							<money-format :value="Number(productDetail.price_availability.price.excl_tax)"
								:locale='`en`' :currency-code='userProfile.default_currency' :subunits-value=false
								:hide-subunits=false>
							</money-format>
						</span>
					</div>
					<p class="productDetail__right--selectItems--soldBy">
						{{ 'Sold by ' + productDetail.soldby }}
					</p>

					<!-- Hierarchical Option Selector -->
					<div class="productDetail__right--selectItems--options"
						v-if="productDetail.option_definitions && productDetail.option_definitions.length > 0">
						<div v-for="rootOption in productDetail.option_definitions" :key="rootOption.id"
							class="root-option-section">
							<h4 class="root-option-title">{{ rootOption.title }}</h4>
							<div class="option-selector-container" :data-root-id="rootOption.id">
								<!-- First level options -->
								<div v-if="rootOption.has_children" class="option-level">
									<label class="option-level-label">{{ rootOption.selection_label }}:</label>
									<div class="option-buttons-group">
										<button v-for="child in getChildren(rootOption.id)" :key="child.id"
											type="button" class="option-button"
											:class="{ active: isSelected(rootOption.id, 0, child.id) }"
											@click="handleOptionClick(rootOption.id, 0, child)">
											{{ child.title }}
										</button>
									</div>
								</div>
								<!-- Root option without children -->
								<div v-else class="option-level">
									<div class="option-buttons-group">
										<button type="button" class="option-button"
											:class="{ active: isSelected(rootOption.id, 0, rootOption.id) }"
											@click="handleOptionClick(rootOption.id, 0, rootOption)">
											{{ rootOption.title }}
										</button>
									</div>
								</div>
								<!-- Dynamic child levels -->
								<div v-for="(level, index) in getOptionLevels(rootOption.id)" :key="index"
									class="option-level">
									<label class="option-level-label">{{ level.label }}:</label>
									<div class="option-buttons-group">
										<button v-for="option in level.options" :key="option.id" type="button"
											class="option-button"
											:class="{ active: isSelected(rootOption.id, index + 1, option.id) }"
											@click="handleOptionClick(rootOption.id, index + 1, option)">
											{{ option.title }}
										</button>
									</div>
								</div>
							</div>
							<!-- Price display for this root option -->
							<div v-if="getOptionPrice(rootOption.id)" class="option-price-display">
								<strong>Price:</strong>
								<span class="price-amount">
									<money-format :value="Number(getOptionPrice(rootOption.id))" :locale="'en'"
										:currency-code="userProfile.default_currency" :subunits-value="false"
										:hide-subunits="false">
									</money-format>
								</span>
							</div>
							<!-- Quantity input for this root option (only if enable_quantity is true on leaf option) -->
							<div v-if="isOptionSelected(rootOption.id) && isQuantityEnabled(rootOption.id)" class="option-quantity-input">
								<label :for="'quantity-' + rootOption.id"><strong>Quantity:</strong></label>
								<input type="number" :id="'quantity-' + rootOption.id" class="quantity-input" min="1"
									:value="getOptionQuantity(rootOption.id)"
									@input="handleQuantityChange(rootOption.id, $event)"
									@change="handleQuantityChange(rootOption.id, $event)" />
							</div>
						</div>
					</div>

					<!-- Total Price Display -->
					<div v-if="totalOptionsPrice > 0" class="total-price-display">
						<strong>Total Price (Product + Options):</strong>
						<span class="total-price-amount">
							<money-format :value="Number(baseProductPrice + totalOptionsPrice)" :locale="'en'"
								:currency-code="userProfile.default_currency" :subunits-value="false"
								:hide-subunits="false">
							</money-format>
						</span>
					</div>

					<div class="checkbox">
						<label v-for="(option) in productDetail.product_options" :key="option.name">
							<input type="checkbox" name="radio" />
							<span>
								<b>{{ option.name }}</b> {{ '(Cost = ' + option.price + ' )' }}
							</span>
						</label>
					</div>
					<!-- <div class="productDetail__right--selectItems--quantity">
						<label>Quantity</label>
						<base-touch-spin />
					</div> -->
					<!-- Add To Cart Button (No Children or Case Definitions) -->
					<button title="Add To Cart" class="btn btn-default full"
						v-if="!added && (!productDetail.case_definitions || productDetail.case_definitions.length == 0) && (!productDetail.children || productDetail.children.length == 0)"
						:disabled="!hasSelectedAllOptions" :class="{ 'btn-disabled': !hasSelectedAllOptions }"
						@click="addToMyCart()">
						<span class="icon big only-icon">
							<svg-icon icon-id="cart-icon" icon-viewbox="0 0 24 24"></svg-icon>
						</span>
						Add to Cart
					</button>
					<div class="inline-button" v-else>
						<!-- Add to Cart Icon Button-->
						<button title="Add To Cart" class="btn btn-default btn-small" v-if="!added"
							:disabled="!hasSelectedAllOptions" :class="{ 'btn-disabled': !hasSelectedAllOptions }"
							@click="addToMyCart()">
							<span class="icon big only-icon">
								<svg-icon icon-id="cart-icon" icon-viewbox="0 0 24 24"></svg-icon>
							</span>
						</button>
						<!-- Start Service for Digital Products -->
						<button title="Start Digital Service" class="btn btn-secondary full"
							@click.prevent="handleStartDigitalService"
							v-if="productDetail.product_class == 'digital-service' && productDetail.case_definitions.length > 0">
							Start This Service
						</button>
						<!-- Start Service for AI Products (Cephalo) -->
						<button title="Start Cephalo.Ai Service" class="btn btn-secondary full"
							@click.prevent="handleStartCepahloService"
							v-if="productDetail.product_class == 'online-ai-service'">
							Start This Service
						</button>
					</div>
					<!-- Added to My Cart Label-->
					<div class="mt-3" v-if="added">
						<label class="productDetail__right--addedToCart">
							<span class="icon">
								<svg-icon icon-id="checked" icon-viewbox="0 0 14 10"></svg-icon> </span>Added to Cart
							Successfully
						</label>
					</div>
				</div>
			</div>
		</div>
		<div class="productDetail__relatedProducts">
			<related-product-slider></related-product-slider>
		</div>
	</div>
</template>

<script>
// [*] Import UI Components
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import BaseOfferNotifications from '@/common/components/base/BaseOfferNotifications.vue';
import BaseTouchSpin from '../common/components/base/BaseTouchSpin.vue';
import RelatedProductSlider from '@/components/productDetails/RelatedProductSlider.vue';
import MoneyFormat from 'vue-money-format';

// [*] Import BreadCrumb
import { productDetailBreadCrumbs } from "@/common/constant/breadCrumbs"

import { mapGetters } from 'vuex';
import { CatalogueHelper } from '@/common/crud-helpers/catalogue';
import { BasketHelper } from '@/common/crud-helpers/basket';
import { apiBase } from '@/conf';
import { CART_ACTIONS } from '@/store/modules/cart/actions';
import { USER_ACTIONS } from '@/store/modules/user/actions';

export default {
	props: {
		productId: String,
	},
	components: {
		MoneyFormat,
		BaseBreadCrumb,
		BaseOfferNotifications,
		BaseTouchSpin,
		RelatedProductSlider,
	},
	data() {
		return {
			breadCrumbsItems: [...productDetailBreadCrumbs],
			product: null,
			// Option definitions state
			optionSelections: {}, // Track selections per root option
			optionLevels: {}, // Track dynamic levels per root option
		};
	},
	computed: {
		...mapGetters(['productDetail', 'userProfile', 'cartLines']),
		baseProductPrice() {
			if (!this.productDetail) return 0;
			if (this.productDetail.product_class === 'online-ai-service' && this.productDetail.cheapest_variant_price_availability) {
				return Number(this.productDetail.cheapest_variant_price_availability.discounted_price) || 0;
			}
			return Number(this.productDetail.discounted_price) || 0;
		},
		totalOptionsPrice() {
			let total = 0;
			Object.values(this.optionSelections).forEach(selection => {
				if (selection && selection.price) {
					total += Number(selection.price);
				}
			});
			return total;
		},
		hasSelectedAllOptions() {
			// Use this.product which is set from this.productDetail in watch
			const product = this.product || this.productDetail;

			// Check if product has option definitions
			if (!product || !product.option_definitions || product.option_definitions.length === 0) {
				console.log('No option definitions, allowing add to cart');
				return true; // No options to select
			}

			// Check if all root options have a selection with an optionId (leaf node)
			const rootOptionIds = product.option_definitions.map(opt => opt.id);
			const allSelected = rootOptionIds.every(rootId => {
				const selection = this.optionSelections[rootId];
				const isSelected = selection && selection.optionId !== null;
				console.log(`Root option ${rootId}: selected=${isSelected}`, selection);
				return isSelected;
			});
			console.log('All options selected:', allSelected);
			return allSelected;
		},
		added: function () {
			if (this.cartLines.length === 0)
				return false
			if (this.product.product_class !== 'online-ai-service') {
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
		productDetail() {
			this.product = this.productDetail
			this.breadCrumbsItems = [
				{
					text: 'Shop',
					href: '/shop/page=1',
				},
				{
					text: this.productDetail.categories[0],
					to: {
						name: 'Shop',
						params: { page: "1" },
						query: { filter: 'category', value: this.productDetail.categories[0] }
					}
				},
				{
					text: this.productDetail.title,
					active: true,
				}
			]
		}
	},
	mounted() {
		CatalogueHelper.getProductDetail({ id: this.productId })
	},
	methods: {
		addToMyCart() {
			if (!this.product) return;

			console.log('Product:', this.product);
			console.log('Option Selections:', this.optionSelections);
			console.log('Has Selected All Options:', this.hasSelectedAllOptions);

			// Validate that all required options are selected
			if (!this.hasSelectedAllOptions) {
				console.error('Not all options selected');
				alert('Please select all required options before adding to cart');
				return;
			}

			let url = this.product.children.length == 0 ? this.product.url : this.product.add_cart_url;
			let params = { "quantity": 1, "url": url }

			// Collect all options (product_options and option_definitions) with initial value 0
			let allOptions = [];

			// Add existing product_options
			if (this.product.product_options.length > 0) {
				allOptions = this.product.product_options.map(item => ({
					"option": item.url,
					"value": 0
				}));
			}

			// Add selected options from option_definitions with value 0 (will update later)
			Object.values(this.optionSelections).forEach(selection => {
				if (selection && selection.optionId) {
					const optionId = selection.baseOptionId || selection.regularOptionId;

					if (optionId) {
						const optionUrl = `${apiBase()}shop/options/${optionId}/`;
						allOptions.push({
							"option": optionUrl,
							"value": 0  // Initially 0, will update to 1
						});
					}
				}
			});

			// Add all options to params - this creates the line attributes
			if (allOptions.length > 0) {
				params["options"] = allOptions;
			}

			console.log('Step 1: Add product to cart with options (value 0):', params);

			// Step 1: Add product to cart with options
			const result = BasketHelper.addCart(params);
			console.log('BasketHelper.addCart result:', result);

			if (result && typeof result.then === 'function') {
				result.then(response => {
					console.log('Add to cart response:', response);

					// Step 2: Update line attributes from 0 to 1 for selected option_definitions
					if (response && response.data) {
						const basket = response.data;
						const basketId = basket.id;

						console.log('Basket ID:', basketId);

						// Refresh cart to get updated cartLines with full line objects including attributes
						BasketHelper.getCart({}).then(() => {
							console.log('Cart refreshed, cartLines:', this.cartLines);

							if (!this.cartLines || this.cartLines.length === 0) {
								console.error('No cart lines found after refresh');
								return;
							}

							// Find the line for the product we just added
							const productId = this.product.children.length == 0 ? this.product.id : this.product.add_cart_url.split('/').filter(p => p).pop();
							console.log('Looking for product ID:', productId);

							// Find the matching line
							let matchedLine = null;
							for (let line of this.cartLines) {
								console.log('Checking line:', line);
								if (line.product_obj && line.product_obj.id == productId) {
									matchedLine = line;
									console.log('Found matching line:', matchedLine);
									break;
								}
							}

							// If not found by product_obj, try by product URL
							if (!matchedLine) {
								for (let line of this.cartLines) {
									if (line.product && line.product.includes(productId)) {
										matchedLine = line;
										console.log('Found matching line by URL:', matchedLine);
										break;
									}
								}
							}

							// Default to last line if still not found
							if (!matchedLine) {
								matchedLine = this.cartLines[this.cartLines.length - 1];
								console.log('Using last line as fallback:', matchedLine);
							}

							if (!matchedLine || !matchedLine.id) {
								console.error('Could not find line with ID');
								return;
							}

							const lineId = matchedLine.id;
							const lineAttributes = matchedLine.attributes || [];
							console.log('Step 2: Updating line attributes - Basket ID:', basketId, 'Line ID:', lineId);
							console.log('Line attributes:', lineAttributes);

							// Build a map of option URLs with their quantities
							const selectedOptionData = new Map();
							Object.values(this.optionSelections).forEach(selection => {
								if (selection && selection.optionId) {
									const optionId = selection.baseOptionId || selection.regularOptionId;
									if (optionId) {
										const optionUrl = `${apiBase()}shop/options/${optionId}/`;
										selectedOptionData.set(optionUrl, {
											quantity: selection.quantity || 1
										});
									}
								}
							});

							console.log('Selected option data to update:', Array.from(selectedOptionData.entries()));

							// Update line attributes using updateCartLineAttr
							const updatePromises = [];
							lineAttributes.forEach(attr => {
								console.log('Checking attribute:', attr);
								// Check if this attribute's option is in our selected options
								if (attr.option && selectedOptionData.has(attr.option)) {
									const optionData = selectedOptionData.get(attr.option);
									console.log('Updating attribute ID:', attr.id, 'for option:', attr.option, 'with quantity:', optionData.quantity);

									const promise = this.$store.dispatch(CART_ACTIONS.UPDTAE_CART_LINE_ATTRIBUTE, {
										basket_id: basketId,
										lineId: lineId,
										attrId: attr.id,
										option: attr.option,
										value: 1,
										quantity: optionData.quantity
									});

									updatePromises.push(promise);
								}
							});

							// Wait for all line attributes to be updated
							if (updatePromises.length > 0) {
								Promise.all(updatePromises)
									.then(() => {
										console.log('All line attributes updated successfully');
										// Refresh cart again to show updated prices with options
										BasketHelper.getCart({});
										this.$store.dispatch(USER_ACTIONS.GET_USER, {});
									})
									.catch(error => {
										console.error('Error updating line attributes:', error);
										if (error.response) {
											console.error('Error response:', error.response.data);
										}
									});
							} else {
								console.log('No option_definitions to update as line attributes');
							}
						}).catch(error => {
							console.error('Error refreshing cart:', error);
						});
					} else {
						console.warn('Add to cart completed but response is undefined');
					}
				}).catch(error => {
					console.error('Add to cart error:', error);
					if (error.response) {
						console.error('Error response:', error.response.data);
					}
				});
			} else {
				console.warn('BasketHelper.addCart did not return a promise');
			}
		},
		handleStartDigitalService() {
			this.$router.push({
				name: 'start_digital_service',
				params: { lang: this.$i18n.locale, productId: String(this.productId), },
			})
		},
		handleStartCepahloService() {
			this.$router.push({
				name: 'Start New AI Service',
				params: { lang: this.$i18n.locale, productId: String(this.productId), product: this.productDetail, }
			})
		},
		// Option Definitions Methods
		getChildren(rootId) {
			// Get initial children from root option (already loaded from backend)
			const rootOption = this.productDetail.option_definitions.find(opt => opt.id === rootId);
			if (!rootOption || !rootOption.has_children) return [];
			return rootOption.children || [];
		},
		getOptionLevels(rootId) {
			return this.optionLevels[rootId] || [];
		},
		isSelected(rootId, level, optionId) {
			const selection = this.optionSelections[rootId];
			if (!selection) return false;
			return selection.levelSelections && selection.levelSelections[level] === optionId;
		},
		getOptionPrice(rootId) {
			const selection = this.optionSelections[rootId];
			return selection?.price || null;
		},
		isOptionSelected(rootId) {
			const selection = this.optionSelections[rootId];
			return selection && selection.optionId !== null;
		},
		getOptionQuantity(rootId) {
			const selection = this.optionSelections[rootId];
			return selection?.quantity || 1;
		},
		isQuantityEnabled(rootId) {
			const selection = this.optionSelections[rootId];
			return selection?.enableQuantity === true;
		},
		handleQuantityChange(rootId, event) {
			const quantity = parseInt(event.target.value) || 1;

			// Ensure quantity is at least 1
			if (quantity < 1) {
				event.target.value = 1;
				return;
			}

			const selection = this.optionSelections[rootId];
			if (selection && selection.unitPrice) {
				const unitPrice = parseFloat(selection.unitPrice);
				const totalPrice = unitPrice * quantity;

				// Update selection
				this.$set(this.optionSelections[rootId], 'quantity', quantity);
				this.$set(this.optionSelections[rootId], 'price', totalPrice);
			}
		},
		handleOptionClick(rootId, level, option) {
			// Initialize selection for this root if not exists
			if (!this.optionSelections[rootId]) {
				this.$set(this.optionSelections, rootId, {
					levelSelections: {},
					unitPrice: null,
					price: null,
					quantity: 1,
					optionId: null,
					baseOptionId: null,
					regularOptionId: null,
					enableQuantity: false,
				});
			}

			// Update level selection
			this.$set(this.optionSelections[rootId].levelSelections, level, option.id);

			// Remove all higher levels
			const currentLevels = this.optionLevels[rootId] || [];
			const newLevels = currentLevels.slice(0, level);
			this.$set(this.optionLevels, rootId, newLevels);

			// Remove selections for higher levels
			Object.keys(this.optionSelections[rootId].levelSelections).forEach(lvl => {
				if (Number(lvl) > level) {
					this.$delete(this.optionSelections[rootId].levelSelections, lvl);
				}
			});

			// If option has children, display them (they're already loaded from backend)
			if (option.has_children && option.children && option.children.length > 0) {
				const levels = this.optionLevels[rootId] || [];
				levels.push({
					label: option.selection_label || 'Select',
					options: option.children,
				});
				this.$set(this.optionLevels, rootId, levels);

				// Clear price and option data as we're not at a leaf yet
				this.optionSelections[rootId].unitPrice = null;
				this.optionSelections[rootId].price = null;
				this.optionSelections[rootId].quantity = 1;
				this.optionSelections[rootId].optionId = null;
				this.optionSelections[rootId].baseOptionId = null;
				this.optionSelections[rootId].regularOptionId = null;
				this.optionSelections[rootId].enableQuantity = false;
			} else {
				// This is a leaf node, set the price and option IDs
				const unitPrice = option.base_price || option.price || 0;
				const quantity = this.optionSelections[rootId].quantity || 1;
				this.optionSelections[rootId].unitPrice = unitPrice;
				this.optionSelections[rootId].price = unitPrice * quantity;
				this.optionSelections[rootId].optionId = option.id;
				this.optionSelections[rootId].baseOptionId = option.base_option_id;
				this.optionSelections[rootId].regularOptionId = option.option_id;
				this.optionSelections[rootId].enableQuantity = option.enable_quantity === true;
			}
		},
	}
};
</script>

<style lang="scss">
.productDetail {
	.productDetailWrapper {
		display: flex;

		@media screen and (max-width: 991px) {
			flex-direction: column-reverse;
		}
	}

	&__left {
		display: flex;
		flex-direction: column;
		align-items: start;
		overflow: hidden;
		width: 70%;
		padding-right: 5%;
		transition: all 0.5s ease;

		@media screen and (max-width: 991px) {
			margin-right: rem(0px);
			margin-top: rem(50px);
		}

		h5 {
			margin-top: rem(25px);
			margin-bottom: rem(15px);
			line-height: 1.1;
		}

		p {
			font-size: rem(14px);

			&.bold-text {
				font-weight: 500;
			}

			span {
				color: var(--secondary);
			}
		}

		a {
			text-decoration: underline;
		}

		img {
			margin-bottom: rem(15px);

			@media screen and (max-width:991px) {
				text-align: center;
			}
		}
	}

	&__right {
		width: 30%;

		@media screen and (max-width: 991px) {
			flex: 0 0 100%;
			max-width: 100%;
		}

		&--selectItems {
			font-size: rem(14px);

			&--Title {
				color: var(--textPrimary);
				font-size: rem(24px);
				line-height: 1.4;
				margin-bottom: rem(25px);
			}

			&--subTitle {
				color: #8e8e8e;
				line-height: 1;
				margin: rem(14px) 0 rem(10px) 0;
			}

			&--price {
				color: var(--textPrimary);
				font-size: rem(28px);
				font-weight: 500;
				line-height: 1.1;
				margin-bottom: rem(10px);
				display: flex;
				align-items: center;

				span {
					color: #8e8e8e;
					font-size: rem(14px);
					margin-left: rem(10px);
					text-decoration: line-through;
					font-weight: 400;
				}
			}

			&--soldBy {
				font-style: italic;
				color: #8e8e8e;
				line-height: 1;
				margin-bottom: rem(10px);
			}

			&--quantity {
				margin: rem(18px) 0 rem(32px) 0;

				label {
					color: var(--default);
					font-size: rem(16px);
					margin-bottom: rem(10px);
				}

				.quantityToggle {
					width: 155px;
				}
			}

			.see-more {
				display: block;
				text-align: center;
				margin-top: rem(35px);
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

			@media screen and (max-width:991px) {
				text-align: center;

				&--quantity {
					.quantityToggle {
						margin: auto;
					}

				}

				&--price {
					justify-content: center;
				}
			}

			@media screen and (max-width:991px) and (min-width:500px) {
				.button-row {
					.btn {
						width: 300px;
						margin: auto;
					}
				}
			}
		}

		&--addedToCart {
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

		.checkbox {
			span {
				padding-bottom: 0;
				padding-left: rem(32px);

				&:after,
				&:before {
					top: 2px !important;
				}

				b {
					font-weight: 400;
					color: #22272e;
					font-size: rem(20px);
				}

				i {
					font-style: normal;
					font-size: rem(16px);
					font-weight: 500;
					color: var(--textPrimary);

					&.oldPrice {
						text-decoration: line-through;
						color: var(--textSecondary);
						font-weight: 400;
						margin-left: rem(8px);
					}
				}
			}
		}
	}

	&__relatedProducts {
		position: relative;
		padding-top: rem(20px);
	}
}

// Option Definitions Styles
.productDetail__right--selectItems--options {
	margin: rem(20px) 0;
}

.root-option-section {
	margin-bottom: rem(25px);
	padding: rem(15px);
	background-color: #f8f9fa;
	border-radius: 8px;
	border: 1px solid #dee2e6;

	&:last-child {
		margin-bottom: 0;
	}
}

.root-option-title {
	font-size: rem(16px);
	font-weight: 700;
	color: #212529;
	margin: 0 0 rem(15px) 0;
	padding-bottom: rem(10px);
	border-bottom: 2px solid var(--secondary);
}

.option-selector-container {
	margin-top: rem(10px);
}

.option-level {
	margin-bottom: rem(15px);

	&:last-child {
		margin-bottom: 0;
	}
}

.option-level-label {
	display: block;
	margin-bottom: rem(10px);
	font-weight: 600;
	color: #495057;
	font-size: rem(13px);
}

.option-buttons-group {
	display: flex;
	flex-wrap: wrap;
	gap: rem(10px);
}

.option-button {
	padding: rem(10px) rem(20px);
	background-color: white;
	border: 2px solid #dee2e6;
	border-radius: 6px;
	font-size: rem(14px);
	font-weight: 500;
	color: #495057;
	cursor: pointer;
	transition: all 0.2s ease;
	min-width: 100px;
	text-align: center;

	&:hover {
		border-color: var(--secondary);
		background-color: #fef5f3;
		color: var(--secondary);
		transform: translateY(-1px);
		box-shadow: 0 2px 4px rgba(234, 90, 67, 0.1);
	}

	&:active {
		transform: translateY(0);
	}

	&.active {
		background-color: var(--secondary);
		border-color: var(--secondary);
		color: white;
		box-shadow: 0 2px 8px rgba(234, 90, 67, 0.3);

		&:hover {
			background-color: #d14a33;
			border-color: #d14a33;
			color: white;
		}
	}
}

.option-price-display {
	padding: rem(10px) rem(14px);
	background-color: #fef5f3;
	border-left: 4px solid var(--secondary);
	border-radius: 4px;
	margin-top: rem(10px);
	font-size: rem(14px);
	animation: fadeIn 0.3s ease-in;

	strong {
		color: #333;
		margin-right: rem(8px);
	}

	.price-amount {
		font-size: rem(16px);
		font-weight: bold;
		color: var(--secondary);
	}
}

.option-quantity-input {
	padding: rem(10px) rem(14px);
	background-color: #f8f9fa;
	border-left: 4px solid #6c757d;
	border-radius: 4px;
	margin-top: rem(10px);
	font-size: rem(14px);
	animation: fadeIn 0.3s ease-in;

	label {
		display: inline-block;
		margin-right: rem(10px);
		color: #495057;
	}

	.quantity-input {
		width: 80px;
		padding: rem(5px) rem(10px);
		border: 2px solid #dee2e6;
		border-radius: 4px;
		font-size: rem(14px);
		text-align: center;
		transition: border-color 0.2s ease;

		&:focus {
			outline: none;
			border-color: var(--secondary);
			box-shadow: 0 0 0 3px rgba(234, 90, 67, 0.1);
		}

		&:hover {
			border-color: #adb5bd;
		}
	}
}

.total-price-display {
	padding: rem(15px) rem(20px);
	background-color: #d4edda;
	border: 2px solid #28a745;
	border-radius: 8px;
	margin-top: rem(15px);
	text-align: center;
	animation: fadeIn 0.3s ease-in;

	strong {
		color: #333;
		margin-right: rem(8px);
	}

	.total-price-amount {
		font-size: rem(20px);
		font-weight: bold;
		color: #28a745;
	}
}

@keyframes fadeIn {
	from {
		opacity: 0;
		transform: translateY(-10px);
	}

	to {
		opacity: 1;
		transform: translateY(0);
	}
}

// Disabled button state
.btn-disabled {
	opacity: 0.6;
	cursor: not-allowed !important;
	pointer-events: none;

	&:hover {
		transform: none !important;
		box-shadow: none !important;
	}
}

// Responsive design for smaller screens
@media (max-width: 768px) {
	.root-option-section {
		padding: rem(12px);
		margin-bottom: rem(20px);
	}

	.root-option-title {
		font-size: rem(15px);
		margin-bottom: rem(12px);
		padding-bottom: rem(8px);
	}

	.option-buttons-group {
		gap: rem(8px);
	}

	.option-button {
		padding: rem(8px) rem(16px);
		font-size: rem(13px);
		min-width: 80px;
	}

	.option-level-label {
		font-size: rem(12px);
	}

	.total-price-display {
		padding: rem(12px) rem(16px);

		.total-price-amount {
			font-size: rem(18px);
		}
	}

	.option-quantity-input {
		padding: rem(8px) rem(12px);

		.quantity-input {
			width: 70px;
			font-size: rem(13px);
			padding: rem(4px) rem(8px);
		}
	}
}
</style>
