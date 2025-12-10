<template>
	<div>
		<product v-for="item in lines" :key="item.index" :product="item.product_obj"  :showAmount="true" :cartLine="item" :basketId="item.basket_id" />
	</div>
</template>

<script>
import Product from '../../cart/partials/Product.vue';
export default {
	components: { Product },
	props: { lines: Array },
};
</script>

<style lang="scss" scoped></style>
