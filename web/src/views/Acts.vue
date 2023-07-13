<script>
import { defaultStore } from '../stores/counter'
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
        return { store }
    },
    data() {
        return {
            searchMode: false,
            act: {
                name: '',
                link: 'template.pdf',  // по-умолчанию грузится шаблон
                displayName: 'Шаблон акта' 
            },
        }
    },
    methods: {
        searchModeOn(link) {
            this.searchMode = true
            this.act.link = link + '.pdf'
            this.act.name = ""
            this.act.displayName = link
        },
        searchModeOff() {
            this.searchMode = false
            this.act.link = 'template.pdf'
            this.act.displayName = 'Шаблон акта'
        },
        preinput() {
            this.act.name = "customer"  // добавляет текст при начале ввода поиска
        },
        inputout() {
            this.search = ""
        },
        async downloadAct(act) {
            await this.store.DownloadAct(act)
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
                <input class="form-control me-4" type="search" placeholder="Поиск" aria-label="Search" @click="preinput()" @keyup.enter="searchModeOn(act.name)" v-model="act.name">
                <button class="btn btn-outline-success" @click="searchModeOn(act.name)">Найти</button>
                <button v-if="searchMode" class="btn btn-outline-secondary" @click="searchModeOff()">Назад</button>
            </div>
        </div>
        <div class="row">
            <div class="col-4 p-4 d-flex justify-content-center">
                <div class="mx-auto">
                    <div class="card shadow rounded" style="width: 30rem;">
                        <div class="card-body">
                            <h6 class="card-subtitle text-body-secondary d-flex justify-content-center">
                                {{ act.displayName }}
                            </h6>
                            <p v-if="!searchMode" class="card-text">Для отображения нужного акта используй поиск. Если акт не отображается - значит его нет в базе данных.</p>
                            <div v-else>
                                <p class="card-text">Открыть в отдельном<a target="_blank" :href="`http://${this.store.backendUrl}/files/acts/${this.act.link}`">окне.</a></p>
                                <a class="card-text" href="#" @click="downloadAct(act.displayName)">Скачать.</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-8 p-4 act-area">
                <div class="mx-auto d-flex justify-content-center">
                    <vue-pdf-embed :width=960 :source="`http://${this.store.backendUrl}/files/acts/${this.act.link}`" />
                </div>
            </div>
        </div>
        <AddAct />
        <ChangeAct />
        <RemoveAct />
        <notifications position="bottom left" width="300" />
    </div>
</template>

<style lang="less">
canvas {
    border: 1px solid rgba(34, 60, 80, 0.2);
    box-shadow: 0px 5px 10px 5px rgba(34, 60, 80, 0.2);
    border-radius: 5px;
}

.act-area {
    height: 160rem;
}
</style>
