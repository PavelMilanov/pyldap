<script>
import { defaultStore } from '../stores/counter'
import CustomerDescribe from './modal/CustomerDescribe.vue'


export default {
    components: {
        CustomerDescribe,
    },
    setup() {
        const store = defaultStore()
        return { store }
    },
    data() {
        return {
            searchMode: false,
            search: '',
            searchForm: [],  // рендер при поиске
            CustomerName: '',
        }
    },
    methods: {
        searchModeOn(search) {
            if (this.searchMode == false) {
                this.searchMode = true
            }
            var cache = []
            var data = this.store.getCustomersTable.tableFull
            data.forEach(function (item) {
                if (item.name.includes(search)) {
                    cache.push({
                        "name": item.name,
                        "description": item.description,
                        "last_logon": item.last_logon,
                        "member_of": item.member_of
                    })
                }
            })
            this.searchForm = cache
        },
        searchModeOff() {
            this.searchMode = false
            this.search = ''
            this.store.getCustomersList()
        },
        preinput() {
            this.search = "customer"  // добавляет текст при начале ввода поиска
        },
        inputout() {
            this.search = ""
        },
        getDescribe(CustomerName) {
            this.CustomerName = CustomerName
        },
        downloadAct(CustomerName) {
            this.store.GetAct(CustomerName)
        },
    },
    created() {
        // this.store.getCustomersList() // отрисовка списка при логе в приложении 1 раз
    }
}
</script>

<template>
    <div class="customers mx-auto">
        <div class="p-3 mx-auto" style="width: 70rem;">
            <div class="d-flex justify-content-center" role="search">
                <input class="form-control me-4" type="search" placeholder="Поиск" aria-label="Search" @mouseout="inputout()" @click="preinput()" @keyup.enter="searchModeOn(search)" v-model="search">
                <button class="btn btn-outline-success" @click="searchModeOn(search)">Найти</button>
                <button v-if="searchMode" class="btn btn-outline-secondary" @click="searchModeOff()">Назад</button>
            </div>
        </div>
        <div class="mx-auto">
            <div v-if="!searchMode" class="row row-cols-auto justify-content-center">
                <div class="card shadow p-3 mb-3 bg-body-tertiary rounded" v-for="(item, index) in this.store.getCustomersTable.tableFull" :key="index" style="width: 18rem; margin: 0.5em;">
                    <div class="card-body">
                        <h5 class="card-title text-center">{{ item.name }}</h5>
                        <p class="card-card-subtitle text-center text-body-secondary">{{ item.description }}</p>
                    </div>
                    <div class="card-footer text-center">
                        <a class="btn btn-primary align-center" data-bs-toggle="modal" data-bs-target="#CustomerDescribe" @click="getDescribe(item.name)">Подробнее</a>
                    </div>
                </div>
            </div>
            <div v-else class="row row-cols-auto justify-content-center">
                <div class="card shadow p-3 mb-5 bg-body-tertiary rounded" v-for="(item, index) in searchForm" :key="index" style="width: 18rem; margin: 0.5em;">

                    <div class="card-body">
                        <h5 class="card-title text-center">{{ item.name }}</h5>
                        <p class="card-card-subtitle text-center text-body-secondary">{{ item.description }}</p>
                    </div>
                    <div class="card-footer text-center">
                        <a class="btn btn-primary align-center" data-bs-toggle="modal" data-bs-target="#CustomerDescribe" @click="getDescribe(item.name)">Подробнее</a>
                    </div>
                </div>
            </div>
        </div>
        <CustomerDescribe :name="this.CustomerName"/>
    </div>
</template>

<style lang="less">

</style>