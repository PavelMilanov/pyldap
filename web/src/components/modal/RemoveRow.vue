<script>
import { defaultStore } from '../../stores/counter'

export default {

    setup() {
        const store = defaultStore()
        return { store }
    },
    data() {
        return {
            index: 0
        }
    },
    methods: {
        async removeRow(index) {
            await this.store.removeNetworkRow(index-1)  // в таблице индекс начинается с 1
            this.index = 0
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
                        <label for="new-ip" class="col-form-label"># записи:</label>
                        <input type="text" class="form-control" id="new-ip" v-model="index">
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="removeRow(index)">Удалить</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="less"></style>