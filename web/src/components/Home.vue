<script>
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
        // const store = defaultStore()
        // return { store }
    },
    data() {
        return {
            component: 0
        }
    },
    methods: {
    
    }
}
</script>

<template>
    <div>
        <div class="main container-fluid bg-primary bg-gradient text-white">
            <nav class="navbar-header">
                <div @click="this.component = 0" class="navbar-header-item">
                    <p>Home</p>
                </div>
                <div @click="this.component = 1" class="navbar-header-item">
                    <p>Network</p>
                </div>
                <div @click="this.component = 2" class="navbar-header-item">
                    <p>Customers</p>
                </div>
                <div @click="this.component = 3" class="navbar-header-item">
                    <p>Computers</p>
                </div>
                <div @click="this.component = 4" class="navbar-header-item">
                    <p>Units</p>
                </div>
                <!-- <div class="navbar-header-item search" role="search">
                    <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                    <button class="btn btn-outline-success" type="submit">Search</button>
                </div> -->
            </nav>
        </div>
        <Network v-if="this.component === 1"/>
        <Customers v-else-if="this.component === 2"/>
        <Computers v-else-if="this.component === 3"/>
        <Units v-else-if="this.component === 4"/>
    </div>
</template>

<style lang="less">
.navbar-header {
    display: flex;
    justify-content: space-around;
    height: 7vh;

    .navbar-header-item {
        margin: 1%;
    }

    .search {
        display: flex;
    }

    div > p {
        position: relative;
        top: 19%;
    }

    div:hover {
        border: 1.5px solid rgb(238, 238, 238);
        border-radius: 10%;
    }
}

</style>
