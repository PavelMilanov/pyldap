<script>
import { defaultStore } from '../stores/counter'
import { useNotification } from '@kyvg/vue3-notification'

export default {

    setup() {
        const store = defaultStore()
        const notify = useNotification()
        return { store, notify }
    },
    data() {
      return {
        form: {
          ip: '',
          description: ''
          }
        }
    },
  methods: {
    async addRow(ip, description) {
      await this.store.addNetworkRow(ip, description)
      this.form.ip = ''
      this.form.description = ''
      this.store.getNetworkList()
      this.$notify({
        type: 'success',
        title: 'Уведомление',
        text: 'Запись добавлена!',
      })
    }
  },
}
</script>

<template>
  <div class="modal fade" id="addRow" tabindex="-1" aria-labelledby="addRowLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="addRowLabel">Добавление новой записи</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
        </div>
        <div class="modal-body">
          <form>
            <div class="mb-3">
              <label for="new-ip" class="col-form-label">Ip-адрес:</label>
              <input type="text" class="form-control" id="new-ip" v-model="form.ip">
            </div>
            <div class="mb-3">
              <label for="new-description" class="col-form-label">Описание:</label>
              <input type="text" class="form-control" id="new-description" v-model="form.description">
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="addRow(form.ip, form.description)">Сохранить</button>
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="less">

</style>