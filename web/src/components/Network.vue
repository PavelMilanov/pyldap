<script>
import { registerRuntimeHelpers } from '@vue/compiler-core'
import { defaultStore } from '../stores/counter'
import AddRow from './modal/AddRow.vue'
import RemoveRow from './modal/RemoveRow.vue'

export default {
    components: {
        AddRow,
        RemoveRow
    },
    setup() {
        const store = defaultStore()
        return { store }
    },
    data() {
        return {
            editable: false,
        }
    },
    methods: {
        editValue() {
            if (this.editable == false) {
                this.editable = true
            }
            else {
                this.editable = false
            }
        },
    },
    created() {
        this.store.getNetworkList()
    },
    updated() {
        this.store.getNetworkList()
    }
}
</script>

<template>
    <div class="network mx-auto" >
        <div class="table-menu p-3 mx-auto" style="height: 5%;">
            <form class="d-flex justify-content-start" role="search">
                <button type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addRow">Добавить</button>
                <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#removeRow">Удалить</button>
                <input class="form-control me-4" type="search" placeholder="Поиск" aria-label="Search">
                <button class="btn btn-outline-success" type="submit">Найти</button>
          </form>
        </div>
        <div class="p-3 mx-auto">
            <table class="table table-hover shadow-lg p-3 mb-5 bg-body-tertiary rounded">
                <thead class="table-light">
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Static Ip</th>
                        <th scope="col">Description</th>
                    </tr>
                </thead>
                <tbody class="table-group-divider">
                    <tr v-for="(item, index) in this.store.getNetworkForms">
                        <th scope="row">{{index+1}}</th>
                        <td v-if="editable == false" @dblclick="editValue">{{item.ip}}</td>
                        <td v-else @dblclick="editValue"><input type="text" v-model="item.ip"></td>
                        <td v-if="editable == false" @dblclick="editValue">{{ item.description }}</td>
                        <td v-else @dblclick="editValue"><input type="text" v-model="item.description"></td>
                    </tr>
                </tbody>
            </table>
            <AddRow />
            <RemoveRow />
        </div>
    </div>
</template>

<style lang="less">

.network {
    width: 85%;
    margin-top: 3%;
}

.d-flex {
    height: 4vh;

    :first-child {
        margin-left: 2%;
        margin-right: 2%;
    }

    :nth-child(2) {
        margin-right: 10%;
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