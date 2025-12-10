<template>
	<div class="deals-and-offers">
		<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
		<h1 class="main-title mb-10">Deals and Offers</h1>
		<p>Get exclusive offers and apply your coupons</p>
		<div class="row">
			<div class="col-md-4 col-sm-6">
				<deals-card />
			</div>
			<div class="col-md-4 col-sm-6">
				<deals-card />
			</div>
			<div class="col-md-4 col-sm-6">
				<deals-card />
			</div>
			<div class="col-md-4 col-sm-6">
				<deals-card />
			</div>
			<div class="col-md-4 col-sm-6">
				<deals-card />
			</div>
			<div class="col-md-4 col-sm-6">
				<deals-card />
			</div>
		</div>
	</div>
</template>

<script>
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import { dealsAndOffersBreadCrumbs } from "@/common/constant/breadCrumbs"

import DealsCard from '../components/DealsAndOffers/DealsCard.vue';

export default {
	components: {
		BaseBreadCrumb,
		DealsCard,
	},
	data() {
		return {
			breadCrumbsItems: [...dealsAndOffersBreadCrumbs],
		};
	},
};
</script>

<style lang="scss" scoped>
.deals-and-offers {
	p {
		font-weight: 400;
		margin-bottom: rem(34px);
	}
}
</style>
