<template>
	<div class="table height-100">
		<div class="table__head">
			<div class="table__row">
				<div class="table__row--cell" data-width="20">ID</div>
				<div class="table__row--cell">Measurement</div>
				<div class="table__row--cell text-center" data-width="30">
					Actions
				</div>
			</div>
		</div>

		<div class="table__body">
			<div
				class="table__row"
				v-for="item in tableContent"
				:key="item.index"
			>
				<div class="table__row--cell" data-label="ID" data-width="20">
					{{ item.id }}
				</div>
				<div class="table__row--cell" data-label="Measurement">
					{{ item.measurement }}
				</div>
				<div
					class="table__row--cell text-center"
					data-label="Actions"
					data-width="30"
				>
					<div class="inline-buttons">
						<a href="#">
							<svg-icon
								:icon-id="item.editIcon"
								:icon-viewbox="item.viewBox"
							>
							</svg-icon>
						</a>
						<a href="#">
							<svg-icon
								:icon-id="item.trashIcon"
								:icon-viewbox="item.viewBox"
							>
							</svg-icon>
						</a>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	data() {
		return {
			tableContent: [
				{
					index: 0,
					id: 1,
					measurement: 'MEASUREME_01',
					editIcon: 'edit-icon',
					trashIcon: 'trash-icon',
					viewBox: '0 0 24 24',
				},
				{
					index: 1,
					id: 1,
					measurement: 'MEASUREME_02',
					editIcon: 'edit-icon',
					trashIcon: 'trash-icon',
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
			&:last-child {
				border-bottom: 1px solid #e9e9e9;
			}
		}
	}
	&__footer {
		border-top: 0 !important;
	}
}
</style>
