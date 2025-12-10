<template>
	<div class="quantityToggle">
		<button
			:disabled="quantity == 0 ? true : false"
			@click="decrement"
			class="decrement"
		>
			<svg-icon icon-id="minus-icon" icon-viewbox="0 0 15 2"></svg-icon>
		</button>
		<input type="text" :value="quantity" />
		<button
			:disabled="quantity == 5 ? true : false"
			@click="increment"
			class="increament"
		>
			<svg-icon icon-id="plus-Icon" icon-viewbox="0 0 15 14"></svg-icon>
		</button>
	</div>
</template>

<script>
BaseIcons: () => import('@/common/components/base/BaseSvgIcons.vue');

export default {
	data() {
		return {
			quantity: 1,
		};
	},
	methods: {
		decrement: function () {
			this.quantity -= 1;
		},
		increment: function () {
			this.quantity += 1;
		},
	},
};
</script>

<style lang="scss" scoped>
.quantityToggle {
	display: flex;
	justify-content: space-around;
	align-items: center;
	width: 196px;
	border-radius: 12px;
	padding: rem(16px);
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
