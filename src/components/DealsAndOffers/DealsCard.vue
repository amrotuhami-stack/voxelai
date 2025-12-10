<template>
	<div class="deal card">
		<div class="card__body">
			<div class="deal__image">
				<!-- <img :src="require(`@/assets/images/${image}.png`)" alt="" /> -->
			</div>
			<button class="btn btn-primary full">Get This Offer</button>
		</div>
	</div>
</template>

<script>
export default {
	props: {
		image: String,
	},
};
</script>

<style lang="scss" scoped>
.deal {
	&.card {
		border-width: 2px;
		border-radius: 16px;
		margin-bottom: rem(24px);
		@media screen and (max-width: 575px) {
			border: 0;
			border-radius: 0;
			border-bottom: 2px solid var(--borderColor);
			.card__body {
				padding: 0;
				padding-bottom: 1.5rem;
			}
		}
	}
	&__image {
		height: 360px;
		// max-width: 360px;
		// width: 100%;
		border-radius: 12px;
		background: var(--imageBg);
		margin-bottom: rem(24px);
		display: flex;
		align-items: center;
		justify-content: center;
		@media screen and (max-width: 991px) {
			height: 250px;
		}
		@media screen and (max-width: 767px) {
			height: 200px;
		}
		img {
			max-width: 100%;
			height: auto;
		}
	}
}
</style>
