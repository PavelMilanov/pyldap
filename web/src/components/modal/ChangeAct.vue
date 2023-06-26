<script>
import { defaultStore } from '../../stores/counter'

export default {

    setup() {
        const store = defaultStore()
        return { store }
    },
    data() {
        return {
            file: '',
            customer: ''
        }
    },
    methods: {
        handleFileUpload() {
            this.file = this.$refs.file.files[0]
        },
        async uploadFile() {
            await this.store.ChangeAct(this.file, this.customer)
        },
        clearData() {
            this.file = ''
            this.customer = ''
        }
    },
}
</script>

<template>
    <div class="modal fade" id="changeAct" tabindex="-1" aria-labelledby="changeActLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="changeActLabel">Замена акта</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"
                        @click="clearData()"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="customer" class="col-form-label">Customer:</label>
                        <input type="text" class="form-control" id="customer" v-model="customer">
                    </div>
                    <div class="input-group">
                        <input type="file" class="form-control" ref="file" id="inputGroupFile04"
                            aria-describedby="inputGroupFileAddon04" aria-label="Upload" v-on:change="handleFileUpload()">
                        <button class="btn btn-outline-secondary" type="button" id="inputGroupFileAddon04"
                            @click="uploadFile()">Отправить</button>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal"
                        @click="clearData()">Закрыть</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="less">
</style>