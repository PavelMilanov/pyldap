<script setup>
import Home from './components/Home.vue';
import Auth from './components/Auth.vue';
import { defaultStore } from './stores/counter'

const store = defaultStore()
var user = store.user
</script>

<template>
  <Home v-if="user.isActive" />
  <Auth v-else />
</template>
