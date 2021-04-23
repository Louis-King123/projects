<template>
    <div style="margin-top: 20px" class="wrapper">

        <bk-container :col="12">
            <bk-row>
                <bk-col :span="2">
                    <div class="">
                        <bk-icon type="folder-open-shape" style="color: #1d91ec;font-size: 100px;margin-left: 30px" />
                    </div>
                </bk-col>
                <bk-col :span="8">
                    <div class="" style="margin-top: 10px">任务名称：test</div>
                    <div class="" style="margin-top: 10px">巡检时间：2020-12-25 11:32:39</div>
                    <div class="" style="margin-top: 10px">巡检结果：本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.</div>
                </bk-col>
                <bk-col :span="2"><div class="">
                    <bk-button title="primary" :text="true" :hover-theme="'primary'" style="border-radius: 20px;margin-bottom: 20px">
                        导出PDF
                    </bk-button>
                    <bk-button title="primary" :text="true" :hover-theme="'primary'" @click="jumpReportHistory" style="border-radius: 20px;margin-left: 5px;margin-bottom: 20px">
                        返回
                    </bk-button>
                </div></bk-col>
            </bk-row>
        </bk-container>
        <bk-divider></bk-divider>

        <div>
            <bk-table style="margin-top: 15px;" col-border fit
                :data="data"
                :pagination="pagination"
                @page-change="handlePageChange"
                @page-limit-change="handlePageLimitChange">
                <bk-table-column label="业务" prop="business"></bk-table-column>
                <bk-table-column label="区域名称" prop="name"></bk-table-column>
                <bk-table-column label="服务器IP" prop="ip"></bk-table-column>
                <bk-table-column label="概要" prop="detail">
                    <template slot-scope="scope">
                        <p v-if="scope.row.detail.length" @click="dialogSetting(scope.$index)" style="cursor: pointer">
                            本次巡检共发现[<span style="color: red">{{scope.row.detail.length}}</span>]项异常
                        </p>
                        <p v-if="!scope.row.detail.length" style="color: green">
                            本次巡检未发现异常
                        </p>
                    </template>

                    <bk-dialog v-model="detailDialog.directive.visible"
                        width="500px"
                        :show-footer="false"
                        :draggable="true"
                        :title=detailDialog.directive.dialogTittle>
                        <p v-for="(item,index) in detailDialog.directive.dialogData" v-bind:key="index" align="center">{{item}}</p>
                    </bk-dialog>
                </bk-table-column>
                <bk-table-column label="操作" width="150">
                    <template slot-scope="scope">
                        <bk-button theme="primary" style="border-radius: 20px" size="small" @click="jumpReportDetail">
                            {{scope.row.id | process}}查看详情
                        </bk-button>
                    </template>
                </bk-table-column>
            </bk-table>
        </div>

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
                data: [
                    {
                        id: '1',
                        business: '蓝鲸—1',
                        name: '上海',
                        ip: '192.168.0.1',
                        detail: ['本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.']
                    },
                    {
                        id: '2',
                        business: '蓝鲸—2',
                        name: '成都',
                        ip: '192.168.0.2',
                        detail: ['本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.']
                    },
                    {
                        id: '3',
                        business: '蓝鲸—3',
                        name: '北京',
                        ip: '192.168.0.3',
                        detail: ['本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.',
                                 '本次共巡检1台服务器，0台巡检失败，1台存在异常，共24项异常.']
                    },
                    {
                        id: '4',
                        business: '蓝鲸—4',
                        name: '深圳',
                        ip: '192.168.0.4',
                        detail: []
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
            jumpReportHistory () {
                // 传递的参数用{{ $route.query.goodsId }}获取
                this.$router.push('/report/history')
                // this.$router.go(-2)
                // 后退两步
            },
            jumpReportDetail () {
                this.$router.push('/report/detail')
            },
            handlePageChange (page) {
                this.pagination.current = page
            //    调用接口
            },
            handlePageLimitChange (lim) {
                console.log(lim)
                this.pagination.current = 1
            //    调用接口
            },
            dialogSetting (arg) {
                const dialogData = this.data[arg]
                this.detailDialog.directive.dialogTittle = dialogData.business
                this.detailDialog.directive.dialogData = dialogData.detail
                this.detailDialog.directive.visible = true
            }
        }
    }
</script>

<style lang="postcss">

</style>
