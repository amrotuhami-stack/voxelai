<template>
	<div>
		<ul class="shipmentProgress">
			<li class="shipmentProgress__item completed">
				Ready for Shipping
				<!-- <p>
					expected on
					<span>Sat. 19/04/2021, at 09:34 [GMT+8]</span>
				</p> !-->
			</li>
			<li class="shipmentProgress__item current">
				Out for Delivery
				<!-- <p>
					expected on
					<span>Sat. 19/04/2021, at 09:34 [GMT+8]</span>
				</p> !-->
			</li>
			<li class="shipmentProgress__item pending">
				Delivered
				<!--<p>
					expected on
					<span>Sat. 19/04/2021, at 09:34 [GMT+8]</span>
				</p> !-->
			</li>
		</ul>
	</div>
</template>

<script>
export default {};
</script>

<style lang="scss" scoped>
.shipmentProgress {
	list-style: none;
	&__item {
		position: relative;
		padding-left: rem(32px);
		font-size: rem(16px);
		color: var(--textSecondary);
		margin-bottom: 0;
		padding-bottom: rem(34px);
		font-weight: 500;
		p {
			margin-bottom: 0;
			font-size: rem(12px) !important;
			color: #c9c9c9 !important;
			font-weight: 400;
			margin-top: rem(4px);
			span {
				color: #c9c9c9;
			}
		}
		&::before {
			content: '';
			position: absolute;
			width: 16px;
			height: 16px;
			border-radius: 50%;
			left: 0;
			top: 5px;
			z-index: 1;
		}
		&:not(:last-child)::after {
			content: '';
			position: absolute;
			width: 1px;
			height: 100%;
			border: 1px dashed #c9c9c9;
			left: 7px;
			top: 5px;
		}
		&.completed {
			&::before {
				background-color: var(--secondary);
				border: 2px solid var(--secondary);
			}
		}
		&.current {
			color: var(--textPrimary);
			p {
				span {
					color: #00966d;
				}
			}
			&::before {
				background-color: #fff;
				border: 2px solid var(--secondary);
			}
		}
		&.pending {
			padding-bottom: rem(12px);
			&::before {
				background-color: #fff;
				border: 2px solid #c9c9c9;
			}
		}
	}
}
</style>
