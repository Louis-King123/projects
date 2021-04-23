<template>
    <div class="jobListContainer">
        <div class="jobListFormContainer">
            <bk-form form-type="inline">
                <bk-form-item label="业务">
                    <bk-select v-model="formData.biz_id" style="width: 190px;">
                        <bk-option
                                class="custom-option"
                                v-for="option in bizList"
                                :key="option['bk_biz_id']"
                                :id="option['bk_biz_id']"
                                :name="option['bk_biz_name']">
                        </bk-option>
                    </bk-select>
                </bk-form-item>

                <bk-form-item label="巡检对象">
                    <bk-select v-model="formData.os_id" style="width: 190px;" @change="handleChangeOs">
                        <bk-option
                                class="custom-option"
                                v-for="option in $store.getters.getOsList"
                                :key="option.id"
                                :id="option.id"
                                :name="option['os_name']">
                        </bk-option>
                    </bk-select>
                </bk-form-item>

                <bk-form-item label="巡检模板">
                    <bk-select v-model="formData.tpl_id" style="width: 190px;">
                        <bk-option
                                class="custom-option"
                                v-for="option in tplList"
                                :key="option.id"
                                :id="option.id"
                                :name="option.tpl_name">
                        </bk-option>
                    </bk-select>
                </bk-form-item>

                <bk-form-item label="创建日期">
                    <bk-date-picker
                            style="width: 190px;"
                            v-model="formData.date"
                            :type="'datetimerange'">
                    </bk-date-picker>
                </bk-form-item>

                <bk-form-item label="任务名">
                    <bk-input
                            style="width: 190px;"
                            v-model="formData.keywords"
                            @keyup.enter.native="search">
                    </bk-input>
                </bk-form-item>

                <bk-form-item>
                    <bk-button @click="search" theme="primary">查询</bk-button>
                </bk-form-item>
            </bk-form>
        </div>

        <div class="jobListTableContainer">

            <div class="addJobBtn f12" @click="handleAddJob">+ 新增任务</div>

            <bk-table
                    :data="taskList"
                    :size="'small'"
                    :pagination="pagination"
                    style="margin-top: 30px;"
                    v-bkloading="{ isLoading: isLoading, zIndex: 10 }"
                    @page-change="handlePageChange"
                    @page-limit-change="handlePageLimitChange"
                    @row-click="handleRowClick">
                <bk-table-column label="业务名称" prop="exec_biz_name"></bk-table-column>
                <bk-table-column label="任务名称" prop="task_name"></bk-table-column>
                <bk-table-column label="创建人" prop="task_op"></bk-table-column>
                <bk-table-column label="通知人" :show-overflow-tooltip="true">
                    <template slot-scope="scope">
                        <span>{{ scope.row.notify_usernames.join(', ') }}</span>
                    </template>
                </bk-table-column>
                <bk-table-column label="巡检对象" prop="task_os_name"></bk-table-column>
                <bk-table-column label="任务模板" prop="task_tpl_name" :show-overflow-tooltip="true"></bk-table-column>
                <bk-table-column label="执行方式">
                    <template slot-scope="scope">
                        <span>{{ setExecSchedule(scope.row.exec_schedule) }}</span>
                    </template>
                </bk-table-column>
                <bk-table-column label="创建时间" width="150" prop="start_time"></bk-table-column>
                <bk-table-column label="操作" width="320">
                    <template slot-scope="scope">
                        <bk-button
                                theme="success"
                                size="small"
                                :disabled="scope.row['exec_state'] === 1"
                                @click.prevent.stop="execute_tpl(scope.row.id)">
                            执行
                        </bk-button>
                        <bk-button
                                theme="warning"
                                size="small"
                                @click.prevent.stop="execute_edit(scope.row)">
                            编辑
                        </bk-button>
                        <bk-button
                                theme="danger"
                                size="small"
                                @click.prevent.stop="execute_del(scope.row.id)">
                            删除
                        </bk-button>
                        <bk-button
                          v-show="scope.row['exec_schedule'] === 'crontab' && scope.row['exec_state'] === 1"
                          theme="default"
                          size="small"
                          @click.prevent.stop="execute_stop(scope.row.id)">
                          暂停
                        </bk-button>
                    </template>
                </bk-table-column>
            </bk-table>

        </div>

        <div>
            <bk-sideslider :is-show.sync="isShow" :quick-close="true" :title="sideSliderTitle" width="700">
                <div slot="content" class="p20" style="height: calc(100vh - 60px);">
                    <div class="listDetailContainer" v-if="!isEdit">
                        <div class="listDetailItem">
                            <h4 class="m0 listDetailItemLabel">巡检对象：</h4>
                            {{ detailData['task_os_name'] }}
                        </div>

                        <div class="listDetailItem">
                            <h4 class="m0 listDetailItemLabel">巡检模板：</h4>
                            {{ detailData['task_tpl_name'] }}
                        </div>

                        <div class="listDetailItem">
                            <h4 class="m0 listDetailItemLabel">任务名：</h4>
                            {{ detailData['task_name'] }}
                        </div>
                        <div class="listDetailItem">
                            <h4 class="m0 listDetailItemLabel">通知人：</h4>
                            <bk-table :size="'small'" :data="notifyUsernames">
                                <bk-table-column label="用户名" prop="username"></bk-table-column>
                            </bk-table>
                        </div>

                        <div class="listDetailItem">
                            <h4 class="m0 listDetailItemLabel">执行账户：</h4>
                            {{ detailData['exec_acc'] }}
                        </div>

                        <div class="listDetailItem">
                            <h4 class="m0 listDetailItemLabel">巡检主机：</h4>
                            <bk-table :size="'small'" :data="hostData">
                              <bk-table-column label="主机IP" prop="bk_host_innerip"></bk-table-column>
                              <bk-table-column label="云区域" prop="bk_cloud_id"></bk-table-column>
                              <bk-table-column label="主机名" prop="bk_host_name"></bk-table-column>
                              <bk-table-column label="操作系统" prop="bk_os_name"></bk-table-column>
                            </bk-table>
                        </div>

                        <div class="listDetailItem">
                            <h4 class="m0 listDetailItemLabel">执行方式：</h4>
                            {{ setExecSchedule(detailData['exec_schedule']) }}&emsp;
                            <span v-if="detailData['exec_schedule'] !== 'instant'">
                              开始时间：{{ $moment(detailData['exec_start_time']).format('YYYY-MM-DD HH:mm:ss') }}&emsp;
                            </span>
                            <span v-if="detailData['exec_schedule'] === 'crontab'">
                              每{{ detailData['exec_timece'] }}天执行一次
                            </span>
                        </div>
                    </div>

                    <div class="listDetailContainer" v-else>
                        <bk-form :label-width="100" :model="editFormData" ref="validateForm" :rules="rules">
                            <bk-form-item label="巡检对象">
                                <bk-input :disabled="isEdit" v-model="curOsName"></bk-input>
                            </bk-form-item>

                            <bk-form-item label="巡检模板">
                                <bk-input :disabled="isEdit" v-model="curTplName"></bk-input>
                            </bk-form-item>

                            <bk-form-item label="任务名称">
                                <bk-input :disabled="isEdit" v-model="editFormData.task_name"></bk-input>
                            </bk-form-item>

                            <bk-form-item label="执行账户">
                                <bk-input :disabled="isEdit" v-model="editFormData.exec_acc"></bk-input>
                            </bk-form-item>

                            <!--TODO 修改通知人 -->
                            <bk-form-item
                              label="选择通知人"
                              :error-display-type="'normal'"
                              :required="true"
                              :property="'notify_usernames'">
                              <bk-select multiple searchable v-model="editFormData.notify_usernames">
                                <bk-option
                                  v-for="user in userList"
                                  :key="user['username']"
                                  :id="user['username']"
                                  :name="`${user['display_name']}(${user.username})`">
                                </bk-option>
                              </bk-select>
                            </bk-form-item>

                            <bk-form-item
                              label="选择业务"
                              :required="true"
                              :property="'biz_id'"
                              :error-display-type="'normal'">
                                <bk-select v-model="editFormData.biz_id" @change="handleChangeBiz">
                                    <bk-option
                                            v-for="biz in bizList"
                                            :key="biz['bk_biz_id']"
                                            :id="biz['bk_biz_id']"
                                            :name="biz['bk_biz_name']">
                                    </bk-option>
                                </bk-select>
                            </bk-form-item>

                            <bk-form-item
                              label="巡检主机"
                              :required="true"
                              :error-display-type="'normal'"
                              :property="'exec_hosts'">
                                <!--<bk-select multiple v-model="editFormData.exec_hosts">
                                    <bk-option
                                            v-for="host in hostList"
                                            :key="host.id"
                                            :id="host.id"
                                            :name="host.id">
                                    </bk-option>
                                </bk-select>-->
                                <bk-button :theme="'default'" @click="handleAddServer">添加服务器</bk-button>
                                <div class="mt10" v-show="editFormData.exec_hosts.length > 0">
                                  <bk-table :size="'small'" :data="editFormData.exec_hosts">
                                    <bk-table-column label="主机IP" prop="bk_host_innerip"></bk-table-column>
                                    <bk-table-column label="云区域" prop="bk_cloud_id"></bk-table-column>
                                    <bk-table-column label="主机名" prop="bk_host_name"></bk-table-column>
                                    <bk-table-column label="操作系统" prop="bk_os_name"></bk-table-column>
                                  </bk-table>
                                </div>
                            </bk-form-item>

                            <bk-form-item
                              label="执行方式"
                              :required="true"
                              :error-display-type="'normal'"
                              :property="'exec_schedule'">
                                <bk-radio-group v-model="editFormData.exec_schedule" @change="handleChangeExecSchedule">
                                    <bk-radio :value="'instant'">单次</bk-radio>
                                    <bk-radio :value="'interval'">定时</bk-radio>
                                    <bk-radio :value="'crontab'">周期</bk-radio>
                                </bk-radio-group>
                            </bk-form-item>

                            <bk-form-item
                              label="执行时间"
                              v-show="editFormData.exec_schedule !== 'instant'"
                              :required="true"
                              :error-display-type="'normal'"
                              :property="'exec_start_time'">
                                <bk-date-picker
                                        style="width: 490px;"
                                        :editable="false"
                                        v-model="editFormData.exec_start_time"
                                        :placeholder="'选择日期时间'"
                                        :type="'datetime'">
                                </bk-date-picker>
                            </bk-form-item>

                            <bk-form-item
                              label="频率"
                              v-show="editFormData.exec_schedule === 'crontab'"
                              :required="true"
                              :error-display-type="'normal'"
                              :property="'exec_timec'">
                                <bk-input v-model="editFormData.exec_timec">
                                    <template slot="append">
                                        <div class="group-text">天/次</div>
                                    </template>
                                </bk-input>
                            </bk-form-item>

                            <bk-form-item>
                                <bk-button
                                        theme="primary"
                                        :loading="isChecking"
                                        @click.stop.prevent="handleSubmit">
                                    提交
                                </bk-button>
                                <bk-button :theme="'default'" @click="handleCancel">取消</bk-button>
                            </bk-form-item>
                        </bk-form>
                    </div>
                </div>
            </bk-sideslider>
        </div>

        <app-select-server ref="appSelectServer"></app-select-server>
    </div>

