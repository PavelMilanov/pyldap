import { createRouter, createWebHistory } from 'vue-router'
import { defaultStore } from '@/stores/counter'
import HomeView from '../views/Home.vue'
import NetworkView from '../views/Network.vue'
import CustomersView from '../views/Customers.vue'
import UnitsView from '../views/Units.vue'
import ActsView from '../views/Acts.vue'
import AuthView from '../views/Auth.vue'
import ActRender from '../views/ActRender.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView,
        },
        {
            path: '/auth',
            name: 'auth',
            component: AuthView
        },
        {
            path: '/network',
            name: 'network',
            component: NetworkView
        },
        {
            path: '/customers',
            name: 'customers',
            component: CustomersView,
        },
        {
            path: '/units',
            name: 'units',
            component: UnitsView
        },
        {
            path: '/acts',
            name: 'acts',
            redirect: {path: '/acts/template', query: {act: 'true'}},
            component: ActsView,
            children: [
                {
                    path: '/acts/:id',
                    name: 'act',
                    component: ActRender,
                    props: true,
                },
            ]
        },
    ]
})

export default router

router.beforeEach((to, from, next) => {
    const store = defaultStore()
    if (to.name !== 'auth' && !store.getUser.isActive) next({ name: 'auth' })  // если пользователь не авторизован, будет редирект на страницу авторизации
    else next()
})