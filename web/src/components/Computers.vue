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

    }
}
</script>

<template>
    <div>
        <p>This is Computers page</p>
    </div>
</template>

<style lang="less"></style>