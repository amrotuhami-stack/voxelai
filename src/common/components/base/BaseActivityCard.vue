<template>
	<div class="activityCard card" :class="color">
		<div class="card__body">
			<div
				class="activityCard__item"
				v-for="(item, index) in data"
				:key="index + 1"
			>
				<div class="activityCard__item--value">{{ item.value }}</div>
				<div class="activityCard__item--label">{{ item.label }}</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	props: {
		data: Array,
		color: String,
	},
};
</script>

<style lang="scss" scoped>
.activityCard {
	@media screen and (max-width: 767px) {
		margin-bottom: 15px !important;
		text-align: center;
		.card__body {
			padding-left: rem(15px);
			padding-right: rem(15px);
		}
	}
	&__item {
		&:first-child {
			padding-bottom: rem(20px);
		}
		&:not(:last-child) {
			border-bottom: 1px solid var(--borderColor);
			margin-bottom: rem(18px);
		}
		&--value {
			font-size: rem(48px);
			font-weight: 500;
			color: var(--textPrimary);
			margin: rem(8px) 0 rem(14px) 0;
			@media screen and (max-width:767px){
				font-size:rem(35px);
			}
		}
		&--label {
			font-size: rem(16px);
			font-weight: 400;
			color: var(--default);
		}
	}
	&.blue {
		background: #eef7fb;
		--borderColor: #a8d5ee;
	}
	&.pink {
		background: #fdefed;
		--borderColor: #f7c0b7;
	}
	&.green {
		background: #edfdf3;
		--borderColor: #a8eec4;
	}
}
</style>
