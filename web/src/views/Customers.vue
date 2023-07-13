<script>
import { defaultStore } from '../stores/counter'

export default {

    setup() {
        const store = defaultStore()
        return { store }
    },
    data() {
        return {
            searchMode: false,
            search: '',
            searchForm: [],  // рендер при поиске
            customer: {},
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
        async getDescribe(CustomerName) {
            let data = await this.store.getCustomerDescribeInfo(CustomerName)
            this.customer = data  // записать новые  
        },
    },
    created() {
        this.store.getCustomersList()
    }
}
</script>

<template>
    <div class="customers">
        <div class="p-3 mx-auto" style="width: 70rem;">
            <div class="d-flex justify-content-center" role="search">
                <input class="form-control me-4" type="search" placeholder="Поиск" aria-label="Search" @mouseout="inputout()" @click="preinput()" @keyup.enter="searchModeOn(search)" v-model="search">
                <button class="btn btn-outline-success" @click="searchModeOn(search)">Найти</button>
                <button v-if="searchMode" class="btn btn-outline-secondary" @click="searchModeOff()">Назад</button>
            </div>
        </div>
        <div class="row">
            <div class="col-3 border-top border-end shadow rounded">
                <table class="table">
                    <thead>
                        <tr>
                            <th scope="col">Атрибут</th>
                            <th scope="col">Описание</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <th>Имя</th>
                            <td>{{ this.customer.name }}</td>
                        </tr>
                        <tr>
                            <th>Описание</th>
                            <td>{{ this.customer.description }}</td>
                        </tr>
                        <tr>
                            <th>IP</th>
                            <td>{{ this.customer.ip }}</td>
                        </tr>
                        <tr>
                            <th>Виден в сети</th>
                            <td>{{ this.customer.last_logon }}</td>
                        </tr>
                        <tr>
                            <th>ОС</th>
                            <td>{{ this.customer.os }} {{ this.customer.version_os }}</td>
                        </tr>
                        <tr>
                            <th>Группы</th>
                            <td>{{ this.customer.member_of ? this.customer.member_of.join(', ') : '' }}</td>
                        </tr>
                        <tr>
                            <th>Подразделение</th>
                            <td>{{ this.customer.unit ? this.customer.unit.join(', ') : '' }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="col-9 customer-container">
                <div v-if="!searchMode" class="row row-cols-auto">
                    <div class="card shadow bg-body-tertiary rounded" v-for="(item, index) in this.store.getCustomersTable.tableFull" :key="index" style="width: 16rem; margin: 0.5em;">
                        <div class="card-body">
                            <h5 class="card-title text-center">{{ item.name }}</h5>
                            <p class="card-card-subtitle text-center text-body-secondary">{{ item.description }}</p>
                        </div>
                        <div class="card-footer text-center">
                            <a class="btn btn-primary align-center" @click="getDescribe(item.name)">Подробнее</a>
                        </div>
                    </div>
                </div>
                <div v-else class="row row-cols-auto justify-content-center">
                    <div class="card shadow bg-body-tertiary rounded" v-for="(item, index) in searchForm" :key="index" style="width: 18rem; margin: 0.5em;">
                        <div class="card-body">
                            <h5 class="card-title text-center">{{ item.name }}</h5>
                            <p class="card-card-subtitle text-center text-body-secondary">{{ item.description }}</p>
                        </div>
                        <div class="card-footer text-center">
                            <a class="btn btn-primary align-center" @click="getDescribe(item.name)">Подробнее</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="less">
.customer-container {
    overflow: auto;
    height: 65rem;
}
</style>