import { ref } from 'vue'
import { defineStore } from 'pinia'
import http from '../services/http'
import router from '@/router'

export const useUserStore = defineStore('user', () => {
  const first = ref(null)
  const last = ref(null)
  const email = ref(null)
  const academy = ref(null)
  const password = ref(null)
  const confirmPassword = ref(null)
  const showPassword = ref(false)

  const form = ref(false)
  async function onSubmit() {
    const data = {
      name: `${first.value} ${last.value}`,
      email: email.value,
      academy: academy.value,
      password: password.value
    }
    try {
      const res = await http.post('/users', data)
      if (res.status === 201) {
        router.push({ name: 'login' })
      }
    } catch (error) {
      console.error(error)
    }
  }

  const rules = {
    required: (value) => !!value || 'Required.',
    min: (v) => v.length >= 8 || 'Min 8 characters',
    matchPassword: () => confirmPassword.value === password.value || 'Passwords must match'
  }

  return {
    first,
    last,
    email,
    academy,
    password,
    confirmPassword,
    showPassword,
    form,
    onSubmit,
    rules
  }
})
