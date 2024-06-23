import { ref } from 'vue'
import { defineStore } from 'pinia'
import http from '../services/http'
import router from '@/router'
import Swal from 'sweetalert2'

export const useRegisterStore = defineStore('register', () => {
  const first = ref(null)
  const last = ref(null)
  const email = ref(null)
  const academy = ref(null)
  const password = ref(null)
  const confirmPassword = ref(null)
  const showPassword = ref(false)

  function clear() {
    first.value = null
    last.value = null
    email.value = null
    academy.value = null
    password.value = null
    confirmPassword.value = null
  }

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
        Swal.fire({
          title: 'Success',
          text: 'User created',
          icon: 'success',
          confirmButtonText: 'OK'
        }).then(() => {
          clear()
          router.push({ name: 'login' })
        })
        // router.push({ name: 'login' })
      }
    } catch (error) {
      clear()
      console.error(error)
      Swal.fire({
        title: 'Error',
        text: `Error: ${error.response.data.message}`,
        icon: 'error',
        confirmButtonText: 'OK'
      })
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
