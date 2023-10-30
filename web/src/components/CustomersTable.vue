<script>
import { defaultStore } from '../stores/counter'
import { useRouter, useRoute } from 'vue-router'


export default {

    setup() {
        const store = defaultStore()
        // const notify = useNotification()
        const route = useRoute()
        return { store, route }
    },
    data() {
        return {
            searchMode: true,
        }
    },
    watch: {
        $route(to, from) {
            if (to.query.name.startsWith('customer')) {
                this.renderCustomer(to.query.name)
            } else {
                this.renderTable()
            }
        },
    },
    methods: {
        async renderCustomer(name) {
            let data = await this.store.getCustomerDescribeInfo(name)
            this.store.getCustomersTable.all = [data]
            this.searchMode = false
        },
        async renderTable() {
            let data = await this.store.getComputersandCustomers(0, 20)
            this.store.getCustomersTable.all = data
            this.searchMode = true
        },
        async changePage(skip, limit) {
            let data = await this.store.getComputersandCustomers(skip, limit)
            this.store.getCustomersTable.all = data
        }
    },
}
</script>

<template>
    <div class="p-3 mx-auto">
        <table class="table table-hover table-striped shadow-lg p-3 mb-5 bg-body-tertiary rounded">
            <thead class="table-light">
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Имя</th>
                    <th scope="col">Описание</th>
                    <th scope="col">Подразделение</th>
                    <th scope="col">IP</th>
                    <th scope="col">MAC</th>
                    <th scope="col">ОС</th>
                    <th scope="col">Группы</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in this.store.getCustomersTable.all" :key="(index)">
                    <th scope="row">{{ index + 1 }}</th>  <!-- Генерация сквозной нумерации -->
                    <td>{{ item.name }}</td>
                    <td>{{ item.description }}</td>
                    <td>{{ item.unit ? item.unit.join(', ') : '-' }}</td>
                    <td>{{ item.ip ? item.ip : '-' }}</td>
                    <td>{{ item.ip ? item.ip : '-' }}</td>
                    <td>{{ item.os + ' ' + item.version_os }}</td>
                    <td>{{ item.member_of ? item.member_of.join(', ') : '-' }}</td>
                </tr>
            </tbody>
        </table>
        <nav v-if="searchMode" aria-label="Page navigation example">
            <ul class="pagination justify-content-center">
                <li class="page-item" @click="changePage(0, 20)">
                <a class="page-link" aria-label="Previous">
                    <span aria-hidden="true">&laquo;</span>
                </a>
                </li>
                <li v-for="(page, index) in this.store.getCustomersTable.pageCount" :key="index" @click="changePage(20*index,20*index+20)" class="page-item">
                    <button class="btn btn-primary page-link">{{ page }}</button>
                </li>
                <li class="page-item" @click="changePage(20 * (this.store.getCustomersTable.pageCount-1), 20 * (this.store.getCustomersTable.pageCount-1) + 20)">
                <button class="btn btn-primary page-link" aria-label="Next">
                    <span aria-hidden="true">&raquo;</span>
                </button>
                </li>
            </ul>
        </nav>
    </div>
</template>

<style lang="less">

</style>