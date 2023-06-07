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
            computers: [],
            unitId: ''
        }
    },
    methods: {
        async getComputers(unit) {
            this.unitId = unit
            let data = await this.store.GetUnitComputersList(unit)
            this.computers = data
        }

    },
    created() {
        this.store.getUnitsTree()
    }
}
</script>

<template>
    <div class="row">
      <div class="col-2">
        <nav id="navbar-unit" class="h-100 flex-column align-items-stretch pe-4 border-end">
          <nav class="nav nav-pills flex-column" v-for="(subtree, tree) in this.store.getUnits" :key="tree">
            <a class="nav-link" :href="`#${tree}`" @click="getComputers(tree)">{{ tree }}</a>
            <nav class="nav nav-pills flex-column" v-for="(item, index) in subtree" :key="index">
              <a class="nav-link ms-3 my-1" :href="`#${tree}-${item}`" @click="getComputers(`${tree}-${item}`)">{{ item }}</a>
            </nav>
          </nav>
        </nav>
      </div>
      <div class="col-8 p-4">
        <div data-bs-spy="scroll" data-bs-target="#navbar-unit" data-bs-smooth-scroll="true" class="scrollspy-example-2" tabindex="0">
          <div :id="`${unitId}`">
            <p>Пользователи: {{ computers.join(', ') }}</p>
          </div>
        </div>
      </div>
    </div>
</template>

<style lang="less">

</style>