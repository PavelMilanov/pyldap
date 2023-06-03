import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'


export const defaultStore = defineStore('default', {

  state: () => ({
    user: {
      isActive: localStorage.isActive,
      token: localStorage.token,
    },
    network: {
      tableRender: [],
      tableFull: []
    },
    pagination: {
      count: 0, // количество страниц, исходя из размера страницы
      range: 20, // размер таблицы на одной странице
      currentPage: 0, // номер страницы пагинации
    },
    customers: {
      tableFull: []
    },
    customer: {},
    units: {},
    BACKEND: import.meta.env.VITE_APP_BACKEND
  }),
  getters: {
    getUser: (state) => state.user,
    getNetworkTable: (state) => state.network,
    getPaginationInfo: (state) => state.pagination,
    getCustomersTable: (state) => state.customers,
    getCustomerInfo: (state) => state.customer,
    getUnits: (state) => state.units,
  },
  actions: {
    async login(login, password) {
      let responseData
      await axios.post(`http://${this.BACKEND}/api/auth/login`, {
        "username": login,
        "password": password
      }).then(function (response) {
        responseData = response.data
      }).catch(function (error) {
        console.log(error)
      })
      if (responseData != null) {
        localStorage.token = responseData
        localStorage.isActive = true
        this.user.token = localStorage.token
        this.user.isActive = localStorage.isActive
        return 'success'
      }
      else {
        localStorage.removeItem("isActive")
        localStorage.removeItem("token")
        return 'failure'
      }
    },
    async getNetworkList() {
      let cache = []
      const headers = { 'Authorization': `Bearer ${this.user.token}` }
      await axios.get(`http://${this.BACKEND}/api/v1/network/`, { headers }).then(
        function (response) {
          cache = response.data
        }
      ).catch(function (error) {
        console.log(error)
      })
      this.network.tableFull = cache
      this.network.tableRender = []
      var idx = Math.ceil(cache.length / this.pagination.range)  // количество записей на одной странице
      this.pagination.count = idx
      for (let i = 0; i < cache.length; i += this.pagination.range) {  // разбивает весь список на подcписки длинной paginationRange
        const chunk = cache.slice(i, i + this.pagination.range)
        this.network.tableRender.push(chunk)
      }
    },
    async addNetworkRow(ip, description) {
      const headers = { 'Authorization': `Bearer ${this.user.token}` }
      await axios.post(`http://${this.BACKEND}/api/v1/network/`, {
        'ip': ip,
        'description': description
      }, { headers }).then().catch(function (error) {
        console.log(error)
      })
    },
    async editNetworkRow(params) {
      let id = params.id
      const headers = { 'Authorization': `Bearer ${this.user.token}` }
      await axios.put(`http://${this.BACKEND}/api/v1/network/${id}`, {
        'ip': params.ip,
        'description': params.description
      }, { headers }).then().catch(function (error) {
        console.log(error)
      })
    },
    async removeNetworkRow(id) {
      let param = id
      const headers = { 'Authorization': `Bearer ${this.user.token}` }
      await axios.delete(`http://${this.BACKEND}/api/v1/network/${param}`, { headers }).then().catch(function (error) {
        console.log(error)
      })
    },
    setPaginationPage(page) {
      this.pagination.currentPage = page
    },
    async getCustomersList() {
      let cache = []
      const headers = { 'Authorization': `Bearer ${this.user.token}` }
      await axios.get(`http://${this.BACKEND}/api/v1/ldap3/users/`, { headers }).then(
        function (response) {
          cache = response.data
        }
      ).catch(function (error) {
        console.log(error)
      })
      this.customers.tableFull = cache
    },
    async getCustomerDescribeInfo(customer) {
      let responseData
      const headers = { 'Authorization': `Bearer ${this.user.token}` }
      await axios.get(`http://${this.BACKEND}/api/v1/ldap3/users/${customer}`, { headers }).then(
        function (response) {
          responseData = response.data
        }
      ).catch(function (error) {
        console.log(error)
      })
      this.customer = responseData
    },
    async getUnitsTree() {
      let responseData
      const headers = { 'Authorization': `Bearer ${this.user.token}` }
      await axios.get(`http://${this.BACKEND}/api/v1/ldap3/organizations/tree`, { headers }).then(
        function (response) {
          responseData = response.data
          console.log(responseData)
        }
      ).catch(function (error) {
        console.log(error)
      })
      this.units = responseData
    }
  },
})
