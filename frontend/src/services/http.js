import axios from 'axios'
import router from '@/router'
const instance = axios.create({
  baseURL: 'http://localhost:3000/',
  headers: {
    'Content-Type': 'application/json'
    // 'Access-Control-Allow-Origin': 'https://aaf4-202-28-78-213.ngrok-free.app/',
  }
})

// กำหนด interceptor สำหรับการตั้งค่า header
instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// กำหนด interceptor สำหรับการตอบกลับ
instance.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response.status === 401) {
      localStorage.removeItem('user')
      localStorage.removeItem('token')
      router.push({ name: 'login' }) // ส่งผู้ใช้ไปที่หน้า Login
    }
    return Promise.reject(error)
  }
)
export default instance
