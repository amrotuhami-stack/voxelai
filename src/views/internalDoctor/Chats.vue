<template>
	<div class="my-chats">
		<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
		<h1 class="main-title">My Chats</h1>
		<p>See all updates about your assigned services</p>
		<div class="contentBox p-0">
			<div class="row section">
				<div class="col-lg-3 section__left">
					<div class="header">
						<h6>Recent Chats</h6>
						<p>{{'Number of Users ( ' + users.length + ' )  ' + '  Number of Chats ( ' + chats.length  + ' )'}}</p>
					</div>
					<div class="body">
						<div v-for="(chat, index) in chats" :key="chat.id">
							<div v-if="getUserObj(chat.contact)" class="user" :class="chat.id == selectedChatId ? 'selected' : ''" @click.prevent="() => laodChat(chat.id)">
								<img src="@/assets/images/icons/profile.svg" alt="Profile Image" />
								<div class="title">
									<h6> {{ getUserObj(chat.contact).name }} <div
										v-if="getUserObj(chat.contact).status == 'available'" class="circle"></div>
									</h6>
									<p v-if="!chat.items">{{ chat.id }}</p>
									<p v-if="chat.items && chat.items.source == 'SERVICE'">{{ 'From Service ' + chat.items.id }}</p>
									<p v-if="chat.items && chat.items.source == 'ORDER'">{{ 'From Order ' + chat.items.id }}</p>
									<p v-if="chat.items && chat.items.source == 'START-DIGTAL'">{{ 'From Digtal Product ' + chat.items.id }}</p>
								</div>
								<div v-if="chat.inbox" class="unReadCounter">
									<p>{{ chat.inbox.messeges.length }}</p>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div class="col-lg-9 section__right">
					<div v-if="selectedChat && getUserObj(selectedChat.contact)">
						<div class="header">
							<div class="title">
								<h6> {{ getUserObj(selectedChat.contact).name }} <div
										v-if="selectedChat.contactStatus == 'available'" class="circle"></div>
								</h6>
								<div class="subTitle">
									<p> {{ 'Last Login ' + getUserObj(selectedChat.contact).login }} </p>
									<div style="width: 24px;"></div>
									<p> {{ 'Email: ' + getUserObj(selectedChat.contact).email }} </p>
								</div>
							</div>
						</div>
						<div class="body">
							<!-- Messege -->
							<div v-for="(msg, index) in messeges" :key="msg.id">
								<div :class="msg.mine ? 'my-messege' : 'messege'">
									<div class="column">
										<div class="bubble" v-if="msg.type == 'TEXT'">
											<p>{{ msg.value }}</p>
											<p class="time">{{ msg.time }}</p>
										</div>
										<div class="bubble pointer" v-if="msg.type == 'FILE'">
											<a :href="msg.value" target="_blank" :title="msg.name" download="">
												<div class="my-row">
													<div>
														<img src="@/assets/images/svg/file.svg" alt="File Icon"
															style="width: 24px;" />
													</div>
													<div style="width: 12px"></div>
													<div>
														<p>{{ msg.name }}</p>
														<p class="subTitle" v-if="msg.status == 'available'">{{
															fileSizeToString(msg.size) + " . " + fileType(msg.name) + "."+ msg.time
															}}</p>
														<p class="subTitle" v-else>{{ 'Uploading ' +
															Math.ceil(msg.progress)
															+ '% of file ' + fileSizeToString(msg.size) }}</p>
													</div>
													<div style="width: 16px"></div>
													<div v-if="msg.status != 'available'" style="width: 24px;">
														<b-spinner small variant="primary"></b-spinner>
													</div>
												</div>
											</a>
										</div>

									</div>
								</div>
							</div>
						</div>
						<div class="actions">
							<div class="row">
								<!--Messege Input Field-->
								<div class="col-lg-10">
									<input type="text" placeholder="Write Messege Here ..." id="messege-field"
										@keyup="(e) => onPressKey(e)" v-model="messege" />
									<input type="file" hidden id="messege-file" @change="(e) => pushFileMessege(e)"
										multiple="multiple" />
								</div>
								<!-- Attach File button -->
								<div class="col-lg-1">
									<a class="icon-button" @click.prevent="onPressUploadButton">
										<img src="@/assets/images/icons/file.png" alt="Attache Button" width="28px" />
									</a>
								</div>
								<div class="col-lg-1">
									<a class="icon-button" @click.prevent="() => pushMessege(this.messege)">
										<img src="@/assets/images/icons/send.png" alt="Send Button" width="28px" />
									</a>
								</div>
								</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
// [*] Import UI Compenents.
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';

// [*] Import Breadcrumbs ...
import { internalDoctorChatsBreadCumbs } from "@/common/constant/breadCrumbs"

// [*] Import vue Components
import { mapGetters } from 'vuex';
import Messenger from '../../common/firebase/messenger';
import { v1 as uuidv1 } from 'uuid';

