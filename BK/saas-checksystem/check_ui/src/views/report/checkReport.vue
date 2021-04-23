<template>
    <div style="margin-top: 20px" class="wrapper"  v-bkloading="{ isLoading: basicLoading, zIndex: 10 }">

        <bk-container :col="12" style="background-color: white;height: 110px">
            <bk-row>
                <bk-col :span="2">
                    <div class="">
                        <bk-icon type="folder-open-shape" style="color: #1d91ec;font-size: 100px;margin-left: 30px;" />
                    </div>
                </bk-col>
                <bk-col :span="8">
                    <div class="" style="margin-top: 10px">任务名称：{{ taskInfo.task_name }}</div>
                    <div class="" style="margin-top: 10px;color: grey">创建时间：{{ taskInfo.start_time }} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 完成时间：{{ taskInfo.end_time }}</div>
                    <div class="" style="margin-top: 10px;color: grey">巡检对象：{{ taskInfo.task_os }}</div>
                </bk-col>
<!--                <bk-col :span="2"><div class="">-->
<!--&lt;!&ndash;                    <bk-button title="primary" :text="true" :hover-theme="'primary'" style="border-radius: 20px;margin-bottom: 20px;margin-top: 10px">&ndash;&gt;-->
<!--&lt;!&ndash;                        导出PDF&ndash;&gt;-->
<!--&lt;!&ndash;                    </bk-button>&ndash;&gt;-->
<!--                    <bk-button title="primary" :text="true" :hover-theme="'primary'" @click="jumpReportHistory" style="border-radius: 20px;margin-left: 5px;margin-bottom: 20px;margin-top: 10px">-->
<!--                        返回-->
<!--                    </bk-button>-->
<!--                </div></bk-col>-->
            </bk-row>
        </bk-container>

        <div style="border:1px solid rgb(228 221 228);margin-top: 15px;border-radius: 5px;height: 160px;width: 96%;margin-left: 2%;background-color: white">
            <div style="margin-left: 20px;margin-top: 10px">结果简报</div>
            <bk-divider></bk-divider>
            <div style="width: 25%;float: left;" align="center">
                <div style="color: grey">巡检主机数</div>
                <div style="margin-top: 10px;font-size: 30px">{{ taskInfo.all_ips }}</div>
            </div>
            <div style="width: 25%;float: left;" align="center">
                <div style="color: grey">巡检失败主机数</div>
                <div style="margin-top: 10px;font-size: 30px;color: orange">{{ taskInfo.failed_host }}</div>
            </div>
            <div style="width: 25%;float: left;" align="center">
                <div style="color: grey">异常主机数</div>
                <div style="margin-top: 10px;font-size: 30px;color: red">{{ taskInfo.error_host }}</div>
            </div>
            <div style="width: 25%;float: left;" align="center">
                <div style="color: grey">异常指标数</div>
                <div style="margin-top: 10px;font-size: 30px;color: red">{{ taskInfo.error_num }}</div>
            </div>
        </div>

        <div style="background-color: white;width: 98%;margin-left: 1%">
            <bk-table style="margin-top: 15px;" fit
                :data="data">
                <bk-table-column label="业务" prop="bk_biz_name" align="center"></bk-table-column>
                <bk-table-column label="巡检对象" prop="task_os" align="center"></bk-table-column>
                <bk-table-column label="模板" prop="task_tpl_name" align="center"></bk-table-column>
                <bk-table-column label="服务器IP" prop="host" align="center"></bk-table-column>
                <bk-table-column label="概要" prop="errors" align="center">
                    <template slot-scope="scope">
                        <p v-if="scope.row.errors.length && scope.row.host_status === 'success'" @click="dialogSetting(scope.$index)" style="cursor: pointer">
                            本次巡检共发现[<span style="color: red">{{scope.row.errors.length}}</span>]项异常
                        </p>
                        <p v-if="!scope.row.errors.length && scope.row.host_status === 'success'" style="color: green">
                            本次巡检未发现异常
                        </p>
<!--                        <p v-if="scope.row.host_status === 'failed'" style="color: red">-->
<!--                            主机巡检失败-->
<!--                        </p>-->
                        <bk-popover v-if="scope.row.host_status === 'failed'" placement="top" :ext-cls="11">
                            <span style="color: red;cursor: pointer;">主机巡检失败</span>
                            <div slot="content" style="white-space: normal;">
