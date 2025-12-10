<template>
	<div>
		<div class="card__body">
			<form>
				<div class="form-group">
					<input
						type="text"
						class="form-control"
						required=""
						name="Card Number"
						placeholder="Card Number"
					/>
					<label class="control-label">Card Number</label>
				</div>
				<div class="row">
					<div class="col-md-6">
						<div class="form-group">
							<input
								type="text"
								class="form-control"
								required=""
								name="MM / YY"
								placeholder="MM / YY"
							/>
							<label class="control-label">MM / YY</label>
						</div>
					</div>
					<div class="col-md-6">
						<div class="form-group">
							<div class="form-group">
								<input
									type="text"
									class="form-control"
									required=""
									name="CVV"
									placeholder="CVV"
								/>
								<label class="control-label">CVV</label>
							</div>
						</div>
					</div>
					<div class="col-md-12">
						<div class="form-group">
							<input
								type="text"
								class="form-control"
								required=""
								name="Cardholder Name"
								placeholder="Cardholder Name"
							/>
							<label class="control-label">Cardholder Name</label>
						</div>
					</div>
				</div>
				<div class="checkbox pt-0">
					<label>
						<input type="checkbox" name="radio" />
						<span class="pb-0">Remember this card</span>
					</label>
				</div>
			</form>
		</div>
	</div>
</template>

<script>
export default {};
</script>

<style lang="scss" scoped></style>
