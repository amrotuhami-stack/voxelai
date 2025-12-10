import { ref, set, child, update, remove, onValue, push, get } from "firebase/database";
import { uploadBytesResumable, getDownloadURL } from "firebase/storage";
import { ref as stoRef } from "firebase/storage";
import { database, storage } from "./index";
import NotificationService from "./inbox";


const WELCOME_MESSEGE = "Welcome to V3Di chat!   Here, you can connect directly with our team of experts for any assistance you need.    Whether you have questions, need technical support, need modifications on the services, our dedicated professionals are here to help you.   Start a chat now and let us know how we can assist you!"

const usersRef = ref(database, '/users')
const chatsRef = ref(database, '/chats')
const messegesRef = ref(database, '/messeges')

const Messenger = {

  async getUser(userId) {
    let user = child(usersRef, `/${userId}`)
    try {
      let response = await get(user);
      if (response.exists()) return response.val();
      else return null;
    }
    catch (error) {
      return null;
    }
  },

  streamUsers(callback) {
    let users = child(usersRef, `/`)
    onValue(users, (snapshot) => {
      callback(snapshot.val())
    })
  },

  createUser(userId, data) {
    return set(child(usersRef, `/${userId}`), data);
  },

  updateUserStatus(userId, data) {
    return set(child(usersRef, `/${userId}/status`), data);
  },

  updateUser(userId, data) {
    return update(child(usersRef, `/${userId}`), data);
  },

  deleteUser(userId) {
    return remove(child(usersRef, `/${userId}`))
  },

  async getChat(userId, chatId) {
    let chat = child(chatsRef, `/${userId}/${chatId}`)
    try {
      let response = await get(chat);
      if (response.exists()) return response.val();
      else return null;
    }
    catch (error) {
      return null;
    }
  },

  async getChats(userId) {
    let chats = child(chatsRef, `/${userId}`)
    try {
      let response = await get(chats);
      if (response.exists()) return response.val();
      else return null;
    }
    catch (error) {
      return null;
    }
  },

  streamChats(userId, callback) {
    let chats = child(chatsRef, `/${userId}`)
    onValue(chats, (snapshot) => {
      callback(snapshot.val())
    })
  },

  async createChat(chatId, userId, targetId, data) {
    
    try {
      await set(child(chatsRef, `/${userId}/${chatId}`), {
        created: new Date().toISOString(),
        status: 'available',
        contact: targetId,
        items: {...data}
      })
      await set(child(chatsRef, `/${targetId}/${chatId}`), {
        created: new Date().toISOString(),
        status: 'un_available',
        contact: userId,
        items: {...data}
      })
      this.pushMessege(userId, chatId, {
        "value": WELCOME_MESSEGE,
        "type": "TEXT",
        "user_id": "admin",
        "status": "available",
        "date": new Date().toISOString(),
      })
    }
    catch (error) {
      return null;
    }
  },

  updateChat(userId, chatId, data) {
    return update(child(chatsRef, `/${userId}/${chatId}`), data);
  },

  pushUnReadMessege(userId, chatId, data) {
    update(child(chatsRef, `/${userId}/${chatId}/inbox`), {last_messege: new Date().toISOString()});
    return push(child(chatsRef, `/${userId}/${chatId}/inbox/messeges`), data);
  },

  updateChatStatus(userId, chatId, data) {
    return set(child(chatsRef, `/${userId}/${chatId}/status`), data);
  },

  streamContactChatStatus(contactId, chatId, callback) {
    let chats = child(chatsRef, `/${contactId}/${chatId}/status`)
    onValue(chats, (snapshot) => {
      callback(snapshot.val())
    })
  },

  removeChatForBoth(userId, connectId, chatId) {
    remove(child(chatsRef, `/${userId}/${chatId}`))
    remove(child(chatsRef, `/${connectId}/${chatId}`))
  },

  streamMesseges(chatId, callback) {
    let messeges = child(messegesRef, `/${chatId}`)
    onValue(messeges, (snapshot) => {
      callback(snapshot.val())
    })
  },

  async pushMessege(contactId, chatId, data) {
    push(child(messegesRef, `/${chatId}`), data);
    

    try {
      let chat = await this.getChat(contactId, chatId);
      if (chat.status != 'available') {
        let user = await this.getUser(data.user_id);

        this.pushUnReadMessege(contactId, chatId, data)
        
        NotificationService.push(contactId, {
          type: 'MESSEGE',
          title: `You have received a message from ${user.name} about order with number ${chatId}.`,
          date: new Date().toISOString(),
          read: false,
          prams: {
            chatId: chatId,
            type: data.type,
            value: data.value,
            from: data.user_id,
          }
        })
      }
    }
    catch (error) {
      return false;
    }
  },

  createMessege(chatId, data) {
    return set(child(messegesRef, `/${chatId}/${data.id}`), data);
  },

  updateMessege(chatId, data) {
    return update(child(messegesRef, `/${chatId}/${data.id}`), data);
  },

  async deleteMessege(chatId, messegeId) {
    try {
      return await remove(child(messegesRef, `/${chatId}/${messegeId}`))
    }
    catch (error) {
      return false
    }

  },

  uploadChatFile(chatId, file, onProgress, onStateChange, onComplete) {
    const storageRef = stoRef(storage, `chats/${chatId}/` + file.name);
    const uploadTask = uploadBytesResumable(storageRef, file);
    uploadTask.on('state_changed', (snapshot) => {
      const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
      onProgress(progress)
      switch (snapshot.state) {
        case 'paused':
          onStateChange(false)
          break;
        case 'running':
          onStateChange(true)
          break;
      }
    },
      (error) => onStateChange(False),
      () => {
        getDownloadURL(uploadTask.snapshot.ref).then((downloadURL) => {
          onComplete(downloadURL);
        });
      }
    );
  }

}


export default Messenger;