<template>
  <v-container>
    <h1 class="text-h5 mb-4">Users</h1>
    <v-data-table :headers="headers" :items="users" />
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const users = ref([]);
const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Name', key: 'name' },
  { title: 'Email', key: 'email' },
];

onMounted(async () => {
  const { data } = await axios.get('/api/staff/users/');
  users.value = data;
});
</script> 