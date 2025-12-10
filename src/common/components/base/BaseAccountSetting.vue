<template>
	<div>
		<b-dropdown>
			<li>
				<router-link
					:to="{name: 'Account Settings', params: { lang: $i18n.locale },}"
					class="user-login"
				>
					Account Settings
				</router-link>
			</li>
			<li>
				<a href="#" @click="logout">
					Logout
				</a>
			</li>
		</b-dropdown>
	</div>
</template>

<script>
import Vue from "vue";
export default {
	props: { notificationItem: Array },
	methods: {
		logout: () => {
			//Vue.keycloak.logout()
			Vue.auth.logUserOut()
		},
	}
};
</script>


<style lang="scss" scoped>
::v-deep {
	.dropdown {
		box-shadow: none !important;
		.dropdown-toggle {
			width: 40px;
			height: 40px;
			background: transparent !important;
			background-color: transparent !important;
			padding:0 !important;
			&:hover,
			&:focus {
				background: transparent !important;
				background-color: transparent !important;
			}
			&::after {
				display: none;
			}
		}
		.dropdown-menu {
			width: 190px;
			padding:0 rem(16px);
			border-radius: 10px !important;
			box-shadow: 0px 4px 25px rgba(107, 107, 107, 0.08);
			right: 0;
			left:auto !important;
			margin-top:rem(64px);
			transform: none !important;
			a{
				color:var(--default);
				padding:rem(20px) 0;
				font-weight:400;
				&:hover{
					    color: var(--secondary) !important;
				}
			}
		}
		.scrollbar-wrap .scrollbar-y {
			width: 0.4em;
		}
		&.show {
			.btn {
				background: transparent !important;
				background-color: transparent !important;
			}
		}
	}
}
</style>
