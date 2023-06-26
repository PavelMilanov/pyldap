<script>
import { defaultStore } from '../../stores/counter'

export default {

    setup() {
        const store = defaultStore()
        return { store }
    },
    data() {
        return {
            customer: ''
        }
    },
    methods: {
        async remove() {
            await this.store.removeAct(this.customer)
            this.customer = ''
        }
    },
}
</script>

<template>
    <div class="modal fade" id="removeAct" tabindex="-1" aria-labelledby="removeActLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="removeActLabel">Удаление акта</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="mb-3">
                            <label for="customer" class="col-form-label">Customer:</label>
                            <input type="text" class="form-control" id="customer" v-model="customer">
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="remove()">Удалить</button>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="less"></style>