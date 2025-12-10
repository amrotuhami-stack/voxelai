<template>
  <div class="contentBox">
    <h2>Billing Address</h2>
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
              v-model="billingAddressForm.first_name"
              @input="() => onBillingFormChanged('first_name')"
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
              v-model="billingAddressForm.last_name"
              @input="() => onBillingFormChanged('last_name')"
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
              v-model="billingAddressForm.email"
              @input="() => onBillingFormChanged('email_address')"
            />
            <label class="control-label">E-mail Address</label>
            <div v-if="error('email_address')">{{ error('email_address')['messege'] }}</div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group">
            <vue-tel-input 
              v-model="billingAddressForm.phone" 
              :styleClasses="error('phone_number') ? 'tel-form-control error' : 'tel-form-control'" 
              :validCharactersOnly="true" 
              @country-changed="onSelect" @input="input"></vue-tel-input>
            <label class="control-label" :class="error('phone_number') ? 'error label' : ''"> Phone number </label>
            <div v-if="error('phone_number')" class="error messege">{{ error('phone_number')['messege'] }}</div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group no-label" :class="error('country') ? 'error' : ''">
            <b-form-select
              v-model="billingAddressForm.country"
              :options="[{ value: null, text: 'Country' }].concat(countries)"
              placeholder="Country"
              @input="() => onBillingFormChanged('country')"
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
              v-model="billingAddressForm.city"
              @input="() => onBillingFormChanged('city')"
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
              v-model="billingAddressForm.line1"
              @input="() => onBillingFormChanged('address')"
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
              v-model="billingAddressForm.zip"
              @input="() => onBillingFormChanged()"
            />
            <label class="control-label">Zip Code</label>
            <div v-if="error('zip_code')">{{ error('zip_code')['messege'] }}</div>
          </div>
        </div>
      </div>
      <div class="checkbox" v-if="billingFormErrors.length == 0">
        <label>
          <input
            type="checkbox"
            name="radio"
            v-model="differentShippingAddress"
          />
          <span>Different shipping address</span>
        </label>
      </div>

      <div class="error">
					<div v-if="billingFormErrors.length > 0">
    					<p class="mb-2 mt-2">Please correct the following billing address error(s):</p>
    					<ul>
      						<li v-for="(error,index) in billingFormErrors" :key="index">{{"[ X ] " + error['messege'] }}</li>
    					</ul>
  					</div>
				</div>
    </form>
  </div>
</template>

<script>
// [*] Vuex State Getter And Action Helper
import { mapGetters } from "vuex";
import { UsersHelper } from '@/common/crud-helpers/users';
import { VueTelInput } from 'vue-tel-input'
// [*] Import form validator
import AppValidator from "@/common/validator"

export default {
  props: {
    countries: Array,
    validation: Function,
  },
  components: {
    VueTelInput,
  },
  data() {
    return {
      differentShippingAddress: null,
      phoneNumberCountryPicked: "",
      
      billingAddressForm: {
				"first_name": null,
				"last_name": null,
				"email": null,
				"phone": null,
				"country": null,
				"city": null,
				"line1": null,
				"zip": null
			},
      billingFormErrors: [],
    };
  },
  computed: {
    ...mapGetters(["userProfile", "invalidPhoneNumber"]),
  },
  mounted() {
    this.differentShippingAddress = this.userProfile.differentShippingAddress;
		this.billingAddressForm = {
			"first_name": this.userProfile.billing_first_name,
			"last_name": this.userProfile.billing_last_name,
			"email": this.userProfile.billing_email,
			"phone": this.userProfile.billing_phone_number,
			"country": this.userProfile.billing_country,
			"city": this.userProfile.billing_city,
			"line1": this.userProfile.billing_address,
			"zip": this.userProfile.billing_zip,
		};
  },
  watch: {
    differentShippingAddress() {
        if(this.differentShippingAddress != this.userProfile.differentShippingAddress) {
          this.onBillingFormChanged()
        }
    },
    userProfile() {
      this.differentShippingAddress = this.userProfile.differentShippingAddress;
			this.billingAddressForm = {
				"first_name": this.userProfile.billing_first_name,
				"last_name": this.userProfile.billing_last_name,
				"email": this.userProfile.billing_email,
				"phone": this.userProfile.billing_phone_number,
				"country": this.userProfile.billing_country,
				"city": this.userProfile.billing_city,
				"line1": this.userProfile.billing_address,
				"zip": this.userProfile.billing_zip,
			};
    }, 
    invalidPhoneNumber() {
      this.validateBillingForm('phone_number');
    },
  },
  methods: {
    onSelect: function(country) {
      this.phoneNumberCountryPicked = country.iso2
      this.billingAddressForm.phone = "+" + country.dialCode
      this.validateBillingForm('phone_number');
    },
    input(value) {
      this.billingAddressForm =  {...this.billingAddressForm, phone: value};
      this.onBillingFormChanged('phone_number');
    },
    onBillingFormChanged(value) {
      let params = {
        "differentShippingAddress": this.differentShippingAddress,
				"billing_first_name": this.billingAddressForm.first_name,
				"billing_last_name": this.billingAddressForm.last_name,
				"billing_email": this.billingAddressForm.email,
				"billing_phone_number": this.billingAddressForm.phone,
				"billing_country": this.billingAddressForm.country,
				"billing_city": this.billingAddressForm.city,
				"billing_address": this.billingAddressForm.line1,
				"billing_zip": this.billingAddressForm.zip,
			};
      if(
        params.differentShippingAddress != this.userProfile.differentShippingAddress ||
        params.billing_first_name != this.userProfile.billing_first_name ||
        params.billing_last_name != this.userProfile.billing_last_name ||
        params.billing_email != this.userProfile.billing_email ||
        params.billing_phone_number.replaceAll(' ','') != this.userProfile.billing_phone_number ||
        params.billing_country != this.userProfile.billing_country ||
        params.billing_country != this.userProfile.billing_country ||
        params.billing_address != this.userProfile.billing_address ||
        params.billing_zip != this.userProfile.billing_zip
      ) {
        UsersHelper.updateUserProfile(params);
        this.validateBillingForm(value);
      }
    },
    validateBillingForm(inputKey) {
      let form = {
				firstName: this.billingAddressForm.first_name,
				lastName: this.billingAddressForm.last_name,
				emailAddress: this.billingAddressForm.email,
				phoneNumber: this.billingAddressForm.phone,
				country: this.billingAddressForm.country,
				city: this.billingAddressForm.city,
				address: this.billingAddressForm.line1,
				zipCode: this.billingAddressForm.zip,
        countryCode: this.phoneNumberCountryPicked,
        invalidPhoneNumber: this.invalidPhoneNumber
			};
			let inputValidationResults = AppValidator.billingAndShippingAddress(form, inputKey);
			let formValidationResults = AppValidator.billingAndShippingAddress(form);
			this.billingFormErrors = [...inputValidationResults]
      this.validation(formValidationResults.length > 0 ? false : true)
		},
    error(key) {
      return this.billingFormErrors.find((item) => item.key == key);
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