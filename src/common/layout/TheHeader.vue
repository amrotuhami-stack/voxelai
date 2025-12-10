<template>
	<div>
		<BaseIcons />
		<!-- <FixedHeader :threshold="150"> -->  
		<header role="banner">
			<div class="container-fluid">
				<div class="flex-row">
					<div class="left-side">
						<a href="#" class="menu-icon" id="menu">
							<img
								src="@/assets/images/icons/menu-icon.png"
								class="img-fluid"
								alt="menu"
							/>
						</a>
						<router-link to="/" title="vetro" class="logo">
							<img
								src="@/assets/images/Logo.png"
								class="img-fluid d-none-sm"
								alt="vetro logo"
							/>
							<img
								src="@/assets/images/Logo.png"
								class="img-fluid d-none show-on-sm"
								alt="vetro logo"
							/>
						</router-link>
						<div class="name-wrapper" v-if="userProfile">
							<div class="name">
								<img
									src="@/assets/images/icons/hand-wave.png"
									alt="handwave"
								/>
								Hi {{ userProfile.first_name }} {{ userProfile.last_name }}
							</div>
							<p style="text-align: center">{{hiMessege}}</p>
						</div>
					</div>
					<!-- <div class="middle-side">
						<form class="search no-label">
							<input
								type="text"
								class="form-control"
								placeholder="Search Everything"
							/>
						</form>
					</div> -->
					<div class="right-side" v-if="userProfile">
						<ul class="list-unstyled">
							<li class="langSelector">
									<img
									src="@/assets/images/flags/usa.png"
									class="img-fluid"
									alt="usa"
								/>
								<!-- <base-lang-selector /> -->
							</li>
							<li>
								<a class="notification" >
									<span v-if="unReadNotificationCounter > 0" class="counter" >{{ unReadNotificationCounter }}</span>
									<base-notifications v-if="notifications.length > 0" :items="notifications"/>
								</a>
							</li>
							<li v-if="cart && !userProfile.is_internal_doctor">
								<a href="#" class="cart">
									<span v-if="cartLines.length > 0" class="counter">{{ cartLines.length }}</span>
									<base-selected-items v-if="cartLines.length > 0"  :cartItem="cartLines" :cart="cart"/>
								</a>
							</li>
							<li v-if="userProfile.photo" class="setting" :style="{backgroundImage: `url(${userProfile.photo})`, backgroundSize: 'cover' }">
								<base-account-setting />
							</li>
							<li v-else class="setting" :style="{backgroundImage: `url(${userAvatar})`, backgroundSize: 'cover' }">
								<base-account-setting />
							</li>
						</ul>
					</div>
				</div>
			</div>
		</header>
		<!-- </FixedHeader> -->
		<!-- <TheMenu @close="closeMenu" /> -->
	</div>
</template>
<script>
// [*] Import UI Compnents ...
import BaseIcons from '@/common/components/base/BaseSvgIcons.vue';
import BaseSelectedItems from '../components/base/BaseSelectedItems.vue';
import BaseNotifications from '../components/base/BaseNotifications.vue';
import BaseLangSelector from '../components/base/BaseLangSelector.vue';
import BaseAccountSetting from '../components/base/BaseAccountSetting.vue';

import { mapGetters } from 'vuex';
import NotificationService from '../firebase/inbox';

