<template>
	<div class="creatNew height-100">
		<div class="creatNew__body">
			<div class="accordion" role="tablist">
				<b-card no-body>
					<b-card-header header-tag="header" role="tab">
						<b-button block v-b-toggle.Info variant="info"
							>Measurement Info</b-button
						>
					</b-card-header>
					<b-collapse
						id="Info"
						visible
						accordion="my-accordion"
						role="tabpanel"
					>
						<b-card-body>
							<div class="form-group">
								<input
									type="text"
									required="required"
									name="Notes"
									placeholder="Enter unique name"
									class="form-control"
								/>
								<label class="control-label"
									>Measurement Name</label
								>
							</div>
							<div class="form-group no-label m-0">
								<b-form-select
									v-model="selected"
									:options="measurementType"
								></b-form-select>
							</div>
						</b-card-body>
					</b-collapse>
				</b-card>
				<b-card no-body>
					<b-card-header header-tag="header" role="tab">
						<b-button block v-b-toggle.Variables variant="info"
							>Input Variables</b-button
						>
					</b-card-header>
					<b-collapse
						id="Variables"
						visible
						accordion="my-accordion"
						role="tabpanel"
					>
						<b-card-body>
							<div class="selectWreapper">
								<div class="form-group no-label">
									<b-form-select
										v-model="selected1"
										:options="AnalysisType"
									></b-form-select>
								</div>
								<div class="form-group no-label">
									<b-form-select
										v-model="selected2"
										:options="PointA"
									></b-form-select>
								</div>
								<div class="form-group no-label">
									<b-form-select
										v-model="selected3"
										:options="PointB"
									></b-form-select>
								</div>
								<div class="form-group no-label">
									<b-form-select
										v-model="selected4"
										:options="PointC"
									></b-form-select>
								</div>
								<div class="form-group no-label">
									<b-form-select
										v-model="selected5"
										:options="PointD"
									></b-form-select>
								</div>
							</div>
						</b-card-body>
					</b-collapse>
				</b-card>
				<b-card no-body>
					<b-card-header header-tag="header" role="tab">
						<b-button block v-b-toggle.Meaning variant="info"
							>Meaning</b-button
						>
					</b-card-header>
					<b-collapse
						id="Meaning"
						visible
						accordion="my-accordion"
						role="tabpanel"
					>
						<b-card-body>
							<div class="form-group">
								<input
									type="text"
									class="form-control"
									required=""
									name="Meaning large"
									placeholder="Meaning large"
								/>
								<label class="control-label"
									>Meaning large</label
								>
							</div>
							<div class="form-group">
								<input
									type="text"
									class="form-control"
									required=""
									name="Meaning Normal"
									placeholder="Meaning Normal"
								/>
								<label class="control-label"
									>Meaning Normal</label
								>
							</div>
							<div class="form-group">
								<input
									type="text"
									class="form-control"
									required=""
									name="Meaning Small"
									placeholder="Meaning Small"
								/>
								<label class="control-label"
									>Meaning Small</label
								>
							</div>
						</b-card-body>
					</b-collapse>
				</b-card>
				<b-card no-body>
					<b-card-header header-tag="header" role="tab">
						<b-button block v-b-toggle.Positions variant="info"
							>Result Text Positions</b-button
						>
					</b-card-header>
					<b-collapse
						id="Positions"
						visible
						accordion="my-accordion"
						role="tabpanel"
					>
						<b-card-body>
							<div class="form-group no-label">
								<b-form-select
									v-model="selected6"
									:options="TextPositions"
								></b-form-select>
							</div>
							<div class="form-group no-label">
								<input
									type="text"
									class="form-control"
									placeholder="Offset X"
								/>
							</div>
							<div class="form-group no-label">
								<input
									type="text"
									class="form-control"
									placeholder="Offset Y"
								/>
							</div>
						</b-card-body>
					</b-collapse>
				</b-card>
				<b-card no-body>
					<b-card-header header-tag="header" role="tab">
						<b-button block v-b-toggle.Normal variant="info"
							>Normal Measurement Value</b-button
						>
					</b-card-header>
					<b-collapse
						id="Normal"
						visible
						accordion="my-accordion"
						role="tabpanel"
					>
						<b-card-body>
							<div class="table">
								<div class="table__head">
									<div class="table__row">
										<div
											class="table__row--cell"
											data-width="8"
										>
											ID
										</div>
										<div
											class="table__row--cell"
											data-width="18"
										>
											Age
										</div>
										<div
											class="table__row--cell"
											data-width="18"
										>
											Sex
										</div>
										<div
											class="table__row--cell"
											data-width="20"
										>
											Race
										</div>
										<div
											class="table__row--cell"
											data-width=""
										>
											Value
										</div>
										<div
											class="table__row--cell"
											data-width=""
										>
											SD
										</div>
									</div>
								</div>

								<div class="table__body">
									<div class="table__row">
										<div
											class="table__row--cell"
											data-label=""
											data-width="8"
										>
											1
										</div>
										<div
											class="table__row--cell"
											data-label="Age"
											data-width="18"
										>
											<div
												class="
													input-group
													form-group
													no-label
												"
											>
												<input
													type="text"
													class="form-control"
													placeholder="21"
												/>
												<span>to</span>
												<input
													type="text"
													class="form-control"
													placeholder="54"
												/>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="Sex"
											data-width="18"
										>
											<div class="form-group no-label">
												<b-form-select
													v-model="selected7"
													:options="Sex"
												></b-form-select>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="Race"
											data-width="20"
										>
											<div class="form-group no-label">
												<b-form-select
													v-model="selected8"
													:options="Race"
												></b-form-select>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="Value"
											data-width=""
										>
											<div class="form-group no-label">
												<input
													type="text"
													class="form-control"
													placeholder="343"
												/>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="SD"
											data-width=""
										>
											<div class="form-group no-label">
												<input
													type="text"
													class="form-control"
													placeholder="343"
												/>
											</div>
										</div>
									</div>
									<div class="table__row">
										<div
											class="table__row--cell"
											data-label=""
											data-width="8"
										>
											2
										</div>
										<div
											class="table__row--cell"
											data-label="Age"
											data-width="18"
										>
											<div
												class="
													input-group
													form-group
													no-label
												"
											>
												<input
													type="text"
													class="form-control"
													placeholder="21"
												/>
												<span>to</span>
												<input
													type="text"
													class="form-control"
													placeholder="54"
												/>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="Sex"
											data-width="18"
										>
											<div class="form-group no-label">
												<b-form-select
													v-model="selected7"
													:options="Sex"
												></b-form-select>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="Race"
											data-width="20"
										>
											<div class="form-group no-label">
												<b-form-select
													v-model="selected8"
													:options="Race"
												></b-form-select>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="Value"
											data-width=""
										>
											<div class="form-group no-label">
												<input
													type="text"
													class="form-control"
													placeholder="343"
												/>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="SD"
											data-width=""
										>
											<div class="form-group no-label">
												<input
													type="text"
													class="form-control"
													placeholder="343"
												/>
											</div>
										</div>
									</div>
									<div class="table__row">
										<div
											class="table__row--cell"
											data-label=""
											data-width="8"
										>
											3
										</div>
										<div
											class="table__row--cell"
											data-label="Age"
											data-width="18"
										>
											<div
												class="
													input-group
													form-group
													no-label
												"
											>
												<input
													type="text"
													class="form-control"
													placeholder="21"
												/>
												<span>to</span>
												<input
													type="text"
													class="form-control"
													placeholder="54"
												/>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="Sex"
											data-width="18"
										>
											<div class="form-group no-label">
												<b-form-select
													v-model="selected7"
													:options="Sex"
												></b-form-select>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="Race"
											data-width="20"
										>
											<div class="form-group no-label">
												<b-form-select
													v-model="selected8"
													:options="Race"
												></b-form-select>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="Value"
											data-width=""
										>
											<div class="form-group no-label">
												<input
													type="text"
													class="form-control"
													placeholder="343"
												/>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="SD"
											data-width=""
										>
											<div class="form-group no-label">
												<input
													type="text"
													class="form-control"
													placeholder="343"
												/>
											</div>
										</div>
									</div>
									<div class="table__row">
										<div
											class="table__row--cell"
											data-label=""
											data-width="8"
										>
											4
										</div>
										<div
											class="table__row--cell"
											data-label="Age"
											data-width="18"
										>
											<div
												class="
													input-group
													form-group
													no-label
												"
											>
												<input
													type="text"
													class="form-control"
													placeholder="21"
												/>
												<span>to</span>
												<input
													type="text"
													class="form-control"
													placeholder="54"
												/>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="Sex"
											data-width="18"
										>
											<div class="form-group no-label">
												<b-form-select
													v-model="selected7"
													:options="Sex"
												></b-form-select>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="Race"
											data-width="20"
										>
											<div class="form-group no-label">
												<b-form-select
													v-model="selected8"
													:options="Race"
												></b-form-select>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="Value"
											data-width=""
										>
											<div class="form-group no-label">
												<input
													type="text"
													class="form-control"
													placeholder="343"
												/>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="SD"
											data-width=""
										>
											<div class="form-group no-label">
												<input
													type="text"
													class="form-control"
													placeholder="343"
												/>
											</div>
										</div>
									</div>
									<div class="table__row">
										<div
											class="table__row--cell"
											data-label=""
											data-width="8"
										>
											5
										</div>
										<div
											class="table__row--cell"
											data-label="Age"
											data-width="18"
										>
											<div
												class="
													input-group
													form-group
													no-label
												"
											>
												<input
													type="text"
													class="form-control"
													placeholder="21"
												/>
												<span>to</span>
												<input
													type="text"
													class="form-control"
													placeholder="54"
												/>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="Sex"
											data-width="18"
										>
											<div class="form-group no-label">
												<b-form-select
													v-model="selected7"
													:options="Sex"
												></b-form-select>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="Race"
											data-width="20"
										>
											<div class="form-group no-label">
												<b-form-select
													v-model="selected8"
													:options="Race"
												></b-form-select>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="Value"
											data-width=""
										>
											<div class="form-group no-label">
												<input
													type="text"
													class="form-control"
													placeholder="343"
												/>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="SD"
											data-width=""
										>
											<div class="form-group no-label">
												<input
													type="text"
													class="form-control"
													placeholder="343"
												/>
											</div>
										</div>
									</div>
									<div class="table__row">
										<div
											class="table__row--cell"
											data-label=""
											data-width="8"
										>
											6
										</div>
										<div
											class="table__row--cell"
											data-label="Age"
											data-width="18"
										>
											<div
												class="
													input-group
													form-group
													no-label
												"
											>
												<input
													type="text"
													class="form-control"
													placeholder="21"
												/>
												<span>to</span>
												<input
													type="text"
													class="form-control"
													placeholder="54"
												/>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="Sex"
											data-width="18"
										>
											<div class="form-group no-label">
												<b-form-select
													v-model="selected7"
													:options="Sex"
												></b-form-select>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="Race"
											data-width="20"
										>
											<div class="form-group no-label">
												<b-form-select
													v-model="selected8"
													:options="Race"
												></b-form-select>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="Value"
											data-width=""
										>
											<div class="form-group no-label">
												<input
													type="text"
													class="form-control"
													placeholder="343"
												/>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="SD"
											data-width=""
										>
											<div class="form-group no-label">
												<input
													type="text"
													class="form-control"
													placeholder="343"
												/>
											</div>
										</div>
									</div>
									<div class="table__row">
										<div
											class="table__row--cell"
											data-label=""
											data-width="8"
										>
											7
										</div>
										<div
											class="table__row--cell"
											data-label="Age"
											data-width="18"
										>
											<div
												class="
													input-group
													form-group
													no-label
												"
											>
												<input
													type="text"
													class="form-control"
													placeholder="21"
												/>
												<span>to</span>
												<input
													type="text"
													class="form-control"
													placeholder="54"
												/>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="Sex"
											data-width="18"
										>
											<div class="form-group no-label">
												<b-form-select
													v-model="selected7"
													:options="Sex"
												></b-form-select>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="Race"
											data-width="20"
										>
											<div class="form-group no-label">
												<b-form-select
													v-model="selected8"
													:options="Race"
												></b-form-select>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="Value"
											data-width=""
										>
											<div class="form-group no-label">
												<input
													type="text"
													class="form-control"
													placeholder="343"
												/>
											</div>
										</div>
										<div
											class="table__row--cell"
											data-label="SD"
											data-width=""
										>
											<div class="form-group no-label">
												<input
													type="text"
													class="form-control"
													placeholder="343"
												/>
											</div>
										</div>
									</div>
								</div>
							</div>
							<div class="rowAdjust">
								<span>Add Row</span>
								<span>Delete Row</span>
							</div>
						</b-card-body>
					</b-collapse>
				</b-card>
			</div>
		</div>
		<div class="creatNew__footer">
			<div class="button-row">
				<button type="button" class="btn btn-secondary pink">
					Create New Measurement
				</button>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	data() {
		return {
			measurementType: [
				{ value: null, text: 'Measurement Type' },
				{ value: 'a', text: 'Measurement Type2' },
				{ value: 'b', text: 'Measurement Type3' },
			],
			selected: null,
			AnalysisType: [
				{ value: null, text: 'Analysis Type' },
				{ value: 'a', text: 'Analysis Type2' },
				{ value: 'b', text: 'Analysis Type3' },
			],
			selected1: null,
			PointA: [
				{ value: null, text: 'PointA' },
				{ value: 'a', text: 'PointA(1)' },
				{ value: 'b', text: 'PointA(2)' },
			],
			selected2: null,
			PointB: [
				{ value: null, text: 'PointB' },
				{ value: 'a', text: 'PointB(1)' },
				{ value: 'b', text: 'PointB(2)' },
			],
			selected3: null,
			PointC: [
				{ value: null, text: 'PointC' },
				{ value: 'a', text: 'PointC(1)' },
				{ value: 'b', text: 'PointC(2)' },
			],
			selected4: null,
			PointD: [
				{ value: null, text: 'PointD' },
				{ value: 'a', text: 'PointD(1)' },
				{ value: 'b', text: 'PointD(2)' },
			],
			selected5: null,
			TextPositions: [
				{ value: null, text: 'Text Positions' },
				{ value: 'a', text: 'Text Positions(1)' },
				{ value: 'b', text: 'Text Positions(2)' },
			],
			selected6: null,
			Sex: [
				{ value: null, text: 'All' },
				{ value: 'a', text: 'Male' },
				{ value: 'b', text: 'Female' },
			],
			selected7: null,
			Sex1: [
				{ value: null, text: 'All' },
				{ value: 'a', text: 'Male' },
				{ value: 'b', text: 'Female' },
			],
			selected8: null,
			Sex2: [
				{ value: null, text: 'All' },
				{ value: 'a', text: 'Male' },
				{ value: 'b', text: 'Female' },
			],
			selected9: null,
			Sex3: [
				{ value: null, text: 'All' },
				{ value: 'a', text: 'Male' },
				{ value: 'b', text: 'Female' },
			],
			selected10: null,
			Sex4: [
				{ value: null, text: 'All' },
				{ value: 'a', text: 'Male' },
				{ value: 'b', text: 'Female' },
			],
			selected11: null,
			Sex5: [
				{ value: null, text: 'All' },
				{ value: 'a', text: 'Male' },
				{ value: 'b', text: 'Female' },
			],
			selected12: null,
			Sex6: [
				{ value: null, text: 'All' },
				{ value: 'a', text: 'Male' },
				{ value: 'b', text: 'Female' },
			],
			selected13: null,
			Race: [
				{ value: null, text: 'All' },
				{ value: 'a', text: '1' },
				{ value: 'b', text: '2' },
			],
			selected8: null,
			Race1: [
				{ value: null, text: 'All' },
				{ value: 'a', text: '1' },
				{ value: 'b', text: '2' },
			],
			selected14: null,
			Race2: [
				{ value: null, text: 'All' },
				{ value: 'a', text: '1' },
				{ value: 'b', text: '2' },
			],
			selected15: null,
			Race3: [
				{ value: null, text: 'All' },
				{ value: 'a', text: '1' },
				{ value: 'b', text: '2' },
			],
			selected16: null,
			Race4: [
				{ value: null, text: 'All' },
				{ value: 'a', text: '1' },
				{ value: 'b', text: '2' },
			],
			selected17: null,
			Race5: [
				{ value: null, text: 'All' },
				{ value: 'a', text: '1' },
				{ value: 'b', text: '2' },
			],
			selected18: null,
			Race6: [
				{ value: null, text: 'All' },
				{ value: 'a', text: '1' },
				{ value: 'b', text: '2' },
			],

			selected19: null,
		};
	},
};
</script>

