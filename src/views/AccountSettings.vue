<template>
	<div class="accountSettings">
		<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
		<div class="container">
			<h1 class="main-title mb-10">Account Settings</h1>
			<p>Change your profile and account settings</p>
			<personal-info :validation="changeFormValidation"></personal-info>
			<billing-address :countries="listOfcountries" :validation="changeFormValidation"></billing-address>
			<shipping-address :countries="listOfcountries" :validation="changeFormValidation"></shipping-address>
			<div class="inline-btns-wrapper stack-on-sm" v-if="userProfileChanged">
				<a href="#" v-if="loading.value" class="btn btn-primary">
					<font-awesome-icon id="spinner" class="spinner hidden" icon="spinner" size="2x" spin />
				</a>
				<a href="#" :class="`${isFormValid ?  'btn btn-primary' : 'btn btn-primary disabled'}`" @click="saveChange" > Save Changes </a>
				<a href="#" class="btn btn-secondary grey" @click="cancelChange"> Cancel </a>
			</div>
		</div>
	</div>
</template>

<script>
// [*] Import UI Components
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import PersonalInfo from '@/components/accountSettings/PersonalInfo.vue';
import BillingAddress from '@/components/accountSettings/BillingAddress.vue';
import ShippingAddress from '@/components/accountSettings/ShippingAddress.vue';

// [*] Import Breadcrumbs
import { accountSettingsBreadCrumbs } from "@/common/constant/breadCrumbs"

// [*] Vuex State Getter And Action Helper
import { CheckoutHelper } from '@/common/crud-helpers/checkout';
import { UsersHelper } from '@/common/crud-helpers/users';
import { mapGetters } from 'vuex';


export default {
	components: {
		BaseBreadCrumb,
		PersonalInfo,
		BillingAddress,
		ShippingAddress,
	},
	data() {
		return {
			breadCrumbsItems: [...accountSettingsBreadCrumbs],
			listOfcountries: [],
			isFormValid: true,
		};
	},
	computed: {
		...mapGetters(['userProfile', 'userProfileChanged', 'countries', 'loading']),
    },
	watch: {
		countries(){
			this.listOfcountries = this.countries.map(country => ({
				value: country.iso_3166_1_a2,
				text: country.printable_name,
			}));
		},
	},
	mounted(){
		UsersHelper.getUserProfile()
		CheckoutHelper.getCountries({});
	},
	methods: {
		saveChange() {
			return UsersHelper.saveUserProfile()
		},
		cancelChange() {
			return UsersHelper.cancelUserProfileChange()
		},
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
		changeFormValidation: function(value) {
			this.isFormValid = value
		}
	},
};
</script>

<style lang="scss">
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
			background: url('../assets/images/icons/Avatar.png');
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
		@media screen and (max-width:767px) and (min-width:416px){
			flex-direction: revert;
			.btn{
				&:not(:last-child){
					margin:0;
				}
			}
		}
		@media screen and (max-width:415px){
			.btn{
				width:100%;
			}
		}
	}
}
</style>
