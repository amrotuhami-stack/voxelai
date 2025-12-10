<template>
	<div class="card">
		<div class="card__head">Order Details</div>
		<div class="card__body">
			<base-inner-scrollbar height="380px" v-if="cartLines">
				<cart-items :lines="cartLines"/>
			</base-inner-scrollbar>
		</div>
	</div>
</template>

<script>
import CartItems from './partials/CartItems.vue';
import { mapGetters } from 'vuex';

export default {
	components: { CartItems },
	computed: {
		...mapGetters(['cartLines']),
	},
	data() {
		return {};
	},
};
</script>

<style lang="scss" scoped>
.card {
	&__head {
		padding: rem(27px) rem(24px);
	}
	&__body {
		padding: 0 0 0 rem(16px);
	}
	::v-deep {
		.cartItem__product {
			margin-top: rem(16px);
			margin-bottom: rem(16px);
			padding-right: rem(16px);
			&--image {
				flex: 0 0 96px;
				max-width: 96px;
			}
			&--title {
				flex: 1;
				max-width: 100%;
				font-size: rem(14px);
				line-height: 1.2;
			}
		}
	}
}
</style>
