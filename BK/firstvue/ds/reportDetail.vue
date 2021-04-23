<template>
    <div style="margin-top: 20px" class="wrapper">
        <div style="border:1px solid rgb(228 221 228);height: 150px">
            <bk-container :col="12">
                <bk-row>
                    <bk-col :span="2">
                        <div class="">
                            <i class="el-icon-s-platform" style="font-size: 100px;margin-left: 30px"></i>
                        </div>
                        <div style="margin-left: 38%">
                            linux
                        </div>
                    </bk-col>
                    <bk-col :span="7">
                        <div class="" style="margin-top: 10px;font-size: 25px;margin-left: 20px;">139.155.233.199</div>
                        <div class="" style="margin-top: 10px">创建时间：2020-12-25 11:32:39</div>
                        <div class="" style="margin-top: 10px">完成时间：2020-12-31 15:30:39</div>
                    </bk-col>
                    <bk-col :span="3"><div class="">
                        <bk-button title="primary" :text="true" :hover-theme="'primary'" @click="jumpReportHistory" style="border-radius: 20px;margin-left: 60%;margin-bottom: 20px;margin-top: 10px">
                            返回<bk-icon type="back2" />
                        </bk-button>
                    </div></bk-col>
                </bk-row>
            </bk-container>
        </div>

                <div style="border:1px solid rgb(228 221 228);margin-top: 20px;border-radius: 5px">
                    <div style="margin-left: 20px;margin-top: 12px;font-size: larger">巡检概览</div>
                    <bk-divider></bk-divider>
                    <bk-container :col="12">
                        <bk-row>
                            <bk-col :span="4">
                                    <div class="content">
                                        <div class="round"  align="center">
                                            <bk-round-progress :width="width" :percent="percent" :config="config" content="异常指标数29%"></bk-round-progress>
                                        </div>
                                    </div>
                            </bk-col>
                            <bk-col :span="8">
                                <div style="font-size: 20px">总体健康情况良好，共巡检72个指标，异常指标数21个，占比29%</div>
                                <div class="circleCss">
                                    <bk-badge class="mr5" val="1" :theme="'danger'" radius="50" position="right"></bk-badge>
                                    安全配置信息
                                    <div class="inlineBlock" style="margin-left: 20%;color: red">14</div>
                                    <div class="inlineBlock" style="margin-left: 9%">
                                        <bk-link underline theme="default" href="/" target="_blank">详情</bk-link>
                                    </div>
                                </div>
                                <div class="circleCss">
                                    <bk-badge class="mr5" val="2" :theme="'warning'" radius="50" position="right"></bk-badge>
                                    系统运行状态信息
                                    <div class="inlineBlock" style="margin-left: 15.5%;color: burlywood">3</div>
                                    <div class="inlineBlock" style="margin-left: 10%">
                                        <bk-link underline theme="default" href="/" target="_blank">详情</bk-link>
                                    </div>
                                </div>
                                <div class="circleCss">
                                    <bk-badge class="mr5" val="3" :theme="'success'" radius="50" position="right"></bk-badge>
                                    系统性能信息
                                    <div class="inlineBlock" style="margin-left: 20%;color: green">2</div>
                                    <div class="inlineBlock" style="margin-left: 10%">
                                        <bk-link underline theme="default" href="/" target="_blank">详情</bk-link>
                                    </div>
                                </div>
                                <div class="circleCss">
                                    <bk-badge class="mr5" val="4" :theme="'info'" radius="50" position="right"></bk-badge>
                                    系统信息
                                    <div class="inlineBlock" style="margin-left: 24.5%;color: blue">2</div>
                                    <div class="inlineBlock" style="margin-left: 10%">
                                        <bk-link underline theme="default" href="/" target="_blank">详情</bk-link>
                                    </div>
                                </div>
                            </bk-col>

                        </bk-row>
                    </bk-container>
                </div>

        <div style=";margin-top: 20px;border-radius: 5px;height: 150px">
            <div style="width: 20%;border:1px solid rgb(228 221 228);height: 140px;" class="inlineBlock">
                <div style="width: 45%" class="inlineBlock">
                    <i style="margin-left: 10px;">CPU使用率</i><br />
                    <span style="font-size: 20px;margin-left: 10px">17%</span><br />
                    <span style="font-size: 25px;margin-left: 10px"></span><br />
                    <span style="font-size: 25px;margin-left: 10px"></span><br />
                </div>
                <div style="width: 45%" class="inlineBlock">
                    <bk-round-progress width="100px" :config="tagConfig" :percent="cpuPercent" style="margin-top: 20px;margin-left: 10px"></bk-round-progress>
                </div>
            </div>

            <div style="width: 25%;border:1px solid rgb(228 221 228);height: 140px;" class="inlineBlock">
                <div style="width: 55%;" class="inlineBlock">
                    <i style="margin-left: 10px;">物理内存使用率</i><br />
                    <span style="font-size: 20px;margin-left: 10px">20%</span><br />
                    <span style="font-size: 4px;margin-left: 10px">内存总量：32011M</span><br />
                    <span style="font-size: 4px;margin-left: 10px">空闲内存：25420M</span><br />
                    <span style="font-size: 4px;margin-left: 10px"></span><br />
                </div>
                <div style="width: 40%" class="inlineBlock">
                    <bk-round-progress width="100px" :config="tagConfig" :percent="memPercent" style="margin-top: 20px;margin-left: 10px"></bk-round-progress>
                </div>
            </div>
            <div style="width: 25%;border:1px solid rgb(228 221 228);height: 140px;" class="inlineBlock">
                <div style="width: 55%" class="inlineBlock">
                    <i style="margin-left: 10px">硬盘空间使用率</i><br />
                    <span style="font-size: 20px;margin-left: 10px">4%</span><br />
                    <span style="font-size: 4px;margin-left: 10px">硬盘总量：5033333836M</span><br />
                    <span style="font-size: 4px;margin-left: 10px">可用空间：4633338195M</span><br />
                    <span style="font-size: 4px;margin-left: 10px"></span><br />
                </div>
                <div style="width: 40%" class="inlineBlock">
                    <bk-round-progress width="100px" :config="tagConfig" :percent="diskPercent" style="margin-top: 20px;margin-left: 10px"></bk-round-progress>
                </div>
            </div>
            <div style="width: 28%;border:1px solid rgb(228 221 228);height: 140px;" class="inlineBlock">
                <div style="width: 60%" class="inlineBlock">
                    <i style="margin-left: 5px">Inode使用率</i><br />
                    <span style="font-size: 20px;margin-left: 10px">10%</span><br />
                    <span style="font-size: 4px;margin-left: 10px">Inode总量：38333077700M</span><br />
                    <span style="font-size: 4px;margin-left: 10px">可用空间：32603335653M</span><br />
                    <span style="font-size: 4px;margin-left: 10px"></span><br />
                </div>
                <div style="width: 35%" class="inlineBlock">
                    <bk-round-progress width="100px" :config="tagConfig" :percent="inNodePercent" style="margin-top: 20px;margin-left: 10px"></bk-round-progress>
                </div>
            </div>

        </div>

        <div style="border:1px solid rgb(228 221 228);margin-top: 15px;border-radius: 5px">

            <bk-collapse>
                <bk-collapse-item>
                    <div style="margin-left: 20px;font-size: larger;" class="blackFont" @click="pictureClick">占用内存TOP10进程</div>
                </bk-collapse-item>
            </bk-collapse>

            <div id="pictureDiv" style="display: none">
                <bk-divider></bk-divider>
                <div id="picture" style="width:500px;height: 400px;float: left" class="inlineBlock"></div>
                <div style="height: 400px;" class="inlineBlock">
                    <div style="height: 400px;" class="inlineBlock">
                        <div class="circleProcess">
                            <bk-icon style="color: rgb(84, 112, 198)" type="circle-shape" />
                            &nbsp;进程1 &nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; 36% &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 占用内存大小
                        </div>
                        <div>
                            <div class="circleProcess">
                            <bk-icon style="color: rgb(145, 204, 117)" type="circle-shape" />
                            &nbsp;进程2 &nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; 36% &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 占用内存大小
                        </div>
                        </div>
                        <div>
                            <div class="circleProcess">
                            <bk-icon style="color: rgb(250, 200, 88)" type="circle-shape" />
                            &nbsp;进程3 &nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; 36% &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 占用内存大小
                        </div>
                        </div>
                        <div>
                            <div class="circleProcess">
                            <bk-icon style="color: rgb(238, 102, 102)" type="circle-shape" />
                            &nbsp;进程4 &nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; 36% &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 占用内存大小
                        </div>
                        </div>
                        <div>
                            <div class="circleProcess">
                            <bk-icon style="color: rgb(115, 192, 222)" type="circle-shape" />
                            &nbsp;进程5 &nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; 36% &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;占用内存大小
                        </div>
                        </div>
                    </div>
                    <div style="height: 400px;" class="inlineBlock">
                        <div class="circleProcess">
                            <bk-icon style="color: rgb(59, 162, 114)" type="circle-shape" />
                            &nbsp;进程6 &nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 36% &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;占用内存大小
                        </div>
                        <div>
                            <div class="circleProcess">
                            <bk-icon style="color: rgb(252, 132, 82)" type="circle-shape" />
                            &nbsp;进程7 &nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 36% &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;占用内存大小
                        </div>
                        </div>
                        <div>
                            <div class="circleProcess">
                            <bk-icon style="color: rgb(154, 96, 180)" type="circle-shape" />
                            &nbsp;进程8 &nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 36% &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;占用内存大小
                        </div>
                        </div>
                        <div>
                            <div class="circleProcess">
                            <bk-icon style="color: rgb(234, 124, 204)" type="circle-shape" />
                            &nbsp;进程9 &nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 36% &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;占用内存大小
                        </div>
                        </div>
                        <div>
                            <div class="circleProcess">
                            <bk-icon style="color: rgb(84, 112, 198)" type="circle-shape" />
                            &nbsp;进程10 &nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 36% &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 占用内存大小
                        </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>

        <bk-collapse>
            <div style="border:1px solid rgb(228 221 228);margin-top: 15px;border-radius: 5px">
                <bk-collapse-item name="1">
                    <div style="margin-left: 20px;font-size: larger" class="blackFont">系统信息</div>
                <div slot="content">
                    <bk-divider></bk-divider>
                    <div style="margin-left: 20px;" class="blackFont">基本信息</div>
                    <div class="wrapper">
                        <bk-container :col="12" margin="20">
                            <bk-row>
                                <bk-col :span="3">
                                    <div class="blackFont" style="float: left;width: 50%">主机名:</div>
                                    <div class="blackFont">test</div>
                                </bk-col>
                                <bk-col :span="3">
                                    <div class="blackFont" style="float: left;width: 50%">物理内存大小:</div>
                                    <div class="blackFont">10T</div>
                                </bk-col>
                                <bk-col :span="3">
                                    <div class="blackFont" style="float: left;width: 70%">交换分区大小:</div>
                                    <div class="blackFont">2T</div>
                                </bk-col>
                                <bk-col :span="3">
                                    <div class="blackFont" style="float: left;width: 50%">硬盘大小:</div>
                                    <div class="blackFont">10G</div>
                                </bk-col>
                            </bk-row>
                            <bk-row>
                                <bk-col :span="3">
                                    <div class="blackFont" style="float: left;width: 50%">CPU类型:</div>
                                    <div class="blackFont">AMD</div>
                                </bk-col>
                                <bk-col :span="3">
                                    <div class="blackFont" style="float: left;width: 50%">CPU个数:</div>
                                    <div class="blackFont">32</div>
                                </bk-col>
                                <bk-col :span="3">
                                    <div class="blackFont" style="float: left;width: 70%">CPU核心数:</div>
                                    <div class="blackFont">64</div>
                                </bk-col>
                                <bk-col :span="3">
                                    <div class="blackFont" style="float: left;width: 50%">操作系统版本:</div>
                                    <div class="blackFont">Centos</div>
                                </bk-col>
                            </bk-row>

                            <bk-row>
                                <bk-col :span="3">
                                    <div class="blackFont" style="float: left;width: 50%">系统在线时长:</div>
                                    <div class="blackFont">100天</div>
                                </bk-col>
                                <bk-col :span="3">
                                    <div class="blackFont" style="float: left;width: 50%">服务器时间:</div>
                                    <div class="blackFont">360天</div>
                                </bk-col>
                                <bk-col :span="3">
                                    <div class="blackFont" style="float: left;width: 70%">最大文件句柄数设置:</div>
                                    <div class="blackFont">200</div>
                                </bk-col>
                                <bk-col :span="3"></bk-col>
                            </bk-row>

                        </bk-container>
                        <bk-divider></bk-divider>
                    </div>
                    <div style="margin-left: 20px;" class="blackFont">系统配置信息</div>
                    <bk-table style="margin-top: 15px;font-size: 15px;margin-left: 15px;width: 99%"
                    :data="systemConfigDate"
                    :size="size">
                    <bk-table-column label="检查项" prop="check_option" style="font-size: 30px"></bk-table-column>
                    <bk-table-column label="检查结果" prop="check_result">
                        <template slot-scope="scope">
                            <span v-if="scope.row.check_result === 'false'"><span style="color: red">未启用</span></span>
                            <span v-if="scope.row.check_result !== 'false'">{{scope.row.check_result | checkResult}}</span>
                        </template>
                    </bk-table-column>
                    <bk-table-column label="推荐值" prop="recommend_value"></bk-table-column>
                </bk-table>
                    <br />
                </div>
            </bk-collapse-item>
            </div>

            <div style="border:1px solid rgb(228 221 228);margin-top: 15px;border-radius: 5px">
                <bk-collapse-item name="2">
                    <div style="margin-left: 20px;font-size: larger" class="blackFont">安全配置信息</div>
                    <div slot="content" class="">
                        <bk-divider></bk-divider>
                        <div style="margin-left: 20px;" class="blackFont">账号安全</div>
                        <bk-table style="margin-top: 15px;font-size: 15px;margin-left: 15px;width: 99%"
                            :data="accountConfigDate"
                            :size="size">
                            <bk-table-column label="检查项" prop="check_option" style="font-size: 30px"></bk-table-column>
                            <bk-table-column label="检查结果" prop="check_result">
                                <template slot-scope="scope">
                                    <span v-if="scope.row.check_result === 'false'"><span style="color: red">未启用</span></span>
                                    <span v-if="scope.row.check_result !== 'false'">{{scope.row.check_result | checkResult}}</span>
                                </template>
                            </bk-table-column>
                            <bk-table-column label="推荐值" prop="recommend_value"></bk-table-column>
                        </bk-table>
                        <br />
