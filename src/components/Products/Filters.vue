<template>
    <div>
        <button :class="toggleDropDown ? 'active' : ''" @click="toggleDropDown = !toggleDropDown" type="button" class="btn btn-secondary toggleFilterbtn" >
            Shop Filter <font-awesome-icon :icon="['fa', 'filter']" />
        </button>
        <div class="shopFilter" :class="toggleDropDown ? 'active' : ''">
            <div class="shopFilter__type">DEALS AND OFFERS</div>
            <ul>
                <li v-if="isDiscountedURL != ''"><a :class="fitterApplaied == 'Discount' ? 'selected_category' : ''" href="" @click.prevent="applyFilter('discount', 'all')">
                    Discount Offers
                </a></li>
                <li v-if="bestSellingURL != ''"><a :class="fitterApplaied == 'BestSelling' ? 'selected_category' : ''" href="" @click.prevent="applyFilter('best-selling', 'all')">
                    Best Selling
                </a></li>
            </ul>
            <div class="shopFilter__type">SERVICES CATEGORIES</div>
            <ul>
                <li><b><a :class="fitterApplaied == 'none' ? 'selected_category' : ''" href="" @click.prevent="fetchAllProductList">
                    Show All
                </a></b></li>
                <li v-for="(category, index) in categories" :key="index" >
                    <a :class="fitterApplaied == category.name ? 'selected_category' : ''" href="" @click.prevent="applyFilter('category', category.name)">
                        {{ category.name }}
                    </a>
                    <!-- <span>({{ category.count }})</span> !-->
                </li>
            </ul>
            <!-- <div class="shopFilter__type" v-if="partners.length > 1">SELLER <a href="" @click.prevent="fetchAllProductList()">Clear</a></div>
                <ul class="checkbox" v-if="partners.length > 1">
                    <li v-for="(partner, index) in partners" :key="index" @click.prevent="fetchOnlyProductListByURL(partner.select_url, partner.name)">
                        <label>
                            <input type="checkbox" name="radio" :checked="fitterApplaied == partner.name ? true : false"/>
                            <span>{{ partner.name }}</span>
                        </label>
                    </li>
                </ul> -->
            </div>
        </div>
</template>

<script>
// [*] Vuex State Getter And Action Helper
import { CatalogueHelper } from '@/common/crud-helpers/catalogue';
import { mapGetters } from 'vuex';

import { backendBase } from '@/conf'


export default {
    props: {
        category: String
    },
	data() {
		return {
            urlQuery: null,

			toggleDropDown: false,
            // Products Filters
            fitterApplaied: 'none',
            bestSellingURL: "",
            isDiscountedURL: "",
            categories : [],
            partners: [],
		};
	},
    computed: {
        ...mapGetters(['productList', 'allFacetData', 'loading'])
    },
	watch: {
		tabIndex: function (e) {
			document.querySelector()
			document.querySelector('.shop__filter .toggleFilterbtn').innerText =
			this.toggleDropDown = !this.toggleDropDown;
		},
        allFacetData() {
			this.categories = this.allFacetData.category.results;
            this.partners = this.allFacetData.soldby.results;

            let bestSellingObject = this.allFacetData.best_selling.results.filter((item) => item.name == 1)
            if(bestSellingObject.length > 0)
                this.bestSellingURL = bestSellingObject[0].select_url;

            let isDiscountedObject = this.allFacetData.is_discounted.results.filter((item) => item.name == 1)
            if(isDiscountedObject.length > 0)
                this.isDiscountedURL = isDiscountedObject[0].select_url;

            if(this.$route.query) {
                this.urlQuery = this.$route.query
            }
		},
        urlQuery() {
            if(!this.urlQuery) return;
            if(this.urlQuery.filter == 'category') {
                let index = this.categories.findIndex((item) => item.name == this.urlQuery.value)
                if(index != -1) {
                    this.fetchOnlyProductListByURL(this.categories[index].select_url, this.categories[index].name)
                }
            }
            if(this.urlQuery.filter == 'discount') {
                this.fetchOnlyProductListByURL(this.isDiscountedURL, 'Discount')
            }
            if(this.urlQuery.filter == 'best-selling') {
                this.fetchOnlyProductListByURL(this.bestSellingURL, 'BestSelling')
            }
        }
	},
    methods: {
        applyFilter: function(type, filter) {
            this.urlQuery = {filter: type, value: filter}
            if(this.$route.query.value === this.urlQuery.value) return;
            this.$router.replace({
                name: 'Shop',
                params: { page: "1" },
                query: this.urlQuery
            })
        },
        fetchOnlyProductListByURL: function(url, filter){
            this.fitterApplaied = filter
            CatalogueHelper.applyFilter(backendBase() + url);
        },
        fetchAllProductList: function(){
            this.urlQuery = null;
            this.$router.replace({query: undefined})
            this.fitterApplaied = 'none'
            CatalogueHelper.getProducts({});
        }
    }
};
</script>

<style lang="scss" scoped>

.shop {
    &__filter {
        .toggleFilterbtn  {
            display: none;
            width: 100%;
            margin-bottom: rem(50px);
            svg {
                margin-left: 8px;
            }
            @media screen and (max-width: 991px) {
                display: block;
            }
        }
    }
}

.shopFilter {
    @media screen and (max-width: 991px) {
        display: none;
    }
    &.active {
        @media screen and (max-width: 991px) {
            display: block;
        }
    }
    &__type {
        font-size: rem(12px);
        font-weight: 500;
        letter-spacing: 1px;
        position: relative;
        padding-left: rem(12px);
        margin-bottom: rem(35px);       
        &::before {
            position: absolute;
            top: -2px;
            left: 0;
            content: '';
            border: 1px solid #6B6B6B;
            width: 2px;
            height: 16px;
        }
    }
    ul {
        list-style: none;
        margin-left: rem(12px);
        margin-bottom: rem(50px);
        li {
            font-size: rem(16px);
            font-weight: 400;
            color: var(--textSecondary);
            display: flex;
            align-items: center;
            justify-content: space-between;
            &:not(:last-child) {
                margin-bottom: rem(28px);
            }
            b {
                font-weight: 500;
                color: var(--textPrimary);
            }
            span {
                font-size: rem(14px);
                margin-left: rem(5px);
            }
        }
    }     
    a {
        color: var(--primary);
        font-weight: 200;
        float: right;
        letter-spacing: 1px;
        &:hover {
            color: var(--secondary);
        }
        &.selected_category {
            font-weight: 500;
        }
    }
    .checkbox {
        padding-top: unset;
        span {
            font-size: rem(16px) !important;
            font-weight: 400;
            padding-bottom: unset !important;
            margin-left: unset;
        }
    }   
    
}
</style>