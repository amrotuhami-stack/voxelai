<template>
	<div id="app" style="height: 100%">
		<!-- <TheMenu @close="closeMenu" /> !-->
		<main role="main" style="min-height: 100vh">
			<the-header />
			<b-overlay :show="overlay" rounded >
				<template #overlay>
					<div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">
						<font-awesome-icon id="spinner" class="spinner mb-3" icon="spinner" size="3x" spin />
						<h4 style="color: var(--secondary);">Sorry, {{ userProfile.first_name }} {{ userProfile.last_name }}</h4>
						<h6>This may take a few secounds while prepare your service</h6>
					</div>
      			</template>
				<div class="dashboard dashboard__nav--close" style="min-height: calc(100vh - 95px)">
					<TheMenu />
					<div class="dashboard__right" v-if="userProfile">
						<router-view />
					</div>
				</div>
			</b-overlay>
		</main>
		<!-- <the-footer /> -->
	</div>
</template>
<script>


// @ is an alias to /src
// import TheFooter from '@/common/layout/TheFooter.vue'
import TheHeader from '@/common/layout/TheHeader.vue';
import TheMenu from '@/common/layout/TheMenu.vue';

import { UsersHelper } from '@/common/crud-helpers/users'
import { BasketHelper } from '@/common/crud-helpers/basket'

import { CommonHelper } from '@/common/crud-helpers/common'

import axios from 'axios'

// [*] Import vue Components
import { mapGetters } from 'vuex';
import Messenger from './common/firebase/messenger';


export default {
	name: 'App',
	components: {
		TheHeader,
		TheMenu,
		// TheFooter,
	},
	computed: {
		...mapGetters(['userProfile', 'overlay']),
    },
	created: function() {
		CommonHelper.showSplashScreen()
		// // Voxel 3DI Authenticiation
		this.$auth.isUserAuth((auth_obj) => {
			if(!auth_obj) return;
			axios.interceptors.request.use(
        	    config => {
        	        config.headers.Authorization = `Bearer ${auth_obj.access_token}`
        	        return config
        	    },
        	    error => {
        	        return Promise.reject(error)
        	    },
        	)
        	UsersHelper.getUserProfile()
			BasketHelper.getCart()
		})

		// Keyclock Authentication 
		// if (this.$keycloak.authenticated) {
        //    axios.interceptors.request.use(
        //        config => {
        //            config.headers.Authorization = `Bearer ${this.$keycloak.idToken}`
        //            return config
        //        },
        //        error => {
        //            return Promise.reject(error)
        //        },
        //    )
        //    UsersHelper.getUserProfile()
		// 	BasketHelper.getCart()
        // }
    },
	watch: {
		userProfile() {
			let guard = this.$route.meta.guard
			if(this.userProfile.is_internal_doctor) {
				if(guard != "Internal Doctor") {
					this.$router.push({name: "Internal Doctor Dashboard", params: {page: '1'}});
				}
				if(this.$root.name == "Home") {
					this.$router.push({name: "Internal Doctor Dashboard",  params: {page: '1'}});
				}
			}
			else {
				if(guard == "Internal Doctor") {
					this.$router.push({name: "Dashboard",  params: {page: '1'}});
				}
			}
			CommonHelper.hideSplashScreen()
			
			let is_doctor = this.userProfile.is_internal_doctor;
			Messenger.updateUser(is_doctor ? 'admin' : this.userProfile.basket.owner.split('/')[8], {
                    "name": is_doctor ? 'Voxel3DI Expert' : this.userProfile.name,
                    "photo": this.userProfile.photo,
                    "email": this.userProfile.email,
                    "status": "available",
                    "type": is_doctor ? "admin" : "user",
                    "last_login": new Date().toISOString()
                }
            )
			window.addEventListener("beforeunload", () => {
            	Messenger.updateUserStatus(is_doctor ? 'admin' : this.userProfile.basket.owner.split('/')[8], 'un_available')
        	});
		}
	}
};
</script>

