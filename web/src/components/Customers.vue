<script>
import { defaultStore } from '../stores/counter'

export default {
    // components: {
    //     Auth,
    //     RootMenu,
    //     VerticalMenu
    // },
    setup() {
        const store = defaultStore()
        return { store }
    },
    data() {
        return {
            searchMode: false,
            search: '',
            searchForm: [],  // рендер при поиске
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
            console.log(cache)
        },
        searchModeOff() {
            this.searchMode = false
            this.search = ''
            this.store.getCustomersList()
        },
    },
    created() {
        this.store.getCustomersList()
    }
}
</script>

<template>
    <div class="customers mx-auto">
        <div class="p-3 mx-auto" style="height: 5%;">
            <div class="d-flex justify-content-start" role="search">
                <button type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addRow">Добавить</button>
                <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#removeRow">Удалить</button>
                <button type="button" class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#editRow">Редактировать</button>
                <input class="form-control me-4" type="search" placeholder="Поиск" aria-label="Search" @keyup.enter="searchModeOn(search)" v-model="search">
                <button class="btn btn-outline-success" @click="searchModeOn(search)">Найти</button>
                <button v-if="searchMode" class="btn btn-info" @click="searchModeOff()">Назад</button>
            </div>
        </div>
        <div class="p-3 mx-auto">
            <div v-if="!searchMode" class="row row-cols-auto justify-content-center">
                <div class="card shadow p-3 mb-5 bg-body-tertiary rounded" v-for="(item, index) in this.store.getCustomersTable.tableFull" :key="index" style="width: 18rem; margin: 0.5em;">
                    <div class="card-body">
                        <h5 class="card-title">{{ item.name }}</h5>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item">{{ item.member_of }}</li>
                            <li class="list-group-item">{{ item.description }}</li>
                        </ul>
                        <a class="btn btn-primary">Подробнее</a>
                    </div>
                </div>
            </div>
            <div v-else class="row row-cols-auto justify-content-center">
                <div class="card shadow p-3 mb-5 bg-body-tertiary rounded" v-for="(item, index) in searchForm" :key="index" style="width: 18rem; margin: 0.5em;">
                    <div class="card-body">
                        <h5 class="card-title">{{ item.name }}</h5>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item">{{ item.member_of }}</li>
                            <li class="list-group-item">{{ item.description }}</li>
                        </ul>
                        <a class="btn btn-primary">Подробнее</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="less">

</style>