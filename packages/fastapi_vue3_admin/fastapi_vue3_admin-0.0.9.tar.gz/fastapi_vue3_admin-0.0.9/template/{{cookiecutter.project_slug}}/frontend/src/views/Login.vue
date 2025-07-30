<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="6" md="4">
        <v-card class="pa-6">
          <h2 class="text-h5 mb-6 text-center">登入</h2>
          <v-text-field v-model="email" label="Email" type="email" required></v-text-field>
          <v-text-field v-model="password" label="Password" type="password" required></v-text-field>
          <v-btn color="primary" block @click="onLogin">登入</v-btn>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../store/user';

const email = ref('');
const password = ref('');
const router = useRouter();
const userStore = useUserStore();

async function onLogin() {
  try {
    await userStore.login(email.value, password.value);
    router.push('/');
  } catch (err) {
    console.error(err);
  }
}
</script> 