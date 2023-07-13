<script setup>
import Home from './views/Home.vue'
import Auth from './views/Auth.vue'
import { useRouter } from 'vue-router'
const router = useRouter()

// const store = defaultStore()
// var user = store.user

function logout() {
  localStorage.removeItem("isActive")
  localStorage.removeItem("token")
  router.replace('/auth')
}
</script>

<template>
  <section>
    <nav class="navbar navbar-expand-lg bg-light">
      <div class="container-fluid">
        <a :href="``" class="navbar-brand">
          <router-link to="/" class="router-link">
            <img src="./assets/bootstrap.svg" alt="Bootstrap" width="40" height="30">
          </router-link>
        </a>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="/network" class="router-link">
                <button class="btn btn-light nav-link">Статические адреса</button>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/customers" class="router-link">
                <button class="btn btn-light nav-link">Пользователи</button>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/units" class="router-link">
                <button class="btn btn-light nav-link">Подразделения</button>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/acts" class="router-link">
                <button class="btn btn-light nav-link">Акты</button>
              </router-link>
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
    <section>
      <RouterView />
    </section>
  </section>
  <!-- <AuthView v-else/> -->
  <!-- <Home v-if="user.isActive" />
  <Auth v-else /> -->
</template>
