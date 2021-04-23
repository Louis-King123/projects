<template>
    <div style="margin-top: 10px">
        <div>
            <bk-form form-type="inline">
                <bk-form-item label="任务名称" :property="'name'">
                    <bk-input v-model="formData.name" placeholder="请输入任务名称"></bk-input>
                </bk-form-item>

                <bk-form-item label="开始时间" :property="'date'">
                    <bk-date-picker placeholder="请选择" :timer="false" v-model="formData.startDate" :disabled="false" style="width: 100%;">
                    </bk-date-picker>
                </bk-form-item>
                <bk-form-item label="结束时间" :property="'date'">
                    <bk-date-picker placeholder="请选择" :timer="false" v-model="formData.endDate" :disabled="false" style="width: 100%;">
                    </bk-date-picker>
                </bk-form-item>

            </bk-form>
        </div>

        <div>
            <bk-table style="margin-top: 15px;" fit
                :data="data"
                :pagination="pagination"
                @page-change="handlePageChange"
                @page-limit-change="handlePageLimitChange">
                <bk-table-column label="业务名称" prop="name" align="center" header-align="center"></bk-table-column>
                <bk-table-column label="执行时间" prop="execTime" align="center"  header-align="center"></bk-table-column>
                <bk-table-column label="任务概览" prop="taskDetail" width="250" align="center"  header-align="center"></bk-table-column>
                <bk-table-column label="任务进度" prop="taskSpeed" align="center"  header-align="center">
                    <template slot-scope="scope">
                        <bk-button v-if="scope.row.status === 'success'" theme="success">
                            {{scope.row.taskSpeed}}%
                        </bk-button>
                        <bk-button v-if="scope.row.status === 'failed'" theme="danger">
                            {{scope.row.taskSpeed}}%
                        </bk-button>
                        <bk-button v-if="scope.row.status === 'processing'" theme="primary">
                            {{scope.row.taskSpeed}}%
                        </bk-button>
                    </template>
                </bk-table-column>
                <bk-table-column label="状态" prop="status" align="center"  header-align="center">
                    <template slot-scope="scope">
                        <p v-if="scope.row.status === 'success'" style="color: green;font-size: 14px">
                            <bk-icon type="check-1" />完成
                        </p>
                        <p v-if="scope.row.status === 'failed'" style="color: red;font-size: 14px">
                            <bk-icon type="close" />失败
                        </p>
                        <p v-if="scope.row.status === 'processing'" style="color: blue;font-size: 14px">
                            <bk-icon type="plus" />进行中
                        </p>
                    </template>
                </bk-table-column>
                <bk-table-column label="操作" width="250" align="center"  header-align="center">
                    <template slot-scope="scope">
                        <bk-button theme="primary" style="border-radius: 20px" size="small" @click="reportCheckPage">
                            {{scope.row.id | process}}详情
                        </bk-button>
                        <bk-button theme="warning" style="border-radius: 20px" size="small">
                            {{scope.row.id | process}}错误汇总
                        </bk-button>
                        <bk-button theme="danger" style="border-radius: 20px" size="small">
                            {{scope.row.id | process}}删除
                        </bk-button>
                    </template>
                </bk-table-column>
            </bk-table>
        </div>

    </div>

</template>

<script>
    export default {
        name: 'historyReport',
        filters: {
            process (arg) {
                return ''
            }
        },
        data () {
            return {
                formData: {
                    name: '',
                    startDate: '',
                    endDate: ''
                },
                data: [
                    {
                        id: '1',
                        name: '蓝鲸—1',
                        execTime: '2020-12-25 11:32:39',
                        taskDetail: '本次共巡检1台服务器，完成1台',
                        taskSpeed: 100,
                        status: 'success',
                        detail: ['本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.']
                    },
                    {
                        id: '2',
                        name: '蓝鲸—2',
                        execTime: '2020-12-25 11:32:39',
                        taskDetail: '本次共巡检2台服务器，完成2台',
                        taskSpeed: 50,
                        status: 'failed',
                        detail: ['本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.']
                    },
                    {
                        id: '3',
                        name: '蓝鲸—3',
                        execTime: '2020-12-25 11:32:39',
                        taskDetail: '本次共巡检3台服务器，完成3台',
                        taskSpeed: 0,
                        status: 'processing',
                        detail: ['本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.']
                    },
                    {
                        id: '4',
                        name: '蓝鲸—4',
                        execTime: '2020-12-25 11:32:39',
                        taskDetail: '本次共巡检4台服务器，完成4台',
                        taskSpeed: 80,
                        status: 'processing',
                        detail: [11111]
                    }
                ],
                pagination: {
                    current: 1,
                    count: 100,
                    limit: 10
                },
                detailDialog: {
                    directive: {
                        visible: false,
                        dialogTittle: '',
                        dialogData: []
                    }
                }
            }
        },

        methods: {
            handlePageChange (page) {
                this.pagination.current = page
            //    调用接口
            },
            handlePageLimitChange (lim) {
                console.log(lim)
                this.pagination.current = 1
            //    调用接口
            },
            reportCheckPage () {
                this.$router.push('/report/check')
            }
        }
    }
</script>

<style scoped>

</style>
