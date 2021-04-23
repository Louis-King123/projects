<template>
    <bk-container :col="12">
        <div class="s-bgc-wt s-pd-20" style="margin-top: 20px;">
            <div>巡检汇总</div>
            <div style="text-align: right">
                <span class="date-tag"
                      :style="{ color: activeDateTagIndex === index ? '#339DFF' : '#5A5A5A' }"
                      v-for="(item, index) in dateTagList"
                      :key="index" @click="changeDateRange"
                      :data-val="index">{{item}}</span>
                <bk-date-picker
                        :value="dateRange"
                        :placeholder="'选择日期范围'"
                        :type="'daterange'"
                        :up-to-now=true
                        :options="datePickerOptions"
                        @change="dateRangeChange"></bk-date-picker>
            </div>
            <div style="display: flex; margin-top: 20px;background-color: #fff;">
                <div class="card-box last" v-for="(item, index) in checkStatistics" :key="index">
                    <div class="card-item-left" :style="{ backgroundColor: item.colorLeft }">
                        <img class="icon-image" :src="item.imgUrl">
                    </div>
                    <div class="card-item-right" :style="{ backgroundColor: item.colorRight }">
                        <div class="card-item-right-top"></div>
                        <div class="card-item-right-middle">
                            {{item.text}}
                            <br>
                            <span>{{item.count}}</span>
                        </div>
                        <div class="card-item-right-bottom"></div>
                    </div>
                </div>
            </div>
        </div>

        <div class="box-bottom">
            <div class="s-pd-20 s-bgc-wt box-bottom-left">
                <div>巡检统计</div>
                <div id="chart"></div>
            </div>
            <div class="box-bottom-middle"></div>
            <div class="s-pd-20 s-bgc-wt box-bottom-right">
                <div style="display: flex; padding-bottom: 10px">
                    <span style="flex: 1">巡检动态</span>
                    <span class="span-more" @click="openCheckReportList">更多</span>
                </div>
                <div style="flex: 1; padding: 10px 5px">
                    <bk-timeline class="status-time"
                             :list="checkActivity"
                             style="margin-top: 20px; padding-top: 10px;"
                             @select="openCheckReportDetail"></bk-timeline>
                </div>

            </div>
        </div>
    </bk-container>

</template>

