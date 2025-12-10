<template>
  <div class="contentBox" v-if="differentShippingAddress">
    <h2>Shipping Address</h2>
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
              v-model="shippingAddressForm.first_name"
              @input="() => onShippingFormChanged('first_name')"
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
              v-model="shippingAddressForm.last_name"
              @input="() => onShippingFormChanged('last_name')"
            />
            <label class="control-label">Last Name</label>
            <div v-if="error('last_name')">{{ error('last_name')['messege'] }}</div>
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
              v-model="shippingAddressForm.email"
              @input="() => onShippingFormChanged('email_address')"
            />
            <label class="control-label">E-mail Address</label>
            <div v-if="error('email_address')">{{ error('email_address')['messege'] }}</div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group">
            <vue-tel-input v-model="shippingAddressForm.phone" :styleClasses="error('phone_number') ? 'tel-form-control error' : 'tel-form-control'" :validCharactersOnly="true" @country-changed="onSelect" @input="input"></vue-tel-input>
            <label class="control-label" :class="error('phone_number')  ? 'error label' : ''"> Phone number </label>
            <div v-if="error('phone_number')" class="error messege">{{ error('phone_number')['messege'] }}</div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group no-label" :class="error('country') ? 'error' : ''">
            <b-form-select
              v-model="shippingAddressForm.country"
              :options="[{ value: null, text: 'Country' }].concat(countries)"
              placeholder="Country"
              @input="() => onShippingFormChanged('country')"
            ></b-form-select>
            <div v-if="error('country')">{{ error('country')['messege'] }}</div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group" :class="error('city') ? 'error' : ''">
            <input
              type="text"
              class="form-control"
              required=""
              name="City"
              placeholder="City"
              v-model="shippingAddressForm.city"
              @input="() => onShippingFormChanged('city')"
            />
            <label class="control-label">City</label>
            <div v-if="error('city')">{{ error('city')['messege'] }}</div>
          </div>
        </div>
        <div class="col-xl-9 col-md-8">
          <div class="form-group" :class="error('address') ? 'error' : ''">
            <input
              type="text"
              class="form-control"
              required=""
              name="Address"
              placeholder="Address"
              v-model="shippingAddressForm.line1"
              @input="() => onShippingFormChanged('address')"
            />
            <label class="control-label">Address</label>
            <div v-if="error('address')">{{ error('address')['messege'] }}</div>
          </div>
        </div>
        <div class="col-xl-3 col-md-4">
          <div class="form-group" :class="error('zip_code') ? 'error' : ''">
            <input
              type="text"
              class="form-control"
              required=""
              name="Zip Code"
              placeholder="Zip Code"
              v-model="shippingAddressForm.zip"
              @input="() => onShippingFormChanged()"
            />
            <label class="control-label">Zip Code</label>
            <div v-if="error('zip_code')">{{ error('zip_code')['messege'] }}</div>
          </div>
        </div>
        <div class="error">
					<div v-if="shippingFormErrors.length > 0">
    					<p class="mb-2 mt-2">Please correct the following shipping address error(s):</p>
    					<ul>
      						<li v-for="(error,index) in shippingFormErrors" :key="index">{{"[ X ] " + error['messege'] }}</li>
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

// [*] Import form validator
import AppValidator from "@/common/validator"

import { VueTelInput } from 'vue-tel-input'
export default {
  components: { VueTelInput },
  props: {
    countries: Array,
    validation: Function,
  },
  data() {
    return {
      differentShippingAddress: null,
      
      phoneNumberCountryPicked: "",
      shippingAddressForm: {
        "first_name": null,
        "last_name": null,
        "email": null,
        "phone": null,
        "country": null,
        "city": null,
        "line1": null,
        "zip": null,
      },
      shippingFormErrors: [],
    };
  },
  computed: {
    ...mapGetters(["userProfile", "invalidPhoneNumber"]),
  },
  mounted() {
    this.differentShippingAddress = this.userProfile.differentShippingAddress;
    this.shippingAddressForm = {
      "first_name": this.userProfile.shipping_first_name,
      "last_name": this.userProfile.shipping_last_name,
      "email": this.userProfile.shipping_email,
      "phone": this.userProfile.shipping_phone_number,
      "country": this.userProfile.shipping_country,
      "city": this.userProfile.shipping_city,
      "line1": this.userProfile.shipping_address,
      "zip": this.userProfile.shipping_zip,
    };
  },
  watch: {
    differentShippingAddress() {
      this.validateShippingForm()
    },
    userProfile() {
      this.differentShippingAddress = this.userProfile.differentShippingAddress;
      this.shippingAddressForm = {
        "first_name": this.userProfile.shipping_first_name,
        "last_name": this.userProfile.shipping_last_name,
        "email": this.userProfile.shipping_email,
        "phone": this.userProfile.shipping_phone_number,
        "country": this.userProfile.shipping_country,
        "city": this.userProfile.shipping_city,
        "line1": this.userProfile.shipping_address,
        "zip": this.userProfile.shipping_zip,
      };
    },
    invalidPhoneNumber() {
      this.validateShippingForm('phone_number');
    },
  },
  methods: {
    onSelect: function(country) {
      this.phoneNumberCountryPicked = country.iso2
      this.shippingAddressForm.phone = "+" + country.dialCode
      this.validateShippingForm('phone_number');
    },
    input(value) {
      this.shippingAddressForm =  {...this.shippingAddressForm, phone: value}
      this.onShippingFormChanged('phone_number');
    },
    onShippingFormChanged(value) {
      let params = {
        "shipping_first_name": this.shippingAddressForm.first_name,
				"shipping_last_name": this.shippingAddressForm.last_name,
				"shipping_email": this.shippingAddressForm.email,
				"shipping_phone_number": this.shippingAddressForm.phone,
				"shipping_country": this.shippingAddressForm.country,
				"shipping_city": this.shippingAddressForm.city,
				"shipping_address": this.shippingAddressForm.line1,
				"shipping_zip": this.shippingAddressForm.zip,
			};
      if(
        params.shipping_first_name != this.userProfile.shipping_first_name ||
        params.shipping_last_name != this.userProfile.shipping_last_name ||
        params.shipping_email != this.userProfile.shipping_email ||
        params.shipping_phone_number.replaceAll(' ','') != this.userProfile.shipping_phone_number ||
        params.shipping_country != this.userProfile.shipping_country ||
        params.shipping_city != this.userProfile.shipping_city ||
        params.shipping_address != this.userProfile.shipping_address ||
        params.shipping_zip != this.userProfile.shipping_zip
      ) {
        UsersHelper.updateUserProfile(params);
        this.validateShippingForm(value);
      }
    },
    validateShippingForm(inputKey) {
			let form = {
				firstName: this.shippingAddressForm.first_name,
				lastName: this.shippingAddressForm.last_name,
				emailAddress: this.shippingAddressForm.email,
				phoneNumber: this.shippingAddressForm.phone,
				country: this.shippingAddressForm.country,
				city: this.shippingAddressForm.city,
				address: this.shippingAddressForm.line1,
				zipCode: this.shippingAddressForm.zip,
				countryCode: this.phoneNumberCountryPicked,
        invalidPhoneNumber: this.invalidPhoneNumber
			};
			let inputValidationResults = AppValidator.billingAndShippingAddress(form, inputKey);
			let formValidationResults = AppValidator.billingAndShippingAddress(form);
			this.shippingFormErrors = [...inputValidationResults]
      if(this.differentShippingAddress) {
        this.validation(formValidationResults.length > 0 ? false : true)
      }
		},
    error(key) {
      return this.shippingFormErrors.find((item) => item.key == key);
    },
  }
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