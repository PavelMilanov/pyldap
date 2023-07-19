<script>
import { defaultStore } from '../stores/counter'
import { useRouter, useRoute } from 'vue-router'

export default {

    setup() {
        const store = defaultStore()
        const router = useRouter()
        const route = useRoute()
        return { store, router, route }
    },
    data() {
        return {
            customer: {
                name: ''
            },
        }
    },
    methods: {
        async search(name) {
            this.router.push({
                path: `/customers/${name}`,
                // query: { customer: name },
            })
        },
        back() {
            this.router.push('/customers')
            this.customer.name = ''
        },
        preinput() {
            this.customer.name = "customer"  // добавляет текст при начале ввода поиска
        },
        inputout() {
            this.customer.name = ""
        },
    },
}
</script>

<template>
    <div class="customers">
        <div class="p-3 mx-auto" style="width: 70rem;">
            <div class="d-flex justify-content-center" role="search">
                <input class="form-control me-4" type="search" placeholder="Поиск" aria-label="Search" @click="preinput()" @keyup.enter="search(customer.name)" v-model="customer.name">
                <button class="btn btn-outline-success" @click="search(customer.name)">Найти</button>
                <button v-if="this.route.params.id != 'all'" class="btn btn-outline-secondary" @click="back()">Назад</button>
            </div>
        </div>
        <div class="row">
            <RouterView />
        </div>
    </div>
</template>

<style lang="less">

</style>