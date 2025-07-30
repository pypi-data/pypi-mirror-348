import { createApp } from 'vue';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import 'vuetify/styles';
import { md3 } from 'vuetify/blueprints';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import './assets/tailwind.css';

const vuetify = createVuetify({
  blueprint: md3,
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#FFD700',
          background: '#F5F5F5',
          surface: '#FFFFFF',
          secondary: '#D3D3D3',
          'on-secondary': '#808080',
        },
      },
    },
  },
});

const app = createApp(App);
const pinia = createPinia();
app.use(router).use(pinia).use(vuetify).mount('#app'); 