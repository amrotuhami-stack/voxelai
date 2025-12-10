<template>
	<div>
		<div class="card">
			<div class="card__head"> 
				Subtotal
			</div>
			<div class="card__body">
				<div class="itemPrice">
					$1,295.00
					<p>$3,276.00</p>
				</div>
				<a href="#" class="btn btn-primary full">Proceed to Checkout</a>
				<div class="couponWrapper">
					<div class="Coupon">
						<input type="text" class="form-control" placeholder="Enter Coupon">
						<button type="button" class="btn btn-secondary">Apply</button>
					</div>
					<ul class="CouponApplied list-unstyled">
						<li>
							<span class="icon">
								<svg-icon icon-id="cross-icon" icon-viewBox="0 0 12 12"></svg-icon>
							</span>
							<p>NEWTOVOXEL</p>
							<span>applied</span>
						</li>
					</ul>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	props: {
		
	},
	data() {
		return {

		};
	},
};
</script>

<style lang="scss" scoped> 
.card{
	
	.itemPrice{
		font-size:rem(32px);
		color:var(--textPrimary);
		font-weight:500;
		p{
			text-decoration-line: line-through;
			color: #8E8E8E;
			margin-bottom:0;
			line-height:1;
			font-weight:400;
			margin-top:rem(10px);
		}
	}
	.Coupon{
		display: flex;
		justify-content: space-between;
		.form-control{
			background: transparent;
			border-radius: 8px;
			height:41px;
			border: 1px solid #C9C9C9;
			color: #8E8E8E;
			font-size:rem(14px);
			margin-right:rem(10px);
			padding-left:rem(18px);
			&::placeholder{
				color: #8E8E8E !important;
				font-size:rem(14px);
				display: block !important;
			}
		}
		.btn{
			height:41px;
			padding:rem(15px);
			font-size:rem(14px);
		}
	}
	.CouponApplied{
		padding-top:rem(12px);
		padding-left:6px;
		color:var(--textPrimary);
		font-size:rem(12px);
		letter-spacing: 1px;
		margin:0;
		li{
			display: flex;
			align-items: center;
			svg{
				width:12px;
				height:12px;
			}
			span{
				color:#00966d;
				font-weight:500;
				&.icon{
					cursor: pointer;
					transform: scale(.9);
					&:hover{
						opacity:.7;
					}
				}
			}
			p{
				color:var(--textPrimary);
				font-size:rem(12px);
				line-height:1;
				margin:0 7px;
				font-weight:500;
			}
		}
		
	}
	.btn{
		&.btn-primary{
			color: #FDEFED;
			background: #F7C0B7;
			border-color:#F7C0B7;
			margin:rem(15px) 0 rem(20px) 0;
			&:hover{
				background: var(--secondary);
				border-color: var(--secondary);
				color:#fff;
			}
		}
	}
}



</style>
