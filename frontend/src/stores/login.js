import { ref } from 'vue'
import { defineStore } from 'pinia'
import http from '../services/http'
import router from '@/router'
import Swal from 'sweetalert2'
import { useExamStore } from './exam'

export const useLoginStore = defineStore('login', () => {
  const examStore = useExamStore()
  const email = ref(null)
  const password = ref(null)
  const showPassword = ref(false)

  const currentUser = ref(JSON.parse(localStorage.getItem('user')))

  function clear() {
    email.value = null
    password.value = null
  }

  const form = ref(false)
  async function onSubmit() {
    const data = {
      email: email.value,
      password: password.value
    }
    try {
      const res = await http.post('/auth/login', data)
      if (res.status === 200) {
        Swal.fire({
          title: 'Success',
          text: 'Logged in',
          icon: 'success',
          confirmButtonText: 'OK'
        }).then(() => {
          clear()
          currentUser.value = res.data.user
          localStorage.setItem('token', res.data.access_token)
          localStorage.setItem('user', JSON.stringify(res.data.user))
          router.push({ name: 'home' })
        })
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

  function logOut() {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    currentUser.value = null
    examStore.clearItems()
    router.push({ name: 'login' })
  }

  const rules = {
    required: (value) => !!value || 'Required.',
    min: (v) => v.length >= 8 || 'Min 8 characters'
  }

  return {
    email,
    password,
    showPassword,
    form,
    onSubmit,
    rules,
    currentUser,
    logOut
  }
})
