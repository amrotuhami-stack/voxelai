<template>
	<div class="vertically-center">
		<div class="image">
			<img
				src="@/assets/images/paypal-logo.png"
				class="img-fluid"
				alt="paypal"
			/>
		</div>
		<p>
			In order to complete your transaction, we will transfer you over to PayPal's secure servers.
		</p>
	</div>
</template>

<script>
export default {
	
};
</script>

<style lang="scss" scoped>
	.vertically-center {
		display: flex;
		align-items: center;
		justify-content: center;
		flex-direction: column;
		max-width: 450px;
		margin-left: auto;
		margin-right: auto;
		text-align: center;
		padding-top: rem(105px);
		padding-bottom: rem(105px);
		p {
			margin-bottom: 0;
			margin-top: rem(25px);
		}
	}
</style>
