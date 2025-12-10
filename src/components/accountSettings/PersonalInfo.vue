<template>
  <div class="contentBox" style="overflow: visible;">
    <h2>Personal Information</h2>
    <div class="accountSettings__picture">
      <div
        class="accountSettings__picture--frame"
        :style="{
          backgroundImage: `url(${form.photo})`,
          backgroundSize: '100px',
        }"
      >
        <img v-if="!form.photo" src="@/assets/images/icons/Avatar.png" alt="" />
      </div>
      <ul class="accountSettings__picture--actions">
        <li>
          <input type="file" name="user_avatar" @change="upload"/>
          <span>Change Photo</span>
        </li>
        <li>
          <a href="javascript:void(0);" class="remove-photo" @click="reset"> Reset </a>
        </li>
      </ul>
    </div>
    <form>
      <div class="row">
        <div class="col-md-6">
          <div class="form-group" :class="error('first_name') ? 'error' : ''">
            <input
              type="text"
              class="form-control"
              required=""
              name="first_name"
              placeholder="First Name"
              v-model="form.first_name"
              @input="validateForm"
            />
            <label class="control-label">First Name</label>
            <div v-if="error('first_name')">{{ error('first_name')['messege'] }}</div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group" :class="error('last_name') ? 'error' : ''">
            <input
              type="text"
              class="form-control"
              required=""
              name="last_name"
              placeholder="Last Name"
              v-model="form.last_name"
              @input="validateForm"
            />
            <label class="control-label">Last Name</label>
            <div v-if="error('last_name')">{{ error('last_name')['messege'] }}</div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group" :class="error('nickname') ? 'error' : ''">
            <input
              type="text"
              class="form-control"
              required=""
              name="nickname"
              placeholder="Nick Name"
              v-model="form.nickname"
              @input="validateForm"
            />
            <label class="control-label">Nick Name</label>
            <div v-if="error('nickname')">{{ error('nickname')['messege'] }}</div>
          </div>
        </div>
        <div class="col-md-6">
          
          <div class="form-group">
            <vue-tel-input 
              v-model="form.phone" 
              :styleClasses="error('phone_number') ? 'tel-form-control error' : 'tel-form-control'" 
              :validCharactersOnly="true" 
              @country-changed="onSelect" @input="input"></vue-tel-input>
            <label class="control-label" :class="error('phone_number') ? 'error label' : ''"> Phone number </label>
            <div v-if="error('phone_number')" class="error messege">{{ error('phone_number')['messege'] }}</div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group" :class="error('Speciality') ? 'error' : ''">
            <input
              type="text"
              class="form-control"
              required=""
              name="Speciality"
              placeholder="Speciality"
              v-model="form.speciality"
              @input="validateForm"
            />
            <label class="control-label">Speciality</label>
            <div v-if="error('Speciality')">{{ error('Speciality')['messege'] }}</div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group" :class="error('email_address') ? 'error' : ''">
            <input
              type="text"
              class="form-control"
              required=""
              name="E-mail Address"
              placeholder="E-mail Address"
              v-model="form.email"
              @input="validateForm"
            />
            <label class="control-label">E-mail Address</label>
            <div v-if="error('email_address')">{{ error('email_address')['messege'] }}</div>
          </div>
        </div>
        <div class="error">
					<div v-if="formErrors.length > 0">
    					<p class="mb-2 mt-2">Please correct the following error(s):</p>
    					<ul>
      						<li v-for="(error,index) in formErrors" :key="index">{{"[ X ] " + error['messege'] }}</li>
    					</ul>
  					</div>
				</div>
      </div>
    </form>
  </div>
</template>

<script>
// [*] Vuex State Getter And Action Helper
import { mapGetters } from "vuex";
import { UsersHelper } from '@/common/crud-helpers/users';
import AppValidator from "@/common/validator"
import { VueTelInput } from 'vue-tel-input'