<!--                                <div class="pt10 pb5 pl10 pr10">{{ scope.row.failed_info }}</div>-->
<!--                                <div class="pt10 pb5 pl10 pr10">这只是一个显示例子</div>-->
                                <div class="pt10 pb5 pl10 pr10">{{ scope.row.failed_info }}</div>
                            </div>
                        </bk-popover>
                    </template>
                </bk-table-column>
                <bk-table-column label="状态" prop="errors" align="center">
                    <template slot-scope="scope">
                        <p v-if="scope.row.host_status === 'success'" style="color: green">
                            <bk-icon type="circle-shape" style="font-size: 1px" />&nbsp;成功
                        </p>
                        <p v-if="scope.row.host_status === 'failed'" style="color: red">
                            <bk-icon type="circle-shape" style="font-size: 1px" />&nbsp;失败
                        </p>
                    </template>
                </bk-table-column>
                <bk-table-column label="操作" width="150" align="center">
                    <template slot-scope="scope">
                        <bk-button theme="default" disabled size="small" v-if="scope.row.host_status === 'failed'">
                            查看详情
                        </bk-button>
                        <bk-button theme="primary" size="small" @click="jumpReportDetail(scope.row)"  v-if="scope.row.host_status === 'success'">
                            {{scope.row.id | process}}查看详情
                        </bk-button>
                    </template>
                </bk-table-column>

                <bk-dialog v-model="detailDialog.directive.visible"
                        :width="1000"
                        :show-footer="false"
                        :position="{ top: 80 }"
                        :title=detailDialog.directive.dialogTittle>
                        <div style="height: 500px;overflow: auto">
                            <bk-table col-border
                                :data="detailDialog.directive.dialogData"
                                :size="size">
                                <bk-table-column label="检查项" prop="quota_name" style="font-size: 30px" align="center"></bk-table-column>
                                <bk-table-column label="检查结果" prop="check_result" align="center">
                                    <template slot-scope="scope">
                                            <p style="color: red">
                                                {{ scope.row.check_result }}
                                            </p>
                                        </template>
                                </bk-table-column>
                                <bk-table-column label="推荐值" prop="recommend_value" align="center"></bk-table-column>
                            </bk-table>
                        </div>
                    </bk-dialog>

            </bk-table>
        </div>
    <bk-button theme="primary" id="errorButton" @click="errorInfo" style="display: none"></bk-button>
    </div>

</template>

<script>
    export default {
        name: 'checkReport',

        filters: {
            process (arg) {
                return ''
            }
        },

        data () {
            return {
                basicLoading: true,
                data: [],
                taskInfo: '',
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
                },
                error: {
                    title: '数据请求失败',
                    msg: ''
                },
                report_id: ''
            }
        },

        mounted () {
            if (this.$route.query.id) {
                this.report_id = this.$route.query.id
            }
            this.getReportInfo()
        },

        methods: {

            async getReportInfo () {
                // const infos = await this.$store.dispatch('fetch_inspection_report_by_id', { 'report_id': this.report_id })
                // if (infos.code) {
                //     this.error.msg = infos.message
                //     document.getElementById('errorButton').click()
                // } else {
                //     this.data = infos.data.hosts
                //     this.pagination.count = this.data.length
                //     this.taskInfo = infos.data
                //     this.basicLoading = false
                // }
                try {
                    this.basicLoading = true
                    const res = await this.$store.dispatch('fetch_inspection_report_by_id', { 'report_id': this.report_id })
                    const { code, data, message } = res
                    if (code) {
                        this.error.msg = message
                        document.getElementById('errorButton').click()
                        return
                    }

                    this.data = data.hosts
                    this.pagination.count = data.length
                    this.taskInfo = data
                } catch (e) {
                    console.log(e)
                } finally {
                    this.basicLoading = false
                }
            },

            jumpReportHistory () {
                // 传递的参数用{{ $route.query.goodsId }}获取
                this.$router.push({
                    name: 'historyReport'
                })
                // this.$router.push('/report/history/')
                // this.$router.go(-2)
                // 后退两步
            },
            jumpReportDetail (obj) {
                const { host } = obj

                if (obj.task_os.toLowerCase().indexOf('windows') !== -1) {
                    // this.$router.push('/report/windows/detail?os=windows&execute_id=' + this.taskInfo.execute_log_id + '&host=' + obj.host)
                    this.$router.push({
                        name: 'windowsDetailReport',
                        query: {
                            os: 'windows',
                            execute_id: this.taskInfo['execute_log_id'],
                            host
                        }
                    })
                }

                if (obj.task_os.toLowerCase().indexOf('centos') !== -1 || obj.task_os.toLowerCase().indexOf('redhat') !== -1
                    || obj.task_os.toLowerCase().indexOf('ubuntu') !== -1 || obj.task_os.toLowerCase().indexOf('debian') !== -1) {
                    // this.$router.push('/report/linux/detail?os=linux&execute_id=' + this.taskInfo.execute_log_id + '&host=' + obj.host)
                    this.$router.push({
                        name: 'linuxDetailReport',
                        query: {
                            os: 'linux',
                            execute_id: this.taskInfo['execute_log_id'],
                            host
                        }
                    })
                }
                // if (obj.task_os.toLowerCase().indexOf('centos') !== -1 || obj.task_os.toLowerCase().indexOf('redhat') !== -1) {
                //     this.$router.push('/report/linux/detail?os=centos&execute_id=' + this.taskInfo.execute_log_id + '&host=' + obj.host)
                // }
                //
                // if (obj.task_os.toLowerCase().indexOf('ubuntu') !== -1 || obj.task_os.toLowerCase().indexOf('debian') !== -1) {
                //     this.$router.push('/report/linux/detail?os=ubuntu&execute_id=' + this.taskInfo.execute_log_id + '&host=' + obj.host)
                // }
            },
            // handlePageChange (page) {
            //     this.pagination.current = page
            // //    调用接口
            // },
            // handlePageLimitChange (lim) {
            //     this.pagination.current = 1
            // //    调用接口
            // },
            dialogSetting (arg) {
                const dialogData = this.data[arg]
                this.detailDialog.directive.dialogTittle = dialogData.task_name
                this.detailDialog.directive.dialogData = dialogData.errors
                this.detailDialog.directive.visible = true
            },
            errorInfo () {
                this.$bkInfo({
                    type: 'error',
                    title: this.error.title,
                    subTitle: this.error.msg,
                    showFooter: false,
                    maskClose: true
                })
            }
        }
    }
</script>

<style lang="postcss">

</style>
