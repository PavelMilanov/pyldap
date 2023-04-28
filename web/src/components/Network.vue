<script>
import { registerRuntimeHelpers } from '@vue/compiler-core'
import { defaultStore } from '../stores/counter'

export default {
   
    setup() {
        const store = defaultStore()
        return { store }
    },
    data() {
        return {
            editable: false,
            form: {
                ip: 'testst',
                description: 'fsdfsd'
            } 
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
    }
}
</script>

<template>
    <div>
        <div class="table-menu p-3 mx-auto" style="width:85%; height: 5%;">
            <form class="d-flex justify-content-start" role="search">
                <button type="button" class="btn btn-primary">btn1</button>
                <button type="button" class="btn btn-primary">btn2</button>
                <input class="form-control me-4" type="search" placeholder="Search" aria-label="Search">
                <button class="btn btn-outline-success" type="submit">Search</button>
          </form>
        </div>
        <div class="p-3 mx-auto" style="width:85%;">
            <table class="table table-hover shadow-lg p-3 mb-5 bg-body-tertiary rounded">
                <thead class="table-light">
                    <tr>
                    <th scope="col">#</th>
                    <th scope="col">Static Ip</th>
                    <th scope="col">Description</th>
                    </tr>
                </thead>
                <tbody class="table-group-divider">
                    <tr>
                    <th scope="row">1</th>
                    <td v-if="editable == false" @dblclick="editValue">{{form.ip}}</td>
                    <td v-else @dblclick="editValue"><input type="text" v-model="form.ip"></td>
                    <td>{{ editable }}</td>
                    </tr>
                    <tr>
                    <th scope="row">2</th>
                    <td>2.2.2.2</td>
                    <td>second</td>
                    </tr>
                </tbody>
            </table>
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