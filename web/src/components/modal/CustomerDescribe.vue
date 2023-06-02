<script>
import { defaultStore } from '../../stores/counter'

export default {

    setup() {
        const store = defaultStore()
        return { store }
    },
    props: {
        'name': String,
    },
    data() {
        return {
            
        }
    },
    methods: {
        getCustomerInfo(name) {
            this.store.getCustomerDescribeInfo(name)
        }
    },
    watch: {
        name(name, oldname) {
            this.getCustomerInfo(name)
        }
    },
}
</script>

<template>
    <div class="modal fade" id="CustomerDescribe" tabindex="-1" aria-labelledby="CustomerDescribeLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="CustomerDescribeLabel">{{ this.name }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="mb-3">
                            <p>Описание: {{ this.store.getCustomerInfo.description ? this.store.getCustomerInfo.description : '' }}</p>
                        </div>
                        <div class="mb-3">
                            <p>Ip: {{ this.store.getCustomerInfo.ip ? this.store.getCustomerInfo.ip : '' }}</p>
                            <p>Был виден в сети: {{ this.store.getCustomerInfo.last_logon }}</p>
                            <p>Группы: {{ this.store.getCustomerInfo.member_of ? this.store.getCustomerInfo.member_of.join(', ') : '' }}</p>
                            <p>ОС: {{ this.store.getCustomerInfo.os }}</p>
                            <p>Версия ОС: {{ this.store.getCustomerInfo.version_os }}</p>
                            <p>Подразделение: {{ this.store.getCustomerInfo.unit ? this.store.getCustomerInfo.unit.join(', ') : '' }}</p>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="less"></style>