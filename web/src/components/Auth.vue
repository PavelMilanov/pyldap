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
            status: '',
            APP_VERSION: import.meta.env.VITE_APP_VERSION,
        }
    },
    methods: {
        async authentification(login, password) {  
            let status = await this.store.login(login, password)
            if (status == 'failure') {
                this.status = status
            }
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
            <input type="text" class="form-control" :class="{'is-invalid': status == 'failure' }" id="floatingInput" placeholder="Login" v-model="this.login">
            <label for="floatingInput">Логин</label>
            <div id="help" class="form-text text-center">Вход разрешен администратору домена</div>
        </div>
        <div class="form-floating">
            <input type="password" class="form-control" id="floatingPassword" :class="{'is-invalid': status == 'failure' }" placeholder="Password" @keyup.enter="authentification(this.login, this.password)" v-model="this.password">
            <label for="floatingPassword">Пароль</label>
            <div class="invalid-feedback">
                Неправильный логин или пароль!
          </div>
        </div>
        <div class="d-flex justify-content-center form-floating">
            <button @click="authentification(this.login, this.password)" class="form-login btn btn-primary">Вход</button>
        </div>
        <div class="d-flex mb-1 justify-content-center">
            <p class="form-text text-center">Версия: {{ this.APP_VERSION }}</p>
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