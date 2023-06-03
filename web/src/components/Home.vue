<script>
import { defaultStore } from '../stores/counter'
import Auth from './Auth.vue'
import Customers from './Customers.vue'
import Computers from './Computers.vue'
import Units from './Units.vue'
import Network from './Network.vue'

export default {

    components: {
        Auth,
        Customers,
        Computers,
        Units,
        Network
    },
    setup() {
        const store = defaultStore()
        return { store }
    },
    data() {
        return {
            component: 0,
        }
    },
    methods: {
    
    },
}
</script>

<template>
    <div>
        <nav class="navbar navbar-expand-lg bg-light">
      <div class="container-fluid">
        <a class="navbar-brand"><img src="../assets/bootstrap.svg" alt="Bootstrap" width="40" height="30"></a>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li @click="this.component = 1" class="nav-item">
              <a class="nav-link" aria-current="page">Статические адреса</a>
            </li>
            <li @click="this.component = 2" class="nav-item">
              <a class="nav-link">Пользователи</a>
            </li>
            <li @click="this.component = 3" class="nav-item">
              <a class="nav-link">Подразделения</a>
            </li>
            <!-- <li class="nav-item">
              <a class="nav-link">Disabled</a>
            </li> -->
          </ul>
        </div>
      </div>
    </nav>
        <Network v-if="this.component === 1"/>
        <Customers v-else-if="this.component === 2"/>
        <!-- <Computers v-else-if="this.component === 3"/> -->
        <Units v-else-if="this.component === 3"/>
    </div>
</template>

<style lang="less">

</style>
