<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue'

const theme = ref('light')
const bg = ref('bg-grey-lighten-3')

function onClick() {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
  bg.value = theme.value === 'light' ? 'bg-grey-lighten-3' : 'bg-grey-darken-3'
}
</script>

<template>
  <v-app :theme="theme" :class="bg">
    <v-app-bar title="Exam Scanner" class="px-3">
      <v-btn
        :prepend-icon="theme === 'light' ? 'mdi-weather-sunny' : 'mdi-weather-night'"
        :text="theme === 'light' ? 'dark' : 'light'"
        slim
        @click="onClick"
      ></v-btn>
      <!-- <v-btn v-bind="RouterLink" to="/">Home</v-btn> -->
    </v-app-bar>
    <v-main class="ma-6">
      <RouterView />
    </v-main>
  </v-app>
</template>
