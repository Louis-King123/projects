<template>
    <div class="operateLogContainer">
        <div class="operateLogFormContent">
            <bk-form form-type="inline">
                <bk-form-item label="操作人">
                    <bk-select
                            style="width: 190px; height: 30px;"
                            searchable
                            multiple
                            display-tag
                            v-model="searchForm.operator">
                        <bk-option
                                v-for="user in userList"
                                :key="user.id"
                                :id="user.username"
                                :name="user.username">
                        </bk-option>
                    </bk-select>
                </bk-form-item>

                <bk-form-item label="选择日期">
                    <bk-date-picker
                            style="width: 190px;"
                            type="daterange"
                            :placeholder="'选择日期'"
                            v-model="searchForm['date_range']"
                    >
                    </bk-date-picker>
                </bk-form-item>

                <bk-form-item label="操作模块">
                    <bk-select style="width: 190px;" v-model="searchForm['operation_module']">
                        <bk-option
                                v-for="module in moduleList"
                                :key="module.id"
                                :id="module.id"
                                :name="module.name">
                        </bk-option>
                    </bk-select>
                </bk-form-item>

                <bk-form-item label="操作类型">
                    <bk-select style="width: 190px;" v-model="searchForm['request_method']">
                        <bk-option
                                v-for="type in typeList"
                                :key="type.id"
                                :id="type.id"
                                :name="type.name">
                        </bk-option>
                    </bk-select>
                </bk-form-item>

                <bk-form-item>
                    <bk-button
                            ext-cls="mr5"
                            theme="primary"
                            @click="handleSearch">
                        查询
                    </bk-button>
                    <bk-button theme="default" @click="handleClear">重置</bk-button>
                </bk-form-item>
            </bk-form>
        </div>

        <div class="operateLogTableContent">
            <div class="mt30">
                <bk-table
                        :data="logList"
                        :size="size"
                        :pagination="pagination"
                        v-bkloading="{ isLoading: isLoading, zIndex: 10 }"
                        @page-change="handlePageChange"
                        @page-limit-change="handlePageLimitChange"
                        @row-click="handleRowClick">
                    <bk-table-column label="操作人" :show-overflow-tooltip="true" prop="username"></bk-table-column>
                    <bk-table-column label="操作时间" :show-overflow-tooltip="true" prop="request_time"></bk-table-column>
                    <bk-table-column label="操作模块" :show-overflow-tooltip="true"
                                     prop="operation_module"></bk-table-column>
                    <bk-table-column label="操作类型" :show-overflow-tooltip="true">
                        <template slot-scope="scope">
                            <span>{{ setRequestMethod(scope.row['request_method']) }}</span>
                        </template>
                    </bk-table-column>
                    <bk-table-column label="操作描述" :show-overflow-tooltip="true"
                                     prop="operation_description"></bk-table-column>
                </bk-table>
            </div>
        </div>

        <div>
            <bk-sideslider
                    :is-show.sync="isShow"
                    :quick-close="true"
                    title="操作详情"
                    width="700">
                <div slot="content" class="dialogContent">
                    <bk-table :data="detailData" :size="size">
                        <bk-table-column label="属性" prop="verbose_name"></bk-table-column>
                        <bk-table-column label="变更前" :show-overflow-tooltip="true" v-if="logType === 'PUT'">
                          <template slot-scope="scope">
                            <span v-if="scope.row['verbose_name'] !== '巡检指标'">
                              {{ scope.row.before }}
                            </span>
                            <span v-else>{{ JSON.stringify(scope.row.before) }}</span>
                          </template>
                        </bk-table-column>
                        <bk-table-column label="变更后" :show-overflow-tooltip="true" v-if="logType === 'PUT'">
                          <template slot-scope="scope">
                            <span v-if="scope.row['verbose_name'] !== '巡检指标'">
                              {{ scope.row.after }}
                            </span>
                            <span v-else>{{ JSON.stringify(scope.row.after) }}</span>
                          </template>
                        </bk-table-column>

                        <bk-table-column label="值" :show-overflow-tooltip="true" v-if="logType === 'POST'">
                          <template slot-scope="scope">
                              <span v-if="scope.row['verbose_name'] !== '巡检指标'">
                                {{ scope.row.after }}
                              </span>
                            <span v-else>{{ JSON.stringify(scope.row.after) }}</span>
                          </template>
                        </bk-table-column>

                        <bk-table-column label="值" :show-overflow-tooltip="true" v-if="logType === 'DELETE' || logType === 'EXECUTE'">
                          <template slot-scope="scope">
                                <span v-if="scope.row['verbose_name'] !== '巡检指标'">
                                  {{ scope.row.before }}
                                </span>
                            <span v-else>{{ JSON.stringify(scope.row.before) }}</span>
                          </template>
                        </bk-table-column>
                    </bk-table>
                </div>
            </bk-sideslider>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'operateLog',
        data () {
            return {
                searchForm: {
                    operator: [],
                    date_range: [],
                    operation_module: '全部',
                    request_method: 'all'
                },
                userList: [],
                moduleList: [
                    {
                        name: '全部',
                        id: '全部'
                    },
                    {
                        name: '模板管理',
                        id: '模板管理'
                    },
                    {
                        name: '自定义巡检',
                        id: '自定义巡检'
                    },
                    {
                        name: '任务管理',
                        id: '任务管理'
                    }
                ],
                typeList: [
                    {
                        name: '全部',
                        id: 'all'
                    },
                    {
                        name: '新增',
                        id: 'POST'
                    },
                    {
                        name: '编辑',
                        id: 'PUT'
                    },
                    {
                        name: '删除',
                        id: 'DELETE'
                    },
                    {
                        name: '执行',
                        id: 'EXECUTE'
                    }
                ],
                pagination: {
                    current: 1,
                    count: 0,
                    limit: 10,
                    limitList: [5, 10, 20]
                },
                size: 'small',
                isLoading: false,
                logList: [],
                isShow: false,
                detailData: [],
                logType: ''
            }
        },
        watch: {},
        async created () {
            this.fetch_bk_users()

            this.handleSearch()
        },
        methods: {
            async fetch_bk_users () {
                try {
                    const res = await this.$store.dispatch('fetch_bk_users')
                    const { data } = res
                    this.userList = data
                } catch (e) {
                    console.log('fetch_bk_users', e)
                }
            },

            // 设置操作类型展示
            setRequestMethod (type = 'POST') {
                const methodObj = {
                    POST: () => {
                        return '新增'
                    },
                    PUT: () => {
                        return '编辑'
                    },
                    DELETE: () => {
                        return '删除'
                    },
                    EXECUTE: () => {
                        return '执行'
                    }
                }

                return methodObj[type]()
            },

            handleRowClick (row) {
                this.logType = row['request_method']
                this.detailData = row['change_detail']
                this.setIsShow()
            },
            handlePageChange (current) {
                this.pagination.current = current
                this.handleSearch()
            },
            handlePageLimitChange (limit) {
                this.pagination.current = 1
                this.pagination.limit = limit
                this.handleSearch()
            },

            // 重置表单
            handleClear () {
                const { keys } = Object

                keys(this.searchForm).forEach(k => {
                    this.searchForm[k] = []

                    if (k === 'operation_module') this.searchForm[k] = '全部'

                    if (k === 'request_method') this.searchForm[k] = 'all'
                })
            },
            // 查询
            handleSearch () {
                const { searchForm } = this
                const { current, limit } = this.pagination
                const copyFormData = JSON.parse(JSON.stringify(searchForm))

                // 判断key对应的值是否存在，没有则删除key，操作模块操作类型选择全部情况删除key
                const { keys } = Object
                keys(copyFormData).forEach(k => {
                    if (k === 'operator' && !copyFormData['operator'][0]) delete copyFormData[k]

                    if (k === 'date_range' && !copyFormData['date_range'][0]) delete copyFormData[k]

                    if (k === 'operation_module' && copyFormData['operation_module'] === '全部') delete copyFormData[k]

                    if (k === 'request_method' && copyFormData['request_method'] === 'all') delete copyFormData[k]
                })

                // 组装 start_time end_time参数
                if (copyFormData['date_range']) {
                    const [startTime, endTime] = copyFormData['date_range']
                    copyFormData['start_time'] = this.$moment(startTime).format('YYYY-MM-DD')
                    copyFormData['end_time'] = this.$moment(endTime).format('YYYY-MM-DD')

                    delete copyFormData['date_range']
                }

                // 组装分页参数
                copyFormData.current = current
                copyFormData.limit = limit

                this.fetch_operation_log(copyFormData)
            },
            // 查询操作日志列表
            async fetch_operation_log (param = {}) {
                const params = { ...param }

                try {
                    this.isLoading = true
                    const res = await this.$store.dispatch('fetch_operation_log', params)
                    const { code } = res
                    if (code !== 0) return

                    const { data } = res
                    this.logList = data.data
                    this.pagination.count = data.count
                } catch (e) {
                    console.log('fetch_operation_log=', e)
                } finally {
                    this.isLoading = false
                }
            },

            // 设置详情侧栏是否展示
            setIsShow (value = true) {
                this.isShow = value
            }
        }
    }
</script>

<style scoped>
    @import './operateLog.css';
</style>
