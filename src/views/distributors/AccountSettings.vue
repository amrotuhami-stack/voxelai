<template>
	<div class="accountSettings">
		<div class="container">
			<h1 class="main-title mb-10">Account Settings</h1>
			<p>Change your profile and account settings</p>
			<div class="contentBox">
				<h2>Personal Information</h2>
				<div class="accountSettings__picture">
					<div class="accountSettings__picture--frame"></div>
					<ul class="accountSettings__picture--actions">
						<li>
							<input type="file" name="file" @change="upload" />
							<span>Change Photo</span>
						</li>
						<li>
							<a
								href="javascript:void(0);"
								@click="reset"
								class="remove-photo"
							>
								Reset
							</a>
						</li>
					</ul>
				</div>
				<form>
					<div class="row">
						<div class="col-md-6">
							<div class="form-group">
								<input
									type="text"
									class="form-control"
									required=""
									value="Mohamed"
									name="First Name"
									placeholder="First Name"
								/>
								<label class="control-label">
									First name
								</label>
							</div>
						</div>
						<div class="col-md-6">
							<div class="form-group">
								<input
									type="text"
									class="form-control"
									required=""
									value="Mohsen"
									name="Last name"
									placeholder="Last name"
								/>
								<label class="control-label"> Last name </label>
							</div>
						</div>
						<div class="col-md-6">
							<div class="form-group">
								<input
									type="text"
									class="form-control"
									required=""
									value="mohsen"
									name="Nickname"
									placeholder="Nickname"
								/>
								<label class="control-label"> Nickname </label>
							</div>
						</div>
						<div class="col-md-6">
							<div class="form-group">
								<input
									type="text"
									class="form-control"
									required=""
									name="Speciality"
									placeholder="Speciality"
								/>
								<label class="control-label">
									Speciality
								</label>
							</div>
						</div>
						<div class="col-md-6">
							<div class="form-group">
								<input
									type="text"
									class="form-control"
									required=""
									name="Email address"
									placeholder="Email address"
								/>
								<label class="control-label">
									Email address
								</label>
							</div>
						</div>
						<div class="col-md-6">
							<div class="form-group">
								<input
									type="text"
									class="form-control"
									required=""
									name="Phone Number"
									placeholder="Phone Number"
								/>
								<label class="control-label">
									Phone number
								</label>
							</div>
						</div>
					</div>
				</form>
				<a
					href="javascript:void(0);"
					class="viewMore"
					v-b-modal="'my-modal'"
				>
					Change Password
					<font-awesome-icon :icon="['fa', 'angle-right']" />
				</a>
				<b-modal ref="my-modal" id="my-modal" centered>
					<div class="modal-title">Change Password</div>
					<p>Voxel is created for every dental practitioner.</p>
					<form>
						<div class="form-group">
							<input
								type="password"
								id="current"
								class="form-control"
								required=""
								name="Current password"
								placeholder="First Current password"
							/>
							<label class="control-label"
								>Current password</label
							>
							<span
								id="currentSpan"
								@click="showPassword('current', 'currentSpan')"
							>
								<svg-icon
									class="show"
									icon-id="eye-icon"
									icon-viewbox="0 0 24 24"
								>
								</svg-icon>
								<svg-icon
									class="hide d-none"
									icon-id="closeEye-icon"
									icon-viewbox="0 0 24 24"
								>
								</svg-icon>
							</span>
						</div>
						<div class="form-group">
							<input
								type="password"
								id="news"
								class="form-control"
								required=""
								name="New password"
								placeholder="First New password"
							/>
							<label class="control-label">New password</label>
							<span
								id="newSpan"
								@click="showPassword('news', 'newSpan')"
							>
								<svg-icon
									class="show"
									icon-id="eye-icon"
									icon-viewbox="0 0 24 24"
								>
								</svg-icon>
								<svg-icon
									class="hide d-none"
									icon-id="closeEye-icon"
									icon-viewbox="0 0 24 24"
								>
								</svg-icon>
							</span>
						</div>
						<div class="form-group">
							<input
								type="password"
								id="confirm"
								class="form-control"
								required=""
								name="confirm password"
								placeholder="confirm password"
							/>
							<label class="control-label"
								>confirm password</label
							>
							<span
								id="confirmSpan"
								@click="showPassword('confirm', 'confirmSpan')"
							>
								<svg-icon
									class="show"
									icon-id="eye-icon"
									icon-viewbox="0 0 24 24"
								>
								</svg-icon>
								<svg-icon
									class="hide d-none"
									icon-id="closeEye-icon"
									icon-viewbox="0 0 24 24"
								>
								</svg-icon>
							</span>
						</div>
						<div class="inline-buttons">
							<button type="button" class="btn btn-primary">
								Update
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
			<div class="contentBox">
				<h2>Billing and Shipping Address</h2>
				<form>
					<div class="row">
						<div class="col-md-6">
							<div class="form-group">
								<input
									type="text"
									class="form-control"
									required=""
									value="Mohamed"
									name="First Name"
									placeholder="First Name"
								/>
								<label class="control-label">
									First name
								</label>
							</div>
						</div>
						<div class="col-md-6">
							<div class="form-group">
								<input
									type="text"
									class="form-control"
									required=""
									value="Mohsen"
									name="Last name"
									placeholder="Last name"
								/>
								<label class="control-label"> Last name </label>
							</div>
						</div>
						<div class="col-md-6">
							<div class="form-group">
								<input
									type="text"
									class="form-control"
									required=""
									name="Email address"
									placeholder="Email address"
								/>
								<label class="control-label">
									Email address
								</label>
							</div>
						</div>
						<div class="col-md-6">
							<div class="form-group">
								<input
									type="text"
									class="form-control"
									required=""
									name="Phone Number"
									placeholder="Phone Number"
								/>
								<label class="control-label">
									Phone number
								</label>
							</div>
						</div>
						<div class="col-md-6">
							<div class="form-group">
								<b-form-select
									v-model="selected"
									:options="country"
								></b-form-select>
								<label class="control-label static-label"
									>Country</label
								>
							</div>
						</div>
						<div class="col-md-6">
							<div class="form-group">
								<b-form-select
									v-model="selected2"
									:options="governorate"
								></b-form-select>
								<label class="control-label static-label"
									>Governorate</label
								>
							</div>
						</div>
						<div class="col-md-6">
							<div class="form-group">
								<b-form-select
									v-model="selected3"
									:options="city"
								></b-form-select>
								<label class="control-label static-label"
									>City</label
								>
							</div>
						</div>
						<div class="col-md-6">
							<div class="form-group">
								<b-form-select
									v-model="selected4"
									:options="area"
								></b-form-select>
								<label class="control-label static-label"
									>Area</label
								>
							</div>
						</div>
						<div class="col-md-9">
							<div class="form-group">
								<input
									type="text"
									class="form-control"
									required=""
									value="7 Sarhan st. Monib, Giza, Egpyt"
									name="Address"
									placeholder="Address"
								/>
								<label class="control-label">Address</label>
							</div>
						</div>
						<div class="col-md-3">
							<div class="form-group">
								<input
									type="text"
									class="form-control"
									required=""
									value="124523"
									name="Zip Code"
									placeholder="Zip Code"
								/>
								<label class="control-label">Zip Code</label>
							</div>
						</div>
					</div>
					<div class="checkbox">
						<label>
							<input type="checkbox" name="radio" />
							<span>Different shipping address</span>
						</label>
					</div>
				</form>
			</div>
			<div class="inline-btns-wrapper stack-on-sm">
				<a href="#" class="btn btn-primary"> Save Changes </a>
				<a href="#" class="btn btn-secondary grey"> Cancel </a>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	data() {
		return {
			value: '',
			selected: null,
			country: [
				{ value: null, text: 'Egypt' },
				{ value: 'a', text: 'This is First option' },
				{ value: 'b', text: 'Selected Option' },
			],
			selected2: null,
			governorate: [
				{ value: null, text: 'Giza' },
				{ value: 'a', text: 'This is First option' },
				{ value: 'b', text: 'Selected Option' },
			],
			selected3: null,
			city: [
				{ value: null, text: 'El Omraniya' },
				{ value: 'a', text: 'This is First option' },
				{ value: 'b', text: 'Selected Option' },
			],
			selected4: null,
			area: [
				{ value: null, text: 'Al Omraneyah Al Gharbeyah' },
				{ value: 'a', text: 'This is First option' },
				{ value: 'b', text: 'Selected Option' },
			],
		};
	},
	methods: {
		hideModal() {
			this.$refs['my-modal'].hide();
		},
		showPassword: function (id, spanId) {
			let input = document.querySelector(`#${id}`);
			let eye = document.querySelector(`#${spanId}`);
			let showicon = eye.querySelector('.show');
			let hideicon = eye.querySelector('.hide');
			if (input.type === 'password') {
				showicon.classList.add('d-none');
				hideicon.classList.remove('d-none');
				return (input.type = 'text');
			} else {
				showicon.classList.remove('d-none');
				hideicon.classList.add('d-none');
				return (input.type = 'password');
			}
		},

		upload: function (e) {
			let imageWraper = document.querySelector(
				'.accountSettings__picture--frame'
			);
			let image = document.querySelector(
				'.accountSettings__picture--frame img'
			);
			if (imageWraper.querySelector('img')) {
				image.src = URL.createObjectURL(e.target.files[0]);
			} else {
				let img = document.createElement('img');
				img.src = URL.createObjectURL(e.target.files[0]);
				imageWraper.appendChild(img);
			}
		},
		reset: function () {
			let imageWraper = document.querySelector(
				'.accountSettings__picture--frame'
			);
			let input = document.querySelector('input[type=file]');
			if (imageWraper.hasChildNodes()) {
				imageWraper.removeChild(imageWraper.childNodes[0]);
				input.value = null;
			}
		},
	},
};
</script>

