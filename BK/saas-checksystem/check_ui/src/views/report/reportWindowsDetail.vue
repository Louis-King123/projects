<template>
    <div class="mt10" v-bkloading="{ isLoading: basicLoading, zIndex: 10 }">
        <div class="wrapper mt20">
            <!-- 报告头 -->
            <div class="ipContainer">
                <bk-container :col="12">
                    <bk-row>
                        <!-- 标识 -->
                        <bk-col :span="2">
                            <div class="titleIconContainer">
                              <i class="el-icon-s-platform" style="font-size: 100px;"></i>
                              <div>Windows</div>
                            </div>
                        </bk-col>
                        <!-- /标识 -->

                        <!-- 时间 -->
                        <bk-col :span="7">
                            <h2>{{ basicInfo.host }}</h2>
                            <div class="greyFont">创建时间：{{ basicInfo['create_time'] }}</div>
                            <div class="mt10 greyFont">完成时间：{{ basicInfo.end_time }}</div>
                        </bk-col>
                        <!-- /时间 -->

                        <!-- 返回按钮 -->
                        <bk-col :span="3">
                          <div class="mt20 backBtnContainer">
                            <bk-button
                              :hover-theme="'primary'"
                              @click="jumpReportHistory"
                              style="border-radius: 20px;">
                              返回
                            </bk-button>
                          </div>
                        </bk-col>
                        <!-- /返回按钮 -->
                    </bk-row>
                </bk-container>
            </div>
            <!-- /报告头 -->

            <!-- 巡检概览 -->
            <div class="overviewContainer">
              <!-- 标题 -->
              <h4 class="overviewTitle">巡检概览</h4>
              <!-- /标题 -->

              <bk-container :col="12">
                <bk-row>
                    <bk-col :span="4">
                        <div class="content">
                            <div class="round" align="center">
                                <bk-round-progress
                                  :width="width"
                                  :percent="(overviewInfo['quota_error_percent'] || 0) / 100"
                                  :config="config"
                                  :content="`异常指标数${(overviewInfo['quota_error_percent'] || 0)}%`">
                                </bk-round-progress>
                            </div>
                        </div>
                    </bk-col>

                    <bk-col :span="8">
                        <div class="textInfoContainer">
                          {{ '总体健康情况' + handleSetHealthTextShow(overviewInfo['quota_error_percent']) + '，共巡检' }}
                          <h3>{{ overviewInfo['quota_total_num'] + '个' }}</h3>
                          <span>指标，异常指标数</span>
                          <h3>{{ overviewInfo['quota_error_num'] + '个' }}</h3>
                          <span>，占比</span>
                          <h3>{{ overviewInfo['quota_error_percent'] + '%' }}</h3>
                        </div>

                        <div
                          class="circleCss"
                          v-for="(v, k) in overviewInfo['quota_error_class_top4']"
                          :key="v['quota_class_id']">

                            <!-- 标记 -->
                            <bk-badge
                              class="mr5"
                              :val="k + 1"
                              :theme="'#000000'"
                              radius="50"
                              position="right">
                            </bk-badge>
                            <!-- /标记 -->

                            <!-- 名称 -->
                            <div class="blackFont w200">
                              {{ v['quota_class_name'] }}
                            </div>
                            <!-- /名称 -->

                            <!-- 数量 -->
                            <div class="blackFont w80">
                              {{ v['quota_error_num'] }}
                            </div>
                            <!-- /数量 -->

                            <!-- 详情按钮 -->
                            <bk-link
                              underline
                              theme="default"
                              @click="handleScroll(v['quota_class_id'])"
                              target="_blank">
                              <em>详情</em>
                            </bk-link>
                            <!-- /详情按钮 -->
                        </div>
                    </bk-col>
                </bk-row>
              </bk-container>
            </div>
            <!-- /巡检概览 -->

            <!-- collapse展示部分 -->
            <bk-collapse v-model="activeName">
                <div
                  class="infoItem"
                  v-for="v in quotaClassDetails"
                  :key="v['quota_class_id']"
                  :id="`quotaClassDetail${v['quota_class_id']}`">
                    <bk-collapse-item :name="v['quota_class_name']">
                        <h3 class="m0">{{ v['quota_class_name'] }}</h3>

                        <div style="margin: -14.6px -10px 0 -10px;" v-show="v['quota_details'].length !== 0">
                          <bk-divider></bk-divider>
                        </div>

                        <div slot="content" class="pb10" align="center">
                            <div class="cardContainer" v-if="v['quota_class_id'] === 12">
                              <div
                                class="cardItem inlineBlock"
                                v-for="(item, index) in v['quota_details']"
                                :key="index"
                                v-show="item['FreeSpace'] !== null && item['Size'] !== null"
                                align="center">
                                <div class="cardItemTitle">
                                  {{ item['DeviceID'] + ':盘剩余空间比' }}
                                </div>

                                <div class="cardItemContent">
                                  <div class="cardItemContentPercentage mt10">
                                    {{ item['FreeSpacePercent'] + '%' }}
                                  </div>

                                  <div class="mt10 mb10">
                                    <bk-progress
                                      :text-inside="true"
                                      :stroke-width='18'
                                      :percent="item['FreeSpacePercent'] / 100 ">
                                    </bk-progress>
                                  </div>
                                </div>

                                <div class="cardItemInfo">
                                  <div>{{ '总大小：' + item['Size'] + 'GB' }}</div>

                                  <div>{{ '剩余空间：' + item['FreeSpace'] + 'GB' }}</div>
                                </div>
                              </div>
                            </div>

                            <div v-else>
                              <bk-table
                                style="margin-top: 10px; max-height: 296px; overflow-y: auto"
                                :data="v['quota_details']"
                                :size="size">

                                <bk-table-column
                                  v-for="(item, index) in tableData[v['quota_class_id']]"
                                  :key="index"
                                  :label="handleSwitchTableLabel(item)"
                                  :prop="item">
                                </bk-table-column>
                              </bk-table>
                            </div>
                        </div>
                    </bk-collapse-item>
                </div>
            </bk-collapse>
            <!-- /collapse展示部分 -->

        </div>
    </div>
