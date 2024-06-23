<script setup>
import { useLoginStore } from '@/stores/login'
import router from '@/router'
const loginStore = useLoginStore()
</script>

<template>
  <v-container class="d-flex align-center justify-center">
    <v-card class="mx-auto pa-12 pb-8" elevation="8" style="width: 600px" rounded="lg">
      <v-form v-model="loginStore.form" @submit.prevent="loginStore.onSubmit">
        <div class="text-subtitle-1 text-medium-emphasis">Account</div>

        <v-text-field
          v-model="loginStore.email"
          density="compact"
          placeholder="Email address"
          prepend-inner-icon="mdi-email-outline"
          variant="outlined"
        ></v-text-field>

        <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
          Password
        </div>

        <v-text-field
          v-model="loginStore.password"
          :append-inner-icon="loginStore.showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :type="loginStore.showPassword ? 'text' : 'password'"
          density="compact"
          placeholder="Enter your password"
          prepend-inner-icon="mdi-lock-outline"
          variant="outlined"
          @click:append-inner="loginStore.showPassword = !loginStore.showPassword"
        ></v-text-field>

        <v-btn
          class="mb-8"
          color="blue"
          size="large"
          variant="tonal"
          :disabled="!loginStore.form"
          type="submit"
          block
        >
          Log In
        </v-btn>

        <v-card-text class="text-center">
          <v-btn
            text
            color="blue"
            append-icon="mdi-chevron-right"
            variant="plain"
            @click="router.push('/register')"
          >
            Sign up now
          </v-btn>
        </v-card-text>
      </v-form>
    </v-card>
  </v-container>
</template>
