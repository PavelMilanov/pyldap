<script>
import { defaultStore } from '../../stores/counter'

export default {

    setup() {
        const store = defaultStore()
        return { store }
    },
    data() {
        return {
            ip: '',
            form: {
                id: 0,
                ip: '',
                description: ''
            }
        }
    },
    watch: {
        ip(newIp, oldIp) {
            var re = /([0-9]{1,3}[\.]){3}[0-9]{1,3}/
            var ipAddress = re.exec(newIp)
            if (ipAddress != null) {
                this.loadForm(ipAddress[0])
            }
        }
    },
    methods: {
        loadForm(patternIp) {
            var cache
            var data = this.store.getNetworkTable.tableFull
            data.forEach(function (item) {
                if (item.ip == patternIp) {
                    cache = [item.id, item.ip, item.description]
                }
            })
            if (cache != null) {
                this.form.id = cache[0]
                this.form.ip = cache[1]
                this.form.description = cache[2]
            }
        },
        async editRow() {
            var params = {
                "id": this.form.id,
                "ip": this.form.ip,
                "description": this.form.description
            }
            await this.store.editNetworkRow(params)
            this.form.id = 0
            this.form.ip = ''
            this.form.description = ''
            this.store.getNetworkList()
        }
    }
}
</script>

<template>
    <div class="modal fade" id="editRow" tabindex="-1" aria-labelledby="editRowLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="editRowLabel">Редактирование записи</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="mb-3">
                            <label for="ip" class="col-form-label">Ip-адрес:</label>
                            <input type="text" class="form-control" id="ip" v-model="ip">
                        </div>
                    </form>
                    <form>
                        <div class="mb-3">
                            <label for="new-ip" class="col-form-label">Новый ip-адрес:</label>
                            <input type="text" class="form-control" id="new-ip" v-model="form.ip">
                        </div>
                        <div class="mb-3">
                            <label for="new-description" class="col-form-label">Новое описание:</label>
                            <input type="text" class="form-control" id="new-description" v-model="form.description">
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="editRow()">Сохранить</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="less">
</style>