<style lang="scss" scoped>
.accountSettings {
	.contentBox {
		margin-bottom: rem(24px);
		@media screen and (max-width: 991px) {
			border: 0;
			border-radius: 0;
			padding: 0;
			border-bottom: 1px solid #e9e9e9;
			padding-bottom: 20px;
			margin-bottom: 20px;
		}
	}
	p {
		margin-bottom: rem(25px);
		font-weight: 400;
	}
	h2 {
		font-size: rem(16px);
		font-weight: 400;
		color: var(--default);
		margin-bottom: rem(26px);
	}
	&__picture {
		display: flex;
		align-items: center;
		margin-bottom: rem(24px);
		&--frame {
			background: url('../../assets/images/icons/Avatar.png');
			position: relative;
			width: 100px;
			height: 100px;
			display: flex;
			align-items: center;
			justify-content: center;
			border-radius: 100px;
			overflow: hidden;
			::v-deep img {
				width: 100%;
				height: 100%;
				object-fit: cover;
				object-position: center;
			}
		}
		&--actions {
			display: flex;
			margin-left: rem(24px);
			list-style: none;
			li {
				position: relative;
				input {
					position: absolute;
					cursor: pointer;
				}
				span {
					color: var(--secondary);
					font-weight: 500;
					font-size: rem(16px);
				}
				&:first-child {
					margin-right: rem(16px);
				}
				a {
					color: var(--textSecondary);
				}
			}
		}
	}
	a.viewMore {
		svg {
			margin-left: rem(14px);
		}
		&:hover svg {
			transform: translate(7px, 0);
		}
	}
	.checkbox {
		padding-top: unset;
		span {
			padding-left: rem(32px) !important;
			padding-bottom: unset !important;
		}
	}
	.inline-btns-wrapper {
		margin-top: unset;
		.btn {
			&.btn-primary,
			&.btn-secondary {
				padding-left: rem(48px);
				padding-right: rem(48px);
			}
		}
		@media screen and (max-width: 767px) and (min-width: 416px) {
			flex-direction: revert;
			.btn {
				&:not(:last-child) {
					margin: 0;
				}
			}
		}
		@media screen and (max-width: 415px) {
			.btn {
				width: 100%;
			}
		}
	}
}
</style>