<script>

    import bizIcon from '@/images/biz.png'
    import countIcon from '@/images/count.png'
    import serverIcon from '@/images/server.png'
    import dangerIcon from '@/images/danger.png'
    import Moment from 'moment'

    export default {
        components: {},
        data () {
            return {
                bizIcon: bizIcon,
                countIcon: countIcon,
                serverIcon: serverIcon,
                dangerIcon: dangerIcon,
                // 初始化时间选择器的值
                dateRange: [new Date(), new Date()],
                checkStatistics: [
                    {
                        text: '巡检业务数',
                        imgUrl: bizIcon,
                        colorLeft: '#5AD8A6',
                        colorRight: '#C2F0DE',
                        count: 0
                    },
                    {
                        text: '巡检主机数',
                        imgUrl: serverIcon,
                        colorLeft: '#58B9E3',
                        colorRight: '#BFE4F4',
                        count: 0
                    },
                    {
                        text: '巡检总次数',
                        imgUrl: countIcon,
                        colorLeft: '#F6BD16',
                        colorRight: '#FBE6AA',
                        count: 0
                    },
                    {
                        text: '巡检异常主机数',
                        imgUrl: dangerIcon,
                        colorLeft: '#EC4646',
                        colorRight: '#F8BCBC',
                        count: 0
                    }
                ],
                chart: null,
                checkActivity: [],
                activeDateTagIndex: 1,
                dateTagList: [
                    '今日',
                    '近7天',
                    '近30天'
                ],
                datePickerOptions: {
                    disabledDate (val) {
                        if (Moment(val).isAfter(new Date())) {
                            return true
                        } else {
                            return false
                        }
                    }
                },
                chartData: {
                    dateList: [],
                    bizCount: [],
                    totalHostCount: [],
                    executeCount: [],
                    errorHostCount: []
                },
                echartsOpts: {
                    // 设备像素比，默认取浏览器的值window.devicePixelRatio
                    devicePixelRatio: window.devicePixelRatio,
                    // 渲染器，支持 'canvas' 或者 'svg'
                    renderer: 'canvas',
                    // 可显式指定实例宽度，单位为像素。如果传入值为 null/undefined/'auto'，则表示自动取 dom（实例容器）的宽度
                    width: 'auto',
                    // 可显式指定实例高度，单位为像素。如果传入值为 null/undefined/'auto'，则表示自动取 dom（实例容器）的高度
                    height: 'auto',
                    // 使用的语言，内置 'ZH' 和 'EN' 两个语言
                    locale: 'ZH'
                },
                options: {
                    // 提示框
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'cross'
                        }
                    },
                    legend: {
                        data: ['巡检业务数', '巡检主机数', '巡检总次数', '异常主机数']
                    },
                    // 设置canvas内部表格的内距
                    grid: {
                        left: '3%',
                        right: '5%',
                        top: '10%',
                        bottom: '10%',
                        containLabel: true
                    },
                    toolbox: {
                        feature: {
                            // dataView: {
                            //     show: true, readOnly: false
                            // },
                            restore: {
                                show: true
                            }
                            // saveAsImage: {
                            //     show: true
                            // }
                        },
                        right: '50px'
                    }
                }
            }
        },
        computed: {},
        watch: {
            dateRange: function (newVal, oldVal) {
                if (newVal[0] && newVal[1]) {
                    this.fetCheckStatisticsByDateRange()
                }
            }
        },
        created () {
            const startDate = new Date()
            const endDate = new Date()
            startDate.setTime(startDate.getTime() - 3600 * 1000 * 24 * 6)
            this.dateRange = [startDate, endDate]
        },
        mounted () {
            window.onresize = () => {
                this.chart.resize()
            }
            this.fetchCheckActivity()
            // this.fetCheckStatisticsByDateRange()
        },
        methods: {
            async fetCheckStatisticsByDateRange () {
                const self = this
                if (self.chart != null && self.chart !== '' && self.chart !== undefined) {
                    self.chart.dispose()
                }
                self.chart = self.$echarts.init(document.getElementById('chart'), 'light', this.echartsOpts)
                self.chart.showLoading()
                const [startDate, endDate] = self.dateRange
                try {
                    const res = await this.$store.dispatch('fetch_check_statistics', {
                        'start_time': Moment(startDate).format('YYYY-MM-DD 00:00:01'),
                        'end_time': Moment(endDate).format('YYYY-MM-DD 23:59:59')
                    })
                    const { data } = res
                    self.checkStatistics[0].count = data.statistics.biz_count
                    self.checkStatistics[1].count = data.statistics.total_host_count
                    self.checkStatistics[2].count = data.statistics.execute_count
                    self.checkStatistics[3].count = data.statistics.error_host_count
                    const options = {
                        tooltip: self.options.tooltip,
                        legend: self.options.legend,
                        grid: self.options.grid,
                        toolbox: self.options.toolbox,
                        xAxis: {
                            type: 'category',
                            name: '日期',
                            axisTick: {
                                alignWithLabel: true
                            },
                            data: data.reports.date_list
                        },
                        yAxis: {
                            type: 'value',
                            name: '数量',
                            position: 'left',
                            axisLine: {
                                show: true
                            },
                            axisLabel: {
                                formatter: '{value}'
                            }
                        },
                        series: [
                            {
                                name: '巡检业务数',
                                type: 'line',
                                data: data.reports.count_data.biz_count,
                                itemStyle: {
                                    // 折线点的颜色
                                    color: self.checkStatistics[0].colorLeft,
                                    lineStyle: {
                                        // 折线颜色
                                        color: self.checkStatistics[0].colorRight
                                    }
                                }
                            },
                            {
                                name: '巡检主机数',
                                type: 'line',
                                data: data.reports.count_data.total_host_count,
                                itemStyle: {
                                    // 折线点的颜色
                                    color: self.checkStatistics[1].colorLeft,
                                    lineStyle: {
                                        // 折线颜色
                                        color: self.checkStatistics[1].colorRight
                                    }
                                }
                            },
                            {
                                name: '巡检总次数',
                                type: 'line',
                                data: data.reports.count_data.execute_count,
                                itemStyle: {
                                    // 折线点的颜色
                                    color: self.checkStatistics[2].colorLeft,
                                    lineStyle: {
                                        // 折线颜色
                                        color: self.checkStatistics[2].colorRight
                                    }
                                }
                            },
                            {
                                name: '异常主机数',
                                type: 'line',
                                data: data.reports.count_data.total_host_count,
                                itemStyle: {
                                    // 折线点的颜色
                                    color: self.checkStatistics[3].colorLeft,
                                    lineStyle: {
                                        // 折线颜色
                                        color: self.checkStatistics[3].colorRight
                                    }
                                }
                            }
                        ]
                    }
                    self.chart.hideLoading()
                    self.chart.setOption(options)
                    self.chart.resize()
                } catch (e) {
                    console.error(e)
                }
            },
            async fetchCheckActivity () {
                // const self = this
                try {
                    const res = await this.$store.dispatch('fetch_check_activity')
                    const { data } = res
                    this.checkActivity = data
                } catch (e) {
                    console.error(e)
                }
            },
            changeDateRange (e) {
                let startDate = new Date()
                const endDate = new Date()
                const dateTag = e.target.innerHTML
                const dateIndex = e.target.dataset.val
                this.activeDateTagIndex = parseInt(dateIndex)
                if (dateTag === '今日') {
                    startDate = new Date()
                } else if (dateTag === '近7天') {
                    startDate.setTime(startDate.getTime() - 3600 * 1000 * 24 * 6)
                } else {
                    startDate.setTime(startDate.getTime() - 3600 * 1000 * 24 * 29)
                }
                this.dateRange = [startDate, endDate]
            },
            dateRangeChange (dateRange, type) {
                const [startDate, endDate] = dateRange
                if (Moment(startDate).isAfter(new Date())) {
                    this.dateRange = [...this.dateRange]
                    return this.$bkMessage({ delay: 3000, message: '开始时间必须早于当前时间', theme: 'error' })
                }
                if (Moment(endDate).isAfter(new Date())) {
                    this.dateRange = [...this.dateRange]
                    return this.$bkMessage({ delay: 3000, message: '结束时间必须早于当前时间', theme: 'error' })
                }
                this.dateRange = dateRange
            },
            openCheckReportList () {
                this.$router.push({
                    name: 'historyReport'
                })
            },
            openCheckReportDetail (reportData) {
                const { id } = reportData
                this.$router.push({
                    name: 'checkReport',
                    query: {
                        id
                    }
                })
            }
        }
    }