<style lang="scss">
// Account Dashboard
.dashboard {
	$parent: &;
	position: relative;
	height: 100%;
	&__left {
		width: 250px;
		height: 100%;
		background: #f5f5f5;
		padding: rem(32px) rem(26px) rem(100px) rem(26px);
		transition: all 0.5s ease;
		position: absolute;
		z-index: 100;
		cursor: pointer;
		left: 0;
		    height: 100%;
			@media screen and (max-width: 1200px) {
				width: 200px;
			}
		&:after {
			background-image: url("data:image/svg+xml,%3Csvg width='12' height='12' viewBox='0 0 12 12' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M12 0H0V12C0 5.37258 5.37258 0 12 0Z' fill='%23F5F5F5'/%3E%3C/svg%3E%0A");
			width: 12px;
			height: 12px;
			top: 0;
			right: -12px;
			content: '';
			position: absolute;
			background-repeat: no-repeat;
		}

		&--title {
			color: #a6a6a6;
			font-size: rem(12px);
			margin-bottom: rem(30px);
			transition: 0.5s all ease-in;
			letter-spacing: 1px;
		}

		&--seprator {
			content: '';
			display: inline-block;
			background: #e3e3e3;
			border-radius: 6px;
			height: 2px;
			width: 32px;
			position: relative;
			top: 30px;
			transition: 0.3s all ease-in-out;
		}

		#{ $parent }__nav {
			list-style: none;
			&--item {
				position: relative;
				margin-bottom: rem(18px);
				&:hover {
					&:before {
						content: '';
						position: absolute;
						left: rem(-26px);
						top: 50%;
						transform: translateY(-50%);
						background: var(--secondary);
						border-radius: 0px 100px 100px 0px;
						width: 3px;
						height: 32px;
					}
				}
				a {
					color: var(--textPrimary);
					text-decoration: none;
					font-size: rem(14px);
					font-weight: 500;
					padding: rem(8px) 0;
					@include flex(center, flex-start);
					flex-wrap: nowrap;
					width: 100%;
					text-transform: capitalize;
					transition: all 0.1s ease;

					span:not(.icon) {
						margin-left: rem(18px);
						transition: all 0.2s ease;
					}
					.icon {
						// width: 55px;
						// height: 55px;
						// min-width: 55px;
						@include flex(center, center);
						// transition: all 0.2s ease;

						opacity: 0.5;
						svg {
							// width: 50%;
							width: 20px;
							height: auto;
						}
					}
					&:hover {
						// color: rgba(48, 48, 48, 1);
						color: var(--secondary);
						.icon {
							opacity: 1;
						}
					}
				}
				&.active {
					&:before {
						content: '';
						position: absolute;
						left: rem(-26px);
						top: 50%;
						transform: translateY(-50%);
						background: var(--secondary);
						border-radius: 0px 100px 100px 0px;
						width: 3px;
						height: 32px;
					}
					a {
						color: var(--secondary);
						.icon {
							opacity: 1;
						}
					}
				}
			}
		}
	}
	&__right {
		height: 100%;
		// margin-left:250px;
		margin-left: 72px;
		padding: rem(50px) rem(48px);
		padding-bottom: rem(100px);
		@media screen and (max-width:1199px){
			padding: rem(30px) rem(24px);
			padding-bottom: rem(70px);
		}
	}
	&__nav--close {
		#{ $parent }__left {
			width: 72px;
			transition: all 0.3s ease;

			&--title {
				@media screen and (min-width: 992px) {
					font-size: 0;
					transform: scale(0);
				}
			}
			&--seprator {
				top: 15px;
			}
			#{ $parent }__nav {
				list-style: none;
				// overflow: hidden;
				a {
					span:not(.icon) {
						@media screen and (min-width: 992px) {
							visibility: hidden;
							opacity: 0;
							font-size: 0;
						}
					}
				}
				&--item {
					&.active {
						a {
							background: transparent;
						}
					}
				}
			}
		}
		#{ $parent }__right{
			margin-left:72px;
		}
	}
}


// responsive 

// @media screen and (max-width: 1600px) and (min-width: 1201px)  {
// 	.dashboard {
// 		$parent: &;
// 		&:not(.dashboard__nav--close) {
// 			#{ $parent }__right {
// 				padding-right: rem(15px);
// 				padding-left: rem(15px);
// 				font-size: 90%;
				
// 			}
// 		}
// 	}
// }

@media screen and (max-width: 991px) { 
	.dashboard {
		$parent: &;
		position: relative;
		&__left {
			float: none;
			position: absolute;
			z-index: 100;
			transition: .3s all ease-in-out;
			left: 0;
			padding-top: rem(32px);
			padding-bottom: rem(60px);
		}
		&__right {
			
			margin-left: 0;
		}
		&__nav--close {
			#{ $parent }__left {
				left: -100%;
				transition: .3s all ease-in-out;
			}
			#{ $parent }__right {
				margin-left: 0;
			}
		}
	}
}

// Account Dashboard
</style>
