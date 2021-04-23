<template>
    <div style="width: 600px; margin: 0 auto; margin-top: 30px;">
        <bk-form :label-width="200" :model="formData" ref="validateForm">
            <bk-form-item label="任务名称" :required="true">
                <bk-input v-model="formData.task_name" placeholder="请输入3到10个以内的字符，不能为admin"></bk-input>
            </bk-form-item>
            <bk-form-item label="系统" :required="true">
                <bk-select v-model="taskOs">
                    <bk-option v-for="option in typeList"
                               :key="option.id"
                               :id="option.id"
                               :name="option.os_name">
                    </bk-option>
                </bk-select>
            </bk-form-item>
            <bk-form-item label="选择模板" :required="true">
                <bk-select v-model="formData.task_tpl_id">
                    <bk-option v-for="toption in tplList"
                               :key="toption.id"
                               :id="toption.id"
                               :name="toption.tpl_name">
                    </bk-option>
                </bk-select>
            </bk-form-item>
            <bk-form-item label="执行账户" :required="true">
                <bk-input v-model="formData.exec_acc" placeholder="root"></bk-input>
            </bk-form-item>
            <bk-form-item label="选择业务" :required="true">
                <bk-select v-model="bizId">
                    <bk-option v-for="biz in bizList"
                               :key="biz.id"
                               :id="biz.id"
                               :name="biz.name">
                    </bk-option>
                </bk-select>
            </bk-form-item>
            <bk-form-item label="选择主机" :required="true">
                <bk-select multiple v-model="groupValue">
                    <bk-option v-for="host in groupList"
                               :key="host.id"
                               :id="host.id"
                               :name="host.name">
                    </bk-option>
                </bk-select>
            </bk-form-item>
            <bk-form-item>
                <bk-button style="float: right" ext-cls="mr5" theme="primary" title="提交" @click.stop.prevent="validate"
                           :loading="isChecking">提交
                </bk-button>
            </bk-form-item>
        </bk-form>
    </div>
</template>

<script>
    export default {
        name: 'add',
        data () {
            return {
                taskOs: 1,
                groupValue: '',
                bizId: 0,
                groupList: [],
                isChecking: false,
                bizList: [],
                formData: {
                    biz_id: 0,
                    task_name: '',
                    task_os: '',
                    task_tpl_id: '',
                    exec_acc: 'root'
                },
                typeList: [],
                tplList: []
            }
        },
        watch: {
            taskOs (val) {
                this.formData.task_os = val
                this.fetch_tpl_list()
            },
            groupValue: function (val) {
                this.formData.exec_hosts = val
            },
            bizId: function (val) {
                this.formData.biz_id = val
                this.groupList = this.bizList[val]['children']
            }
        },
        mounted () {
            this.search_host_by_biz()
            this.fetch_tpl_list()
            this.get_os_list()
        },
        methods: {
            get_os_list: function () {
                const self = this
                const res = this.$store.dispatch('get_init_data', 'get_os_list')
                res.then(function (data) {
                    self.typeList = data.data
                })
            },
            async fetch_tpl_list () {
                const res = await this.$store.dispatch('fetch_tpl_list', { 'os': this.taskOs })
                const { data } = res
                this.tplList = data
            },
            search_host_by_biz: function () {
                const self = this
                const res = this.$store.dispatch('search_host_by_biz')
                res.then(function (data) {
                    const val = data.data
                    self.bizList = val
                })
            },
            validate: function () {
                const self = this
                this.isChecking = true
                const res = this.$store.dispatch('task_add', this.formData)
                res.then(function (result) {
                    self.isChecking = false
                    self.$bkNotify({ title: 'sucess', message: '添加成功' })
                })
            }

        }
    }
</script>

<style scoped>

</style>
