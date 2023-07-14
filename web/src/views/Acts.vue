<script>
import { defaultStore } from '../stores/counter'
import { useRouter, useRoute } from 'vue-router'
import VuePdfEmbed from 'vue-pdf-embed'
import AddAct from '../components/AddAct.vue'
import ChangeAct from '../components/ChangeAct.vue'
import RemoveAct from '../components/RemoveAct.vue'

export default {
    components: {
        VuePdfEmbed,
        AddAct,
        ChangeAct,
        RemoveAct
    },
    setup() {
        const store = defaultStore()
        const router = useRouter()
        const route = useRoute()
        return { store, router, route }
    },
    data() {
        return {
            act: {
                name: '',

            },
        }
    },
    methods: {
        async search(link) {
            let customer = await this.getCustomerInfo(link)
            this.router.push({
                path: `/acts/${link}`,
                query:  {act: customer['act']},
            })
        },
        back() {
            this.router.push('/acts')
            this.act.name = ''
        },
        preinput() {
            this.act.name = "customer"  // добавляет текст при начале ввода поиска
        },
        inputout() {
            this.search = ""
        },
        async getCustomerInfo(CustomerName) {
            let data = await this.store.getCustomerDescribeInfo(CustomerName)
            return data
        },
    },
}
</script>

<template>
    <div class="acts mx-auto">
        <div class="p-4 mx-auto" style="width: 70rem;">
            <div class="d-flex justify-content-center" role="search">
                <button type="button" class="btn btn-outline-success" data-bs-toggle="modal" data-bs-target="#addAct">Добавить</button>
                <button type="button" class="btn btn-outline-danger" data-bs-toggle="modal" data-bs-target="#removeAct">Удалить</button>
                <button type="button" class="btn btn-outline-warning" data-bs-toggle="modal" data-bs-target="#changeAct">Заменить</button>
                <input class="form-control me-4" type="search" placeholder="Поиск" aria-label="Search" @click="preinput()" @keyup.enter="search(act.name)" v-model="act.name">
                <button class="btn btn-outline-success" @click="search(act.name)">Найти</button>
                <button v-if="this.route.params.id != 'template'" class="btn btn-outline-secondary" @click="back()">Назад</button>
            </div>
        </div>
        <div class="row">
            <RouterView />
        </div>
        <AddAct />
        <ChangeAct />
        <RemoveAct />
        <notifications position="bottom left" width="300" />
    </div>
</template>

<style lang="less">

</style>
