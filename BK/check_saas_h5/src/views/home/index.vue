<template>
    <bk-container :col="12">
        <bk-row class="row-home">
            <bk-col :span="3">
                <div class="col-md">
                    <div class="col-md-left" style="background: #44B549;">
                        <bk-icon type="folder-open-shape" />
                    </div>
                    <div class="col-md-right" style="background: #54bf59;">
                        巡检业务数:{{appCount}}
                    </div>
                </div>
            </bk-col>
            <bk-col :span="3">
                <div class="col-md">
                    <div class="col-md-left" style="background: #3a84ff;">
                        <bk-icon type="pc-shape" />
                    </div>
                    <div class="col-md-right" style="background: #699df4;">
                        巡检主机数:{{serverCount}}
                    </div>
                </div>
            </bk-col>
            <bk-col :span="3">
                <div class="col-md">
                    <div class="col-md-left" style="background: #ff9c01;">
                        <bk-icon type="data2-shape" />
                    </div>
                    <div class="col-md-right" style="background: #ffb848;">
                        巡检总次数:{{checkCount}}
                    </div>
                </div>
            </bk-col>
            <bk-col :span="3">
                <div class="col-md">
                    <div class="col-md-left" style="background: #ea3636;">
                        <bk-icon type="exclamation-triangle-shape" />
                    </div>
                    <div class="col-md-right" style="background: #ff5656;">
                        巡检问题主机数:{{errorCount}}
                    </div>
                </div>
            </bk-col>

        </bk-row>
        <bk-row class="row-home">
            <bk-col :span="6">
                <bk-row>
                    <bk-col :span="4">
                        <span class="status-text">巡检动态</span>
                        <bk-timeline class="status-time" :list="dataList">
                        </bk-timeline>
                    </bk-col>
                    <bk-col :span="2"><a class="status-text-a">查看更多</a></bk-col>
                </bk-row>
            </bk-col>
            <bk-col :span="6">
                <canvas id="chart"></canvas>
            </bk-col>
        </bk-row>

    </bk-container>
</template>

<script>
    import Chart from '@blueking/bkchart.js'

    export default {
        components: {},
        data () {
            return {
                chart: null,
                appCount: 0,
                checkCount: 0,
                errorCount: 0,
                serverCount: 0,
                dataList: [
                    { tag: '一天前', content: '由<strong>pony</strong>上线到蓝鲸市场' },
                    { tag: '16:59', content: '<div style="color: red;">由<strong>tony</strong>部署到生产环境并发布至应用市场</div>' },
                    { tag: '一天前', content: '由<strong>allen</strong>部署到预发布环境' },
                    {
                        tag: '2天前',
                        content: '<div>由<strong>allen</strong>上线到<span style="color: #3c96ff;">蓝鲸市场</span></div>'
                    },
                    {
                        tag: '一周前',
                        content: '由<strong>tony</strong>部署到<p style="color: #ff5656">生产环境</p>并发布至<strong>应用市场</strong>'
                    }
                ]
            }
        },
        created () {
            // this.get_count_obj()
        },
        mounted () {
        },
        methods: {
            async get_count_obj () {
                const self = this

                try {
                    const res = await this.$store.dispatch('getCountObj')
                    const { data } = res
                    self.appCount = data.data.app_count
                    self.checkCount = data.data.check_count
                    self.errorCount = data.data.error_count
                    self.serverCount = data.data.server_count
                    self.dataList = data.report_list

                    const context = document.getElementById('chart')
                    self.chart = new Chart(context, {
                        'type': 'line',
                        'data': {
                            'labels': data.task_list.categories,
                            'datasets': [
                                {
                                    'label': '本月巡检次数',
                                    'fill': false,
                                    'backgroundColor': 'rgb(89,255,92)',
                                    'borderColor': 'rgb(24,255,67)',
                                    'data': data.task_list.data
                                }
                            ]
                        },
                        'options': {
                            'layout': { 'padding': 10 },
                            'legend': { 'position': 'bottom' },
                            'title': { 'display': true, 'text': '每月历史巡检次数统计' }
                        }
                    })

                    console.log(data)
                } catch (e) {
                    console.error(e)
                }
            }
        }
    }
</script>

<style scoped>
    @import './index.css';
</style>
