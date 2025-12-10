<template>
	<div class="shop">
		<!-- <base-offer-notifications /> -->
		<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
		<h1 class="main-title mb-50">Shop</h1>
		<div class="grid" data-grid-item-gap="20" data-grid-item-width="1/2">
			<div class="shop__filter">
				<shop-filters />
			</div>
			<div class="shop__listing">
				<div class="row" v-if="products.length == 0" >
					<div class="col-md-4 col-sm-6" v-for="(_, index) in 6" :key="'shop_item' + index">
						<product-item :product="{}" :productListIndex="index" :skelton="true" />
					</div>
				</div>
				<div class="row">
					<div
						class="col-md-4 col-sm-6"
						v-for="(item, index) in products"
						:key="index"
					>
						<product-item :product="item" :productListIndex="index" />
					</div>
				</div>
				<!-- <base-pagination v-if="products.length" path="/shop/page=" :itemPerPage="3" :count='productsCount'/> -->
			</div>
		</div>
	</div>
</template>

<script>
// [*] Import UI Components .
import productItem from '../components/Products/productItem.vue';
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import BaseOfferNotifications from '../common/components/base/BaseOfferNotifications.vue';
import shopFilters from '../components/Products/Filters.vue';
import BasePagination from '@/common/components/base/BasePagination.vue';

// [*] Import Breadcrumbs
import { shopBreadCrumbs } from "@/common/constant/breadCrumbs"

// [*] Vuex State Getter And Action Helper
import { CatalogueHelper } from '@/common/crud-helpers/catalogue';
import { mapGetters } from 'vuex';


export default {
	props: {
		page: String,
	},
	components: {
		productItem,
		BaseBreadCrumb,
		BaseOfferNotifications,
		shopFilters,
		BasePagination
	},
	data() {
		return {
			breadCrumbsItems: [...shopBreadCrumbs],
			products: [],
		};
	},
	mounted() {
        CatalogueHelper.getProducts({'page': this.page});
    },
	computed: {
		...mapGetters(['productList', 'loading', 'productsCount']),
    },
	watch: {
		page() {
			CatalogueHelper.getProducts({'page': this.page});
		},
        productList() {
            this.products = this.productList;
        },
    },
};
</script>

<style lang="scss" scoped>
.shop {
	.grid {
		@media screen and (min-width: 992px) {
			grid-template-columns: 280px 1fr;
		}
		@media screen and (max-width: 991px) {
			grid-template-columns: none;
		}
	}
	::v-deep {
		.productItem__info--title {
			@include truncate(1);
		}
	}
	&__listing{
		.row{
			@media screen and (max-width:1300px) and (min-width:992px){
				>div{
					max-width:50%;
					flex:0 0 50%;
				}
			}
		}
		@media screen and (max-width:575px){
			::v-deep{
				.card{
					max-width:400px;
					margin:auto auto rem(25px) auto;
				}
			}
		}
	}
}
</style>
