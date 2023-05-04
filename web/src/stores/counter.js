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
    // async getNetworkRow(ip) {
    //   let param = ip
    //   let cache = []
    //   this.searchForm = []
      // await axios.get(`http://localhost:8000/api/v1/network/${param}`).then(
      //   function (response) {
      //     cache = response.data
      //   }
      // ).catch(function (error) {
      //   console.log(error)
      // })
    //   console.log(this.forms)
    //   this.searchForm.push({"ip": cache.ip, "description": cache.description})
    // },
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