<style lang="scss" scoped>
.creatNew {
	@media screen and (min-width: 992px) {
		border-radius: 12px;
		border: 2px solid #e9e9e9;
	}
	.accordion {
		padding: rem(20px);
		margin-top: 0;
		@media screen and (max-width: 991px) {
			padding-left: 0;
			padding-right: 0;
		}
		.card > {
			.card-header {
				.btn {
					border: 0;
					padding: 0;
					padding-left: 20px;
					height: auto;
					font-size: rem(16px);
					color: #6b6b6b;
					font-weight: normal;
					&:after {
						width: 15px;
						height: 13px;
						top: 50%;
						transform: translateY(-50%);
						left: 2px;
						right: auto;
					}
					&.not-collapsed {
						color: var(--textPrimary);
						&:after {
							background-image: url("data:image/svg+xml,%3Csvg width='14' height='8' viewBox='0 0 14 8' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M12.5858 0C13.4767 0 13.9229 1.07714 13.2929 1.70711L7.70711 7.29289C7.31658 7.68342 6.68342 7.68342 6.29289 7.29289L0.707105 1.70711C0.0771403 1.07714 0.523309 0 1.41421 0L12.5858 0Z' fill='%23F7C0B7'/%3E%3C/svg%3E%0A");
							height: 8px;
						}
					}
					&.collapsed {
						&:after {
							background-image: url("data:image/svg+xml,%3Csvg width='8' height='14' viewBox='0 0 8 14' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M-5.93854e-07 1.41421C-6.32796e-07 0.523308 1.07714 0.0771417 1.70711 0.707107L7.29289 6.29289C7.68342 6.68342 7.68342 7.31658 7.29289 7.70711L1.70711 13.2929C1.07714 13.9229 -6.65859e-08 13.4767 -1.05529e-07 12.5858L-5.93854e-07 1.41421Z' fill='%23E9E9E9'/%3E%3C/svg%3E%0A");
						}
					}
				}
			}
		}
		.card {
			padding:2px 0;
			.card-body {
				padding-top: rem(20px);
			}
		}
		.form-group {
			.control-label {
				font-weight: 400;
			}
			.custom-select {
				color: #8e8e8e;
				@media screen and (max-width: 991px) {
					min-width: 140px;
				}
			}
			&.b-input {
				.form-control {
					background: #fcfcfc;
					border-radius: 12px;
					border: 2px solid var(--textPrimary);
				}
			}
			&.no-label{
				.form-control{
					padding-top:12px;
				}
			}
		}
	}
	.custom-select {
		background-image: url("data:image/svg+xml,%3Csvg width='10' height='6' viewBox='0 0 10 6' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M8.58579 0C9.47669 0 9.92286 1.07714 9.29289 1.70711L5.70711 5.29289C5.31658 5.68342 4.68342 5.68342 4.29289 5.29289L0.707108 1.70711C0.0771428 1.07714 0.523309 0 1.41421 0H8.58579Z' fill='%238E8E8E'/%3E%3C/svg%3E%0A");
	}
	// &__body{
	// 	padding-bottom:rem(100px);
	// }
	&__footer {
		border-top: 2px solid #e9e9e9;
		padding: rem(20px);
		@media screen and (max-width: 991px) {
			padding-left: 0;
			padding-right: 0;
		}
		.button-row {
			margin: 0;
			@media screen and (max-width: 767px) {
				justify-content: center;
			}
			@media screen and (max-width: 575px) {
				.btn {
					width: 100%;
				}
			}
		}
	}
	.table {
		@media screen and (min-width: 992px) {
			border: 2px solid #e9e9e9;
			border-radius: 12px;
			overflow: hidden;
		}
		margin-bottom: rem(16px);
		&__body {
			border: 0;
		}
		&__head {
			border: 0;
			border-bottom: 1px solid #e9e9e9;
		}
		&__row {
			&:hover {
				background: transparent !important;
			}
			&--cell {
				padding-right: 15px;
				&:last-child {
					text-align: left !important;
				}
			}
		}
		.input-group {
			display: flex;
			align-items: center;
			flex-wrap: nowrap;
			span {
				font-size: rem(12px);
				color: #8e8e8e;
				font-weight: 400;
				margin: 0 5px !important;
				position: static;
				width: auto;
				height: auto;
			}
			.form-control {
				text-align: center;
			}
		}
		.form-group {
			margin: 0;
			.form-control {
				height: 42px;
				padding: 0 5px !important;
				border-radius: 7px !important;
				border: 2px solid transparent;
				font-weight: 400;
				@media screen and (max-width: 1500px) {
					font-size: rem(14px);
				}
				&:focus {
					border: 2px solid var(--textPrimary);
				}
			}
		}
		.custom-select {
			height: 40px;
			border-radius: 7px;
			padding: 8px;
			background-position: calc(100% - 11px) 55%;
			font-weight: 400;
			@media screen and (max-width: 1500px) {
				font-size: rem(14px);
			}
		}
	}
	.rowAdjust {
		display: flex;
		align-items: center;
		padding-left: rem(20px);
		span {
			color: var(--primary);
			font-weight: 500;
			font-size: rem(14px);
			cursor: pointer;
			&:hover {
				text-decoration: underline;
			}
			&:not(:last-child) {
				margin-right: rem(20px);
			}
		}
	}
}
</style>
