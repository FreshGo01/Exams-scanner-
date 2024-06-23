<script setup>
import { useRegisterStore } from '../stores/register.js'
const registerStore = useRegisterStore()
</script>

<template>
  <v-container class="d-flex align-center justify-center">
    <v-card class="mx-auto pa-12 pb-8" style="width: 600px" rounded="lg" elevation="8">
      <v-form v-model="registerStore.form" @submit.prevent="registerStore.onSubmit">
        <div class="text-subtitle-1 text-medium-emphasis">First Name</div>
        <v-text-field
          v-model="registerStore.first"
          density="compact"
          placeholder="Enter your first name"
          variant="outlined"
        ></v-text-field>

        <div class="text-subtitle-1 text-medium-emphasis">Last Name</div>
        <v-text-field
          v-model="registerStore.last"
          density="compact"
          placeholder="Enter your last name"
          variant="outlined"
        ></v-text-field>

        <div class="text-subtitle-1 text-medium-emphasis">Email Address</div>
        <v-text-field
          v-model="registerStore.email"
          density="compact"
          placeholder="Enter your email address"
          variant="outlined"
        ></v-text-field>

        <div class="text-subtitle-1 text-medium-emphasis">Academy</div>
        <v-text-field
          v-model="registerStore.academy"
          density="compact"
          placeholder="Enter your academy"
          variant="outlined"
        ></v-text-field>

        <div class="text-subtitle-1 text-medium-emphasis">Password</div>
        <v-text-field
          v-model="registerStore.password"
          :append-inner-icon="registerStore.showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :rules="[registerStore.rules.required, registerStore.rules.min]"
          :type="registerStore.showPassword ? 'text' : 'password'"
          color="primary"
          placeholder="Enter your password"
          variant="outlined"
          @click:append-inner="registerStore.showPassword = !registerStore.showPassword"
        ></v-text-field>

        <div class="text-subtitle-1 text-medium-emphasis">Confirm Password</div>
        <v-text-field
          v-model="registerStore.confirmPassword"
          :append-inner-icon="registerStore.showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :rules="[
            registerStore.rules.required,
            registerStore.rules.min,
            registerStore.rules.matchPassword
          ]"
          :type="registerStore.showPassword ? 'text' : 'password'"
          color="primary"
          placeholder="Enter your password"
          variant="outlined"
          @click:append-inner="registerStore.showPassword = !registerStore.showPassword"
        ></v-text-field>
        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>

          <!-- ปุ่ม Complete Registration ในกรอบ -->
          <v-btn
            color="blue"
            size="large"
            variant="tonal"
            text
            right
            :disabled="!registerStore.form"
            type="submit"
          >
            <span class="mr-2">Complete</span>
            <v-icon right>mdi-chevron-right</v-icon>
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-container>
</template>