<!--                        &#45;&#45;-->
                        <div style="margin-left: 20px;" class="blackFont">系统安全</div>
                        <bk-table style="margin-top: 15px;font-size: 15px;margin-left: 15px;width: 99%"
                            :data="systemSafeDate"
                            :size="size">
                            <bk-table-column label="检查项" prop="check_option" style="font-size: 30px"></bk-table-column>
                            <bk-table-column label="检查结果" prop="check_result">
                                <template slot-scope="scope">
                                    <span v-if="scope.row.check_result === 'false'"><span style="color: red">未启用</span></span>
                                    <span v-if="scope.row.check_result !== 'false'">{{scope.row.check_result | checkResult}}</span>
                                </template>
                            </bk-table-column>
                            <bk-table-column label="推荐值" prop="recommend_value"></bk-table-column>
                        </bk-table>
                        <br />
<!--                        &#45;&#45;-->
                        <div style="margin-left: 20px;" class="blackFont">SSH安全设置</div>
                        <bk-table style="margin-top: 15px;font-size: 15px;margin-left: 15px;width: 99%"
                            :data="sshSafeDate"
                            :size="size">
                            <bk-table-column label="检查项" prop="check_option" style="font-size: 30px"></bk-table-column>
                            <bk-table-column label="检查结果" prop="check_result">
                                <template slot-scope="scope">
                                    <span v-if="scope.row.check_result === 'false'"><span style="color: red">未启用</span></span>
                                    <span v-if="scope.row.check_result !== 'false'">{{scope.row.check_result | checkResult}}</span>
                                </template>
                            </bk-table-column>
                            <bk-table-column label="推荐值" prop="recommend_value"></bk-table-column>
                        </bk-table>
                        <br />
