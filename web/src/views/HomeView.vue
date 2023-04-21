<script>
// import Ip from "../components/Ip.vue"
// import { defaultStore } from '../stores/counter'
</script>

<template>
  <div class="main container-fluid bg-secondary bg-gradient text-white">
    <nav class="navbar-header">
      <div  class="navbar-header-item">
        <p>Static Ip</p>
      </div>
      <div class="navbar-header-item">
        <p>Customers</p>
      </div>
      <div class="navbar-header-item">
        <p>Computers</p>
      </div>
      <div class="navbar-header-item">
        <p>Units</p>
      </div>
      <div class="navbar-header-item search" role="search">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
        <button class="btn btn-outline-success" type="submit">Search</button>
      </div>
    </nav>
    <!-- <Ip /> -->
  </div>
</template>

<style lang="less">
// .main {
//   border: 1px solid black;
// }

.navbar-header {
  display: flex;
  justify-content: space-around;
  

  .navbar-header-item {
    margin: 1%;
    // border: 1px solid black;
  }

  .search {
    display: flex;
  }
}


</style>