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
    async authentificate(login, password) {
      let responseData
      console.log(login, password)
      await axios.post(`http://localhost:8000/api/auth/`, {
        "username": login,
        "password": password
      }).then(function (response) {
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
    async getNetworkList() {
      let cache = [] 
      await axios.get(`http://localhost:8000/api/v1/network/`).then(
        function (response) {
          cache = response.data
        }
      ).catch(function (error) {
        console.log(error)
      })
      this.forms = cache
    },
    async addNetworkRow(ip, description) {
      await axios.post(`http://localhost:8000/api/v1/network/`, {
        'ip': ip,
        'description': description
      }).then().catch(function (error) {
        console.log(error)
      })
    },
    async editNetworkRow(params) {
      let id = params.id
      await axios.put(`http://localhost:8000/api/v1/network/${id}`, {
        'ip': params.ip,
        'description': params.description
      }).then().catch(function (error) {
        console.log(error)
      })
    },
    async removeNetworkRow(id) {
      let param = id
      await axios.delete(`http://localhost:8000/api/v1/network/${param}`).then().catch(function (error) {
        console.log(error)
      })
    }
  },
})