<!--                        &#45;&#45;-->
                        <div style="margin-left: 20px;" class="blackFont">用户安全</div>
                        <bk-table style="margin-top: 15px;font-size: 15px;margin-left: 15px;width: 99%"
                            :data="userSafeDate"
                            :size="size">
                            <bk-table-column label="检查项" prop="check_option" style="font-size: 30px"></bk-table-column>
                            <bk-table-column label="检查结果" prop="check_result">
                                <template slot-scope="scope">
                                    <span v-if="scope.row.check_result === 'false'"><span style="color: red">未启用</span></span>
                                    <span v-if="scope.row.check_result !== 'false'">{{scope.row.check_result | checkResult}}</span>
                                </template>
                            </bk-table-column>
                            <bk-table-column label="推荐值" prop="recommend_value"></bk-table-column>
                        </bk-table>
                        <br />
<!--                        &#45;&#45;-->
                        <div style="margin-left: 20px;" class="blackFont">网络安全</div>
                        <bk-table style="margin-top: 15px;font-size: 15px;margin-left: 15px;width: 99%"
                            :data="interSafeDate"
                            :size="size">
                            <bk-table-column label="检查项" prop="check_option" style="font-size: 30px"></bk-table-column>
                            <bk-table-column label="检查结果" prop="check_result">
                                <template slot-scope="scope">
                                    <span v-if="scope.row.check_result === 'false'"><span style="color: red">未启用</span></span>
                                    <span v-if="scope.row.check_result !== 'false'">{{scope.row.check_result | checkResult}}</span>
                                </template>
                            </bk-table-column>
                            <bk-table-column label="推荐值" prop="recommend_value"></bk-table-column>
                        </bk-table>
                        <br />
                    </div>
                </bk-collapse-item>
            </div>

            <div style="border:1px solid rgb(228 221 228);margin-top: 15px;border-radius: 5px">
                <bk-collapse-item name="3">
                    <div style="margin-left: 20px;font-size: larger" class="blackFont">系统运行状态信息</div>
                    <div slot="content" class="">
                        <bk-divider></bk-divider>
                        <div style="margin-left: 20px;" class="blackFont">系统运行状态</div>
                        <bk-table style="margin-top: 15px;font-size: 15px;margin-left: 15px;width: 99%"
                            :data="systemRunStatus"
                            :size="size">
                            <bk-table-column label="检查项" prop="check_option" style="font-size: 30px"></bk-table-column>
                            <bk-table-column label="检查结果" prop="check_result">
                                <template slot-scope="scope">
                                    <span v-if="scope.row.check_result === 'false'"><span style="color: red">未启用</span></span>
                                    <span v-if="scope.row.check_result !== 'false'">{{scope.row.check_result | checkResult}}</span>
                                </template>
                            </bk-table-column>
                            <bk-table-column label="推荐值" prop="recommend_value"></bk-table-column>
                        </bk-table>
                        <br />
                    </div>
                </bk-collapse-item>
            </div>

            <div style="border:1px solid rgb(228 221 228);margin-top: 15px;border-radius: 5px">
                <bk-collapse-item name="4">
                    <div style="margin-left: 20px;font-size: larger" class="blackFont">系统性能信息</div>
                    <div slot="content" class="">
                        <bk-divider></bk-divider>
                        <div style="margin-left: 20px;" class="blackFont">系统性能信息</div>
                        <bk-table style="margin-top: 15px;font-size: 15px;margin-left: 15px;width: 99%"
                            :data="systemPerformanceInfo"
                            :size="size">
                            <bk-table-column label="检查项" prop="check_option" style="font-size: 30px"></bk-table-column>
                            <bk-table-column label="检查结果" prop="check_result">
                                <template slot-scope="scope">
                                    <span v-if="scope.row.status === 'false'"><span style="color: red">{{ scope.row.check_result }}</span></span>
                                    <span v-if="scope.row.status !== 'false'">{{ scope.row.check_result }}</span>
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

