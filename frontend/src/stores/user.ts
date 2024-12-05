// Utilities
import { getUser } from '@/api/user';
import { User } from '@/types/auth';
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const token = ref('');
  const user = ref<User>()

  const getTokenFromLocal = () => {
    token.value = localStorage.getItem('authToken') || ''
  }

  const getUserInfo = async () => {
    if (user.value) return
    try {
      const response = await getUser()
      if (response.success) {
        user.value = response.data.data
      }
    } catch (error) {
      console.log(error)
    }
  }

  watch(token, (newToken) => {
    if (newToken) {
      localStorage.setItem('authToken', newToken)
    }
  })

  return {
    token,
    user,
    getTokenFromLocal,
    getUserInfo,
  }
})
