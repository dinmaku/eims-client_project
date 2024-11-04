import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import router from './router';
import { setupCalendar, Calendar, DatePicker } from 'v-calendar';

import 'v-calendar/style.css';

const app = createApp(App);

// Set up the calendar before mounting
app.use(setupCalendar, {});

// Register components
app.component('VCalendar', Calendar);
app.component('VDatepicker', DatePicker);

// Use the router
app.use(router);

// Mount the app
app.mount('#app');