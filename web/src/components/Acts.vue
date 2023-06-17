<script>
import { defaultStore } from '../stores/counter'
import VuePdfEmbed from 'vue-pdf-embed'


export default {
    components: {
        VuePdfEmbed,
    },
    setup() {
        const store = defaultStore()
        return { store }
    },
    data() {
        return {
            searchMode: false,
            act: {
                name: '',
                link: ''
            }
        }
    },
    methods: {
        searchModeOn(link) {
            this.searchMode = true
            this.act.link = link + '.pdf/'
            this.act.name = ""
        },
        searchModeOff() {
            this.searchMode = false
        },
        preinput() {
            this.act.name = "customer"  // добавляет текст при начале ввода поиска
        },
    },
}
</script>

<template>
    <div class="acts mx-auto">
        <div class="p-3 mx-auto" style="width: 70rem;">
            <div class="d-flex justify-content-center" role="search">
                <button type="button" class="btn btn-outline-success" data-bs-toggle="modal" data-bs-target="#addRow">Добавить</button>
                <button type="button" class="btn btn-outline-danger" data-bs-toggle="modal" data-bs-target="#removeRow">Удалить</button>
                <button type="button" class="btn btn-outline-warning" data-bs-toggle="modal" data-bs-target="#editRow">Заменить</button>
                <input class="form-control me-4" type="search" placeholder="Поиск" aria-label="Search" @click="preinput()" @keyup.enter="searchModeOn(act.name)" v-model="act.name">
                <button class="btn btn-outline-success" @click="searchModeOn(act.name)">Найти</button>
                <button v-if="searchMode" class="btn btn-outline-secondary" @click="searchModeOff()">Назад</button>
            </div>
        </div>
        <div class="mx-auto">
            <vue-pdf-embed v-if="searchMode" :source="`http://${this.store.backendUrl}/files/acts/${this.act.link}`" />
        </div>
    </div>
</template>

<style lang="less">
</style>
