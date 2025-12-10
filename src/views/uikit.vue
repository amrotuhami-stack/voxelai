<template>
	<div class="uikit" style="padding-bottom: 50px">
		<div class="container">
			<h1 class="text-center">UIKIT</h1>
			<div class="button-row">
				<button class="btn btn-default">I am Default</button>
				<button class="btn btn-default full">
					I am Default Full width
				</button>
				<button class="btn btn-default">
					<span class="icon big">
						<svg-icon
							icon-id="cart-icon"
							icon-viewbox="0 0 24 24"
						></svg-icon>
					</span>
					Add to Cart
				</button>

				<button class="btn btn-default btn-small">
					<span class="icon big only-icon">
						<svg-icon
							icon-id="cart-icon"
							icon-viewbox="0 0 24 24"
						></svg-icon>
					</span>
				</button>
			</div>
			<div class="button-row">
				<button class="btn btn-primary">I am primary</button>
				<button class="btn btn-primary full">
					I am primary Full width
				</button>
				<button class="btn btn-primary">
					<span class="icon">
						<svg-icon
							icon-id="plus-icon"
							icon-viewbox="0 0 17 18"
						></svg-icon>
					</span>
					New Service
				</button>
			</div>
			<div class="button-row">
				<button class="btn btn-secondary">I am secondary</button>
				<button class="btn btn-secondary full">
					I am secondary Full width
				</button>
			</div>
			<button class="btn btn-secondary pink">I am secondary</button>

			<h2 class="mt-50 mb-30">Input Fields</h2>

			<!-- moveable label -->
			<div class="form-group">
				<input
					type="text"
					class="form-control"
					required=""
					name="name"
					placeholder="Name"
				/>
				<label class="control-label">Name</label>
			</div>
			<!-- moveable label -->
			<!-- date picker -->
			<div class="form-group">
				<b-form-datepicker
					placeholder="MM / YY"
					v-model="value"
				></b-form-datepicker>
			</div>

			<div class="search">
				<input
					type="text"
					class="form-control"
					placeholder="Search Everything"
				/>
			</div>
			<!-- static label -->
			<div class="form-group">
				<!-- <select name="" class="selectpicker" title="kuwait">
          <option value="">Kuwait</option>
          <option value="">Kuwait</option>
          <option value="">Kuwait</option>
        </select> -->
				<input
					type="text"
					class="form-control"
					required=""
					name="E-mail Address"
					placeholder="E-mail Address"
				/>
				<label class="control-label static-label">E-mail Address</label>
			</div>
			<!-- static label -->
			<div class="form-group">
				<b-form-select
					v-model="selected"
					:options="options"
				></b-form-select>
				<label class="control-label static-label">City</label>
			</div>

			<!-- h1 h2 h3 h4 h5  -->
			<div class="mt-50"></div>
			<h1>h1 .. 64px</h1>
			<h2>h2 .. 48</h2>
			<h3>h3 .. 32</h3>
			<h4>h4 .. 24</h4>
			<h5>h5 .. 20</h5>
			<h6>h6 .. 16</h6>

			<!-- h1 h2 h3 h4 h5  -->

			<a href="#" class="see-more">See More Details</a>

			<br />
			<div class="inline-btns-wrapper">
				<div class="inline-btns">
					<a href="#" class="btn btn-primary">Next</a>
					<a href="#">Skip for now</a>
				</div>
				<a href="#" class="btn btn-secondary">Back</a>
			</div>
		</div>
	</div>
</template>

//
<script>
// const menu = {
//     label: 'All',
// }

// export default {
//     data() {
//         return {
//             menu_options: [
//                 { code: 'all', label: 'All' },
//                 { code: 'a', label: 'This is First option' },
//                 { code: 'b', label: 'Selected Option' },
//                 { code: 'c', label: 'Third Option' },
//             ],

//             selected_menu: menu,
//         }
//     },
// }
//
</script>

<script>
export default {
	data() {
		return {
			value: '',
			selected: null,
			options: [
				{ value: null, text: 'Please select an option' },
				{ value: 'a', text: 'This is First option' },
				{ value: 'b', text: 'Selected Option' },
				{
					value: { C: '3PO' },
					text: 'This is an option with object value',
				},
				{ value: 'd', text: 'This one is disabled', disabled: true },
			],
		};
	},
};
</script>
