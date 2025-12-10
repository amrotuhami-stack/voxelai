import {initializeApp} from "firebase/app";
import { getDatabase } from "firebase/database";
import { getStorage } from "firebase/storage";


const firebaseConfig = {
  apiKey: "AIzaSyBXyTrK0hdYt5ST-oLub3GF0Y-5n67aZCg",
  authDomain: "voxel3di.firebaseapp.com",
  databaseURL: "https://voxel3di-default-rtdb.firebaseio.com",
  projectId: "voxel3di",
  storageBucket: "voxel3di.appspot.com",
  messagingSenderId: "986874250922",
  appId: "1:986874250922:web:d0a5cfff063c4b3de2f2d3",
  measurementId: "G-R4D6BX101L"
};

const app = initializeApp(firebaseConfig);

export const database = getDatabase(app);
export const storage = getStorage(app);