export default {
	components: {
		BaseIcons,
		BaseSelectedItems,
		BaseNotifications,
		BaseLangSelector,
		BaseAccountSetting,
	},
	data() {
		return {
			userAvatar: require('@/assets/images/icons/Avatar.png'),
			notifications:[],
			unReadNotificationCounter: 0,
			hiMessege: "Start First Service Now!",
		};
	},
	computed: {
		...mapGetters(['userProfile', 'cart', 'cartLines', 'serviceList']),
    },
	watch: {
		userProfile() {
			if(this.userProfile.is_internal_doctor) {
				this.hiMessege = "Hope you have a good day!"
			}
			let userId = this.userProfile.is_internal_doctor? 'admin' : this.userProfile.basket.owner.split('/')[8]
			
			NotificationService.stream(userId, (resp) => {
				this.notifications = []
				this.unReadNotificationCounter = 0;
        	    for (const [key, value] of Object.entries(resp || {})) {
        	        let dateAsString = new Date(value.date).toLocaleDateString([], { dateStyle: 'full' })
        	        let timeAsString = new Date(value.date).toLocaleTimeString([], { timeStyle: 'short' })

					if(!value.read || value.read == false) {
						this.unReadNotificationCounter++;
						new Notification('VOXEL 3DI New Messege', {
							body: value.title,
							tag: key,
							icon: '@/assets/images/Logo.png'
						})
					}
        	        this.notifications = [
        	            ...this.notifications,
        	            { id: key, ...value, formatedDate: `${dateAsString} ${timeAsString}`}
        	        ]
        	    }
				this.notifications.reverse()
			})
		},
		serviceList() {
			if(this.serviceList.length > 0) {
				this.hiMessege = "Welcome Back!"
			}
		}
	},
	mounted() {
		var menuToggler = document.querySelector('.menu-icon');
		var menuTogglerLeft = document.querySelector('.dashboard__left');
		let dashboard = document.querySelector('.dashboard'); 

		var mob = window.matchMedia('(max-width: 1205px)');

		menuToggler.addEventListener('click', (event) => {
			dashboard.classList.toggle('dashboard__nav--close');
		});

		function responsive(e){
			if(e.matches){
				// mob code
				// menuToggler.addEventListener('click', (event) => {
				// 	dashboard.classList.toggle('dashboard__nav--close');
				// });
				// mob code
			}else{
				// dekstop code
				// menuToggler.addEventListener('mouseenter', (event) => {
				// 	dashboard.classList.toggle('dashboard__nav--close');
				// });
				// menuToggler.addEventListener('mouseleave', (event) => {
				// 	dashboard.classList.toggle('dashboard__nav--close');
				// });
				// for left
				menuTogglerLeft.addEventListener('mouseenter', (event) => {
					dashboard.classList.remove('dashboard__nav--close');
				});
				menuTogglerLeft.addEventListener('mouseleave', (event) => {
					dashboard.classList.add('dashboard__nav--close');
				});
				// dekstop code 
			}
		}
		responsive(mob);
		mob.addEventListener('change',responsive)
	},
	methods: {
		openMyNotifications() {
			console.log(Math.random())
		},
	}
}
</script>

