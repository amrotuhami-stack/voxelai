<template>
	<div class="table">
		<div class="table__head">
			<div class="table__row">
				<div class="table__row--cell" data-width="20">ID</div>
				<div class="table__row--cell">Analysis Name</div>
				<div class="table__row--cell" data-width="20">Actions</div>
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
						data-label="ID"
						data-width="20"
					>
						{{ item.id }}
					</div>
					<div class="table__row--cell" data-label="Analysis Name">
						{{ item.name }}
					</div>
					<div
						class="table__row--cell"
						data-label="Actions"
						data-width="20"
					>
						<a href="#">
							<svg-icon
								:icon-id="item.icon"
								:icon-viewbox="item.viewBox"
							>
							</svg-icon>
						</a>
					</div>
				</div>
			</base-smooth-scrollbar>
		</div>
		<div class="table__footer">
			<button class="btn btn-secondary full pink" v-b-modal="'my-modal'">
				Add New
			</button>
			<b-modal ref="my-modal" id="my-modal" centered>
				<div class="modal-title">New Custom Analysis</div>
				<p>Enter unique name to create new analyis</p>
				<form>
					<div class="form-group">
						<input
							type="text"
							id="current"
							class="form-control"
							autocomplete="off"
							required=""
							name="Analyis Name"
							placeholder="First Analyis Name"
						/>
						<label class="control-label">Analyis Name</label>
					</div>
					<div class="inline-buttons">
						<button type="button" class="btn btn-primary">
							save
						</button>
						<a
							href="javascript:void(0)"
							@click="hideModal"
							class="link"
							>Cancel</a
						>
					</div>
				</form>
			</b-modal>
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
					id: 1,
					name: 'CUSTOM ANALYSIS_01',
					icon: 'trash-icon',
					viewBox: '0 0 24 24',
				},
				{
					index: 1,
					id: 1,
					name: 'CUSTOM ANALYSIS_01',
					icon: 'trash-icon',
					viewBox: '0 0 24 24',
				},
			],
		};
	},
	methods: {
		hideModal() {
			this.$refs['my-modal'].hide();
		},
	},
};
</script>

<style lang="scss" scoped>
.table {
	height: calc(100% - 28px) !important;
	&__body{
		height: calc(100% - 125px);
	}
}
</style>