</template>

<script>
    export default {
        name: 'list',
        data () {
            return {
                bizList: [],
                tplList: [],
                formData: {
                    biz_id: null,
                    os_id: null,
                    tpl_id: null,
                    date: [],
                    keywords: ''
                },
                report: [],
                taskList: [],
                pagination: {
                    current: 1,
                    count: 0,
                    limit: 10,
                    limitList: [5, 10, 20]
                },
                isLoading: false,
                isShow: false,
                detailData: {},
                hostData: [],
                notifyUsernames: [],
                isEdit: false,
                sideSliderTitle: '任务详情',
                editFormData: {
                    task_name: '',
                    notify_usernames: [],
                    exec_acc: 'root',
                    biz_id: null,
                    exec_hosts: [],
                    exec_schedule: 'instant',
                    exec_start_time: new Date(),
                    exec_timec: 1
                },
                rules: {
                    notify_usernames: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        }
                    ],
                    biz_id: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        }
                    ],
                    exec_hosts: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        }
                    ],
                    exec_schedule: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        }
                    ],
                    exec_start_time: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        },
                        {
                            validator: function () {
                                return true
                            },
                            message: '不可早于当前系统时间',
                            trigger: 'blur'
                        }
                    ],
                    exec_timec: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        },
                        {
                            validator: function (val) {
                                const { isInteger } = Number
                                return isInteger(Number(val)) && Number(val) > 0
                            },
                            message: '需为大于0的整数',
                            trigger: 'blur'
                        }
                    ]
                },
                userList: [],
                hostList: [],
                curOsName: '',
                curTplName: '',
                isChecking: false,
                taskOs: null,
                taskTplId: null,
                editId: null,
                originalHostsResult: [],
                bkBizId: null
            }
        },
        watch: {},
        created () {
            this.business_list()

            this.fetch_task_list()

            this.fetch_user_list()
        },
        methods: {
            handleAddServer () {
                const { editFormData, taskOs } = this

                const messageCof = {
                    message: '请先选择业务',
                    theme: 'warning',
                    delay: 3000
                }
                if (!editFormData['biz_id']) return this.$bkMessage(messageCof)

                const params = {
                    id: editFormData['biz_id'],
                    osId: taskOs
                }
                this.$refs.appSelectServer.opDialogPop(params)
            },
            handleGetHostsResult (hostResult) {
                this.editFormData['exec_hosts'] = hostResult

                this.originalHostsResult = hostResult
            },

            handleReturnOriginalResult () {
                const { originalHostsResult } = this
                return originalHostsResult
            },
            handleClearOriginalResult () {
                const { editFormData } = this
                if (editFormData['exec_hosts'].length === 0) this.originalHostsResult = []
            },

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
                this.formData.os_id = value

                if (!value) {
                    this.tplList = []
                    this.formData.tpl_id = null
                    return
                }

                this.fetch_tpl_list(value)
            },

            // 获取巡检模板数据
            async fetch_tpl_list () {
                try {
                    const { os_id } = this.formData
                    const params = { os_id }

                    const res = await this.$store.dispatch('fetch_tpl_list', params)
                    const { data } = res
                    this.tplList = data
                } catch (e) {
                    console.log('fetch_tpl_list', e)
                }
            },

            // 获取通知人数据
            async fetch_user_list () {
                try {
                    const res = await this.$store.dispatch('fetch_user_list')
                    const { data } = res
                    this.userList = data
                } catch (e) {
                    console.log('fetch_user_list', e)
                }
            },

            handleAddJob () {
                this.$router.push({
                    name: 'jobAdd'
                })
            },

            handlePageChange (current) {
                this.pagination.current = current
                this.fetch_task_list()
            },
            handlePageLimitChange (limit) {
                this.pagination.current = 1
                this.pagination.limit = limit
                this.fetch_task_list()
            },
            search () {
                this.fetch_task_list()
            },
            // 获取任务列表数据
            async fetch_task_list () {
                try {
                    this.isLoading = true

                    const { pagination, formData } = this

                    // 删除没有值对应的key
                    const { keys } = Object
                    const copyFormData = JSON.parse(JSON.stringify(formData))
                    keys(copyFormData).forEach(k => {
                        if (!copyFormData[k]) delete copyFormData[k]

                        if (k === 'date' && !copyFormData['date'][0]) delete copyFormData[k]
                    })

                    if (copyFormData['date']) {
                        const [startTime, endTime] = copyFormData['date']
                        copyFormData['date'][0] = this.$moment(startTime).format('YYYY-MM-DD HH:mm:ss')
                        copyFormData['date'][1] = this.$moment(endTime).format('YYYY-MM-DD HH:mm:ss')
                    }

                    const params = {
                        page: pagination.current,
                        size: pagination.limit,
                        ...copyFormData
                    }

                    const res = await this.$store.dispatch('fetch_task_list', params)

                    const { data } = res
                    this.taskList = data.data
                    this.pagination.count = data.count
                } catch (e) {
                    console.log('fetch_task_list', e)
                } finally {
                    this.isLoading = false
                }
            },

            // 设置执行方式展示
            setExecSchedule (schedule = 'instant') {
                const scheduleObj = {
                    instant: () => {
                        return '单次'
                    },
                    interval: () => {
                        return '定时'
                    },
                    crontab: () => {
                        return '周期'
                    }
                }

                return scheduleObj[schedule]()
            },

            // 表格点击行函数
            async handleRowClick (row) {
                this.detailData = row

                this.hostData = row['exec_hosts']

                const usernames = row['notify_usernames']
                this.notifyUsernames = []
                usernames.forEach(item => {
                    this.notifyUsernames.push({
                        username: item
                    })
                })
                const params = {
                    type: 'detail',
                    isShow: true
                }
                await this.setSideSliderConfig(params)
            },

            execute_edit (row) {
                const {
                    id,
                    exec_biz_id,
                    task_name,
                    notify_usernames,
                    exec_schedule,
                    exec_acc,
                    exec_hosts,
                    exec_start_time,
                    exec_timece
                } = row
                this.curOsName = row['task_os_name']
                this.curTplName = row['task_tpl_name']
                this.taskOs = row['task_os']
                this.taskTplId = row['task_tpl']
                this.editId = id
                this.originalHostsResult = row['exec_hosts']
                this.bkBizId = row['exec_biz_id']

                // 回填表单数据
                this.editFormData = {
                    task_name,
                    exec_acc,
                    exec_schedule,
                    exec_start_time,
                    exec_hosts,
                    exec_timec: exec_timece,
                    biz_id: exec_biz_id,
                    notify_usernames: notify_usernames
                }
                if (this.editFormData.exec_schedule !== 'instant') {
                    this.openExecStartTimeValidator()
                }

                const params = {
                    type: 'edit',
                    isShow: true
                }
                this.setSideSliderConfig(params)
            },
            handleChangeBiz (value) {
                const { bkBizId, originalHostsResult } = this
                console.log(bkBizId, value)
                if (value !== bkBizId) {
                    // this.hostList = []
                    this.editFormData.exec_hosts = []
                }

                if (value === bkBizId) {
                    this.editFormData.exec_hosts = originalHostsResult
                }

                // this.search_host_by_biz(value)
            },
            async search_host_by_biz (k) {
                try {
                    const res = await this.$store.dispatch('search_host_by_biz')

                    const { data } = res
                    this.hostList = data[k].children
                } catch (e) {
                    console.log('search_host_by_biz', e)
                }
            },
            // 根据单选框的值重新赋值执行时间和频率的值
            handleChangeExecSchedule (value) {
                if (value !== 'crontab') this.editFormData.exec_timec = 1

                if (value !== 'instant') this.openExecStartTimeValidator()

                if (value === 'instant') {
                    this.editFormData.exec_start_time = new Date()

                    this.closeExecStartTimeValidator()
                }
            },
            // 屏蔽执行时间是否早于当前时间的判断
            closeExecStartTimeValidator () {
                this.rules.exec_start_time[1].validator = () => true
            },
            // 开启执行时间是否早于当前时间的判断
            openExecStartTimeValidator () {
                this.rules.exec_start_time[1].validator = val => val.getTime() >= Date.now()
            },

            handleSubmit () {
                this.$refs.validateForm.validate().then(async () => {
                    try {
                        this.isChecking = true
                        const { taskTplId, taskOs, editId, editFormData } = this

                        const copyFormData = JSON.parse(JSON.stringify(editFormData))
                        copyFormData['exec_start_time'] = this.$moment(copyFormData['exec_start_time']).format('YYYY-MM-DD HH:mm:ss')

                        const data = {
                            task_tpl_id: taskTplId,
                            task_os: taskOs,
                            task_id: editId,
                            ...copyFormData
                        }

                        const res = await this.$store.dispatch('task_add', data)

                        const { code, message } = res
                        const theme = code === 0 ? 'success' : 'error'

                        this.$bkMessage({ delay: 3000, message, theme })

                        if (code === 0) {
                            this.handleCancel()
                            this.fetch_task_list()
                        }

                        // const h = this.$createElement
                        // const tipDom = this.$bkInfo({
                        //     type: theme,
                        //     title: msg,
                        //     showFooter: false,
                        //     subHeader: h('div', {
                        //         style: {
                        //             width: '90px',
                        //             height: '40px',
                        //             display: 'flex',
                        //             alignItems: 'center',
                        //             justifyContent: 'center',
                        //             borderRadius: '6px',
                        //             color: '#FFFFFF',
                        //             background: '#1d91ec',
                        //             cursor: 'pointer',
                        //             margin: '0 auto'
                        //         },
                        //         on: {
                        //             click: () => {
                        //                 this.$router.push({
                        //                     name: 'jobList'
                        //                 })
                        //                 setTimeout(() => tipDom.close())
                        //             }
                        //         }
                        //     }, '返回列表')
                        // })
                    } catch (e) {
                        console.log('task_add=', e)
                    } finally {
                        this.isChecking = false
                    }
                }, validator => {
                    return false
                })
            },
            handleCancel () {
                this.isShow = false
            },

            async execute_del (taskId) {
                this.$bkInfo({
                    title: '确认要删除任务?',
                    type: 'warning',
                    confirmLoading: true,
                    confirmFn: async () => {
                        const params = {
                            task_id: taskId
                        }
                        const res = await this.$store.dispatch('execute_del', params)
                        const { code, message } = res
                        const theme = code === 0 ? 'success' : 'error'
                        await this.$bkMessage({ delay: 2000, message, theme })

                        if (code === 0) this.fetch_task_list()
                    }
                })
            },

            async execute_tpl (taskId) {
                this.$bkInfo({
                    title: '确认要执行任务?',
                    confirmLoading: true,
                    confirmFn: async () => {
                        const params = {
                            task_id: taskId
                        }
                        const res = await this.$store.dispatch('execute_task', params)
                        const { code, message } = res
                        const theme = code === 0 ? 'success' : 'error'
                        await this.$bkMessage({ delay: 2000, message, theme })

                        if (code === 0) this.fetch_task_list()
                    }
                })
            },

            async execute_stop (taskId) {
                this.$bkInfo({
                    title: '确认要暂停任务?',
                    type: 'warning',
                    confirmLoading: true,
                    confirmFn: async () => {
                        const params = {
                            task_id: taskId
                        }
                        const res = await this.$store.dispatch('execute_stop', params)
                        const { code, message } = res
                        const theme = code === 0 ? 'success' : 'error'
                        await this.$bkMessage({ delay: 2000, message, theme })

                        if (code === 0) this.fetch_task_list()
                    }
                })
            },

            setSideSliderConfig (params = {}) {
                const { type, isShow } = params

                if (type === 'edit') {
                    this.sideSliderTitle = '编辑任务'
                    this.isEdit = true
                }

                if (type === 'detail') {
                    this.sideSliderTitle = '任务详情'
                    this.isEdit = false
                }

                this.isShow = isShow
            }
        }
    }
</script>

<style scoped>
    .jobListContainer {
        padding: 20px;
    }

    .jobListFormContainer {
        padding: 20px;
        background: #fff;
    }

    .jobListTableContainer {
        margin-top: 20px;
        background: #fff;
        padding: 20px;
    }

    .addJobBtn {
        line-height: 30px;
        text-align: center;
        border: 1px dashed #1890FF;
        border-radius: 6px;
        color: #1890FF;
        cursor: pointer;
    }

    .listDetailContainer {
        width: 600px;
        margin: 20px auto 0 auto;
    }

    .listDetailItem {
        display: flex;
        align-items: flex-start;
        margin: 20px 0;
        font-size: 14px;
    }

    .listDetailItemLabel {
        width: 100px;
        text-align: right;
        margin-right: 20px !important;
    }

    /*设置UI内部组件样式*/
    .bk-form-item {
        margin: 0 8px 8px 0 !important;
    }

    /deep/ .bk-form.bk-inline-form .bk-form-item .bk-label {
        width: 80px !important;
    }

    .bk-form-radio {
        margin-right: 30px;
    }
</style>
