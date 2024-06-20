<script setup>
import { ref } from 'vue'

const first = ref(null)
const last = ref(null)
const email = ref(null)
const academy = ref(null)
const password = ref(null)
const confirmPassword = ref(null)
const showPassword = ref(false)

const rules = {
  required: (value) => !!value || 'Required.',
  min: (v) => v.length >= 8 || 'Min 8 characters',
  matchPassword: () => confirmPassword.value === password.value || 'Passwords must match'
}
</script>

<template>
  <v-container class="d-flex align-center justify-center">
    <v-card class="mx-auto pa-12 pb-8" style="width: 600px" rounded="lg" elevation="8">
      <v-container>
        <div class="text-subtitle-1 text-medium-emphasis">First Name</div>
        <v-text-field
          v-model="first"
          density="compact"
          placeholder="Enter your first name"
          variant="outlined"
        ></v-text-field>

        <div class="text-subtitle-1 text-medium-emphasis">Last Name</div>
        <v-text-field
          v-model="last"
          density="compact"
          placeholder="Enter your last name"
          variant="outlined"
        ></v-text-field>

        <div class="text-subtitle-1 text-medium-emphasis">Email Address</div>
        <v-text-field
          v-model="email"
          density="compact"
          placeholder="Enter your email address"
          variant="outlined"
        ></v-text-field>

        <div class="text-subtitle-1 text-medium-emphasis">Academy</div>
        <v-text-field
          v-model="academy"
          density="compact"
          placeholder="Enter your academy"
          variant="outlined"
        ></v-text-field>

        <div class="text-subtitle-1 text-medium-emphasis">Password</div>
        <v-text-field
          v-model="password"
          :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :rules="[rules.required, rules.min]"
          :type="showPassword ? 'text' : 'password'"
          color="primary"
          placeholder="Enter your password"
          variant="outlined"
          @click:append-inner="showPassword = !showPassword"
        ></v-text-field>

        <div class="text-subtitle-1 text-medium-emphasis">Confirm Password</div>
        <v-text-field
          v-model="confirmPassword"
          :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :rules="[rules.required, rules.min, rules.matchPassword]"
          :type="showPassword ? 'text' : 'password'"
          color="primary"
          placeholder="Enter your password"
          variant="outlined"
          @click:append-inner="showPassword = !showPassword"
        ></v-text-field>
      </v-container>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>

        <!-- ปุ่ม Complete Registration ในกรอบ -->
        <v-btn color="blue" size="small" variant="tonal" text right>
          <span class="mr-2">Complete</span>
          <v-icon right>mdi-chevron-right</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>
