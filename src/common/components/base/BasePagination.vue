<template>
	<div class="pagination">
		<div class="count">Count: {{ count }}</div>
		<div v-if="count && itemPerPage">
			<b-pagination-nav
				:link-gen="linkGen"
				:number-of-pages="pagesCount()"
				align="center"
				use-router
			></b-pagination-nav>
		</div>
	</div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
	props: {
		path: String,
		itemPerPage: Number,
		count: Number
	},
	data() {
		return {

		};
	},
	
	methods: {
		linkGen(pageNum) {
			return this.path +  `${pageNum}`;
		},
		pagesCount() {
			let mod = this.count % this.itemPerPage
			return   mod == 0 ? this.count / this.itemPerPage : (this.count / this.itemPerPage) + 1
		}
	},
};
</script>

<style lang="scss" scoped>
.pagination {
	margin-top: rem(24px);
	display: flex;
	justify-content: space-between;
	align-items: center;
	.count {
		font-size: rem(14px);
		color: var(--textSecondary);
		font-weight: 400;
	}
	::v-deep {
		.pagination {
			padding: 5px 0;
			.page-item {
				height: 32px;
				width: 35px;
				@include flex(center, center);
				margin-bottom: 0;
				.page-link {
					background: transparent;
					color: var(--default);
					font-weight: 400;
					font-size: rem(14px);
					padding: 0 6px;
					margin: 0px;
					display: block;
					@include flex(center, center);
					height: 100%;
					width: 100%;
					&.page-link {
						outline: none;
					}
					// &:focus {
					// 	border: 3px dashed var(--primary);
					// 	outline: none;
					// }
				}
				&.active {
					a {
						color: #fff;
						background: #1a90d2;
						border-radius: 8px;
						border: 1px solid #1a90d2;
						font-weight: 400;
					}
				}
				// &:not(:last-child) {
				// 	margin-right: rem(12px);
				// }
			}
		}
	}
}
</style>
