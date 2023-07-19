import { createRouter, createWebHistory } from 'vue-router'
import { defaultStore } from '@/stores/counter'
import HomeView from '../views/Home.vue'
import NetworkView from '../views/Network.vue'
import CustomersView from '../views/Customers.vue'
import UnitsView from '../views/Units.vue'
import ActsView from '../views/Acts.vue'
import AuthView from '../views/Auth.vue'
import ActRender from '../components/ActRender.vue'
import CustomerRender from '../components/CustomerRender.vue'

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
            redirect: { path: '/customers/all' },
            component: CustomersView,
            children: [
                {
                    path: '/customers/:id',
                    name: 'customer',
                    component: CustomerRender,
                    props: true,
                }
            ]
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
    if (to.name !== 'auth' && !store.getUser.isActive) {  // если пользователь не авторизован, будет редирект на страницу авторизации
        next({ name: 'auth' }) 
    }
    else {
        next()
    }
})

router.afterEach((to, from) => {
    const store = defaultStore()

})
