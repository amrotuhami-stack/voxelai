<template>
	<div >
		<b-dropdown v-on:shown="readMyNotifications">
			<div class="notifications">
				<base-inner-scrollbar height="400px">
					<div v-for="(item, index) in myNotifications" :key="item.id">
						<div class="notifications__label" v-if="item.today && index == 0">Today</div>
						<div class="notifications__label" v-if="!item.today && (index == 0 || myNotifications[index - 1].today)">Recent</div>
						<div class="notifications__item" :class="!item.clicked || item.clicked == false ? 'unClicked' : ''" >
						
							<div class="notifications__item--icon">
								<svg-icon
										v-if="item.type == 'MESSEGE'"
										icon-id="letter-icon"
										icon-viewbox="0 0 24 24"
								></svg-icon>
								<svg-icon
										v-if="item.type == 'SERVICE'"
										icon-id="letterpad-icon"
										icon-viewbox="0 0 24 24"
								></svg-icon>
								<svg-icon
										v-if="item.type == 'ORDER'"
										icon-id="wallet"
										icon-viewbox="0 0 24 24"
								></svg-icon>
								<svg-icon
										v-if="item.type == 'PROMO'"
										icon-id="start-icon"
										icon-viewbox="0 0 24 24"
								></svg-icon>
							</div>
							<div class="notifications__item--detail">
								<p>{{item.title}}</p>
								<p class="notifications__item--detail--time">{{item.formatedDate}}</p>
							</div>
							<a class="abs-link" @click.prevent="() => redirectNoification(item)"></a>
						</div>
					</div>
				</base-inner-scrollbar>
				
			</div>
			
		</b-dropdown>
	</div>
</template>

<script>
import NotificationService from '../../firebase/inbox';
import { mapGetters } from 'vuex';
import Messenger from '../../firebase/messenger';

export default {
	props: { 
		items: Array,
	},
	data() {
		return {
			myNotifications: []
		};
	},
	computed: {
		...mapGetters(['userProfile']),
    },
	mounted() {
		this.myNotifications = []
		this.items.map((item) => {
			if(new Date(item.date).toLocaleDateString() == new Date().toLocaleDateString()) {
				this.myNotifications = [...this.myNotifications, {...item, today: true}]
			}
			else {
				this.myNotifications = [...this.myNotifications, {...item, today: false}]
			}
		})
	},
	watch: {
		items() {
			this.myNotifications = []
			this.items.map((item) => {
				if(new Date(item.date).toLocaleDateString() == new Date().toLocaleDateString()) {
					this.myNotifications = [...this.myNotifications, {...item, today: true}]
				}
				else {
					this.myNotifications = [...this.myNotifications, {...item, today: false}]
				}
			})
		}
	},
	methods: {
		readMyNotifications() {
			Notification.requestPermission()
			this.items.map((item) => {
				if(!item.read || item.read == false) {
					NotificationService.update(this.userProfile.is_internal_doctor ? 'admin' : this.userProfile.id, {...item, read: true,})
				}
			})
		},
		redirectNoification(item) {
			NotificationService.update(
				this.userProfile.is_internal_doctor ? 'admin' : this.userProfile.id, 
				{...item, read: true, clicked: true},
			)
			Messenger.getChat(this.userProfile.id, item.prams.chatId).then((chatObj) => {
				if(this.userProfile.is_internal_doctor) {
					this.$router.push({ name: 'Internal Doctor Chats', params: { lang: this.$i18n.locale, page: '1'}, query: {id: item.prams.chatId}})
					return;
				}
				if(chatObj.items.source == 'ORDER') {
					this.$router.push({
						name: 'continue-service-flow',
						params: {lang: this.$i18n.locale, type: 'order', index: String(chatObj.items.id),},
					})
					return;
				}
				if(chatObj.items.source == 'START-DIGTAL') {
					this.$router.push({
						name: 'start_digital_service',
						params: {lang: this.$i18n.locale, productId: String(chatObj.items.id),},
					})
					return;
				}
				if(chatObj.items.source == 'SERVICE') {
					this.$router.push({
						name: 'continue-service-flow',
						params: {lang: this.$i18n.locale, type: 'service', index: String(chatObj.items.id),},
					})
					return;
				}
			})
		}
	}


};
</script>
<style lang="scss">
	.notifications{
		.unClicked {
			background-color: rgb(239, 245, 252);
		}
		&__label {
			padding: 6px 16px;
			font-weight:400 !important;
			font-size: 14px !important;
			color:var(--textSecondary) !important;
			margin:0 !important;
			line-height:1.2 !important;
		}
		&__item{
			display: flex;
			position: relative;
			padding-left: rem(24px);
			padding-right: rem(24px);
			padding-top:rem(12px);
			padding-bottom:rem(12px);
			&--label{
				width: 100%;
			}
			&--icon{
				width:rem(35px);
				min-width:rem(35px);
				height:rem(35px);
				background: var(--imageBg);
				border-radius: 8px;
				@include flex (center , center);
				margin-right:8px;
				svg{
					width:16px;
				}
			}
			&--detail{
				p{
					font-weight:400 !important;
				}
				&--time{
					font-weight:400 !important;
					font-size: 12px !important;
					color:var(--textSecondary) !important;
					margin:0 !important;
					line-height:1.2 !important;
				}
			}
		}
		.seeAll{
			display: block;
			text-align: center;
			margin-top:rem(25px);
		}
	}
</style>
<style lang="scss" scoped>
::v-deep {
	.dropdown {
		box-shadow: none !important;
		.dropdown-toggle {
			width: 24px;
			height: 24px;
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
			width: 300px;
			padding:rem(0px);
			padding-top: 12px !important;
			padding-right:0;
			border-radius: 10px !important;
			box-shadow: 0px 2px 11px rgba(107, 107, 107, 0.16);
			right: 0;
			left:auto !important;
			margin-top:rem(64px);
			transform: none !important;
			@media screen and (max-width:414px){
				width:250px;
			}
			.button-row {
				.btn {
					background-color: var(--secondary) !important;
					color: #ffffff !important;
					border: 2px solid var(--secondary);
					@include flex(center, center);
					height: 52px;
					padding: rem(16px);
					border-radius: 8px;
					&:hover {
						background-color: #fff !important;
						color: var(--secondary) !important;
					}
				}
			}
			p{
				font-size:rem(14px);
				font-weight:500;
				color:var(--textPrimary);
				line-height:1.4;
				margin-bottom:10px;
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
