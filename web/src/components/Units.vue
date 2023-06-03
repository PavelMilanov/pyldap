<script>
import { defaultStore } from '../stores/counter'

export default {
    // components: {
    //     Auth,
    //     RootMenu,
    //     VerticalMenu
    // },
    setup() {
        const store = defaultStore()
        return { store }
    },
    data() {
        return {
        }
    },
    methods: {

    },
    created() {
        this.store.getUnitsTree()
    }
}
</script>

<template>
    <div class="p-5 mx-auto">
        <nav style="--bs-breadcrumb-divider: '>';" aria-label="breadcrumb">
            <ol v-for="(subtree, tree) in this.store.getUnits" :key="tree" class="breadcrumb">
                <li class="breadcrumb-item">{{ tree }}</li>
                <li class="breadcrumb-item" aria-current="page">
                    <ol v-for="(item, index) in subtree" :key="index" class="breadcrumb">
                        <li class="breadcrumb-item">{{ item }}</li>
                    </ol>
                </li>
            </ol>
        </nav>
    </div>
</template>

<style lang="less">
.breadcrumb-item+.breadcrumb-item::before {  // для выравнивания элементов после ">"
    padding-right: 0;
}
</style>