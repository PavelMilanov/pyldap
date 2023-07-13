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
            file: '',
            customer: 'customer'
        }
    },
    methods: {
        handleFileUpload() {
            this.file = this.$refs.file.files[0]
        },
        async uploadFile() {
            await this.store.UploadAct(this.file, this.customer)
            this.$notify({
                type: 'success',
                title: 'Уведомление',
                text: 'Файл добавлен!',
            })
            this.clearData()
        },
        clearData() {
            this.file = ''
            this.customer = 'customer'
        }
    },
}
</script>

<template>
    <div class="modal fade" id="addAct" tabindex="-1" aria-labelledby="addActLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="addActLabel">Добавление нового акта</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть" @click="clearData()"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="new-act" class="col-form-label">Customer:</label>
                        <input type="text" class="form-control" id="new-act" v-model="customer">
                    </div>
                    <div class="input-group">
                        <input type="file" class="form-control" ref="file" id="inputGroupFile04" aria-describedby="inputGroupFileAddon04" aria-label="Upload" v-on:change="handleFileUpload()">
                        <button class="btn btn-outline-secondary" type="button" id="inputGroupFileAddon04" data-bs-dismiss="modal" @click="uploadFile()">Отправить</button>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="clearData()">Закрыть</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="less">
</style>