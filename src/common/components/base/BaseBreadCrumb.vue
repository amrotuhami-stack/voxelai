<template>
	<div class="breadCrumb">
		<b-breadcrumb :items="items" ></b-breadcrumb>
	</div>
</template>

<script>
export default {
	props: {
		items: Array,
	},
	data() {
		return {};
	},
};
</script>

<style lang="scss" scoped>
.breadCrumb {
	margin-bottom: rem(32px);
	::v-deep {
		.breadcrumb {
			background: transparent;
			&-item {
				margin-bottom: 10px;
				color: var(--textSecondary);
				opacity: 1;
				font-size: rem(14px);
				font-weight: 400;
				padding-right: rem(24px);
				padding-left: rem(8px);
				position: relative;
				text-transform: capitalize;
				&:first-child {
					padding-left: 0;
				}
				&:not(:first-child) {
					&::before {
						content: '/';
						position: absolute;
						top: 50%;
						transform: translateY(-50%);
						left: -10px;
						color: #c9c9c9;
						padding-right: 0;
						// @media screen and (max-width: 405px) {
						// 	left: 0px;
						// }
					}
				}
				a {
					color: var(--primary);
					opacity: 1;
					font-size: rem(14px);
					font-weight: 500;
					transition: 0.3s ease all;
					text-transform: capitalize;
					text-decoration: none;
					&:hover {
						opacity: 0.8;
					}
				}
			}
		}
	}
}
</style>
