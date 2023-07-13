import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import Notifications from '@kyvg/vue3-notification'

import './assets/main.less'
import "bootstrap/dist/css/bootstrap.min.css"
import 'bootstrap-icons/font/bootstrap-icons.css'
import "bootstrap"

const app = createApp(App)

app.use(createPinia()).use(Notifications)
app.use(router)

app.mount('#app')
