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
      <div class="col-2 p-4">
        <!-- <div class="d-flex" style="height: 200px;"> -->
          <!-- </div> -->
          <ol>
            <li v-for="(subtree, tree) in this.store.getUnits" :key="tree">
              <a class="tree-link" :href="`#${tree}`" @click="getComputers(tree)">{{ tree }}</a>
              <ol>
                <li v-for="(item, index) in subtree" :key="index">
                  <a class="tree-link" :href="`#${tree}-${item}`" @click="getComputers(`${tree}-${item}`)">{{ item }}</a>
                </li>
              </ol>
            </li>
          </ol>
        </div>
      <div class="col-4 p-4 border-start">
        <div class="table-container">
          <table class="table table-bordered">
            <caption class="caption-top">{{ this.unitId }}</caption>
            <thead>
              <tr>
                <th scope="col">№</th>
                <th scope="col">Пользователи</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in this.computers" :key="index">
                <th scope="row">{{ index+1 }}</th>
                <td>{{ item }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
</template>

<style lang="less">

.tree-link {
  text-decoration: none;
  color: rgb(41, 40, 40);
}

.table-container {
  overflow: auto;
  height: 65rem;
}
</style>