export default {
	props: {
		page: String,
	},
	components: {
		BaseBreadCrumb,
	},
	computed: {
		...mapGetters(['userProfile',]),
	},
	data() {
		return {
			breadCrumbsItems: [...internalDoctorChatsBreadCumbs],
			users: [],
			chats: [],
			firstRender: true,

			selectedChatId: "",
			selectedChat: null,
			messeges: [],
			messege: "",
		};
	},
	created() {
		Messenger.streamUsers((resp) => {
			this.users = [];
			for (const [key, value] of Object.entries(resp || {})) {
				if (key == "admin") return
				let lastLoginAsString = new Date(value.last_login).toLocaleDateString([], { dateStyle: 'full' })
				let lastLoginTimeAsString = new Date(value.last_login).toLocaleTimeString([], { timeStyle: 'short' })
				this.users = [
					...this.users,
					{ id: key, ...value, login: lastLoginAsString + " " + lastLoginTimeAsString }
				]
			}
		})
		Messenger.streamChats('admin', (resp) => {
			this.chats = []
			for (const [key, value] of Object.entries(resp || {})) {
				if(value.inbox) {
					let newInbox = {
						last_messege: new Date(value.inbox.last_messege),
						messeges: [],
					}
					for (const [mkey, mvalue] of Object.entries(value.inbox.messeges || {})) {
						newInbox.messeges = [...newInbox.messeges, {...mvalue}]
					}
					value.inbox = newInbox
				}
				this.chats = [...this.chats, { id: key, ...value } ]
			}
			if(this.firstRender) {
				this.laodChat(this.$route.query.id ? this.$route.query.id : this.chats[0].id)
				this.firstRender = false
			}
		})
		window.addEventListener("beforeunload", () => {
            Messenger.updateChatStatus('admin', this.selectedChatId, 'un_available')
        });
		
	},
	destroyed() {
        Messenger.updateChatStatus('admin', this.selectedChatId, 'un_available')
    },
	beforeRouteUpdate(to, from, next) {
		this.laodChat(to.query.id ? to.query.id : this.chats[0].id)
		next()
	},
	watch: {
		selectedChatId() {
			if (this.selectedChatId != "") {
				this.selectedChat = this.chats.find((chat) => chat.id == this.selectedChatId)
				Messenger.streamContactChatStatus(this.selectedChat.contact, this.selectedChatId, (value) => {
					this.selectedChat = { ...this.selectedChat, contactStatus: value }
				})
				Messenger.updateChat('admin', this.selectedChatId, {inbox: null})
			}
		}
	},
	methods: {
		getUserObj(userId) {
			let user =  this.users.find((user) => user.id == userId);
			if(user == undefined) return false
			return user
		},
		laodChat(chatId) {
			if(this.selectedChatId != "" & !this.firstRender) {
				Messenger.updateChatStatus('admin', this.selectedChatId, 'un_available')
			}

			// For Chat Id Like SD-1-1
			this.selectedChatId = chatId;

			// Sign Me as Avalible on chat
			Messenger.updateChatStatus('admin', this.selectedChatId, 'available')

			// Stream Chat Messeges
			Messenger.streamMesseges(this.selectedChatId, (resp) => {
				this.messeges = []
				for (const [key, value] of Object.entries(resp || {})) {
					let timeAsString = new Date(value.date).toLocaleTimeString([], { timeStyle: 'short' })
					this.messeges = [
						...this.messeges,
						{ id: key, ...value, mine: value.user_id == 'admin' ? true : false, time: timeAsString, }
					]
				}
			})


		},
		fileSizeToString(value) {
            let fileSize = value.toString()
            if (fileSize.length < 7) return `${Math.round(+fileSize / 1024).toFixed(1)} KB`
            return `${(Math.round(+fileSize / 1024) / 1000).toFixed(1)} MB`
        },
        fileType(name) {
            return name.split('.')[1].toUpperCase();
        },
        onPressKey(event) {
            if (event.key === "Enter") {
                this.pushMessege(this.messege)
            }
        },
        onPressUploadButton() {
            document.getElementById('messege-file').click()
        },
		pushMessege(value) {
            Messenger.pushMessege(this.selectedChat.contact, this.selectedChatId, {
                "value": value,
                "type": "TEXT",
                "user_id": 'admin',
                "status": "available",
                "date": new Date().toISOString(),
            })
            this.messege = "";
        },
        pushFileMessege(event) {
            let files = event.target.files
            for (let file of files) {
                var id = uuidv1()
                file.uuid = id
                Messenger.createMessege(this.selectedChatId, {
                    "id": id,
                    "value": "",
                    "type": "FILE",
                    "user_id": 'admin',
                    "status": "uploading",
                    "date": new Date().toISOString(),
                    "name": file.name,
                    "size": file.size,
                    "progress": 0
                })
            }
            for (let file of files) {
                Messenger.uploadChatFile(this.selectedChatId, file,
                    (value) => Messenger.updateMessege(this.selectedChatId, { 'id': file.uuid, 'progress': value }),
                    (value) => !value ? Messenger.updateMessege(this.selectedChatId, { 'id': file.uuid, 'status': 'deleted' }) : null,
                    (value) => {
                        Messenger.deleteMessege(this.selectedChatId, file.uuid).then((_) => {
                            Messenger.pushMessege(this.selectedChat.contact, this.selectedChatId, {
                                "value": value,
                                "type": "FILE",
                                "user_id": 'admin',
                                "status": "available",
                                "date": new Date().toISOString(),
                                "name": file.name,
                                "size": file.size,
                            })
                        })
                    },
                );
            }

        },
	}

};
</script>

