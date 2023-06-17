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
            page: 0
        }
    },
    methods: {
      goPage(number) {
        this.page = number
      },
  },
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
    <div v-if="this.page === 0" class="mx-auto">
      <div class="row">
        <div class="col-3 p-4">
          p1
        </div>
        <div class="col-3 p-4">
          p2
        </div>
        <div class="col-3 p-4">
          p3
        </div>
        <div class="col-3 p-4">
          p4
        </div>
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
