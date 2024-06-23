// import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import '@mdi/font/css/materialdesignicons.css' // Import MDI styles
import Swal from 'sweetalert2'

const app = createApp(App)

app.config.globalProperties.$swal = Swal
app.use(vuetify)
app.use(createPinia())
app.use(router)

app.mount('#app')
