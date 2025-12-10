<template>
	<div class="table selectedItems">
		<div class="table__head">
			<div class="table__row">
				<div class="table__row--cell" data-width="22">ORD</div>
				<div class="table__row--cell" data-width="12">ID</div>
				<div class="table__row--cell">Measurement</div>
				<div class="table__row--cell" data-width="20">Remove</div>
			</div>
		</div>

		<div class="table__body">
			<base-smooth-scrollbar height="288px">
				<div
					class="table__row"
					v-for="item in tableContent"
					:key="item.index"
				>
					<div
						class="table__row--cell"
						data-label="ORD"
						data-width="22"
					>
						{{ item.ord }}
					</div>
					<div
						class="table__row--cell"
						data-label="ID"
						data-width="12"
					>
						{{ item.id }}
					</div>
					<div class="table__row--cell" data-label="Measurement">
						{{ item.measurement }}
					</div>
					<div
						class="table__row--cell"
						data-label="Remove"
						data-width="20"
					>
						<svg-icon
							icon-id="remove-icon"
							icon-viewbox="0 0 24 24"
						>
						</svg-icon>
					</div>
				</div>
			</base-smooth-scrollbar>
		</div>
		<div class="table__footer">
			<div class="order">
				<label>ORDER</label>
				<div class="d-flex align-items-center">
					<span
						><font-awesome-icon :icon="['fas', 'angle-up']"
					/></span>
					<span
						><font-awesome-icon :icon="['fas', 'angle-down']"
					/></span>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import BaseSmoothScrollbar from '../../../common/components/base/BaseSmoothScrollbar.vue';
export default {
	components: { BaseSmoothScrollbar },

	data() {
		return {
			tableContent: [
				{
					index: 0,
					ord: 1,
					id: 44,
					measurement: 'MEASUREME_01',
					icon: 'remove-icon',
					viewBox: '0 0 24 24',
				},
			],
		};
	},
};
</script>

<style lang="scss" scoped>
.table {
	&__body {
		.table__row {
			&:not(:last-child) {
				border-bottom: 2px solid var(--borderColor) !important;
			}
		}
		.table__row--cell {
			padding: 0;
		}
		::v-deep .remove-icon {
			@media screen and (min-width:992px){
				display: table-cell !important;
			}
		}
	}
	&__footer {
		.order {
			display: flex;
			align-items: center;
			label {
				font-size: rem(12px);
				color: #8e8e8e;
				font-weight: 400;
				margin: 0 rem(10px) 0 0;
				padding: 0;
				text-transform: uppercase;
			}
			span {
				width: 32px;
				height: 32px;
				border-radius: 8px;
				border: 3.25px solid #a8d5ee;
				@include flex(center, center);
				cursor: pointer;
				svg {
					color: #1a90d2;
				}
				&:not(:last-child) {
					margin-right: 10px;
				}
				&:hover {
					opacity: 0.7;
				}
			}
		}
	}
}
</style>
