<template>
    <div style="margin-top: 10px">
        <bk-table :data="taskList">
            <bk-table-column label="任务名称" prop="task_name"></bk-table-column>
            <bk-table-column label="任务模板" prop="task_tpl"></bk-table-column>
            <bk-table-column label="执行用户" prop="task_op"></bk-table-column>
            <bk-table-column label="执行主机" width="120">
                <template slot-scope="scope">
                    {{ scope.row.exec_hosts.split(',').join('\n') }}
                </template>
            </bk-table-column>
            <bk-table-column label="执行用户名" prop="exec_acc"></bk-table-column>
            <bk-table-column label="执行计划" prop="exec_schedule"></bk-table-column>
            <bk-table-column label="执行进度">
                <template slot-scope="scope">
                    <bk-progress :text-inside="true"
                                 :stroke-width='18'
                                 :percent="scope.row.exec_progress / scope.row.exec_quota_total"
                                 :theme="scope.row.exec_state <= 2 ? 'success' : 'danger'"></bk-progress>
                </template>
            </bk-table-column>
            <bk-table-column label="时间" width="150" prop="start_time"></bk-table-column>
            <!--            <bk-table-column label="时间" width="150" prop="end_time"></bk-table-column>-->
            <!--            <bk-table-column label="通知类型" prop="notify_type" width="80"></bk-table-column>-->
            <!--            <bk-table-column label="通知用户信息" prop="notify_receiver" width="150"></bk-table-column>-->
            <bk-table-column label="操作" min-width="150">
                <template slot-scope="scope">
                    <bk-button theme="primary" v-if="scope.row.exec_state > 0" size="small" @click="fetch_report(scope.row.id)">查看报告</bk-button>
                    <bk-button theme="warning"  v-else size="small" @click="execute_tpl(scope.row.id)">执行</bk-button>
                </template>
            </bk-table-column>
        </bk-table>

        <bk-dialog v-model="reportVisible" theme="primary" title="巡检报告" width="1200" :show-footer="false">
            <bk-collapse>
                <bk-collapse-item v-for="r in report" v-bind:key="r.quota_name" :name="r.quota_name">
                    {{ r.quota_name }}
                    <div slot="content">
                        <bk-table :data="r.result">
                            <bk-table-column label="主机IP" prop="ip"></bk-table-column>
                            <bk-table-column label="巡检值" prop="val"></bk-table-column>
                            <bk-table-column label="对比值" prop="threshold"></bk-table-column>
                            <bk-table-column label="报警">
                                <template slot-scope="scope">{{ scope.row.warning ? '异常' : '正常' }}</template>
                            </bk-table-column>
                        </bk-table>
                    </div>
                </bk-collapse-item>
            </bk-collapse>
        </bk-dialog>
    </div>

</template>

<script>
    export default {
        name: 'list',
        data () {
            return {
                reportVisible: false,
                report: [],
                taskList: []
            }
        },
        created: function () {
            this.fetch_task_list()
        },
        methods: {
            async execute_tpl (taskId) {
                this.$bkInfo({
                    title: '确认要执行模板?',
                    confirmLoading: true,
                    confirmFn: async () => {
                        const res = await this.$store.dispatch('execute_task', { task_id: taskId })
                        console.log(res)
                    }
                })
            },
            async fetch_task_list () {
                const res = await this.$store.dispatch('fetch_task_list')
                this.taskList = res.data
            },
            async fetch_report (taskTd) {
                const self = this
                const res = await this.$store.dispatch('fetch_report', { task_id: taskTd })
                self.report = res.data
                self.reportVisible = true
            }

        }
    }
</script>

<style scoped>

</style>
