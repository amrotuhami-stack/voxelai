<template>
	<div class="offerBar">
		<div class="offerBar--text">
			<span class="offerBar--icon">
				<svg-icon
					icon-id="discount"
					icon-viewbox="0 0 32 32"
				></svg-icon>
			</span>
			Special Limited Offer Get
			<b> 30 </b>% off Now.
			<a href="#" class="see-more viewMore">
				get the offer
				<font-awesome-icon :icon="['fa', 'angle-right']" />
			</a>
		</div>
		<div class="offerBar--countdown">Ends in 10:53:43</div>
	</div>
</template>

<script>
export default {};
</script>

<style lang="scss" scoped>
.offerBar {
	background: linear-gradient(345.63deg, #ebaea4 -196.47%, #f7c0b7 90.84%);
	position: relative;
	// background: #f7c0b7;
	// opacity: 0.9;
	padding: rem(16px) rem(48px);
	border-radius: 34px;
	margin-bottom: rem(34px);
	display: flex;
	align-items: center;
	justify-content: space-between;
	z-index: 2;
	overflow: hidden;
	@media screen and (max-width: 767px) {
		flex-direction: column;
		height: auto;
		text-align: center;
		border-radius: 12px;
	}
	&::before {
		position: absolute;
		content: '';
		width: 100%;
		height: 100%;
		background-image: url('../../../assets/images/offer-background.png');
		background-repeat: no-repeat;
		background-size: cover;
		top: 0;
		left: 0;
		z-index: 1;
	}
	&--text {
		font-size: rem(16px);
		font-weight: 400;
		color: var(--textPrimary);
		display: flex;
		align-items: center;
		position: relative;
		z-index: 2;
		@media screen and (max-width: 767px) {
			flex-wrap: wrap;
			justify-content: center;
		}
	}
	b {
		display: inline-block;
		font-weight: 500;
		margin-left: rem(3px);
		@media screen and (max-width: 767px) {
			display: inline;
		}
	}
	&--icon {
		margin-right: rem(12px);
		color: #EA5A43;
		svg {
			width: 32px;
			height: 32px;
		}
		@media screen and (max-width: 767px) {
			margin-bottom: rem(10px);
			margin-right: 0;
			flex: 0 0 100%;
		}
	}
	.see-more {
		font-size: rem(16px);
		font-weight: 700;
		margin-left: rem(12px);
		text-decoration: underline;
		text-transform: uppercase;
		@media screen and (max-width: 767px) {
			margin-left: rem(0px);
			flex: 0 0 100%;
			margin-top: rem(10px);
			margin-bottom: rem(10px);
		}
	}
	&--countdown {
		font-size: rem(16px);
		font-weight: 500;
		color: var(--textPrimary);
		z-index: 2;
	}
}
</style>
