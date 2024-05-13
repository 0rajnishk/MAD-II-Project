import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import axios from "axios";

// global Axios instance
const instance = axios.create({
  baseURL: "http://127.0.0.1:5050/",
});

const app = createApp(App)


app.config.globalProperties.$http = instance;
app.use(router)

app.mount('#app')
