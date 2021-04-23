<template>
    <div style="margin-top: 10px;" v-bkloading="{ isLoading: basicLoading, zIndex: 10 }">
        <div style="margin-top: 20px" class="wrapper">
            <div style="border:1px solid rgb(228 221 228);height: 150px;background-color: white">
                <bk-container :col="12">
                    <bk-row>
                        <bk-col :span="2">
                            <div class="">
                                <i class="el-icon-s-platform" style="font-size: 100px;margin-left: 20%"></i>
                            </div>
                            <div style="margin-left: 38%">
                                Linux
                            </div>
                        </bk-col>
                        <bk-col :span="7">
                            <div class="" style="margin-top: 10px;font-size: 25px;margin-left: 20px;">{{ taskHost.host }}</div>
                            <div class="" style="margin-top: 10px;color: grey">创建时间：{{ taskHost.create_time }}</div>
                            <div class="" style="margin-top: 10px;color: grey">完成时间：{{ taskHost.end_time }}</div>
                        </bk-col>
                        <bk-col :span="3"><div class="">
                            <bk-button title="primary" :text="true" :hover-theme="'primary'" @click="jumpReportHistory" style="border-radius: 20px;margin-left: 60%;margin-bottom: 20px;margin-top: 10px">
                                返回
                            </bk-button>
                        </div></bk-col>
                    </bk-row>
                </bk-container>
            </div>

            <div id="divInspectionInfo" style="border:1px solid rgb(228 221 228);margin-top: 20px;border-radius: 5px;background-color: white;width: 98%;margin-left: 1%;display: none">
                <div style="margin-left: 20px;margin-top: 12px;font-size: larger">巡检概览</div>
                <bk-divider></bk-divider>
                <bk-container :col="12">
                    <bk-row>
                        <bk-col :span="4" style="margin-top: 15px">
                            <div class="content">
                                <div class="round"  align="center" :class="{ 'active': true }">
                                    <bk-round-progress :width="width" :percent="percent" :config="config" :content="inspectionContent"></bk-round-progress>
                                </div>
                            </div>
                        </bk-col>
                        <bk-col :span="8">
                            <div style="font-size: 20px">总体健康情况良好，共巡检{{ inspectionInfo.inspection_count }}个指标，异常指标数{{ inspectionInfo.inspection_error }}个，占比{{ inspectionInfo.error_percent }}%</div>
                            <div class="circleCss" v-for="(item, index) in inspectionInfo.error_detail" v-bind:key="index">
                                <bk-badge class="mr5" :val="index" :theme="themeInfo[index]" radius="50" position="right"></bk-badge>
                                <div class="inlineBlock" style="width: 20%">{{ item.class_name }}</div>
                                <div class="inlineBlock" style="margin-left: 20%;color: red;width: 20px">{{ item.error_count }}</div>
                                <div class="inlineBlock" style="margin-left: 9%">
                                    <bk-link underline theme="default" @click="dialogSetting(index)" target="_blank">详情</bk-link>
                                </div>
                            </div>
                            <br />

                            <bk-dialog v-model="detailDialog.directive.visible"
                                       :width="1000"
                                       :show-footer="false"
                                       :position="{ top: 80 }"
                                       :title=detailDialog.directive.dialogTittle>
                                <div style="height: 500px;overflow: auto;width: 100%">
                                    <bk-table col-border
                                              :data="detailDialog.directive.dialogData"
                                              :size="size">
                                        <bk-table-column label="检查项" prop="check_option" style="font-size: 30px;width: 100px" align="center"></bk-table-column>
                                        <bk-table-column label="检查结果" prop="check_result" style="font-size: 30px;width: 33%;" align="center">
                                            <template slot-scope="scope">
                                                <p style="color: red">
                                                    {{ scope.row.check_result }}
                                                </p>
                                            </template>
                                        </bk-table-column>
                                        <bk-table-column label="推荐值" prop="recommend_value" style="font-size: 30px;width: 33%" align="center"></bk-table-column>
                                    </bk-table>
                                </div>

                            </bk-dialog>

                        </bk-col>

                    </bk-row>
                </bk-container>
            </div>

            <div class="usageRateInfoContainer">
                <bk-container :col="12">
                    <bk-row>
                        <bk-col :span="colSpan">
                            <div style="width: 100%;margin: 5px auto;">
                                <div style="width: 100%;height: 140px;border:1px solid rgb(228 221 228);">
                                    <div style="width: 50%;" class="inlineBlock">
                                        <span style="margin-left: 10px;color: grey">CPU使用率</span><br />
                                        <span v-if="hostRate.cpu.result_status === true" style="font-size: 20px;margin-left: 10px">{{ hostRate.cpu.percentInt }}%</span>
                                        <span v-if="hostRate.cpu.result_status === false" style="font-size: 20px;margin-left: 10px;color: red">{{ hostRate.cpu.percentInt }}%</span><br />
                                        <span style="font-size: 25px;margin-left: 10px"></span><br />
                                        <span style="font-size: 25px;margin-left: 10px"></span><br />
                                    </div>
                                    <div style="width: 40%" class="inlineBlock" :class="{ 'active': hostRate.cpu.result_status === false }">
                                        <bk-round-progress width="100px" :config="tagConfig" :percent="hostRate.cpu.percent" style="margin-top: 20px;margin-left: 10px;"></bk-round-progress>
                                    </div>
                                </div>
                            </div>
                        </bk-col>
                        <bk-col :span="colSpan">
                            <div style="margin: 5px auto;">
                                <div style="height: 140px;border:1px solid rgb(228 221 228);">
                                    <div style="width: 50%;" class="inlineBlock">
                                        <span style="margin-left: 10px;color: grey">物理内存使用率</span><br />
                                        <span v-if="hostRate.memory.result_status === true" style="font-size: 20px;margin-left: 10px">{{ hostRate.memory.percentInt }}%</span>
                                        <span v-if="hostRate.memory.result_status === false" style="font-size: 20px;margin-left: 10px;color: red">{{ hostRate.memory.percentInt }}%</span><br />
                                        <span style="font-size: 14px;margin-left: 10px;color: grey">内存总量：{{ hostRate.memory.total }}</span><br />
                                        <span style="font-size: 14px;margin-left: 10px;color: grey">空闲内存：{{ hostRate.memory.free }}MB</span><br />
                                        <span style="font-size: 14px;margin-left: 10px"></span><br />
                                    </div>
                                    <div style="width: 40%" class="inlineBlock"  :class="{ 'active': hostRate.memory.result_status === false }">
                                        <bk-round-progress width="100px" :config="tagConfig" :percent="hostRate.memory.percent" style="margin-top: 20px;margin-left: 10px"></bk-round-progress>
                                    </div>
                                </div>
                            </div>
                        </bk-col>
                        <bk-col :span="colSpan">
                            <div style="margin: 5px auto;">
                                <bk-popover :placement="'top'" width="300" ext-cls="customStyle">
                                    <div style="height: 140px;border:1px solid rgb(228 221 228); cursor: pointer;">
                                        <div style="width: 50%" class="inlineBlock">
                                            <span style="margin-left: 10px;color: grey">硬盘空间使用率</span><br />
                                            <span style="font-size: 20px;margin-left: 10px">{{ singleDisk.percentInt }}</span><br />
                                            <span style="font-size: 14px;margin-left: 10px;color: grey">硬盘总量：{{ singleDisk.total }}</span><br />
                                            <span style="font-size: 14px;margin-left: 10px;color: grey">可用空间：{{ singleDisk.free }}</span><br />
                                            <span style="font-size: 14px;margin-left: 10px"></span><br />
                                        </div>
                                        <div style="width: 40%" class="inlineBlock">
                                            <bk-round-progress width="100px" :config="tagConfig" :percent="singleDisk.percent" style="margin-top: 20px;margin-left: 10px"></bk-round-progress>
                                        </div>
                                    </div>
                                    <div slot="content">
                                        <div v-for="(item, index) in hostRate.disk" v-bind:key="index">
                                            <div style="width: 55%" class="inlineBlock">
                                                <span style="margin-left: 10px;color: grey">名称：{{ item.name }}</span><br />
                                                <span style="margin-left: 10px;color: grey">硬盘空间使用率：{{ item.percentInt }}</span><br />
                                                <span style="font-size: 14px;margin-left: 10px;color: grey">硬盘总量：{{ item.total }}</span><br />
                                                <span style="font-size: 14px;margin-left: 10px;color: grey">可用空间：{{ item.free }}</span><br />
                                                <span style="font-size: 14px;margin-left: 10px"></span><br />
                                            </div>
                                            <div style="width: 35%" class="inlineBlock">
                                                <bk-round-progress width="100px" :config="tagConfig" :percent="item.percent" style="margin-top: 20px;margin-left: 10px"></bk-round-progress>
                                            </div>
                                        </div>
                                    </div>
                                </bk-popover>
                            </div>
                        </bk-col>
                        <bk-col :span="colSpan">
                            <div style="margin: 5px auto;">
                                <bk-popover :placement="'top'" width="300" ext-cls="customStyle">
                                    <div style="height: 140px;border:1px solid rgb(228 221 228); cursor: pointer;">
                                        <div style="width: 50%" class="inlineBlock">
                                            <span style="margin-left: 5px;color: grey">Inode使用率</span><br />
                                            <span style="font-size: 20px;margin-left: 10px">{{ singleInode.percentInt }}</span><br />
                                            <span style="font-size: 14px;margin-left: 10px;color: grey">Inode总量：{{ singleInode.total }}</span><br />
                                            <span style="font-size: 14px;margin-left: 10px;color: grey">可用空间：{{ singleInode.free }}</span><br />
                                            <span style="font-size: 14px;margin-left: 10px"></span><br />
                                        </div>
                                        <div style="width: 40%" class="inlineBlock">
                                            <bk-round-progress width="100px" :config="tagConfig" :percent="singleInode.percent" style="margin-top: 20px;margin-left: 10px"></bk-round-progress>
                                        </div>
                                    </div>
                                    <div slot="content">
                                        <div v-for="(item, index) in hostRate.inode" v-bind:key="index">
                                            <div style="width: 55%" class="inlineBlock">
                                                <span style="margin-left: 10px;color: grey">名称：{{ item.name }}</span><br />
                                                <span style="margin-left: 5px;color: grey">Inode使用率：{{ item.percentInt }}</span><br />
                                                <span style="font-size: 14px;margin-left: 10px;color: grey">Inode总量：{{ item.total }}</span><br />
                                                <span style="font-size: 14px;margin-left: 10px;color: grey">可用空间：{{ item.free }}</span><br />
                                                <span style="font-size: 14px;margin-left: 10px"></span><br />
                                            </div>
                                            <div style="width: 35%" class="inlineBlock">
                                                <bk-round-progress width="100px" :config="tagConfig" :percent="item.percent" style="margin-top: 20px;margin-left: 10px"></bk-round-progress>
                                            </div>
                                            <br />
                                        </div>
                                    </div>
                                </bk-popover>
                            </div>
                        </bk-col>
                    </bk-row>
                </bk-container>
            </div>

            <div style="border:1px solid rgb(228 221 228);margin-top: 15px;border-radius: 5px;background-color: white;width: 98%;margin-left: 1%;display: none" id="memDisplay">

                <bk-collapse>
                    <bk-collapse-item>
                        <div style="margin-left: 20px;font-size: 20px;" class="blackFont" @click="pictureClick">占用内存TOP10进程</div>
                    </bk-collapse-item>
                </bk-collapse>

                <div id="pictureDiv" style="display: none">
                    <bk-divider></bk-divider>
                    <div id="picture" style="width:450px;height: 400px;float: left" class="inlineBlock"></div>
                    <div style="height: 400px;font-size: 12px;margin-top: 30px;margin-left: 20px" class="inlineBlock">
                        <div style="height: 400px;" class="inlineBlock">
                            <div class="circleProcess">
                                <bk-icon style="color: rgb(84, 112, 198)" type="circle-shape" />
                                &nbsp;<span style="color: grey;width: 100px">{{ memoryTop.process[0] }} &nbsp;&nbsp;|&nbsp;&nbsp;{{ processValue[0]['value'] }}% &nbsp;&nbsp;占用内存</span>
                            </div>
                            <div>
                                <div class="circleProcess">
                                    <bk-icon style="color: rgb(145, 204, 117)" type="circle-shape" />
                                    &nbsp;<span style="color: grey">{{ memoryTop.process[1] }} &nbsp;&nbsp;|&nbsp;&nbsp;{{ processValue[1]['value'] }}% &nbsp;&nbsp;占用内存</span>
                                </div>
                            </div>
                            <div>
                                <div class="circleProcess">
                                    <bk-icon style="color: rgb(250, 200, 88)" type="circle-shape" />
                                    &nbsp;<span style="color: grey;">{{ memoryTop.process[2] }} &nbsp;&nbsp;|&nbsp;&nbsp;{{ processValue[2]['value'] }}% &nbsp;&nbsp;占用内存</span>
                                </div>
                            </div>
                            <div>
                                <div class="circleProcess">
                                    <bk-icon style="color: rgb(238, 102, 102)" type="circle-shape" />
                                    &nbsp;<span style="color: grey">{{ memoryTop.process[3] }} &nbsp;&nbsp;|&nbsp;&nbsp;{{ processValue[3]['value'] }}% &nbsp;&nbsp;占用内存大小</span>
                                </div>
                            </div>
                            <div>
                                <div class="circleProcess">
                                    <bk-icon style="color: rgb(115, 192, 222)" type="circle-shape" />
                                    &nbsp;<span style="color: grey">{{ memoryTop.process[4] }} &nbsp;&nbsp;|&nbsp;&nbsp; {{ processValue[4]['value'] }}% &nbsp;&nbsp;占用内存</span>
                                </div>
                            </div>
                        </div>
                        <div style="height: 400px;margin-left: 40px" class="inlineBlock">
                            <div class="circleProcess">
                                <bk-icon style="color: rgb(59, 162, 114)" type="circle-shape" />
                                &nbsp;<span style="color: grey;width: 50px">{{ memoryTop.process[5] }} &nbsp;&nbsp;|&nbsp;&nbsp;{{ processValue[5]['value'] }}% &nbsp;&nbsp;占用内存</span>
                            </div>
                            <div>
                                <div class="circleProcess">
                                    <bk-icon style="color: rgb(252, 132, 82)" type="circle-shape" />
                                    &nbsp;<span style="color: grey">{{ memoryTop.process[6] }} &nbsp;&nbsp;|&nbsp;&nbsp;{{ processValue[6]['value'] }}% &nbsp;&nbsp;占用内存</span>
                                </div>
                            </div>
                            <div>
                                <div class="circleProcess">
                                    <bk-icon style="color: rgb(154, 96, 180)" type="circle-shape" />
                                    &nbsp;<span style="color: grey">{{ memoryTop.process[7] }} &nbsp;&nbsp;|&nbsp;&nbsp;{{ processValue[7]['value'] }}% &nbsp;&nbsp;占用内存</span>
                                </div>
                            </div>
                            <div>
                                <div class="circleProcess">
                                    <bk-icon style="color: rgb(234, 124, 204)" type="circle-shape" />
                                    &nbsp;<span style="color: grey">{{ memoryTop.process[8] }} &nbsp;&nbsp;|&nbsp;&nbsp;{{ processValue[8]['value'] }}% &nbsp;&nbsp;占用内存</span>
                                </div>
                            </div>
                            <div>
                                <div class="circleProcess">
                                    <bk-icon style="color: rgb(84, 112, 198)" type="circle-shape" />
                                    &nbsp;<span style="color: grey">{{ memoryTop.process[9] }} &nbsp;|&nbsp;&nbsp; {{ processValue[9]['value'] }}% &nbsp;&nbsp;占用内存</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <bk-collapse>
                <div style="border:1px solid rgb(228 221 228);margin-top: 15px;border-radius: 5px;background-color: white;width: 98%;margin-left: 1%">
                    <bk-collapse-item name="1">
                        <div style="margin-left: 20px;font-size: 20px;margin-top: 2px" class="blackFont">基本信息</div>
                        <div slot="content">
                            <bk-divider></bk-divider>
                            <div class="" style="">
                                <div class="wrapper">
                                    <bk-container :col="12">
                                        <bk-row>
                                            <bk-col :span="6" v-for="(item, index) in systemBaseInfo" v-bind:key="index" style="font-size: 14px;">
                                                <div style="float: left;width: 33%;margin-top: 10px;margin-left: 15px;color: #0f0f0f;margin-bottom: 10px">{{ item.check_option }}:</div>
                                                <div style="margin-top: 10px;color: #0f0f0f;margin-bottom: 10px">{{ item.check_result }}</div>
                                            </bk-col>
                                        </bk-row>
                                    </bk-container>
                                </div>
                            </div>
                        </div>
                    </bk-collapse-item>
                </div>

                <div v-for="(item, index) in allQuotaList" v-bind:key="index" style="border:1px solid rgb(228 221 228);margin-top: 15px;border-radius: 5px;background-color: white;width: 98%;margin-left: 1%;">
                    <bk-collapse-item :name="index">
                        <div style="margin-left: 20px;font-size: 20px;margin-top: 2px" class="blackFont">
                            <span style="display: inline-block;width: 150px">{{ item.name }}</span>
                            <div v-if="item.error_num > 0" class="inlineBlock" style="font-size: 15px;margin-left: 30px;width: 300px">
                                <bk-badge val="!" :theme="'danger'" radius="50" position="right"></bk-badge>
                                发现异常服务共<span style="color: red;font-size: 13px">[{{ item.error_num }}]</span>条</div>
                        </div>
                        <div slot="content" class="">
                            <bk-divider></bk-divider>
                            <bk-table style="margin-top: 15px;font-size: 15px;margin-left: 15px;width: 99%"
                                      :data="item.info"
                                      :size="size">
                                <bk-table-column label="检查项" prop="check_option" style="font-size: 30px"></bk-table-column>
                                <bk-table-column label="检查结果" prop="check_result">
                                    <template slot-scope="scope">
                                        <span v-if="scope.row.status === 'false'"><span style="color: red">{{ scope.row.check_result }}</span></span>
                                        <span v-if="scope.row.status !== 'false'"><span style="">{{ scope.row.check_result }}</span></span>
                                    </template>
                                </bk-table-column>
                                <bk-table-column label="推荐值" prop="recommend_value"></bk-table-column>
                            </bk-table>
                            <br />
                        </div>
                    </bk-collapse-item>
                </div>
            </bk-collapse>

        </div>
        <bk-button theme="primary" id="errorButton" @click="errorInfo" style="display: none"></bk-button>
    </div>

