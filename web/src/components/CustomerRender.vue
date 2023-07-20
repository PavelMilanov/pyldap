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
            customerList: this.store.customers.tableFull, 
            customer: {},
            customerInfo: {},
            customerCount: 20
        }
    },
    watch: {
        $route(to, from) {
            this.renderCustomer(to.params.id)
        },
    },
    methods: {
        async renderCustomer(name) {
            let data = await this.store.getCustomer(name)
            this.customer = data
        },
        async renderCustomers(skip=0, limit=20) {
            if (this.store.customers.tableFull.length == 0) {
                await this.store.getCustomersList(skip, limit)
                this.customerCount += limit
            } else {
                await this.store.getCustomersList(skip, limit)
                this.customerCount += limit
            }
        },
        async getDescribe(CustomerName) {
            let data = await this.store.getCustomerDescribeInfo(CustomerName)
            this.customerInfo = data  // записать новые  
        },
    },
    created() {
        this.renderCustomers()
    }
}
</script>

<template>
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
                        <td>{{ this.customerInfo.name }}</td>
                    </tr>
                    <tr>
                        <th>Описание</th>
                        <td>{{ this.customerInfo.description }}</td>
                    </tr>
                    <tr>
                        <th>IP</th>
                        <td>{{ this.customerInfo.ip }}</td>
                    </tr>
                    <tr>
                        <th>ОС</th>
                        <td>{{ this.customerInfo.os }} {{ this.customerInfo.version_os }}</td>
                    </tr>
                    <tr>
                        <th>Группы</th>
                        <td>{{ this.customerInfo.member_of ? this.customerInfo.member_of.join(', ') : '' }}</td>
                    </tr>
                    <tr>
                        <th>Подразделение</th>
                        <td>{{ this.customerInfo.unit ? this.customerInfo.unit.join(', ') : '' }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="col-9 customer-container">
            <div v-if="this.route.params.id == 'all'" class="row row-cols-auto justify-content-center">
                <div class="card shadow bg-body-tertiary rounded" v-for="(item, index) in this.store.customers.tableFull" :key="index"
                    style="width: 18rem; margin: 0.5em;">
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
                <div class="card shadow bg-body-tertiary rounded" style="width: 18rem; margin: 5em;">
                    <div class="card-body">
                        <h5 class="card-title text-center">{{ customer.name }}</h5>
                        <p class="card-card-subtitle text-center text-body-secondary">{{ customer.description }}</p>
                    </div>
                    <div class="card-footer text-center">
                        <a class="btn btn-primary align-center" @click="getDescribe(customer.name)">Подробнее</a>
                    </div>
                </div>
            </div>
            <div v-if="this.customerList && this.route.params.id == 'all'" class="card-footer text-center" style="margin: 2rem;">
                <a class="btn btn-primary align-center" @click="renderCustomers(0, this.customerCount)">Загрузить больше</a>
            </div>
        </div>
    </div>
</template>

<style lang="less">
// .customer-container {
//     overflow: auto;
//     height: 65rem;
// }
</style>