<template>
  <v-app>
    <v-navigation-drawer app permanent>
      <v-list>
        <v-list-item-title class="text-h6 pa-4">Admin</v-list-item-title>
        <v-list-item link to="/">
          <v-list-item-title>Dashboard</v-list-item-title>
        </v-list-item>
        <v-list-item link to="/staff/users">
          <v-list-item-title>Users</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template> 