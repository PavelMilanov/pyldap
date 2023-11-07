import { defineStore } from 'pinia'
import axios from 'axios'
import download from 'downloadjs'

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
      customersAll: [],
      computersAll: [],
      all: [],
      pageCount: Math.ceil(localStorage.customersCount / 20)
    },
    units: {
      tree: {},
    },
    customersCount: localStorage.customersCount,
    BACKEND: import.meta.env.VITE_APP_BACKEND
  }),
  getters: {
    getUser: (state) => state.user,
    getNetworkTable: (state) => state.network,
    getPaginationInfo: (state) => state.pagination,
    getCustomersTable: (state) => state.customers,
    getUnits: (state) => state.units.tree,
    getCustomersCount: (state) => state.customersCount,
    backendUrl: (state) => state.BACKEND,
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
        localStorage.removeItem("isActive")
        localStorage.removeItem("token")
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
    async getComputersandCustomers(skip, limit) {
      let cache = []
      const headers = { 'Authorization': `Bearer ${this.user.token}` }
      await axios.get(`http://${this.BACKEND}/api/v1/ldap3/users/all/customers/info`, { headers, params: { skip: skip, limit: limit } }).then(
        function (response) {
          cache = response.data
        }
      ).catch(function (error) {
        console.log(error)
        localStorage.removeItem("isActive")
        localStorage.removeItem("token")
      })
      this.customers.all = cache
      return cache
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
        localStorage.removeItem("isActive")
        localStorage.removeItem("token")
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
    async getComputersList(skip, limit) {
      let cache = []
      const headers = { 'Authorization': `Bearer ${this.user.token}` }
      await axios.get(`http://${this.BACKEND}/api/v1/ldap3/computers/all`, { headers, params: { skip: skip, limit: limit } }).then(
        function (response) {
          cache = response.data
        }
      ).catch(function (error) {
        console.log(error)
        localStorage.removeItem("isActive")
        localStorage.removeItem("token")
      })
      this.customers.computersAll
      return cache
    },
    async addNetworkRow(ip, description) {
      const headers = { 'Authorization': `Bearer ${this.user.token}` }
      await axios.post(`http://${this.BACKEND}/api/v1/network/`, {
        'ip': ip,
        'description': description
      }, { headers }).then(
        function (response) {
          console.log(response)
        }).catch(function (error) {
          console.log(error)
          localStorage.removeItem("isActive")
          localStorage.removeItem("token")
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
        localStorage.removeItem("isActive")
        localStorage.removeItem("token")
      })
    },
    async removeNetworkRow(id) {
      let param = id
      const headers = { 'Authorization': `Bearer ${this.user.token}` }
      await axios.delete(`http://${this.BACKEND}/api/v1/network/${param}`, { headers }).then().catch(function (error) {
        console.log(error)
        localStorage.removeItem("isActive")
        localStorage.removeItem("token")
      })
    },
    setPaginationPage(page) {
      this.pagination.currentPage = page
    },
    async getCustomer(customer) {
      let responseData
      const headers = { 'Authorization': `Bearer ${this.user.token}` }
      await axios.get(`http://${this.BACKEND}/api/v1/ldap3/users/${customer}`, { headers }).then(
        function (response) {
          responseData = response.data
        }
      ).catch(function (error) {
        console.log(error)
        localStorage.removeItem("isActive")
        localStorage.removeItem("token")
      })
      return responseData
    },
    async getCustomersList() {
      let cache
      // let responseHeader
      const headers = { 'Authorization': `Bearer ${this.user.token}` }
      await axios.get(`http://${this.BACKEND}/api/v1/ldap3/users/count`, { headers }).then(
        function (response) {
          cache = response.data
          console.log(cache)
          // responseHeader = response.headers['x-customers-count']
        }
      ).catch(function (error) {
        console.log(error)
        localStorage.removeItem("isActive")
        localStorage.removeItem("token")
      })
      // this.customers.customersAll = cache
      localStorage.customersCount = cache
      return cache
    },
    async getCustomerDescribeInfo(customer) {
      let responseData
      let responseHeader
      const headers = { 'Authorization': `Bearer ${this.user.token}` }
      await axios.get(`http://${this.BACKEND}/api/v1/ldap3/users/${customer}/info`, { headers }).then(
        function (response) {
          responseData = response.data
          responseHeader = response.headers['x-customer-act']
        }
      ).catch(function (error) {
        console.log(error)
        localStorage.removeItem("isActive")
        localStorage.removeItem("token")
      })
      responseData['act'] = responseHeader
      return responseData
    },
    async getUnitsTree() {
      let responseData
      const headers = { 'Authorization': `Bearer ${this.user.token}` }
      await axios.get(`http://${this.BACKEND}/api/v1/ldap3/organizations/tree`, { headers }).then(
        function (response) {
          responseData = response.data
        }
      ).catch(function (error) {
        console.log(error)
        localStorage.removeItem("isActive")
        localStorage.removeItem("token")
      })
      this.units.tree = responseData
    },
    async GetUnitComputersList(unit) {
      let responseData
      const headers = { 'Authorization': `Bearer ${this.user.token}`}
      await axios.get(`http://${this.BACKEND}/api/v1/ldap3/organizations/${unit}`, { headers }).then(
        function (response) {
          responseData = response.data
        }
      ).catch(function (error) {
        console.log(error)
        localStorage.removeItem("isActive")
        localStorage.removeItem("token")
      })
      return responseData
    },
    async DownloadAct(customer) {
      const headers = { 'Authorization': `Bearer ${this.user.token}`, 'Content-Type': 'multipart/form-data' }
      await axios.get(`http://${this.BACKEND}/api/v1/files/act/${customer}/download`, { headers, responseType: 'blob' }).then(
        function (response) {
          const content = response.headers['content-type']
          download(response.data, customer, content)
        }
      ).catch(function (error) {
        console.log(error)
      })
    },
    async UploadAct(data, customer) {
      const headers = { 'Authorization': `Bearer ${this.user.token}`, 'Content-Type': 'multipart/form-data' }
      let formData = new FormData()
      formData.append('file', data)
      await axios.post(`http://${this.BACKEND}/api/v1/files/act/${customer}/upload`, formData, { headers }).then(
        function (response) {
          console.log(response)
        }
      ).catch(function (error) {
        console.log(error)
      })
    },
    async ChangeAct(data, customer) {
      const headers = { 'Authorization': `Bearer ${this.user.token}`, 'Content-Type': 'multipart/form-data' }
      let formData = new FormData()
      formData.append('file', data)
      await axios.put(`http://${this.BACKEND}/api/v1/files/act/${customer}/change`, formData, { headers }).then(
        function (response) {
          console.log(response)
        }
      ).catch(function (error) {
        console.log(error)
      })
    },
    async removeAct(customer) {
      const headers = { 'Authorization': `Bearer ${this.user.token}` }
      await axios.delete(`http://${this.BACKEND}/api/v1/files/act/${customer}/delete`, { headers }).then(
        function (response) {
          console.log(response)
        }).catch(function (error) {
        console.log(error)
      })
    },
    getAllMessages() {
      var cache = []
      const headers = { 'Authorization': `Bearer ${this.user.token}` }
      axios.get(`http://${this.BACKEND}/api/v1/network/netclient/messages`, { headers }).then(
        function (response) {
          cache = response.data
          cache.pop()  // удаляется последний элемент, последний элемент получается по веб-сокету
          cache.forEach(element => {  // загружаются все сообщения из кеша
            var message = element.time + ": " + element.client + " " + element.message
            document.querySelector("#Logon-log").value += message + "\n"
          })
        }).catch(function (error) {
          console.log(error)
        })
    },
  },
})
