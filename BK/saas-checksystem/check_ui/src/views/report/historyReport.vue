<template>
    <!-- 容器 -->
    <div class="reportHistoryContainer">
        <!-- 表单 -->
        <div class="formContainer">
            <bk-form form-type="inline">
                <bk-form-item label="选择业务">
                    <bk-select placeholder="选择业务" v-model="formData.exec_biz_id" style="width: 190px">
                        <!--<bk-option v-for="option in biz"
                            :key="option.id"
                            :id="option.id"
                            :name="option.name">
                        </bk-option>-->
                        <bk-option
                          v-for="option in bizList"
                          :key="option['bk_biz_id']"
                          :id="option['bk_biz_id']"
                          :name="option['bk_biz_name']">
                        </bk-option>
                    </bk-select>
                </bk-form-item>

                <bk-form-item label="巡检对象">
                    <bk-select placeholder="巡检对象" v-model="formData.task_os" style="width: 190px" @change="handleChangeOs">
                        <bk-option v-for="option in $store.getters.getOsList"
                            :key="option.id"
                            :id="option.id"
                            :name="option.os_name">
                        </bk-option>
                    </bk-select>
                </bk-form-item>

                <bk-form-item label="巡检模板">
                    <bk-select placeholder="巡检模板" v-model="formData.task_tpl" style="width: 190px">
                        <!--<bk-option v-for="option in tpls"
                            :key="option.id"
                            :id="option.id"
                            :name="option.tpl_name">
                        </bk-option>-->
                        <bk-option
                          class="custom-option"
                          v-for="option in tplList"
                          :key="option.id"
                          :id="option.id"
                          :name="option.tpl_name">
                        </bk-option>
                    </bk-select>
                </bk-form-item>

                <bk-form-item label="日期范围">
                    <bk-date-picker
                      style="width: 190px;"
                      @change="ChangeTime"
                      :placeholder="'选择日期范围'"
                      :type="'daterange'">
                    </bk-date-picker>
                </bk-form-item>

                <bk-form-item>
                  <bk-button :theme="'primary'" :title="'搜索'" @click="searchReportSet">搜索</bk-button>
                </bk-form-item>

            </bk-form>
        </div>
        <!-- /表单 -->

        <!-- 表格 -->
        <div class="tableContainer">
            <bk-table style="margin-top: 30px;" fit
                :data="data"
                :pagination="pagination"
                v-bkloading="{ isLoading: basicLoading, zIndex: 10 }"
                @page-change="handlePageChange"
                @page-limit-change="handlePageLimitChange">
                <bk-table-column label="报告ID" prop="execute_log_id" align="center" header-align="center"></bk-table-column>
                <bk-table-column label="业务" prop="bk_biz_name" align="center" header-align="center"></bk-table-column>
                <bk-table-column label="任务名" prop="task_name" align="center" header-align="center"></bk-table-column>
                <bk-table-column label="巡检对象" prop="task_os" align="center" header-align="center"></bk-table-column>
                <bk-table-column label="模版" prop="tpl_name" align="center" sortable header-align="center"></bk-table-column>
                <bk-table-column label="执行时间" prop="start_time" align="center" sortable header-align="center"></bk-table-column>
                <bk-table-column label="完成时间" prop="end_time" align="center" sortable header-align="center"></bk-table-column>
                <bk-table-column label="操作" align="center"  header-align="center">
                    <template slot-scope="scope">
                        <bk-button theme="primary" size="small" @click="reportCheckPage(scope.row.execute_log_id)">
                            查看报告详情
                        </bk-button>
                    </template>
                </bk-table-column>
            </bk-table>
        </div>
        <!-- /表格 -->

        <bk-button theme="primary" id="errorButton" @click="errorInfo" style="display: none"></bk-button>
    </div>
    <!-- /容器 -->
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
                basicLoading: false,
                formData: {
                    'task_tpl': '',
                    'task_os': '',
                    'exec_biz_id': '',
                    'start_time': '',
                    'end_time': ''
                },
                searchFlag: true,
                statusList: [
                    { 'id': 0, name: '未执行' },
                    { 'id': 1, name: '执行中' },
                    { 'id': 2, name: '执行完成' },
                    { 'id': 3, name: '执行错误' }
                ],
                data: [],
                biz: [],
                oss: [],
                tpls: [],
                pagination: {
                    current: 1,
                    count: 0,
                    limit: 10,
                    limitList: [5, 10, 20]
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

                bizList: [],
                tplList: []
            }
        },

        created () {
            this.business_list()
        },
        mounted () {
            this.getHistoryList()
        },

        methods: {
            // 获取业务列表数据
            async business_list () {
                try {
                    const res = await this.$store.dispatch('get_init_data', 'business_list')
                    const { data } = res
                    this.bizList = data
                } catch (e) {
                    console.log('business_list', e)
                }
            },
            // 切换巡检对象函数
            handleChangeOs (value) {
                this.formData.task_os = value

                if (!value) {
                    this.tplList = []
                    this.formData.task_tpl = null
                    return
                }

                this.fetch_tpl_list(value)
            },
            // 获取巡检模板数据
            async fetch_tpl_list () {
                try {
                    const { task_os } = this.formData
                    const params = {
                        os_id: task_os
                    }

                    const res = await this.$store.dispatch('fetch_tpl_list', params)
                    const { data } = res
                    this.tplList = data
                } catch (e) {
                    console.log('fetch_tpl_list', e)
                }
            },
            async getHistoryList (param = {}) {
                const { current, limit } = this.pagination
                const params = {
                    ...param,
                    current,
                    limit
                }
                try {
                    this.basicLoading = true
                    const res = await this.$store.dispatch('fetch_history_list', params)
                    if (res.code) {
                        this.error.msg = res.msg
                        document.getElementById('errorButton').click()
                        return
                    }
                    const { data } = res
                    this.data = data.data
                    this.pagination.count = data.count
                } catch (e) {
                    console.log('fetch_history_list=', e)
                } finally {
                    this.basicLoading = false
                }
            },
            handlePageChange (current) {
                this.pagination.current = current
                this.getHistoryList(this.formData)
            //    调用接口
            },
            handlePageLimitChange (limit) {
                this.pagination.current = 1
                this.pagination.limit = limit
                this.getHistoryList(this.formData)
            //    调用接口
            },

            reportCheckPage (id) {
                this.$router.push({
                    name: 'checkReport',
                    query: {
                        id
                    }
                })
            },
            searchReportSet () {
                this.pagination.current = 1
                this.pagination.limit = this.pagination.limit
                this.getHistoryList(this.formData)
            },
            // // 搜索
            // searchReport () {
            //     const self = this
            //     self.basicLoading = true
            //     const infos = this.$store.dispatch('fetch_history_list', self)
            //     infos.then(function (result) {
            //         self.data = result.data.data
            //         self.basicLoading = false
            //         self.pagination.count = result.data.count
            //     })
            // },
            errorInfo () {
                this.$bkInfo({
                    type: 'error',
                    title: this.error.title,
                    subTitle: this.error.msg,
                    showFooter: false,
                    maskClose: true
                })
            },
            ChangeTime (date, type) {
                this.formData.start_time = date[0]
                this.formData.end_time = date[1]
            }
        }
    }
</script>

<style lang="postcss" scoped>
    .inlineBlock {
        display: inline-block;
    }

    .reportHistoryContainer {
      padding: 20px;

      .formContainer {
        padding: 20px;
        background: #ffffff;
        margin-bottom: 20px;

        .bk-form-item {
          margin: 0 8px 8px 0 !important;
        }

        /deep/.bk-form.bk-inline-form .bk-form-item .bk-label {
          width: 80px !important;
        }
      }

      .tableContainer {
        padding: 20px;
        background: #ffffff;
      }
    }
</style>
