<script>
import { defaultStore } from '../stores/counter'

export default {
    setup() {
        const store = defaultStore()
        return { store }
    },
    data() {
        return {
            login: '',
            password: '',
        }
    },
    methods: {
        async authentification(login, password) {  
            await this.store.login(login, password)
        },
    }
}
</script>

<template>
    <div class="auth mx-auto border border-secondary-subtle shadow-lg bg-body-tertiary rounded">
        <div class="d-flex justify-content-center">
            <p>Авторизация</p>
        </div>
        <div class="form-floating">
            <input type="text" class="form-control" id="floatingInput" placeholder="Login" v-model="this.login">
            <label for="floatingInput">Логин</label>
            <div id="help" class="form-text">Вход разрешен администратору домена</div>
        </div>
        <div class="form-floating">
            <input type="password" class="form-control" id="floatingPassword" placeholder="Password" v-model="this.password">
            <label for="floatingPassword">Пароль</label>
        </div>
        <div class="d-flex justify-content-center form-floating">
            <button @click="authentification(this.login, this.password)" class="form-login btn btn-primary">Вход</button>
        </div>
    </div>
</template>

<style leng="less">

.auth {
    margin-top: 20%;
    width: 40vh;
}

.auth > div {
    margin:auto;
    margin-top: 5%;
    margin-bottom: 5%;
    width: 70%;
}
</style>