export default {
  props: {
    validation: Function,
  },
  components: {
    VueTelInput
  },
  data() {
    return {
      username: null,
      formErrors: [],
      phoneNumberCountryPicked: "",
      form: {
        "first_name": null,
        "last_name": null,
        "nickname": null,
        "speciality": null,
        "email": null,
        "phone_number": null,
		    "photo": null,
      },
    };
  },
  computed: {
    ...mapGetters(["userProfile"]),
  },
  watch: {
    userProfile() {
      this.username = this.userProfile.username;
      this.form = {
        "photo": this.userProfile.photo,
        "first_name": this.userProfile.first_name,
        "last_name": this.userProfile.last_name,
        "nickname": this.userProfile.nick_name,
        "speciality": this.userProfile.speciality,
        "email": this.userProfile.email,
        "phone_number": this.userProfile.phone_number,
      };
    },
  },
  methods: {
    onSelect: function(country) {
      this.phoneNumberCountryPicked = country.iso2
      this.form.phone_number = "+" + country.dialCode
      this.validateForm()
      this.updateUserProfile()
    },
    input(value) {
      this.form =  {...this.form, phone_number: value}
      this.updateUserProfile()
    },
    updateUserProfile: function () {
      let params = {
        "username": this.username,
		    "name":  this.form.first_name + " " + this.form.last_name,
		    "first_name": this.form.first_name,
		    "last_name": this.form.last_name,
		    "nick_name": this.form.nickname,
		    "speciality": this.form.speciality,
		    "phone_number": this.form.phone_number,
		    "email": this.form.email,
      };
      if(
        params.username != this.userProfile.username ||
        params.first_name != this.userProfile.first_name ||
        params.last_name != this.userProfile.last_name ||
        params.nick_name != this.userProfile.nick_name ||
        params.speciality != this.userProfile.speciality ||
        params.email != this.userProfile.email ||
        params.phone_number.replaceAll(' ','') != this.userProfile.phone_number
      ) UsersHelper.updateUserProfile(params)
    },
    upload: function (e) {
      UsersHelper.updateUserProfileImage(e.target.files[0])
    },
    reset: function () {
      UsersHelper.resetUserProfileImage()
    },
    validateForm() {
			let error = AppValidator.personalInfo({
				firstName: this.form.first_name,
				lastName: this.form.last_name,
				nickname: this.form.nickname,
				speciality: this.form.speciality,
				emailAddress: this.form.email,
				phoneNumber: this.form.phone_number,
				countryCode: this.phoneNumberCountryPicked,
			})
			this.formErrors = [...error]
      this.validation(this.formErrors.length > 0 ? false : true)
      if(this.formErrors.length == 0) this.updateUserProfile()
		},
    
    error(key) {
      return this.formErrors.find((item) => item.key == key);
    },
    
  },
};
</script>


<style lang="scss">
.tel-form-control {
	position: relative;
	height: 64px;
	font-size: rem(16px);
	background-color: #f5f5f5;
	outline: none;
	border: 0px;
	border-radius: 12px;
  box-shadow: none;
	transition: all 0.2s;
	touch-action: manipulation;
	padding: 12px 25px;
	font-weight: 500;
	padding-top: rem(30px);

  &.error {
    border-radius: 12px;
		border:2px solid #cc0033;
		background-color: #fce4e4;
  }

	@media screen and (max-width: 767px) {
		font-size: rem(14px);
	}

  input {
    background-color: #f5f5f5;
  }

  div {
    z-index: 20;
  }

	&:focus {
		outline: none;
		box-shadow: none;
		color: var(--textPrimary);
		background-color: #fcfcfc;
		border: 2px solid #171716;
	}
}

.error {
  &.messege {
		padding: rem(12px);
		font-size: rem(16px);
		color: #cc0033;
	}
	&.label {
		color: #B00020;
	}
  color: #cc0033;
  p {
		margin: rem(0px);
	}
  ul {
		list-style-type: none;
    margin-bottom: rem(15px);
		li {
			padding-left: rem(10px);
			margin-bottom: rem(10px);
		}
	}
}

</style>


<!-- <a
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
				</b-modal> -->