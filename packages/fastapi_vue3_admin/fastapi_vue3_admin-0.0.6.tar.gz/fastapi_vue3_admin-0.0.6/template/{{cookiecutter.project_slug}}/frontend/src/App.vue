<template>
  <v-app>
    <v-main class="d-flex align-center justify-center fill-height">
      <v-card class="pa-8" elevation="2">
        <v-row class="mb-4" align="center" justify="center">
          <v-col cols="12" class="text-center">
            <h1 class="text-h4 font-weight-bold">{{ cookiecutter.project_slug }}</h1>
            <p class="text-subtitle-1">灰白 + 金黃色範例介面</p>
          </v-col>
        </v-row>
        <v-row align="center" justify="center">
          <v-btn color="primary" @click="fetchHello">呼叫 API</v-btn>
        </v-row>
        <v-row v-if="message" class="mt-4" align="center" justify="center">
          <v-col cols="12" class="text-center">
            <v-alert type="success" :text="message" />
          </v-col>
        </v-row>
      </v-card>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const message = ref('');

async function fetchHello() {
  try {
    const { data } = await axios.get('/api/public/hello/');
    message.value = data.message;
  } catch (error) {
    console.error(error);
  }
}
</script> 