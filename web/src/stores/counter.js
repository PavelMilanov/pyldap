import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'


export const defaultStore = defineStore('default', {

  state: () => ({
    user: {
      isActive: false,
      token: '',
    },
    forms: [],
  }),
  getters: {
    getUser: (state) => state.user,
    getNetworkForms: (state) => state.forms,
  },
  actions: {
    async login(login, password) {
      let responseData
      await axios.post(`http://localhost:8000/api/auth/login`, {
        "username": login,
        "password": password
      }).then(function (response) {
        responseData = response.data
      }).catch(function (error) {
        console.log(error)
      })
      if (responseData != null) {
        this.user.isActive = true
        this.user.token = responseData
      }
    },
    async getNetworkList() {
      let cache = []
      const headers = { 'Authorization': `Bearer ${this.user.token}` }
      await axios.get(`http://localhost:8000/api/v1/network/`, { headers }).then(
        function (response) {
          cache = response.data
        }
      ).catch(function (error) {
        console.log(error)
      })
      this.forms = cache
    },
    async addNetworkRow(ip, description) {
      const headers = { 'Authorization': `Bearer ${this.user.token}` }
      await axios.post(`http://localhost:8000/api/v1/network/`, {
        'ip': ip,
        'description': description
      }, { headers }).then().catch(function (error) {
        console.log(error)
      })
    },
    async editNetworkRow(params) {
      let id = params.id
      const headers = { 'Authorization': `Bearer ${this.user.token}` }
      await axios.put(`http://localhost:8000/api/v1/network/${id}`, {
        'ip': params.ip,
        'description': params.description
      }, { headers }).then().catch(function (error) {
        console.log(error)
      })
    },
    async removeNetworkRow(id) {
      let param = id
      const headers = { 'Authorization': `Bearer ${this.user.token}` }
      await axios.delete(`http://localhost:8000/api/v1/network/${param}`, { headers }).then().catch(function (error) {
        console.log(error)
      })
    }
  },
})
