<template>
	<div class="dashboard__left" style="height: 100%">
		<div class="dashboard__left--scroll" v-if="userProfile">
			<!-- <p class="dashboard__left--welcome">
            Hello <span>Mahad@alanasrisolutions.com</span>
        	</p> -->
			<h5 class="dashboard__left--title">MY WORKSAPCE</h5>
			<ul class="dashboard__nav" v-if="!userProfile.is_internal_doctor">
				<li class="dashboard__nav--item">
					<router-link
						:to="{
							name: 'Dashboard',
							params: {
								lang: $i18n.locale, page: '1'
							},
						}"
						class="user-login"
					>
						<span class="icon">
							<svg-icon
								icon-id="activity"
								icon-viewbox="0 0 24 24"
							></svg-icon>
						</span>
						<span>Dashboard</span>
					</router-link>
				</li>
				<li class="dashboard__nav--item">
					<router-link
						:to="{
							name: 'Start Existing Services',
							params: {
								lang: $i18n.locale, page: '1'
							},
						}"
						class="user-login"
					>
						<span class="icon">
							<svg-icon
								icon-id="plus"
								icon-viewbox="0 0 24 24"
							></svg-icon>
						</span>
						<span>New Service</span>
					</router-link>
				</li>
				<li class="dashboard__nav--item">
					<router-link
						:to="{
							name: 'My Patient',
							params: {
								lang: $i18n.locale,
								page: '1'
							},
						}"
						class="user-login"
					>
						<span class="icon">
							<svg-icon
								icon-id="user"
								icon-viewbox="0 0 24 24"
							></svg-icon>
						</span>
						<span>My Patients</span>
					</router-link>
				</li>
				<li class="dashboard__nav--item">
					<router-link
						:to="{
							name: 'My Order',
							params: {
								lang: $i18n.locale, page: '1'
							},
						}"
						class="user-login"
					>
						<span class="icon">
							<svg-icon
								icon-id="document"
								icon-viewbox="0 0 24 24"
							></svg-icon>
						</span>
						<span>My Orders</span>
					</router-link>
				</li>
			</ul>
			<ul class="dashboard__nav" v-else>
				<li class="dashboard__nav--item">
					<router-link
						:to="{ name: 'Internal Doctor Dashboard', params: { lang: $i18n.locale, page: '1'},}"
						class="user-login"
					>
						<span class="icon">
							<svg-icon icon-id="activity" icon-viewbox="0 0 24 24"></svg-icon>
						</span>
						<span>Dashboard</span>
					</router-link>
				</li>
				<li class="dashboard__nav--item">
					<router-link
						:to="{ name: 'Internal Doctor Chats', params: { lang: $i18n.locale, page: '1'},}"
						class="user-login"
					>
						<span class="icon">
							<svg-icon icon-id="chat" icon-viewbox="0 0 24 24"></svg-icon>
						</span>
						<span>Chats</span>
					</router-link>
				</li>
			</ul>
			<div class="dashboard__left--seprator"></div>
			<h5 class="dashboard__left--title mt-30" v-if="!userProfile.is_internal_doctor">Voxel3DI SERVICES</h5>
			<ul class="dashboard__nav" v-if="!userProfile.is_internal_doctor">
				<li class="dashboard__nav--item">
					<router-link
						:to="{
							name: 'Shop',
							params: {
								lang: $i18n.locale,
								page: '1'
							},
						}"
						class="user-login"
					>
						<span class="icon">
							<svg-icon
								icon-id="discovery"
								icon-viewbox="0 0 24 24"
							></svg-icon>
						</span>
						<span>Explore Shop</span>
					</router-link>
				</li>
				<li class="dashboard__nav--item">
					<router-link
						:to="{
							name: 'MedicalImagingDashboard',
							params: {
								lang: $i18n.locale,
							},
						}"
						class="user-login"
					>
						<span class="icon">
							<svg-icon
								icon-id="scan"
								icon-viewbox="0 0 24 24"
							></svg-icon>
						</span>
						<span>Medical Imaging</span>
					</router-link>
				</li>
				<!-- <li class="dashboard__nav--item">
					<router-link
						:to="{
							name: 'Deals and Offers',
							params: {
								lang: $i18n.locale,
							},
						}"
						class="user-login"
					>
						<span class="icon">
							<svg-icon
								icon-id="discount"
								icon-viewbox="0 0 32 32"
							></svg-icon>
						</span>
						<span>Deals and Offers</span>
					</router-link>
				</li>
				<li class="dashboard__nav--item">
					<router-link
						:to="{
							name: 'Dashboard',
							params: {
								lang: $i18n.locale,
							},
						}"
						class="user-login"
					>
						<span class="icon">
							<svg-icon
								icon-id="layer"
								icon-viewbox="0 0 24 24"
							></svg-icon>
						</span>
						<span>Pricing Plans</span>
					</router-link>
				</li> !-->
				<li class="dashboard__nav--item">
					<router-link
						:to="{
							name: 'Account Settings',
							params: {
								lang: $i18n.locale,
							},
						}"
						class="user-login"
					>
						<span class="icon">
							<svg-icon
								icon-id="setting"
								icon-viewbox="0 0 24 24"
							></svg-icon>
						</span>
						<span>Account Settings</span>
					</router-link>
				</li>
				<li class="dashboard__nav--item">
					<router-link
						:to="{
							name: 'Help Center',
							params: {
								lang: $i18n.locale,
							},
						}"
						class="user-login"
					>
						<span class="icon">
							<svg-icon
								icon-id="info-circle"
								icon-viewbox="0 0 24 24"
							></svg-icon>
						</span>
						<span>Help Center</span>
					</router-link>
				</li>
			</ul>
		</div>
	</div>
</template>

<script>
// import "@/assets/css/disclosure-navigation.css";
// import "@/assets/js/Menu.js";
// import Menu from "@/common/layout/mixin/Menu";
import { mapGetters } from 'vuex';

export default {
	computed: {
		...mapGetters(['userProfile']),
    },
	// mixins: [Menu],
	// props: {
	//   IsOpen: Boolean,
	// },
	// mounted() {
	// },
};
</script>
