import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'


export const defaultStore = defineStore('default', {

  state: () => ({
    user: {
      isActive: false,
      token: '',
    },
    forms: [
      {
        ip: '192.168.1.10',
        description: 'description'
      },
    ]
  }),
  getters: {
    getUser: (state) => state.user,
    getNetworkForms: (state) => state.forms,
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
    async addNetworkRow(ip, description) {
      this.forms.push({ip, description})
    },
    async removeNetworkRow(index) {
      this.forms.splice(index, 1)
    }
  },
})
