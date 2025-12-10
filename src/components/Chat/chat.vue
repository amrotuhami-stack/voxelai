<template>
    <div class="chat-container">
        <!-- Header Section -->
        <div class="chat-container__header">
            <img src="@/assets/images/icons/Avatar.png" alt="Voxel3di Logo" />
            <div class="title">
                <h6>Voxel3DI Expert</h6>
                <p>usually response withen a few minutes</p>
            </div>
        </div>
        <!-- Body Section -->
        <div class="chat-container__body">
            <!-- Messege -->
            <div v-for="(msg, index) in messeges">
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
                                        <img src="@/assets/images/svg/file.svg" alt="File Icon" style="width: 24px;" />
                                    </div>
                                    <div style="width: 12px"></div>
                                    <div>
                                        <p>{{ msg.name }}</p>
                                        <p class="subTitle" v-if="msg.status == 'available'">{{
                                            fileSizeToString(msg.size) + " . " + fileType(msg.name) + " . " + msg.time
                                            }}</p>
                                        <p class="subTitle" v-else>{{ 'Uploading ' + Math.ceil(msg.progress) + '% of file ' + fileSizeToString(msg.size) }}</p>
                                    </div>
                                    <div style="width: 16px"></div>
                                    <div v-if="msg.status != 'available'" style="width: 24px;">
                                        <b-spinner small variant="primary" label="Text Centered"></b-spinner>
                                    </div>
                                </div>
                            </a>
                        </div>

                    </div>
                </div>
            </div>
        </div>
        <!-- Actions Section -->
        <div class="row chat-container__actions">
            <!--Messege Input Field-->
            <div class="col-lg-8">
                <input type="text" placeholder="Write Messege Here ..." id="messege-field" @keyup="(e) => onPressKey(e)"
                    v-model="messege" />
                <input type="file" hidden id="messege-file" @change="(e) => pushFileMessege(e)" multiple="multiple" />
            </div>
            <!-- Attach File button -->
            <div class="col-lg-2">
                <a class="icon-button" @click.prevent="onPressUploadButton">
                    <img src="@/assets/images/icons/file.png" alt="Attache Button" width="28px" />
                </a>
            </div>
            <div class="col-lg-2">
                <a class="icon-button" @click.prevent="() => pushMessege(this.messege)">
                    <img src="@/assets/images/icons/send.png" alt="Send Button" width="28px" />
                </a>
            </div>
        </div>
    </div>
</template>


<script>
import Messenger from '../../common/firebase/messenger';
import { v1 as uuidv1 } from 'uuid';

export default {
    props: {
        id: String,
        user: String,
        contact: String,
        items: Object,
    },
    data() {
        return {
            chatId: "",
            messege: "",
            messeges: [],
        }
    },
    created() {
        this.chatId = this.id;
        Messenger.getChat(this.user, this.chatId).then((chat) => {
            if (!chat || !chat.contact) {
                this.startNewChat()
            }
            else {
                Messenger.updateChat(this.user, this.chatId, {items: {...this.items}})
                Messenger.updateChat(this.contact, this.chatId, {items: {...this.items}})
                Messenger.updateChat(this.user, this.chatId, {inbox: null})
            }
            Messenger.updateChatStatus(this.user, this.chatId, 'available')
            
        })

        Messenger.streamMesseges(this.chatId, (resp) => {
            this.messeges = []
            for (const [key, value] of Object.entries(resp || {})) {
                let timeAsString = new Date(value.date).toLocaleTimeString([], { timeStyle: 'short' })
                this.messeges = [
                    ...this.messeges,
                    { id: key, ...value, mine: value.user_id == this.user ? true : false, time: timeAsString, }
                ]
            }
        })
        window.addEventListener("beforeunload", () => {
            if(this.messeges.length < 2) {
                Messenger.deleteMessege(this.chatId, this.messeges[0].id);
                Messenger.removeChatForBoth(this.user, this.contact, this.chatId)
            }
            else {
                Messenger.updateChatStatus(this.user, this.chatId, 'un_available')
            }

        });       
    },
    destroyed() {
        if(this.messeges.length < 2) {
            Messenger.deleteMessege(this.chatId, this.messeges[0].id);
            Messenger.removeChatForBoth(this.user, this.contact, this.chatId)
        }
        else {
            Messenger.updateChatStatus(this.user, this.chatId, 'un_available')
        }
    },
    methods: {
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
        startNewChat() {
            Messenger.createChat(this.chatId, this.user, this.contact, this.items );
        },
        pushMessege(value) {
            Messenger.pushMessege(this.contact, this.chatId, {
                "value": value,
                "type": "TEXT",
                "user_id": this.user,
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
                Messenger.createMessege(this.chatId, {
                    "id": id,
                    "value": "",
                    "type": "FILE",
                    "user_id": this.user,
                    "status": "uploading",
                    "date": new Date().toISOString(),
                    "name": file.name,
                    "size": file.size,
                    "progress": 0
                })
            }
            for (let file of files) {
                Messenger.uploadChatFile(this.chatId, file,
                    (value) => Messenger.updateMessege(this.chatId, { 'id': file.uuid, 'progress': value }),
                    (value) => !value ? Messenger.updateMessege(this.chatId, { 'id': file.uuid, 'status': 'deleted' }) : null,
                    (value) => {
                        Messenger.deleteMessege(this.chatId, file.uuid).then((_) => {
                            Messenger.pushMessege(this.contact, this.chatId, {
                                "value": value,
                                "type": "FILE",
                                "user_id": this.user,
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
}
</script>

<style lang="scss" scoped>
.chat-container {
    &__header {
        padding: 16px;
        display: flex;
        flex-direction: row;
        align-items: center;
        border-bottom: solid 1px #eaeaea;

        img {
            width: rem(54px);
            height: rem(54px);
        }

        .title {
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            margin-left: 12px;

            h6 {
                margin-bottom: rem(8px);
                padding: 0;
                font-size: rem(14px);
                color: var(--textPrimary) !important;
                text-align: left;
                font-weight: 400;
            }

            p {
                margin-bottom: 0px;
                font-size: rem(12px);
                color: var(--textSecondary) !important;
                text-align: left;
            }
        }
    }

    &__body {
        height: 350px;
        overflow: auto;
        display: flex;
        flex-direction: column;
        padding: rem(16px);

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

    &__actions {
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

    .icon-button {
        padding: 8px;
        margin: 0px;
        background-color: transparent;
    }
}
</style>