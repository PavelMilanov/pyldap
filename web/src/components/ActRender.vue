<script>
import { defaultStore } from '../stores/counter'
import { useNotification } from '@kyvg/vue3-notification'
import { useRoute } from 'vue-router'
import VuePdfEmbed from 'vue-pdf-embed'

export default {
    components: {
        VuePdfEmbed,
    },
    setup() {
        const store = defaultStore()
        const notify = useNotification()
        const route = useRoute()
        return { store, notify, route }
    },
    data() {
        return {
            id: 'acts/template.pdf',  // по-умолчанию грузится шаблон,
            actsTable: [],
        }
    },
    watch: {
        $route(to, from) {
            this.render(to)
            this.renderActs()
        },
    },
    methods: {
        async downloadAct(act) {
            await this.store.DownloadAct(act)
        },
        render(data) {
            this.id = data.path + '.pdf'
        },
        async renderActs() {
            let acts = await this.store.getActsTable()
            console.log(acts)
            this.actsTable = acts
        }
    },
    created () {
        this.renderActs()
    }
}
</script>

<template>
    <div class="row">
        <div class="col-4 p-4 d-flex justify-content-center">
            <div class="mx-auto">
                <div class="card shadow rounded mb-3" style="width: 30rem;">
                    <div class="card-body">
                        <h6 class="card-subtitle text-body-secondary d-flex justify-content-center">
                            {{ this.route.params.id == 'template'? 'Шаблон акта': id.slice(6,-4) }}
                        </h6>
                        <p v-if="this.route.params.id == 'template'" class="card-text">Для отображения нужного акта используй поиск. Если акт не отображается - значит его нет в базе данных.</p>
                        <div v-else-if="this.route.params.id != 'template' && this.route.query.act == 'true'">
                            <p class="card-text">Открыть в отдельном<a target="_blank" :href="`http://${this.store.backendUrl}/files/${this.id}`">окне.</a></p>
                            <a class="card-text" href="#" @click="downloadAct(id.slice(6, -4))">Скачать.</a>
                        </div>
                    </div>
                </div>
                    <table class="table table-striped shadow-lg p-3 mb-5 bg-body-tertiary rounded" style="width: 30rem;">
                        <thead class="table-light">
                            <tr>
                                <th scope="col">#</th>
                                <th scope="col">Акт</th>
                                <th scope="col">Описание</th>
                            </tr>
                        </thead>
                        <tbody class="table-group-divider">
                            <tr v-for="(item, index) in this.actsTable" :key="(index)">
                                <th scope="row">{{ (index + 1)}}</th>
                                <td>{{ item.customer }}</td>
                                <td>{{ item.name }}</td>
                            </tr>
                        </tbody>
                    </table>
            </div>
        </div>
        <div class="col-8 p-4 act-area">
            <div v-if="this.route.query.act == 'true'" class="mx-auto d-flex justify-content-center">
                <vue-pdf-embed :width=960 :source="`http://${this.store.backendUrl}/files/${this.id}`" />
            </div>
            <p v-else class="card-text text-center">
                Акт не загружен
            </p>
        </div>
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