<style lang="scss" scoped>
.my-chats {
	.main-title {
		margin-bottom: rem(10px);
	}

	h2 {
		font-size: rem(28px);
	}

	.section {
		h6 {
			margin-bottom: rem(6px);
			padding: 0;
			font-size: rem(16px);
			color: var(--textPrimary) !important;
			text-align: left;
			font-weight: 400;
			display: flex;
			align-items: center;

			.circle {
				margin: 0px 8px 0px 8px;
				background-color: rgb(7, 216, 7);
				width: 8px;
				height: 8px;
				border-radius: 100px;
			}
		}

		p {
			margin-bottom: 0px;
			font-size: rem(14px);
			color: var(--textSecondary) !important;
			text-align: left;
			font-weight: 400;
		}

		&__left {
			padding: 0px;
			border-right: 1px solid #eaeaea;

			.header {
				padding: rem(16px);
				padding-left: rem(32px);
				height: rem(75px);
				border-bottom: 1px solid #eaeaea;
				display: flex;
				justify-content: center;
				flex-direction: column;
			}

			.body {
				display: flex;
				flex-direction: column;

				.selected {
					background-color: #feffd291;
				}

				.user {
					display: flex;
					flex-direction: row;
					align-items: center;
					padding: 12px;
					padding-left: 32px;
					border-bottom: 1px solid #eaeaea;

					img {
						width: 24px;
					}
					.title {
						margin-left: rem(12px);
						width: 100%;
						h6 {
							font-size: 14px;
						}
						p {
							font-size: 12px;
						}
					}
					.unReadCounter {
						width: rem(24px);
						height: rem(24px);
						p {color: white !important; font-size: 12px;}
						background-color: rgb(248, 203, 0);
						border-radius: 6px;
						display: flex;
						justify-content: center;
						align-items: center;
					}
				}
			}
		}

		&__right {
			padding: 0px;

			.header {
				padding: rem(16px);
				border-bottom: 1px solid #eaeaea;
				height: rem(75px);

				.subTitle {
					display: flex;
					flex-direction: row;
				}
			}

			.body {
				height: 500px;
				overflow: auto;
				display: flex;
				flex-direction: column;
				padding: rem(16px);
				padding-right: rem(32px);

				p {
					margin-bottom: 0px;
					font-size: rem(14px);
					color: var(--textPrimary) !important;
					text-align: left;
					white-space: pre-line;
				}

				.my-row {
					display: flex;
					flex-direction: row;
					align-items: center;
				}

				.pointer {
					cursor: pointer;
				}

				.my-messege {
					display: flex;
					flex-direction: row;
					justify-content: flex-end;

					.column {
						display: flex;
						flex-direction: column;
						align-items: flex-end;

						.bubble {
							max-width: 340px;
							padding: 12px;
							margin-bottom: 8px;
							background-color: #f4f6f2;
							border-radius: 12px 12px 0px 12px;
							display: flex;
							flex-direction: column;
							align-items: flex-end;
						}

						.subTitle {
							margin-top: 4px;
							font-size: rem(11px);
							color: var(--textSecondary) !important;
							text-align: left;
						}

						.time {
							font-size: rem(10px);
							color: var(--textSecondary) !important;
							text-align: left;
						}
					}

				}

				.messege {
					display: flex;
					flex-direction: row;
					justify-content: flex-start;

					.column {
						display: flex;
						flex-direction: column;
						justify-content: flex-start;

						.bubble {
							max-width: 340px;
							padding: 12px;
							margin-bottom: 8px;
							background-color: #FEFFD2;
							border-radius: 12px 12px 12px 0px;
							display: flex;
							flex-direction: column;
							align-items: flex-start;
						}

						.time {
							font-size: rem(10px);
							color: var(--textSecondary) !important;
							text-align: left;
						}

						.subTitle {
							margin-top: 4px;
							font-size: rem(11px);
							color: var(--textSecondary) !important;
							text-align: left;
						}
					}
				}
			}
			.actions {
        		padding: 16px;
        		border-top: solid 1px #eaeaea;

        		input {
        		    font-size: rem(14px);
        		    background-color: transparent;
        		    outline: none;
        		    border: 0;
        		    font-weight: 400;
        		    height: rem(32px);
        		}
			
        		input::placeholder {
        		    opacity: 1 !important;
        		    color: var(--textSecondary) !important;
        		}
    		}
		}
	}

}
</style>
