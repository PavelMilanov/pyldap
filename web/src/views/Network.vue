<script>
import { defaultStore } from '../stores/counter'
import AddRow from '../components/AddRow.vue'
import EditRow from '../components/EditRow.vue'
import RemoveRow from '../components/RemoveRow.vue'

export default {
    components: {
        AddRow,
        EditRow,
        RemoveRow,
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
            tableIndex: 1,
        }
    },
    methods: {
        searchModeOn(search) {
            if (this.searchMode == false) {
                this.searchMode = true
            }
            var cache = []
            var data = this.store.getNetworkTable.tableFull
            data.forEach(function (item) {
                if (item.ip == search || item.description.toLowerCase().includes(search.toLowerCase())) {
                    cache.push({
                        "ip": item.ip,
                        "description": item.description
                    })
                }
            })
            this.searchForm = cache
        },
        searchModeOff() {
            this.searchMode = false
            this.search = ''
            this.store.getNetworkList()
        },
        changePage(index, currentPage) {
            this.store.setPaginationPage(index)
            this.tableIndex = currentPage
        },
    },
    created() {
        this.store.getNetworkList()
    }
}
</script>

<template>
    <div class="network mx-auto" >
        <div class="p-3 mx-auto">
            <div class="d-flex justify-content-start" role="search">
                <button type="button" class="btn btn-outline-success" data-bs-toggle="modal" data-bs-target="#addRow">Добавить</button>
                <button type="button" class="btn btn-outline-danger" data-bs-toggle="modal" data-bs-target="#removeRow">Удалить</button>
                <button type="button" class="btn btn-outline-warning" data-bs-toggle="modal" data-bs-target="#editRow">Редактировать</button>
                <input class="form-control me-4" type="search" placeholder="Поиск" aria-label="Search" @keyup.enter="searchModeOn(search)" v-model="search">
                <button class="btn btn-outline-success" @click="searchModeOn(search)">Найти</button>
                <button v-if="searchMode" class="btn btn-outline-secondary" @click="searchModeOff()">Назад</button>  <!--Для того, чтобы выйти из режима редактирования-->
            </div>
        </div>
        <div class="p-3 mx-auto">
            <table class="table table-hover table-striped shadow-lg p-3 mb-5 bg-body-tertiary rounded">
                <thead class="table-light">
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Ip адрес</th>
                        <th scope="col">Описание</th>
                    </tr>
                </thead>
                <tbody v-if="!searchMode" class="table-group-divider">
                    <tr v-for="(item, index) in this.store.getNetworkTable.tableRender[this.store.getPaginationInfo.currentPage]" :key="(index)">
                        <th scope="row">{{ (index + 1) + (this.store.getPaginationInfo.currentPage * this.store.getPaginationInfo.range ) }}</th>  <!-- Генерация сквозной нумерации -->
                        <td>{{ item.ip }}</td>
                        <td>{{ item.description }}</td>
                    </tr>
                </tbody>
                <tbody v-else class="table-group-divider">
                    <tr v-for="(item, index) in searchForm" :key="(index)">
                        <th scope="row">{{ index + 1 }}</th>
                        <td>{{ item.ip }}</td>
                        <td>{{ item.description }}</td>
                    </tr>
                </tbody>
            </table>
            <nav v-if="!searchMode" aria-label="Page navigation example">
                <ul class="pagination justify-content-center">
                    <li class="page-item " :class="{ 'disabled': this.tableIndex == 1 }" @click="changePage(0, 1)">
                    <a class="page-link" aria-label="Previous">
                        <span aria-hidden="true">&laquo;</span>
                    </a>
                    </li>
                    <li v-for="(page, index) in this.store.getPaginationInfo.count" :key="index" @click="changePage(index, page)" class="page-item">
                        <button class="btn btn-primary page-link">{{ page }}</button>
                    </li>
                    <li class="page-item" :class="{ 'disabled': this.tableIndex == this.store.getPaginationInfo.count }" @click="changePage(this.store.getPaginationInfo.count-1, this.store.getPaginationInfo.count)">
                    <button class="btn btn-primary page-link" aria-label="Next">
                        <span aria-hidden="true">&raquo;</span>
                    </button>
                    </li>
                </ul>
            </nav>
            <AddRow />
            <EditRow />
            <RemoveRow />
            <notifications position="bottom right" width="300" />
        </div>
    </div>
</template>

<style lang="less">

.d-flex {
    height: 4vh;

    :first-child {
        margin-left: 2%;
        margin-right: 2%;
    }

    :nth-child(2) {
        margin-right: 2%;
    }

    :nth-child(3) {
        margin-right: 10%;
    }

    :last-child {
        margin-left: 2%;
    }

    .form-control {
        width: 30%;
    }
}

th:first-child {
    width: 6vh;
}

th:nth-child(2) {
    width: 20vh;
}

th:last-child {
    width: 50vh;
}

</style>