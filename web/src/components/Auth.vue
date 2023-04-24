<script>
import { defaultStore } from '../stores/counter'

export default {
    setup() {
        const store = defaultStore()
        return { store }
    },
    data() {
        return {
            authForm: true,
            login: '',
            password: '',
        }
    },
    methods: {
        isActive() {
            if (this.store.getUser.isActive === true) {
                this.$router.push('/')
            }
        },
        async authentification(login, password) {  
            await this.store.postAuthentification(login, password)
            setTimeout(this.isActive, 1000)
        },

    }
}
</script>

<template>
    <div class="d-flex justify-content-center align-items-center bg-secondary bg-gradient">
        <div class="form bg-light shadow-lg rounded">
            <div class="form-floating m-3">
                <input v-model="login" type="text" class="form-control" id="floatingInput">
                <label for="floatingInput">Логин</label>
                <div id="help" class="form-text">Вход разрешен администратору домена</div>
            </div>
            <div class="form-floating m-3">
                <input v-model="password" type="password" class="form-control" id="floatingPassword">
                <label for="floatingPassword">Пароль</label>
            </div>
            <div class="form-floating m-3">
                <button @click="authentification(this.login, this.password)" class="btn btn-primary">Вход</button>
            </div>
        </div>
    </div>
</template>

<style leng="less">
.d-flex {
    height: 100vh;
}
</style>