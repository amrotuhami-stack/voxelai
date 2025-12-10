<template>
	<div class="empty-shopping-cart">
		<!-- <base-offer-notifications /> -->
		<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
		<h1 class="main-title mb-25">Shopping Cart</h1>
		<div class="contentBox">
			<div class="image">
				<img src="../assets/images/file.png" class="img-fluid" />
			</div>
			<p>Your cart is empty.</p>
			<p>Keep shopping to find a service!</p>
			<router-link
				:to="{
					name: 'Shop',
					params: {
						lang: $i18n.locale,
						page: '1'
					},
				}"
				class="btn btn-primary"
			>
				Keep Shopping
			</router-link>
			<!-- <button class="btn btn-primary">Keep Shopping</button> -->
		</div>
	</div>
</template>

<script>
import BaseOfferNotifications from '../common/components/base/BaseOfferNotifications.vue';

import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import { emptyShoppingCartBreadCrumbs } from "@/common/constant/breadCrumbs"

export default {
	components: {
		BaseBreadCrumb,
		BaseOfferNotifications,
	},
	data() {
		return {
			breadCrumbsItems: [...emptyShoppingCartBreadCrumbs],
		};
	},
};
</script>

<style lang="scss" scoped>
.empty-shopping-cart {
	.contentBox {
		display: flex;
		align-items: center;
		justify-content: center;
		flex-direction: column;
		padding: rem(64px);
		@media screen and (max-width: 991px) {
			text-align: center;
			border: 0;
			padding-left: rem(15px);
			padding-right: rem(15px);
		}
	}
	.image {
		text-align: center;
		margin-bottom: rem(50px);
	}
	p {
		font-size: rem(20px);
		color: var(--textSecondary);
		margin-bottom: rem(3px);
		font-weight: 400;
	}
	.btn {
		margin-top: rem(22px);
		padding-right: rem(88px);
		padding-left: rem(88px);
		box-shadow: 0px 9px 25px rgba(234, 90, 67, 0.35) !important;
	}
}
</style>