</script>

<style scoped>
    .card-box {
        display: flex;
        flex-direction: row;
        flex: 1;
        box-shadow: 10px 10px 6px #c3cdd7;
        height: 150px;
        line-height: 150px;
        text-align: center;
        margin-right: 20px;
    }

    .card-item-left {
        flex: 1;
        font-size: 30px;
        color: white
    }

    .card-item-right {
        flex: 2;
        color: white;
        display: flex;
        flex-direction: column;
    }

    .card-item-right-top {
        flex: 1;
    }

    .card-item-right-middle {
        height: 70px;
        line-height: 35px;
        color: #7F7F7F;
        font-weight: bold;

    }
    .card-item-right-middle span {
        font-size: 30px;
        font-weight: bold;
        color: #333333;
    }
    .card-item-right-bottom {
        flex: 1;
    }

    .s-bgc-wt {
        background-color: white;
    }

    .s-pd-20 {
        padding: 20px;
    }

    .last:last-child {
        margin-right: 0 !important;
    }

    .icon-image {
        height: 50px;
        width: 50px;
        margin-top: 50px;
    }

    .date-tag {
        font-size: 14px;
        color: #5A5A5A;
        margin-right: 20px;

    }

    .date-tag .acitve {
        color: #339DFF;
    }

    .date-tag:hover {
        cursor: pointer;
        color: #339DFF;
    }

    .box-bottom {
        display: flex;
        margin-top: 20px;
        margin-bottom: 20px;
        height: calc(100vh - 59px - 52px - 32px - 2px - 264px - 20px - 20px - 20px - 5px);
    }
    #chart {
        height: calc(100vh - 59px - 52px - 32px - 2px - 264px - 20px - 20px - 20px - 5px - 20px);
    }

    .box-bottom > div {
        height: 100%;
    }

    .box-bottom-left {
        flex: 3;
    }

    .box-bottom-right {
        flex: 1;
        display: flex;
        flex-direction: column;
    }
    .box-bottom-right>div:nth-child(2) {
        overflow-y: auto;
    }

    .box-bottom-middle {
        width: 20px;
    }

    .span-more {
        width: 45px;
        text-align: center;
        border: 1px solid #7F7F7F;
        border-radius: 5px;
        color: #7F7F7F;
        font-size: 14px;
    }

    .span-more:hover {
        cursor: pointer;
        color: #339DFF;
        text-decoration-line: underline;
    }
    /deep/.bk-timeline .bk-timeline-title {
         font-size: 13px;
    }
    /deep/.bk-timeline .bk-timeline-title:hover {
         color: #339DFF;
         cursor: pointer;
         text-decoration-line: underline;
    }
    /deep/.bk-timeline .bk-timeline-content {
        color: #B3B3B3;
        font-size: 12px;
        padding-bottom: 0;
        margin-bottom: 0;
    }
    /deep/.bk-timeline li {
        padding-bottom: 15px;
        margin-bottom: 0;
    }
</style>
