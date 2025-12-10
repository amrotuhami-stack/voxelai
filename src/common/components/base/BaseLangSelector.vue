<template>
	<div>
		<b-dropdown>
			<div class="langSelector">
				<a href="#">
					<img
						src="@/assets/images/flags/usa.png"
						class="img-fluid"
						alt="usa"
					/>
					English
				</a>
				<a href="#">
					<img
						src="@/assets/images/flags/arabic.png"
						class="img-fluid"
						alt="usa"
					/>
					العربيه
				</a>
			</div>
		</b-dropdown>
	</div>
</template>

<script>

export default {
	
};
</script>
<style lang="scss">
	.langSelector{
		a{
			display: block;
			padding:rem(20px) 0;
			font-size:rem(16px);
			color:var(--default) !important;
			font-weight:400 !important;
			&:hover{
				color: var(--secondary) !important;
			}
			&:not(:last-child){
				border-bottom:1px solid #E9E9E9;
			}
			img{
				margin-right:10px;
			}
		}
	}
</style>
<style lang="scss" scoped>
::v-deep {
	.dropdown {
		box-shadow: none !important;
		.dropdown-toggle {
			width: 24px;
			height: 24px;
			background: transparent !important;
			background-color: transparent !important;
			padding:0 !important;
			&:hover,
			&:focus {
				background: transparent !important;
				background-color: transparent !important;
			}
			&::after {
				display: none;
			}
		}
		.dropdown-menu {
			width: 190px;
			padding:0 rem(18px);
			border-radius: 10px !important;
			box-shadow: 0px 2px 11px rgba(107, 107, 107, 0.16);
			right: 0;
			left:auto !important;
			margin-top:rem(64px);
			transform: none !important;
			
			
		}
		&.show {
			.btn {
				background: transparent !important;
				background-color: transparent !important;
			}
		}
		
	}
}
</style>
