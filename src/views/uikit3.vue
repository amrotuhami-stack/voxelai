<template>
	<div class="uikit3">
		<div class="container">
			<font-awesome-icon :icon="['fas', 'address-book']" />
			<font-awesome-icon :icon="['fab', 'font-awesome']" />
			<font-awesome-icon :icon="['fa', 'angle-right']" />
			<base-offer-notifications />
			<!-- <i class="fal fa-angle-right"></i> -->
			<div class="row">
				<div class="col col-md-4">
					<product-item />
				</div>
				<div class="col col-md-4">
					<product-item />
				</div>
				<div class="col col-md-4">
					<product-item />
				</div>
				<div class="col col-md-4">
					<div class="productItem card">
						<div class="card__body">
							<div class="productItem__image">
								<img
									alt=""
									src="@/assets/images/product-image.png"
									class="img-fluid"
								/>
							</div>
							<div class="productItem__info">
								<div class="productItem__info--title">
									3D Implant Planning
								</div>
								<div class="productItem__info--price">
									$79.00
									<span
										class="productItem__info--actualprice"
									>
										$109.00
									</span>
								</div>
								<div class="productItem__info--soldby">
									<i>Sold by</i>
									Voxel
								</div>
								<a href="#" class="productItem__info--seemore"
									>see more details</a
								>
								<div class="inline-button">
									<a
										href="#"
										class="btn btn-default btn-small"
									>
										<span class="icon big only-icon">
											<svg-icon
												icon-id="cart-icon"
												icon-viewbox="0 0 24 24"
											></svg-icon>
										</span>
									</a>
									<a href="#" class="btn btn-default full">
										Start This Service
									</a>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div class="col col-md-4">
					<div class="productItem card">
						<div class="card__body">
							<div class="productItem__image">
								<img
									alt=""
									src="@/assets/images/product-image.png"
									class="img-fluid"
								/>
							</div>
							<div class="productItem__info">
								<div class="productItem__info--title">
									3D Implant Planning
								</div>
								<div class="productItem__info--price">
									$79.00
									<span
										class="productItem__info--actualprice"
									>
										$109.00
									</span>
								</div>
								<div class="productItem__info--soldby">
									<i>Sold by</i>
									Voxel
								</div>
								<a href="#" class="productItem__info--seemore"
									>see more details</a
								>
								<div class="button-row">
									<a
										href="#"
										class="btn btn-secondary full green"
									>
										<span class="icon">
											<svg-icon
												icon-id="checked"
												icon-viewbox="0 0 14 10"
											></svg-icon> </span
										>Added to Cart Successfully
									</a>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div class="dummy-svg">
				<ul>
					<li>
						<svg-icon
							icon-id="activity"
							icon-viewbox="0 0 24 24"
						></svg-icon>
					</li>
					<li>
						<svg-icon
							icon-id="plus"
							icon-viewbox="0 0 24 24"
						></svg-icon>
					</li>
					<li>
						<svg-icon
							icon-id="user"
							icon-viewbox="0 0 24 24"
						></svg-icon>
					</li>
					<li>
						<svg-icon
							icon-id="document"
							icon-viewbox="0 0 24 24"
						></svg-icon>
					</li>
					<li>
						<svg-icon
							icon-id="discovery"
							icon-viewbox="0 0 24 24"
						></svg-icon>
					</li>
					<li>
						<svg-icon
							icon-id="discount"
							icon-viewbox="0 0 24 24"
						></svg-icon>
					</li>
					<li>
						<svg-icon
							icon-id="layer"
							icon-viewbox="0 0 24 24"
						></svg-icon>
					</li>
					<li>
						<svg-icon
							icon-id="setting"
							icon-viewbox="0 0 24 24"
						></svg-icon>
					</li>
					<li>
						<svg-icon
							icon-id="info-circle"
							icon-viewbox="0 0 24 24"
						></svg-icon>
					</li>
					<li>
						<svg-icon
							icon-id="user2"
							icon-viewbox="0 0 32 32"
						></svg-icon>
					</li>
					<li>
						<svg-icon
							icon-id="wallet"
							icon-viewbox="0 0 32 32"
						></svg-icon>
					</li>
				</ul>
			</div>
		</div>
	</div>
</template>
<script>
import BaseOfferNotifications from '../common/components/base/BaseOfferNotifications.vue';
import productItem from '../components/Products/productItem.vue';
export default {
	components: {
		productItem,
		BaseOfferNotifications,
	},
};
</script>

<style lang="scss" scoped>
.dummy-svg {
	svg {
		width: 25px;
	}
	ul {
		list-style: none;
		display: flex;
	}
	li {
		color: #ea5a43;
		margin-right: rem(15px);
	}
}
</style>
