<script>
import { defaultStore } from '../stores/counter'


export default {

    components: {
        
    },
    setup() {
        const store = defaultStore()
        return { store }
    },
    data() {
        return {
          page: 0,
          connection: null,
          cache: null
        }
  },
    watch: {
    logonInfo(items) {
      console.log(items)
      }
    },
    methods: {
      goPage(number) {
        this.page = number
      },
  },
  created() {
    this.connection = new WebSocket("ws://localhost:8000/api/v1/ws/netclients")

    this.connection.onmessage = function (event) {
      if (event.data == this.cache) {  // если не было новых сообщений и пришло тоже самое
        return
      }
      var jsondata = JSON.parse(event.data)
      var message = jsondata["time"] + ": " + jsondata["client"] + " авторизовался" 
      document.querySelector("#Logon-log").value += message + "\n"
      this.cache = event.data
    }

    this.connection.onopen = function (event) {
      console.log(event)
      console.log("connection oppened")
    }

    setInterval(() => {  // триггер для обновления данных по вебсокету.
      this.connection.send('info')
    }, 6000)
  }
}
</script>

<template>
    <div class="mb-3 mx-auto">
      <div class="home container-fluid text-center">
        <div class="p-3 row">
          <div class="col-6">
              <div class="card">
                <div class="card-header">
                  <p class="card-title">Инфо</p>
                </div>
                <div class="body">
                  <p class="card-text m-2">Всего пользователей: {{ this.store.getCustomersCount }}</p>
                </div>
              </div>
              <div class="mt-2">
                <textarea class="form-control" id="Logon-log" rows="10"></textarea>
              </div>
          </div>
          <div class="col-6">
            <div class="card">
              <div class="card-header">
                <p class="card-title">Навигация</p>
              </div>
              <div class="card-body">
                <div class="accordion" id="accordionNavigation">
                    <div class="accordion-item">
                      <h2 class="accordion-header">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                          Статические адреса
                        </button>
                      </h2>
                      <div id="collapseOne" class="accordion-collapse collapse" data-bs-parent="#accordionNavigation">
                        <div class="accordion-body">
                          Таблица для учета статических ip. Большинство ip учитываются на UserGate.
                        </div>
                      </div>
                    </div>
                    <div class="accordion-item">
                      <h2 class="accordion-header">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                          Пользователи
                        </button>
                      </h2>
                      <div id="collapseTwo" class="accordion-collapse collapse" data-bs-parent="#accordionNavigation">
                        <div class="accordion-body">
                          Вывод информации о пользователях AD.
                        </div>
                      </div>
                    </div>
                    <div class="accordion-item">
                      <h2 class="accordion-header">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                          Подразделения
                        </button>
                      </h2>
                      <div id="collapseThree" class="accordion-collapse collapse" data-bs-parent="#accordionNavigation">
                        <div class="accordion-body">
                          Вывод списка подразделений. Так же выводит информацию о пользователях в конкретном подразделдении.
                        </div>
                      </div>
                    </div>
                    <div class="accordion-item">
                      <h2 class="accordion-header">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseFour" aria-expanded="false" aria-controls="collapseThree">
                          Акты
                        </button>
                      </h2>
                      <div id="collapseFour" class="accordion-collapse collapse" data-bs-parent="#accordionNavigation">
                        <div class="accordion-body">
                          Учёт актов. Позволяет добавлять, изменять, удалять акты для конкретного польльзователя.
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
        </div>
      </div>
    </div>
</template>

<style lang="less">
</style>