</template>

<script>
    const echarts = require('echarts/lib/echarts')
    // 引入饼状图组件
    require('echarts/lib/chart/pie')
    // 引入提示框和title组件
    require('echarts/lib/component/tooltip')
    require('echarts/lib/component/title')

    export default {
        name: 'checkReport',
        filters: {
            checkResult (arg) {
                if (arg === 'true') {
                    return '启用'
                }
                return arg
            },
            checkResultOfNum (param) {
                const result = param.check_result
                const recommend = param.recommend_value
                console.log(result, recommend)
                if (recommend.indexOf('>') !== -1) {
                    const le = recommend.split('=').length
                    if (result > recommend[le]) {
                        return result
                    } else {
                        const ht = '<span style="color: red">' + result + '</span>'
                        return '<span v-html="' + ht + '"></span>'
                    }
                }
                if (recommend.indexOf('<') !== -1) {
                    const se = recommend.split('=').length
                    console.log(se)
                }
                return result
            }
        },
        data () {
            return {
                data: {
                    'mem': 32011,
                    'pictureRound': 'false'
                },
                size: 'small',
                cpuPercent: 0.17,
                memPercent: 0.2,
                diskPercent: 0.04,
                inNodePercent: 0.1,
                percent: 0.29,
                width: '200px',
                config: {
                    strokeWidth: 12,
                    bgColor: '#f0f1f5',
                    activeColor: '#ea3636'
                },
                tagConfig: {
                    strokeWidth: 12,
                    bgColor: 'green',
                    activeColor: '#ea3636'
                },
                // 系统配置信息
                systemConfigDate: [
                    {
                        check_option: 'NTP配置',
                        check_result: 'false',
                        recommend_value: '启用'
                    },
                    {
                        check_option: 'LVM配置',
                        check_result: 'false',
                        recommend_value: '启用'
                    },
                    {
                        check_option: '系统运行模式',
                        check_result: '3',
                        recommend_value: '3'
                    },
                    {
                        check_option: 'syslog日志审核',
                        check_result: 'true',
                        recommend_value: '启用'
                    },
                    {
                        check_option: 'syslog日志转储策略',
                        check_result: 'true',
                        recommend_value: '启用'
                    },
                    {
                        check_option: '系统审计功能',
                        check_result: 'true',
                        recommend_value: '启用'
                    },
                    {
                        check_option: '网络日志服务器功能',
                        check_result: 'true',
                        recommend_value: '启用'
                    }
                ],

                // 账号安全
                accountConfigDate: [
                    {
                        check_option: '空口令的账号',
                        check_result: 'false',
                        recommend_value: '无'
                    },
                    {
                        check_option: 'UID为0的非root账号',
                        check_result: 'true',
                        recommend_value: '无'
                    },
                    {
                        check_option: '拥有sudo权限账号或组',
                        check_result: 'true',
                        recommend_value: '无'
                    },
                    {
                        check_option: '普通账号UMASK值设置',
                        check_result: '22',
                        recommend_value: '27'
                    }
                ],

                // 系统安全
                systemSafeDate: [
                    {
                        check_option: '远程连接的超时时间(S)',
                        check_result: '90',
                        recommend_value: '<=900'
                    },
                    {
                        check_option: 'GRUB密码设置',
                        check_result: 'false',
                        recommend_value: '启用'
                    },
                    {
                        check_option: '系统的CORE DUMP',
                        check_result: 'true',
                        recommend_value: '启用'
                    },
                    {
                        check_option: 'Ctrl+Alt+Del组合键启用状态',
                        check_result: 'false',
                        recommend_value: '关闭'
                    },
                    {
                        check_option: 'Selinux启用状态',
                        check_result: 'false',
                        recommend_value: '关闭'
                    },
                    {
                        check_option: '防火墙启用状态',
                        check_result: 'false',
                        recommend_value: '关闭'
                    }
                ],

                // SSH安全设置
                sshSafeDate: [
                    {
                        check_option: 'GSSAPIAuthentication',
                        check_result: 'yes',
                        recommend_value: 'no'
                    },
                    {
                        check_option: 'GSSAPICleanupCredentials',
                        check_result: 'no',
                        recommend_value: 'no'
                    },
                    {
                        check_option: '协议1/2开启状态',
                        check_result: 'false',
                        recommend_value: '仅开发协议2'
                    },
                    {
                        check_option: '远程root是否开启',
                        check_result: 'true',
                        recommend_value: '启用'
                    },
                    {
                        check_option: 'X11Forwarding',
                        check_result: 'yes',
                        recommend_value: 'no'
                    }
                ],

                // 用户安全
                userSafeDate: [
                    {
                        check_option: '密码最长使用天数',
                        check_result: '9999',
                        recommend_value: '<=90'
                    },
                    {
                        check_option: '密码最短使用天数',
                        check_result: '0',
                        recommend_value: '>=6'
                    },
                    {
                        check_option: '密码需要满足的最短长度',
                        check_result: '8',
                        recommend_value: '>=8'
                    },
                    {
                        check_option: '用户密码到期前警告天数',
                        check_result: '10',
                        recommend_value: '>=10'
                    },
                    {
                        check_option: '用户密码复杂度策略',
                        check_result: 'false',
                        recommend_value: '启用'
                    },
                    {
                        check_option: '密码重复使用次数',
                        check_result: 'false',
                        recommend_value: '>=5'
                    },
                    {
                        check_option: '密码允许尝试登录次数',
                        check_result: 'false',
                        recommend_value: '<=3'
                    },
                    {
                        check_option: '失败登录锁定时间（S）',
                        check_result: '1000',
                        recommend_value: '>=600'
                    }
                ],

                // 网络安全
                interSafeDate: [
                    {
                        check_option: 'IP伪装功能状态',
                        check_result: 'false',
                        recommend_value: '关闭'
                    },
                    {
                        check_option: '多ip绑定功能状态',
                        check_result: 'false',
                        recommend_value: '关闭'
                    },
                    {
                        check_option: '数据包转发功能状态',
                        check_result: 'true',
                        recommend_value: '关闭'
                    },
                    {
                        check_option: 'ICMP接收重定向转发功能',
                        check_result: 'false',
                        recommend_value: '关闭'
                    },
                    {
                        check_option: 'ICMP发送重定向转发功能',
                        check_result: 'false',
                        recommend_value: '关闭'
                    }
                ],

                // 系统运行状态
                systemRunStatus: [
                    {
                        check_option: '设置开机启动但未启动的服务',
                        check_result: 'ftp',
                        recommend_value: '无'
                    },
                    {
                        check_option: '错误日志的数量（messages）',
                        check_result: '8',
                        recommend_value: '0'
                    },
                    {
                        check_option: '错误日志的数量（dmesg）',
                        check_result: '6',
                        recommend_value: '0'
                    },
                    {
                        check_option: '登录失败次数（30天）',
                        check_result: '12500',
                        recommend_value: '<=100'
                    },
                    {
                        check_option: '僵尸进程信息',
                        check_result: '无',
                        recommend_value: '无'
                    }
                ],

                // 系统性能信息
                systemPerformanceInfo: [
                    {
                        check_option: '系统负载状况15min',
                        check_result: '4',
                        recommend_value: '<=3',
                        status: 'false'
                    },
                    {
                        check_option: '交换分区使用率（%）',
                        check_result: '0',
                        recommend_value: '<=10%',
                        status: 'true'
                    },
                    {
                        check_option: '交换分区可用空间（MB）',
                        check_result: '0',
                        recommend_value: '>=512',
                        status: 'false'
                    },
                    {
                        check_option: '硬盘IO使用率（%）',
                        check_result: '10%',
                        recommend_value: '<=90%',
                        status: 'true'
                    },
                    {
                        check_option: 'ESTABLISHED状态的连接数',
                        check_result: '3',
                        recommend_value: '<=2000',
                        status: 'true'
                    },
                    {
                        check_option: 'TIME_WAIT状态的连接数',
                        check_result: '120',
                        recommend_value: '<=500',
                        status: 'true'
                    },
                    {
                        check_option: '网卡当前数据接收速率（kb/s）',
                        check_result: '722',
                        recommend_value: '<=10240',
                        status: 'true'
                    },
                    {
                        check_option: '网卡当前数据发送速率（kb/s）',
                        check_result: '61',
                        recommend_value: '<=1024',
                        status: 'true'
                    }
                ]
            }
        },

        mounted () {
            this.initData()
        },

        methods: {
            jumpReportHistory () {
                // 传递的参数用{{ $route.query.goodsId }}获取
                this.$router.push('/report/history')
                // this.$router.go(-2)
                // 后退两步
            },

            initData () {
                // 基于准备好的dom，初始化echarts实例
                const myChart = echarts.init(document.getElementById('picture'))

                // 绘制图表
                myChart.setOption({
                    title: {
                        text: '内存\n' + this.data.mem + 'M',
                        // subtext: '',
                        x: 'center',
                        y: 'center'
                    },
                    tooltip: {
                        trigger: 'item',
                        formatter: '{a} <br/>{b} : {c} ({d}%)'
                    },
                    legend: {
                        orient: 'vertical',
                        bottom: 'bottom',
                        data: ['进程1', '进程2', '进程3', '进程4', '进程5', '进程6', '进程7', '进程8', '进程9', '进程10']
                    },

                    series: [
                        {
                            name: '访问来源',
                            type: 'pie',
                            radius: ['30%', '70%'],
                            // left: ['50%', '60%'],
                            center: '50%',
                            data: [
                                { value: 10, name: '进程1' },
                                { value: 20, name: '进程2' },
                                { value: 8, name: '进程3' },
                                { value: 12, name: '进程4' },
                                { value: 13, name: '进程5' },
                                { value: 7, name: '进程6' },
                                { value: 23, name: '进程7' },
                                { value: 17, name: '进程8' },
                                { value: 4, name: '进程9' },
                                { value: 6, name: '进程10' }
                            ],
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
            }
        }
    }
</script>

<style lang="postcss">
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
</style>
