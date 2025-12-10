import { ref, child, update, remove, onValue, push, get } from "firebase/database";

import { database } from "./index";

const inboxRef = ref(database, '/notifications')

// NotificationService Object
// {
//     ID: GENRATED BY FIREBASE
//     TYPE: MESSEGE | UPDATE
//     VALUE: TEXT
//     DATE: DATE_AND_TIME
//     URL: ON_CLICK_URL
//     PRAMS: OBJECT
//     READ: FALSE | TRUE
// }

const NotificationService =  {

  async get(userId) {
    let notification = child(inboxRef, `/${userId}`)
    try {
      let response = await get(notification);
      if (response.exists()) return response.val();
      else return null;
    }
    catch(error) {
      return null;
    }
  },

  stream(userId, callback) {
    let notifications = child(inboxRef, `/${userId}`)
    onValue(notifications, (snapshot) => {
      callback(snapshot.val())
    })
  },

  async push(userId, data) {
    try {
      return await push(child(inboxRef, `/${userId}`), data);
    }
    catch(error) {
        return null;
    }
  },

  update(userId, data) {
    try {
        return update(child(inboxRef, `/${userId}/${data.id}`), data);
    }
    catch(error) {
        return null
    }
  },

  delete(userId, notificationId) {
    try {
        return remove(child(chatsRef, `/${userId}/${notificationId}`))
    }
    catch(error) {
        return null;
    }
  }
}


export default NotificationService;