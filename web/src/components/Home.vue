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
      logout() {
        localStorage.removeItem("isActive")
        localStorage.removeItem("token")
        location.reload()
      }
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
        <a @click="goPage(0)" :href="``" class="navbar-brand">
          <img src="../assets/bootstrap.svg" alt="Bootstrap" width="40" height="30">
        </a>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li @click="goPage(1)" class="nav-item">
              <button class="btn btn-light nav-link">Статические адреса</button>
            </li>
            <li @click="goPage(2)" class="nav-item">
              <button class="btn btn-light nav-link">Пользователи</button>
            </li>
            <li @click="goPage(3)" class="nav-item">
              <button class="btn btn-light nav-link">Подразделения</button>
            </li>
            <li @click="goPage(4)" class="nav-item">
              <button class="btn btn-light nav-link">Акты</button>
            </li>
          </ul>
        </div>
        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
              <button @click="logout()" class="btn btn-light nav-link mx-4">Выход</button>
          </li>
        </ul>
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
                <div class="accordion" id="accordionNavigation">
                    <div class="accordion-item">
                      <h2 class="accordion-header">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                          Статические адреса
                        </button>
                      </h2>
                      <div id="collapseOne" class="accordion-collapse collapse" data-bs-parent="#accordionNavigation">
                        <div class="accordion-body">
                          Таблица для учета статических ip. Большинство ip учитываются на UserGate.
                        </div>
                      </div>
                    </div>
                    <div class="accordion-item">
                      <h2 class="accordion-header">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                          Пользователи
                        </button>
                      </h2>
                      <div id="collapseTwo" class="accordion-collapse collapse" data-bs-parent="#accordionNavigation">
                        <div class="accordion-body">
                          Вывод информации о пользователях AD.
                        </div>
                      </div>
                    </div>
                    <div class="accordion-item">
                      <h2 class="accordion-header">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                          Подразделения
                        </button>
                      </h2>
                      <div id="collapseThree" class="accordion-collapse collapse" data-bs-parent="#accordionNavigation">
                        <div class="accordion-body">
                          Вывод списка подразделений. Так же выводит информацию о пользователях в конкретном подразделдении.
                        </div>
                      </div>
                    </div>
                    <div class="accordion-item">
                      <h2 class="accordion-header">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseFour" aria-expanded="false" aria-controls="collapseThree">
                          Акты
                        </button>
                      </h2>
                      <div id="collapseFour" class="accordion-collapse collapse" data-bs-parent="#accordionNavigation">
                        <div class="accordion-body">
                          Учёт актов. Позволяет добавлять, изменять, удалять акты для конкретного польльзователя.
                        </div>
                      </div>
                    </div>
                </div>
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
