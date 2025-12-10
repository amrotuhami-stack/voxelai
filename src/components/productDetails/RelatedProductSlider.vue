<template>
	<div class="productDetail__relatedProducts" v-if="relatedProducts.length > 0">
		<div class="sectionTitle">Related Products</div>
		<carousel  navigationLayout="side_navigation" :carousel-settings="sliderOption" >
			<div class="swiper-slide" v-for="(item, index) in relatedProducts" :key="item.id">
				<product-item :product="item" :productListIndex="index"/> 
			</div>
		</carousel>
	</div>
</template>

<script>
// [*] Import UI Components
import productItem from '@/components/Products/productItem.vue';

// [*] Vuex State Getter And Action Helper
import { CatalogueHelper } from '@/common/crud-helpers/catalogue';
import { mapGetters } from 'vuex';

export default {
	components: {
		productItem,
	},
	data() {
		return {
			sliderOption: {
                speed: 1000,
				spaceBetween: 20,
				breakpoints: {
					1351: {
						slidesPerView: 4,
						spaceBetween: 20,
					},
					1300: {
						slidesPerView: 3,
						spaceBetween: 15,
					},
					720: {
						slidesPerView: 3,
						spaceBetween: 15,
					},
					485: {
						slidesPerView: 2,
						spaceBetween: 10,
					},
					370: {
						slidesPerView: 1,
					},
				},
            },
		};
	},
	computed: {
		...mapGetters(['relatedProducts']),
	},
	methods: {
		getProducts: function() {
			CatalogueHelper.getProducts({});
		},
	}
};
</script>

<style lang="scss">
	.dashboard {
		$parent: &;
		&:not(.dashboard__nav--close) {
			#{ $parent }__right{
				.productItem { 
					.card{
						&__body{
							padding:rem(8px);
						}
					}
				}
			}
		}
	} 
</style>
<style lang="scss" scoped>
.sectionTitle{
		font-size:rem(28px);
		color:var(--black);
		font-weight:500;
	}
	.productDetail{
		&__relatedProducts{
			position:relative;
			.sectionTitle{
				margin-bottom:rem(35px);
			}
		}
	}

.productDetail__relatedProducts {
	.baseSliderWrapper {
		@media screen and (max-width: 991px ) {
			::v-deep .sliderNavigation {
				&__controls {
					justify-content: space-between;
    				max-width: 130px;
				}
			}
		}

		@media screen and (max-width: 575px ) {
			padding-bottom: 60px;
			::v-deep .sliderNavigation {
				top: auto;
				margin: auto;
				bottom: 0;
				left: 0;
				&__controls {
					margin: auto;
				}
			}
		}
	}
}
	
</style>
