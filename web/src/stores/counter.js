import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'


export const defaultStore = defineStore('default',{

  state: () => ({
    user: {
      isActive: false,
      token: '',
    },
  }),
  getters: {
    getUser: (state) => state.user,
  },
  actions: {
    async postAuthentification(login, password) {
      let responseData
      const params = new URLSearchParams()
      params.append('username', login)
      params.append('password', password)
      await axios.post(`http://localhost:8000/api/auth/`, params
      ).then(function (response) {
        responseData = response.data
        console.log(responseData)
      }).catch(function (error) {
        console.log(error)
      })
      if (responseData != null) {
        this.user.isActive = true
        this.user.token = responseData
      }
    },
  },
})