<style lang="scss" scoped>
header {
	background: #f5f5f5;
	display: flex;
	align-items: center;
	padding-top: rem(24px);
	padding-bottom: rem(24px);
	padding-right: rem(32px);
	padding-left: rem(9px);
	@media screen and (max-width: 1200px) {
		padding-right: rem(0px);
		padding-left: rem(0px);
	}
	@media screen and (max-width: 991px) {
		padding-top: rem(15px);
		padding-bottom: rem(15px);
	}
	@media screen and (max-width: 575px) {
		padding-top: rem(14px);
		padding-bottom: rem(14px);
	}
	.flex-row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		.left-side {
			display: flex;
			align-items: center;
			flex: 0 0 500px;
			@media screen and (max-width: 1300px) {
				flex: 0 0 420px;
			}
			@media screen and (max-width: 1200px) {
				flex: 0 0 410px;
			}
			@media screen and (max-width: 991px) {
				flex: 1;
			}
			.menu-icon {
				display: block;
				margin-right: rem(20px);
				@media screen and (max-width:767px){
					margin-right:rem(16px);
				}
			}
			.logo {
				margin-right: 50px;
				img {
					max-width: rem(175px);
				}
				@media screen and (max-width: 1300px) {
					margin-right: 30px;
				}
				@media screen and (max-width: 1200px) {
					margin-right: 25px;
				}
				@media screen and (min-width:1025px){
					&:hover {
						opacity: 0.75;
					}
				}
			}
			.name-wrapper {
				@media screen and (max-width: 575px) {
					display: none;
				}
				.name {
					margin-bottom: 5px;
					position: relative;
					color: #171717;
					font-weight: 500;
				}
				p {
					margin-bottom: 0;
					color: var(--textSecondary);
				}
			}
		}
		.middle-side {
			flex: 1;
			padding: 0 rem(15px);
			@media screen and (max-width: 991px) {
				display: none;
			}
			form {
				input {
					background: #e9e9e9;
					padding: rem(12px) rem(24px);
					padding-left: rem(58px);
					border-radius: 12px;
					border: 0;
					background-image: url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M11 3C6.58172 3 3 6.58172 3 11C3 15.4183 6.58172 19 11 19C15.4183 19 19 15.4183 19 11C19 6.58172 15.4183 3 11 3ZM11 5C14.3137 5 17 7.68629 17 11C17 14.3137 14.3137 17 11 17C7.68629 17 5 14.3137 5 11C5 7.68629 7.68629 5 11 5Z' fill='%238E8E8E'/%3E%3Cg opacity='0.5'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M15.2926 15.2971C15.6529 14.9365 16.2201 14.9085 16.6125 15.2133L16.7068 15.2965L20.7068 19.2928C21.0975 19.6832 21.0978 20.3164 20.7074 20.7071C20.3471 21.0677 19.7799 21.0957 19.3875 20.7908L19.2932 20.7077L15.2932 16.7113C14.9025 16.321 14.9022 15.6878 15.2926 15.2971Z' fill='%238E8E8E'/%3E%3C/g%3E%3C/svg%3E%0A");
					background-repeat: no-repeat;
					background-position: rem(27px) center;
					max-height: 56px;
				}
			}
		}
		.right-side {
			flex: 0 0 280px;
			display: flex;
			justify-content: flex-end;
			@media screen and (max-width: 1300px) {
				flex: 0 0 215px;
			}
			@media screen and (max-width: 1200px) {
				flex: 0 0 180px;
			}
			@media screen and (max-width: 575px) {
				flex: 1;
			}
			ul {
				display: flex;
				align-items: center;
				margin-bottom: 0;
				li {
					&:not(:last-child) {
						margin-right: rem(27px);
						@media screen and (max-width: 1200px) {
							margin-right: rem(18px);
						}
						@media screen and (max-width: 374px) {
							margin-right: rem(13px);
						}
					}
					.notification {
						display: inline-block;
						background-image: url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M12.0367 2H11.9636C8.38057 2 5.07636 4.43258 4.75003 7.71108C4.73108 7.91522 4.71758 8.12158 4.70831 8.34L4.69516 8.78596L4.69024 9.463L4.71376 9.37545C4.58599 9.95509 4.28977 10.4959 3.85314 10.9412L3.75085 11.0637C3.30191 11.6982 3.04263 12.4363 3.0024 13.2006L3.00102 13.4472C2.97799 14.4452 3.34703 15.4366 4.03622 16.2183C4.95979 17.1265 6.12991 17.6562 7.38183 17.7681C10.4447 18.0776 13.5464 18.0776 16.6207 17.7671C17.8613 17.6609 19.0355 17.1294 19.9074 16.2685C20.5939 15.5052 20.9662 14.5944 20.998 13.6493L20.9992 13.2531C20.9614 12.439 20.7 11.6987 20.245 11.0659L20.151 10.9536L19.9935 10.7801C19.6921 10.4249 19.4712 10.0204 19.3425 9.5903L19.3002 9.429L19.2902 9.03587L19.2899 8.36062L19.2838 8.08476L19.2702 7.84006C19.2672 7.79981 19.2638 7.75931 19.26 7.7178C18.9222 4.43055 15.6175 2 12.0367 2ZM11.9636 4H12.0367C14.6672 4 17.0473 5.75057 17.2695 7.91235L17.2836 8.12226L17.2899 8.37884L17.2918 9.20733L17.2989 9.44358L17.3129 9.66776L17.3338 9.80825L17.4052 10.0904C17.6164 10.8365 17.9948 11.5306 18.514 12.127L18.6422 12.266L18.6212 12.2336C18.8521 12.5547 18.9823 12.9233 19.0003 13.301L18.9992 13.4388C19.0132 13.9789 18.8238 14.4837 18.4601 14.8895C17.9664 15.3744 17.2302 15.7077 16.4348 15.7758C13.479 16.0743 10.512 16.0743 7.57145 15.7772C6.7631 15.7048 6.02567 15.371 5.48599 14.8425C5.17672 14.4877 4.98905 13.9835 5.00076 13.47L5.00102 13.2531L5.01978 13.0841C5.05716 12.8551 5.14374 12.6137 5.27588 12.3864L5.35724 12.258L5.28119 12.3415C5.97796 11.6309 6.45767 10.755 6.66687 9.80599L6.69032 9.59072L6.6932 8.92326L6.69689 8.72389C6.70393 8.41769 6.71775 8.15138 6.74084 7.9025C6.95508 5.7503 9.33255 4 11.9636 4Z' fill='%238E8E8E'/%3E%3Cg opacity='0.5'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M14.3446 19.2447C14.7618 18.8828 15.3934 18.9275 15.7553 19.3446C16.1173 19.7618 16.0725 20.3934 15.6554 20.7553C15.4049 20.9727 15.1203 21.1642 14.8229 21.3188C13.8539 21.8435 12.6499 22.0761 11.4581 21.9781C10.2509 21.8788 9.13367 21.4471 8.34076 20.7519C7.92549 20.3878 7.884 19.756 8.24809 19.3408C8.61219 18.9255 9.24399 18.884 9.65927 19.2481C10.1112 19.6443 10.8222 19.919 11.622 19.9849C12.4374 20.0519 13.2535 19.8943 13.885 19.5525C14.0607 19.461 14.2151 19.3571 14.3446 19.2447Z' fill='%238E8E8E'/%3E%3C/g%3E%3C/svg%3E%0A");
						width: 24px;
						height: 24px;
						background-repeat: no-repeat;
						position:relative;
						.counter {
							color: #ffffff;
							font-weight: 500;
							font-size: 12px;
							background: #1a90d2;
							display: flex;
							align-items: center;
							justify-content: center;
							border: 2px solid #f5f5f5;
							border-radius: 9px;
							width: 22px;
							height: 16px;
							position: absolute;
							right: -8px;
							top: -6px;
							@media screen and (max-width:575px){
								font-size:10px;
							}
						}
						@media screen and (min-width:1025px){
							&:hover{
								background-image: url("data:image/svg+xml,%0A%3Csvg width='24' height='24' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M12.0367 2H11.9636C8.38057 2 5.07636 4.43258 4.75003 7.71108C4.73108 7.91522 4.71758 8.12158 4.70831 8.34L4.69516 8.78596L4.69024 9.463L4.71376 9.37545C4.58599 9.95509 4.28977 10.4959 3.85314 10.9412L3.75085 11.0637C3.30191 11.6982 3.04263 12.4363 3.0024 13.2006L3.00102 13.4472C2.97799 14.4452 3.34703 15.4366 4.03622 16.2183C4.95979 17.1265 6.12991 17.6562 7.38183 17.7681C10.4447 18.0776 13.5464 18.0776 16.6207 17.7671C17.8613 17.6609 19.0355 17.1294 19.9074 16.2685C20.5939 15.5052 20.9662 14.5944 20.998 13.6493L20.9992 13.2531C20.9614 12.439 20.7 11.6987 20.245 11.0659L20.151 10.9536L19.9935 10.7801C19.6921 10.4249 19.4712 10.0204 19.3425 9.5903L19.3002 9.429L19.2902 9.03587L19.2899 8.36062L19.2838 8.08476L19.2702 7.84006C19.2672 7.79981 19.2638 7.75931 19.26 7.7178C18.9222 4.43055 15.6175 2 12.0367 2ZM11.9636 4H12.0367C14.6672 4 17.0473 5.75057 17.2695 7.91235L17.2836 8.12226L17.2899 8.37884L17.2918 9.20733L17.2989 9.44358L17.3129 9.66776L17.3338 9.80825L17.4052 10.0904C17.6164 10.8365 17.9948 11.5306 18.514 12.127L18.6422 12.266L18.6212 12.2336C18.8521 12.5547 18.9823 12.9233 19.0003 13.301L18.9992 13.4388C19.0132 13.9789 18.8238 14.4837 18.4601 14.8895C17.9664 15.3744 17.2302 15.7077 16.4348 15.7758C13.479 16.0743 10.512 16.0743 7.57145 15.7772C6.7631 15.7048 6.02567 15.371 5.48599 14.8425C5.17672 14.4877 4.98905 13.9835 5.00076 13.47L5.00102 13.2531L5.01978 13.0841C5.05716 12.8551 5.14374 12.6137 5.27588 12.3864L5.35724 12.258L5.28119 12.3415C5.97796 11.6309 6.45767 10.755 6.66687 9.80599L6.69032 9.59072L6.6932 8.92326L6.69689 8.72389C6.70393 8.41769 6.71775 8.15138 6.74084 7.9025C6.95508 5.7503 9.33255 4 11.9636 4Z' fill='%231A90D2'/%3E%3Cg opacity='0.5'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M14.3446 19.2447C14.7618 18.8828 15.3934 18.9275 15.7553 19.3446C16.1173 19.7618 16.0725 20.3934 15.6554 20.7553C15.4049 20.9727 15.1203 21.1642 14.8229 21.3188C13.8539 21.8435 12.6499 22.0761 11.4581 21.9781C10.2509 21.8788 9.13367 21.4471 8.34076 20.7519C7.92549 20.3878 7.884 19.756 8.24809 19.3408C8.61219 18.9255 9.24399 18.884 9.65927 19.2481C10.1112 19.6443 10.8222 19.919 11.622 19.9849C12.4374 20.0519 13.2535 19.8943 13.885 19.5525C14.0607 19.461 14.2151 19.3571 14.3446 19.2447Z' fill='%231A90D2'/%3E%3C/g%3E%3C/svg%3E%0A");
							}
						}
					}
					.cart {
						display: inline-block;
						background-image: url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M2.10579 1.55301C2.33514 1.09431 2.86945 0.888905 3.34011 1.05965L3.44743 1.10579L3.59733 1.18074C4.97532 1.86974 5.95455 3.15299 6.26045 4.65386L6.30312 4.89259L6.31822 4.99522L18.5608 4.99592C18.6925 4.99592 18.8239 5.00458 18.9543 5.02183L19.1489 5.05413C20.7156 5.36733 21.7514 6.84803 21.5322 8.41017L21.5026 8.58402L20.3023 14.5883C20.0336 15.9323 18.8916 16.9154 17.5381 16.995L17.3605 17.0002H8.71606C7.29457 17.0002 6.07719 16.0046 5.78287 14.6301L5.75094 14.4564L4.32637 5.1967C4.18828 4.29909 3.65187 3.51603 2.87337 3.06181L2.7029 2.96959L2.55301 2.89465C2.05903 2.64766 1.8588 2.04698 2.10579 1.55301ZM7.72768 14.1523C7.79696 14.6026 8.15995 14.9441 8.60359 14.9939L8.71606 15.0002H17.3605C17.7975 15.0002 18.1788 14.7175 18.3112 14.3103L18.3411 14.1963L19.5414 8.19195C19.6497 7.65038 19.2984 7.12359 18.7569 7.01532L18.6593 7.00078L18.5608 6.99592L6.62622 6.99522L7.72768 14.1523Z' fill='%238E8E8E'/%3E%3Cg opacity='0.5'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M12 9C11.4477 9 11 9.44772 11 10C11 10.5523 11.4477 11 12 11H16C16.5523 11 17 10.5523 17 10C17 9.44772 16.5523 9 16 9H12ZM9.5 19C10.3275 19 11 19.673 11 20.501C11 21.329 10.3275 22 9.5 22C8.67255 22 8 21.329 8 20.501C8 19.673 8.67255 19 9.5 19ZM16.5 19C17.3275 19 18 19.673 18 20.501C18 21.329 17.3275 22 16.5 22C15.6725 22 15 21.329 15 20.501C15 19.673 15.6725 19 16.5 19Z' fill='%238E8E8E'/%3E%3C/g%3E%3C/svg%3E%0A");
						width: 24px;
						height: 24px;
						background-repeat: no-repeat;
						position: relative;
						z-index: 100;
						.counter {
							color: #ffffff;
							font-weight: 500;
							font-size: 12px;
							background: #1a90d2;
							display: flex;
							align-items: center;
							justify-content: center;
							border: 2px solid #f5f5f5;
							border-radius: 9px;
							width: 22px;
							height: 16px;
							position: absolute;
							right: -8px;
							top: -6px;
							@media screen and (max-width:575px){
								font-size:10px;
							}
						}
						@media screen and (min-width:1025px){
							&:hover{
								background-image: url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M2.10579 1.55301C2.33514 1.09431 2.86945 0.888905 3.34011 1.05965L3.44743 1.10579L3.59733 1.18074C4.97532 1.86974 5.95455 3.15299 6.26045 4.65386L6.30312 4.89259L6.31822 4.99522L18.5608 4.99592C18.6925 4.99592 18.8239 5.00458 18.9543 5.02183L19.1489 5.05413C20.7156 5.36733 21.7514 6.84803 21.5322 8.41017L21.5026 8.58402L20.3023 14.5883C20.0336 15.9323 18.8916 16.9154 17.5381 16.995L17.3605 17.0002H8.71606C7.29457 17.0002 6.07719 16.0046 5.78287 14.6301L5.75094 14.4564L4.32637 5.1967C4.18828 4.29909 3.65187 3.51603 2.87337 3.06181L2.7029 2.96959L2.55301 2.89465C2.05903 2.64766 1.8588 2.04698 2.10579 1.55301ZM7.72768 14.1523C7.79696 14.6026 8.15995 14.9441 8.60359 14.9939L8.71606 15.0002H17.3605C17.7975 15.0002 18.1788 14.7175 18.3112 14.3103L18.3411 14.1963L19.5414 8.19195C19.6497 7.65038 19.2984 7.12359 18.7569 7.01532L18.6593 7.00078L18.5608 6.99592L6.62622 6.99522L7.72768 14.1523Z' fill='%231A90D2'/%3E%3Cg opacity='0.5'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M12 9C11.4477 9 11 9.44772 11 10C11 10.5523 11.4477 11 12 11H16C16.5523 11 17 10.5523 17 10C17 9.44772 16.5523 9 16 9H12ZM9.5 19C10.3275 19 11 19.673 11 20.501C11 21.329 10.3275 22 9.5 22C8.67255 22 8 21.329 8 20.501C8 19.673 8.67255 19 9.5 19ZM16.5 19C17.3275 19 18 19.673 18 20.501C18 21.329 17.3275 22 16.5 22C15.6725 22 15 21.329 15 20.501C15 19.673 15.6725 19 16.5 19Z' fill='%231A90D2'/%3E%3C/g%3E%3C/svg%3E");
							}
						}
					}
					&.langSelector{
						position:relative;
						>img{
							position: absolute;
							top:50%;
							left:50%;
							transform: translate(-50% , -50%);
						}
					}
					&.setting {
						background-color: transparent;
						width: 40px;
						height: 40px;
						display: flex;
						align-items: center;
						justify-content: center;
						border-radius: 100px;
						@media screen and (max-width:767px){
							width:35px;
							height:35px;
						}
					}
				}
			}
		}
	}
}

@media screen and (max-width: 575px) {
	.d-none-sm {
		display: none !important;
	}
	.show-on-sm {
		display: block !important;
	}
}
</style>
