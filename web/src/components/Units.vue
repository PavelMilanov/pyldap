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
    <div class="row">
      <div class="col-4">
        <nav id="navbar-unit" class="h-100 flex-column align-items-stretch pe-4 border-end">
          <nav class="nav nav-pills flex-column" v-for="(subtree, tree) in this.store.getUnits" :key="tree">
            <a class="nav-link" :href="`#${tree}`">{{ tree }}</a>
            <nav class="nav nav-pills flex-column" v-for="(item, index) in subtree" :key="index">
              <a class="nav-link ms-3 my-1" :href="`#${item}`">{{ item }}</a>
            </nav>
          </nav>
        </nav>
      </div>
      <div class="col-8">
        <div data-bs-spy="scroll" data-bs-target="#navbar-unit" data-bs-smooth-scroll="true" class="scrollspy-example-2" tabindex="0" v-for="(subtree, tree) in this.store.getUnits" :key="tree">
          <div id="{{ tree }}">
            <h4>{{ tree }}</h4>
            <p>fggdffhfghdfghfdhfgh</p>
          </div>
        </div>
      </div>
    </div>
</template>

<style lang="less">

</style>