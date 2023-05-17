<script>
import { defaultStore } from '../../stores/counter'

export default {

    setup() {
        const store = defaultStore()
        return { store }
    },
    data() {
        return {
            ip: ''
        }
    },
    methods: {
        async removeRow(ip) {
            var data = this.store.getNetworkTable.tableFull
            var param
            data.forEach(function (item) {
                if (item.ip == ip) {
                    param = item.id
                }
            })
            await this.store.removeNetworkRow(param)
            this.ip = ''
            this.store.getNetworkList()
        }
    }
}
</script>

<template>
    <div class="modal fade" id="removeRow" tabindex="-1" aria-labelledby="removeRowLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="removeRowLabel">Удаление записи</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                </div>
                 <div class="modal-body">
                    <form>
                        <div class="mb-3">
                        <label for="new-ip" class="col-form-label">Ip-адрес:</label>
                        <input type="text" class="form-control" id="new-ip" v-model="ip">
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="removeRow(ip)">Удалить</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="less"></style>