</template>

<script>
    const echarts = require('echarts/lib/echarts')
    // 引入饼状图组件
    require('echarts/lib/chart/pie')
    // 引入提示框和title组件
    require('echarts/lib/component/tooltip')
    require('echarts/lib/component/title')

    export default {
        name: 'reportLinuxDetail',
        filters: {
            checkResult (arg) {
                if (arg === 'true') {
                    return '启用'
                }
                return arg
            }
        },
        data () {
            return {
                colSpan: 3,
                fullWidth: document.documentElement.clientWidth,

                data: {
                    'pictureRound': 'false'
                },

                error: {
                    title: '数据请求失败',
                    msg: ''
                },

                detailDialog: {
                    directive: {
                        visible: false,
                        dialogTittle: '',
                        dialogData: []
                    }
                },

                themeInfo: ['danger', 'warning', 'success', 'info', 'primary'],

                taskHost: '',

                inspectionInfo: {
                    'error_detail': []
                },
                percent: 0, // 巡检概览异常指标百分比%
                inspectionContent: '',

                // 请求后端的数据
                paramForm: {
                    'os': '',
                    'execute_id': '',
                    'host': ''
                },

                // cpu memory disk inode使用率
                hostRate: {
                    'cpu': [],
                    'memory': [],
                    'disk': [],
                    'inode': []
                },

                singleDisk: {},
                singleInode: {},

                basicLoading: true,
                size: 'small',
                width: '200px',
                config: {
                    strokeWidth: 12,
                    bgColor: '#2aabd2',
                    activeColor: '#ea3636'
                },
                tagConfig: {
                    strokeWidth: 12,
                    bgColor: '#2aabd2',
                    activeColor: '#ea3636'
                },
                // 占用内存TOP10进程
                memoryTop: {
                    'memory': '',
                    'process': [],
                    'processValue': []
                },
                processValue: [{ 'name': '', 'value': '' }, { 'name': '', 'value': '' }, { 'name': '', 'value': '' }, { 'name': '', 'value': '' }, { 'name': '', 'value': '' }, { 'name': '', 'value': '' }, { 'name': '', 'value': '' }, { 'name': '', 'value': '' }, { 'name': '', 'value': '' }, { 'name': '', 'value': '' }],

                // 系统配置信息
                // 基本信息
                systemBaseInfo: '',

                allQuotaList: []
            }
        },

        created () {
            this.handleResize()
            window.addEventListener('resize', this.handleResize)
        },
        beforeDestroy () {
            window.removeEventListener('resize', this.handleResize)
        },

        mounted () {
            this.paramForm.os = this.$route.query.os
            this.paramForm.execute_id = this.$route.query.execute_id
            this.paramForm.host = this.$route.query.host
            this.fetchLinuxDetail()
        },

        methods: {
            // 动态获取当前屏幕宽度
            handleResize (event) {
                this.fullWidth = document.documentElement.clientWidth
                this.colSpan = 3
            },

            fetchLinuxDetail () {
                const self = this
                const infos = this.$store.dispatch('fetch_inspection_report_detail', this.paramForm)
                infos.then(function (result) {
                    if (result.code) {
                        self.error.msg = result.message
                        document.getElementById('errorButton').click()
                        return
                    }

                    self.taskHost = result.data.task_host
                    // ------- 巡检概览
                    if (result.data.inspection_info) {
                        self.divDiaplay('divInspectionInfo')
                        self.inspectionInfo = result.data.inspection_info
                        self.percent = self.inspectionInfo.error_percent / 100
                        self.inspectionContent = '异常指标数' + self.inspectionInfo.error_percent + '%'
                    }
                    // ----- CPU，物理内存，硬盘空间 inode(使用率）

                    self.hostRate = result.data.host_rate
                    console.log(self.hostRate.cpu[0])
                    if (self.hostRate.cpu[0]) {
                        self.hostRate.cpu = self.hostRate.cpu[0]
                        self.hostRate.cpu.percent = self.hostRate.cpu.percentInt / 100
                    } else {
                        self.hostRate.cpu = {
                            result_status: true,
                            percent: 0,
                            percentInt: 0
                        }
                    }

                    // if (!self.hostRate.cpu[0]) {
                    //     self.hostRate.cpu = {
                    //         result_status: true,
                    //         percent: 0,
                    //         percentInt: 0
                    //     }
                    // }

                    if (self.hostRate.memory[0]) {
                        self.hostRate.memory = self.hostRate.memory[0]
                        self.hostRate.memory.percent = self.hostRate.memory.percentInt / 100
                    } else {
                        self.hostRate.memory = {
                            result_status: true,
                            percent: 0,
                            percentInt: 0
                        }
                    }

                    // if (!self.hostRate.memory[0]) {
                    //     self.hostRate.memory = {
                    //         result_status: true,
                    //         percent: 0,
                    //         percentInt: 0
                    //     }
                    // }

                    if (self.hostRate.disk) {
                        self.singleDisk = self.hostRate.disk[0]
                    }
                    if (self.hostRate.inode) {
                        self.singleInode = self.hostRate.inode[0]
                    }
                    // -------- 占用内存TOP10进程
                    if (result.data.memory_top.processValue) {
                        self.divDiaplay('memDisplay')
                        self.memoryTop = result.data.memory_top
                        self.processValue = result.data.memory_top.processValue
                    }
                    // -------- 系统信息
                    self.systemBaseInfo = result.data.base_info
                    self.allQuotaList = result.data.table_list_sorted

                    if (self.memoryTop.process !== '') {
                        self.initData()
                    }
                    self.basicLoading = false
                })
            },
            jumpReportHistory () {
                // this.$router.push('/report/history')
                this.$router.push({
                    name: 'historyReport'
                })
            },

            dialogSetting (arg) {
                this.detailDialog.directive.dialogTittle = this.inspectionInfo.error_detail[arg].class_name
                this.detailDialog.directive.dialogData = this.inspectionInfo.error_detail[arg].error_info
                this.detailDialog.directive.visible = true
            },

            divDiaplay (id) {
                document.getElementById(id).style.display = 'block'
            },

            initData () {
                // 基于准备好的dom，初始化echarts实例
                const myChart = echarts.init(document.getElementById('picture'))

                // 绘制图表
                myChart.setOption({
                    title: {
                        text: '内存\n' + this.memoryTop.memory,
                        // subtext: '',
                        x: 'center',
                        y: 'center'
                    },
                    tooltip: {
                        trigger: 'item',
                        // formatter: '{a} <br/>{b} : {c} ({d}%)'
                        formatter: '{a}:{b}({c}%)'
                    },
                    legend: {
                        orient: 'vertical',
                        bottom: 'bottom',
                        data: this.memoryTop.process
                    },

                    series: [
                        {
                            name: '进程名称',
                            type: 'pie',
                            radius: ['30%', '70%'],
                            // left: ['50%', '60%'],
                            center: '50%',
                            data: this.memoryTop.processValue,
                            itemStyle: {
                                emphasis: {
                                    shadowBlur: 10,
                                    shadowOffsetX: 1,
                                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                                }
                            }
                        }
                    ]
                })
            },
            pictureClick () {
                if (this.data.pictureRound === 'true') {
                    this.data.pictureRound = 'false'
                    document.getElementById('pictureDiv').style.display = 'none'
                    return
                }
                if (this.data.pictureRound === 'false') {
                    this.data.pictureRound = 'true'
                    document.getElementById('pictureDiv').style.display = 'block'
                }
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

<style lang="postcss" scoped>
    .usageRateInfoContainer {
        width: 98%;
        min-height: 150px;
        padding: 5px;
        margin: 20px auto 0 auto;
        border-radius: 5px;
        background: #fff;
    }
    /deep/.bk-grid-row {
        margin-top: 0 !important;
    }

    /deep/.bk-tooltip {
        width: 100%;
    }

    /deep/.bk-grid-container { padding: 5px !important }

    /deep/.bk-tooltip-ref {
        width: 100%;
    }

    /deep/.active .num {
        color: #f00 !important;
    }

    .circleCss {
        margin-top: 15px;
    }
    .inlineBlock {
        display: inline-block;
    }
    .circleProcess {
        margin-top: 15%;
    }
    .blackFont {
        color: #0f0f0f;
    }
    .bk-grid-row {
        margin-top: 20px;
    }
    .greyFont {
        color: grey;
    }
</style>
