<template>
	<div class="activityCard card" :class="color">
		<div class="activityCard__icon">
			<svg-icon
				:icon-id="data.icon"
				:icon-viewbox="data.viewBox"
			></svg-icon>
		</div>
		<div class="activityCard__detail">
			<span>{{ data.value }}</span>
			<p>{{ data.label }}</p>
		</div>
		<b-dropdown class="action-dropdown" v-if="data.isDropdown">
			<b-dropdown-item href="#"> Add funds to wallet </b-dropdown-item>
			<b-dropdown-item href="#"> Withdrawal request </b-dropdown-item>
		</b-dropdown>
	</div>
</template>

<script>
export default {
	props: {
		data: Object,
		color: String,
	},
};
</script>

<style lang="scss" scoped>
.activityCard {
	overflow: unset !important;
	padding: rem(24px) !important;
	display: flex;
	flex-direction: row;
	align-items: center;
	::v-deep .dropdown {
		position: absolute;
		top: 40px;
		right: 15px;
		@media screen and (max-width:1199px){
			top: 20px;
    		right: 5px;
		}
		.dropdown-toggle{
			&::after{
				right:0 !important;
				left:auto !important;
			}
		}
		.dropdown-menu{
			left: auto !important;
    		right: 0 !important;
		}
	}
	&__icon {
		margin-right: rem(24px);
		width: rem(62px);
		min-width: rem(62px);
		height: rem(62px);
		border-radius: 100%;
		background-color: var(--imageBg);
		@include flex(center, center);
		svg {
			width: 32px;
			height: 32px;
		}
	}
	&__detail {
		span {
			font-size: rem(32px);
			font-weight: 500;
			color: var(--textPrimary);
			margin: rem(8px) 0 rem(14px) 0;
			@media screen and (max-width: 767px) {
				font-size: rem(35px);
			}
		}
		p {
			font-size: rem(16px);
			font-weight: 400;
			color: var(--default);
			margin: 0;
			margin-top: 5px;
		}
	}
	&.green {
		background: #edfdf3;
		--borderColor: #a8eec4;
		--imageBg: rgba(94, 238, 238, 0.1);
	}
	@media screen and (max-width:1199px) and (min-width:992px){
		padding:rem(24px) rem(16px) !important;
	}
	@media screen and (max-width:767px){
		margin-bottom:rem(25px) !important;
	}
}
</style>