</template>

<script>
    export default {
        name: 'reportWindowsDetail',
        data () {
            return {
                basicLoading: false,
                size: 'small',
                width: '200px',
                config: {
                    strokeWidth: 12,
                    bgColor: '#f0f1f5',
                    activeColor: '#ea3636'
                },

                basicInfo: {},
                overviewInfo: {},
                quotaClassDetails: [],
                activeName: [],
                tableData: {}
            }
        },

        created () {
            this.fetchWindowsDetail()
        },

        methods: {
            async fetchWindowsDetail () {
                try {
                    this.basicLoading = true
                    const { os, execute_id, host } = this.$route.query
                    const params = {
                        os,
                        execute_id,
                        host
                    }
                    const res = await this.$store.dispatch('fetch_inspection_report_detail', params)
                    const { data, code } = res
                    if (code !== 0) return
                    this.basicInfo = data['basic_info']
                    this.overviewInfo = data['overview_info']
                    this.quotaClassDetails = data['quota_class_details']

                    data['quota_class_details'].forEach(item => {
                        // 设置折叠面板默认展示
                        this.activeName.push(item['quota_class_name'])

                        // 处理表格展示字段
                        this.tableData[item['quota_class_id']] = []
                        if (item['quota_details'].length !== 0) {
                            const { keys } = Object
                            keys(item['quota_details'][0]).forEach(k => {
                                if (k !== 'result_status') {
                                    this.tableData[item['quota_class_id']].push(k)
                                }
                            })
                        }
                    })
                } catch (e) {

                } finally {
                    this.basicLoading = false
                }
            },

            jumpReportHistory () {
                this.$router.push({
                    name: 'historyReport'
                })
            },

            // 巡检概览查看详情
            handleScroll (param) {
                const scrollConfig = {
                    behavior: 'smooth'

                }
                document.getElementById(`quotaClassDetail${param}`).scrollIntoView(scrollConfig)
            },

            // 设置表格label展示
            handleSwitchTableLabel (param) {
                const obj = {
                    // 系统异常服务展示
                    Caption: () => '服务名称',
                    StartMode: () => '启动模式',
                    State: () => '运行状态',
                    Status: () => '健康状态',

                    // 近七天错误日志展示
                    EventID: () => '事件ID',
                    Source: () => '来源',
                    EntryType: () => '类型',
                    Count: () => '出现次数',
                    TimeGenerated: () => '最近一次出现时间',

                    // 常规字段展示
                    quota_name: () => '检查项目',
                    check_result: () => '检查结果',
                    recommend_value: () => '推荐值',
                    result_status: () => {}
                }

                return obj[param]()
            },

            // 设置健康状态文案展示
            handleSetHealthTextShow (param) {
                if (param <= 20) return '优秀'
                if (param > 20 && param < 40) return '良好'
                if (param >= 40) return '较差'
            }
        }
    }
</script>

<style lang="postcss" scoped>
    .redFont {
      color: #ff0000;
    }
    .blackFont {
      color: #000000;
      font-size: 14px;
      font-weight: 600;
    }
    .orangeFont {
      color: #ff9c01;
    }
    .greenFont {
      color: #2dcb56;
    }
    .grayFont {
      color: #c4c6cc;
    }
    .w200 {
      width: 200px;
    }
    .w80 {
      width: 80px;
    }
    .ipContainer {
      border:1px solid rgb(228 221 228);
      height: 150px;
      background-color: white;

      .titleIconContainer {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }

      .backBtnContainer {
        display: flex;
        padding-right: 20px;
        justify-content: flex-end;
      }
    }

    .overviewContainer {
      width: 98%;
      border:1px solid rgb(228 221 228);
      border-radius: 5px;
      background-color: white;
      margin: 20px 0 0 1%;

      .overviewTitle {
        margin: 0;
        padding: 15px;
        border-bottom: 1px solid #ccc;
      }

      .textInfoContainer {
        height: 30px;
        font-size: 18px;
        display: flex;
        align-items: flex-end;

        h3 {
          margin: 0;
        }
      }
    }

    .infoItem {
      width: 98%;
      margin: 20px 0 0 1%;
      border:1px solid rgb(228 221 228);
      border-radius: 6px;
      background-color: #ffffff;

      .cardContainer {
        .cardItem {
          width: 24.25%;
          height: 170px;
          border:1px solid rgb(228 221 228);
          border-radius: 4px;
          margin: 10px 0 0 1%;

          .cardItemTitle {
            height: 35px;
            background-color: #d9d9d9;
            color: grey;
            font-size: 16px;
            text-align:center;
            line-height: 35px;
          }

          .cardItemContent {
            width: 80%;
            border-bottom: 1px solid #ccc;

            .cardItemContentPercentage {
              height: 35px;
              color: #0f0f0f;
              text-align:left;
              line-height: 35px;
              font-size: 30px;
            }
          }

          .cardItemInfo {
            width: 100%;
            height: calc(100% - 118px);
            display: flex;
            align-items: center;
            justify-content: space-around;
            font-size: 12px;
          }
        }

        .inlineBlock:nth-of-type(4n + 1) {
          margin: 10px 0 0 0;
        }
      }
    }

    .circleCss {
        margin-top: 15px;
        display: flex;
        align-items: center;
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
