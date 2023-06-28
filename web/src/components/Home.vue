<script>
import { defaultStore } from '../stores/counter'
import Auth from './Auth.vue'
import Customers from './Customers.vue'
import Acts from './Acts.vue'
import Units from './Units.vue'
import Network from './Network.vue'

export default {

    components: {
        Auth,
        Customers,
        Acts,
        Units,
        Network
    },
    setup() {
        const store = defaultStore()
        return { store }
    },
    data() {
        return {
          page: 0,
        }
    },
    methods: {
      goPage(number) {
        this.page = number
      },
  },
  created() {
    this.store.getCustomersList()
  }
}
</script>

<template>
  <div>
    <nav class="navbar navbar-expand-lg bg-light">
      <div class="container-fluid">
        <a @click="goPage(0)" class="navbar-brand">
          <img src="../assets/bootstrap.svg" alt="Bootstrap" width="40" height="30">
        </a>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li @click="goPage(1)" class="nav-item">
              <a class="nav-link">Статические адреса</a>
            </li>
            <li @click="goPage(2)" class="nav-item">
              <a class="nav-link">Пользователи</a>
            </li>
            <li @click="goPage(3)" class="nav-item">
              <a class="nav-link">Подразделения</a>
            </li>
            <li @click="goPage(4)" class="nav-item">
              <a class="nav-link">Акты</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div v-if="this.page === 0" class="mb-3 mx-auto">
      <div class="home container-fluid text-center">
        <div class="p-3 row">
          <div class="col-6">
            <div class="card">
              <div class="card-header">
                <p class="card-title">Навигация</p>
              </div>
              <div class="card-body">
                <ol class="list-group list-group-numbered">
                  <li class="list-group-item">Статические адреса</li>
                  <li class="list-group-item">Пользователи</li>
                  <li class="list-group-item">Подразделения</li>
                  <li class="list-group-item">Акты</li>
                </ol>
              </div>
            </div>
          </div>
          <div class="col-6">
            <div class="card">
              <div class="card-header">
                <p class="card-title">Инфо</p>
              </div>
              <div class="body">
                <p class="card-text m-2">Всего пользователей: {{ this.store.getCustomersCount }}</p>
              </div>
            </div>
          </div>
          <!-- <div class="col-4">
            <div class="card">
              <p class="card-title"></p>
            </div>
          </div> -->
        </div>
        <!-- <div class="p-3 row">
          <div class="col-4">
            <div class="card">
              <p class="card-title"></p>
            </div>
          </div>
        </div> -->
      </div>
    </div>
    <Network v-else-if="this.page === 1"/>
    <Customers v-else-if="this.page === 2"/>
    <Units v-else-if="this.page === 3"/>
    <Acts v-else-if="this.page === 4"/>
  </div>
</template>

<style lang="less">
</style>
