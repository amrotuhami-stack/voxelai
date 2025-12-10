<template>
	<div class="serverDown">
		<base-offer-notifications />
		<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
		<h1 class="main-title mb-50">Shop</h1>
		<div class="grid" data-grid-item-gap="40" data-grid-item-width="1/2">
			<div class="shop__filter">
				<shop-filters />
			</div>
			<div class="contentBox">
				<div class="image">
					<img src="@/assets/images/monitor.png" class="img-fluid" />
				</div>
				<h2>Our server is feeling a little down</h2>
				<p>please try again in a few moments.</p>
				<p>We'll be back up in no time.</p>
				<a href="#">Try Again</a>
			</div>
		</div>
	</div>
</template>

<script>
import BaseOfferNotifications from '../common/components/base/BaseOfferNotifications.vue';
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import { serverDownBreadCrumbs } from "@/common/constant/breadCrumbs"

import productItem from '../components/Products/productItem.vue';
import shopFilters from '../components/Products/Filters.vue';
export default {
	components: {
		productItem,
		BaseBreadCrumb,
		BaseOfferNotifications,
		shopFilters,
	},
	data() {
		return {
			breadCrumbsItems: [...serverDownBreadCrumbs],
		};
	},
};
</script>

<style lang="scss" scoped>
.serverDown {
	.grid {
		@media screen and (min-width: 992px) {
			grid-template-columns: 280px 1fr;
		}
		@media screen and (max-width: 991px) {
			grid-template-columns: none;
		}
	}
	.contentBox {
		padding: rem(64px);
		text-align: center;
		align-self: baseline;
		border-width: 2px;
		border-radius: 16px;
		h2 {
			font-size: rem(28px);
			margin-bottom: rem(24px);
			@media screen and (max-width:767px){
				font-size:rem(23px);
			}
		}
		@media screen and (max-width: 991px) {
			text-align: center;
			border: 0;
			padding-left: rem(15px);
			padding-right: rem(15px);
		}
	}
	.image {
		margin-bottom: rem(48px);
	}
	p {
		font-size: rem(16px);
		color: var(--textSecondary);
		margin-bottom: rem(3px);
	}
	a {
		margin-top: rem(25px);
		display: block;
	}
}
</style>
