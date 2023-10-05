import { initializeApp } from "firebase/app";
import { getDatabase,set,child,get,update,remove,ref } from "firebase/database";

const config = {
    apiKey: "AIzaSyB9hGpepr9Byve6EwEOvmZKqLfdng_QyTU",
    authDomain: "code-watch.firebaseapp.com",
    databaseURL: "https://code-watch-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "code-watch",
    storageBucket: "code-watch.appspot.com",
    messagingSenderId: "987328026189",
    appId: "1:987328026189:web:a6cbff6de12fe149efee04",
    measurementId: "G-S6872999EL"
}

const app = initializeApp(config)
const db = getDatabase(app)

const Ref = ref(db)
get(Ref).then((snapshot) => {
    console.log(snapshot.val())
})

