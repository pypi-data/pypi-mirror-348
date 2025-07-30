import { defineStore } from 'pinia';
import axios from 'axios';

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: null,
  }),
  actions: {
    async login(email, password) {
      const form = new URLSearchParams();
      form.append('username', email);
      form.append('password', password);
      const { data } = await axios.post('/api/staff/auth/login', form);
      this.token = data.access_token;
      localStorage.setItem('token', this.token);
    },
    logout() {
      this.token = '';
      localStorage.removeItem('token');
    },
  },
}); 